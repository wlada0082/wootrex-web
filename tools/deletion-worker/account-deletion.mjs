const recipient = 'wootrex@seznam.cz';
const origins = new Set(['https://wootrex.cz', 'https://www.wootrex.cz']);
const day = 86400;

function response(origin, status, body) {
  const headers = { 'Cache-Control': 'no-store', 'Vary': 'Origin',
    'Content-Type': 'application/json; charset=utf-8', 'X-Content-Type-Options': 'nosniff' };
  if (origins.has(origin)) headers['Access-Control-Allow-Origin'] = origin;
  if (status === 204) {
    headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS';
    headers['Access-Control-Allow-Headers'] = 'Content-Type';
  }
  if (status === 429) headers['Retry-After'] = '60';
  return new Response(body ? JSON.stringify(body) : null, { status, headers });
}

export async function deletionRequest(request, env) {
  const origin = request.headers.get('Origin');
  const reply = (status, code) => response(origin, status, code ? { code } : null);
  if (!origins.has(origin)) return reply(403, 'origin_not_allowed');
  if (request.method === 'OPTIONS') return reply(204);
  if (request.method !== 'POST') return reply(405, 'method_not_allowed');
  if (request.headers.get('Content-Type')?.split(';')[0].trim().toLowerCase() !== 'application/json') {
    return reply(415, 'invalid_request');
  }
  if (!env.DB || !env.DELETION_RATE_LIMITER || !env.RESEND_API_KEY) return reply(503, 'unavailable');
  try {
    const ip = request.headers.get('CF-Connecting-IP');
    if (!ip) return reply(403, 'origin_not_allowed');
    if (!(await env.DELETION_RATE_LIMITER.limit({ key: ip })).success) return reply(429, 'rate_limited');

    let data;
    const reader = request.body?.getReader();
    if (!reader) return reply(400, 'invalid_request');
    try {
      const bytes = new Uint8Array(1024);
      let offset = 0;
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        if (offset + value.length > bytes.length) {
          await reader.cancel();
          return reply(413, 'invalid_request');
        }
        bytes.set(value, offset);
        offset += value.length;
      }
      data = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes.subarray(0, offset)));
    } catch {
      return reply(400, 'invalid_request');
    } finally {
      reader.releaseLock();
    }

    const email = typeof data?.email === 'string' ? data.email.trim().toLowerCase() : '';
    if (data?.website !== '' || Object.keys(data).length !== 2 || email.length > 254 ||
        !/^[^\s@<>\u0000-\u001f\u007f]+@[^\s@<>\u0000-\u001f\u007f]+\.[^\s@<>\u0000-\u001f\u007f]+$/.test(email)) {
      return reply(400, 'invalid_request');
    }

    const now = Math.floor(Date.now() / 1000);
    const result = await env.DB.prepare(`INSERT INTO account_deletion_requests (email,id,created_at,next_attempt)
      VALUES (?,?,?,?) ON CONFLICT(email) DO NOTHING`).bind(email, crypto.randomUUID(), now, now).run();
    if (!result.success) return reply(503, 'unavailable');
    return reply(202, 'request_received');
  } catch {
    return reply(503, 'unavailable');
  }
}

export async function sendPendingRequests(env, now = Math.floor(Date.now() / 1000)) {
  if (!env.RESEND_API_KEY) return;

  if (!env.RESEND_API_KEY) return;

  const rows = await env.DB.prepare(`UPDATE account_deletion_requests SET lease=?, next_attempt=?
    WHERE id IN (SELECT id FROM account_deletion_requests WHERE sent_at IS NULL AND next_attempt<=?
    ORDER BY next_attempt LIMIT 10) RETURNING id,email,lease`)
    .bind(crypto.randomUUID(), now + 900, now).all();

  for (const { id, email, lease } of rows.results) {
    try {
      const result = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json',
          'Idempotency-Key': `wootrex-account-deletion/${id}`,
        },
        redirect: 'error',
        signal: AbortSignal.timeout(5000),
        body: JSON.stringify({
          from: 'WOOTREX <account-requests@notify.wootrex.cz>',
          to: [recipient],
            subject: `WOOTREX - zadost o odstraneni uctu - ${id}`,
            text: `Reference: ${id}\nE-mail uctu: ${email}\nPred jakymkoliv mazanim overte vlastnictvi uctu.\n`,
        }),
      });
      if (!result.ok) continue;
      const receipt = await result.json();
      if (typeof receipt?.id !== 'string' || !receipt.id) continue;
    } catch {
      // The lease expires automatically, allowing a later attempt.
      continue;
    }
    await env.DB.prepare('UPDATE account_deletion_requests SET sent_at=?, lease=NULL WHERE id=? AND lease=?')
      .bind(now, id, lease).run();
  }

  // Retain undelivered requests for follow-up even during a long outage.
  await env.DB.prepare('DELETE FROM account_deletion_requests WHERE sent_at<=?')
    .bind(now - day).run();
}
