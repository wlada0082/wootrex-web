import test from 'node:test';
import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import { deletionRequest, sendPendingRequests } from '../deletion-worker/account-deletion.mjs';

test('SQLite outbox is durable, deduplicated and retries delivery', async t => {
  const sqlite = new DatabaseSync(':memory:');
  t.after(() => sqlite.close());
  sqlite.exec(readFileSync(new URL('../deletion-worker/0002_account_deletion_requests.sql', import.meta.url), 'utf8'));
  let allowed = true, fail = true;
  const deliveries = [];
  const attempts = new Map();
  t.mock.method(globalThis, 'fetch', async (url, options) => {
    const mail = JSON.parse(options.body);
    const key = options.headers['Idempotency-Key'];
    assert.equal(url, 'https://api.resend.com/emails');
    assert.equal(options.method, 'POST');
    assert.equal(options.headers.Authorization, 'Bearer mock-token');
    assert.equal(options.redirect, 'error');
    assert.equal(key, `wootrex-account-deletion/${mail.subject.split(' - ').at(-1)}`);
    assert.equal(mail.from, 'WOOTREX <account-requests@notify.wootrex.cz>');
    assert.deepEqual(mail.to, ['wootrex@seznam.cz']);
    attempts.set(key, (attempts.get(key) ?? 0) + 1);
    if (fail) return new Response(null, { status: 429 });
    deliveries.push(mail);
    return Response.json({ id: mail.subject });
  });
  const env = {
    DB: { prepare(sql) {
      const statement = sqlite.prepare(sql);
      return { bind(...args) { return {
        run() { statement.run(...args); return {success:true}; },
        all() { return {results:statement.all(...args)}; },
      }; } };
    } },
    DELETION_RATE_LIMITER: { limit() { return {success:allowed}; } },
    RESEND_API_KEY: 'mock-token',
  };
  const submit = (data, origin = 'https://wootrex.cz', method = 'POST') => deletionRequest(
    new Request('https://feedback.wootrex.cz/account-deletion-requests', {
      method, headers:{'Origin':origin,'CF-Connecting-IP':'192.0.2.1','Content-Type':'application/json'},
      body:method === 'POST' ? JSON.stringify(data) : undefined,
    }), env);
  const request = {email:'A@example.test',website:''};
  const preflight = await submit(null, undefined, 'OPTIONS');
  assert.equal(preflight.status, 204);
  assert.equal(preflight.headers.get('Access-Control-Allow-Origin'), 'https://wootrex.cz');
  assert.equal((await submit(request,'https://elsewhere.test')).status,403);
  assert.equal((await submit({...request,website:'bot'})).status,400);
  assert.equal((await submit({...request,email:'x'.repeat(1100)})).status,413);
  allowed = false;
  assert.equal((await submit(request)).status,429);
  allowed = true;
  for (const email of ['A@example.test','a@example.test','b@example.test']) {
    const result = await submit({email,website:''});
    assert.equal(result.status,202);
    assert.deepEqual(await result.json(),{code:'request_received'});
  }
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS count FROM account_deletion_requests').get().count,2);
  const now = Math.floor(Date.now()/1000)+1;
  await sendPendingRequests(env,now);
  fail = false;
  await sendPendingRequests(env,now+899);
  assert.equal(deliveries.length,0);
  await Promise.all([sendPendingRequests(env,now+900),sendPendingRequests(env,now+900)]);
  assert.equal(deliveries.length,2);
  assert.deepEqual([...attempts.values()], [2, 2]);
  assert.ok(deliveries.some(m=>m.text.includes('a@example.test')));
  await sendPendingRequests(env,now+901);
  assert.equal(deliveries.length,2);
  await sendPendingRequests(env,now+87300);
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS count FROM account_deletion_requests').get().count,0);
  const broken = {...env,DB:{prepare(){throw Error('no database');}}};
  const failure = await deletionRequest(new Request('https://feedback.wootrex.cz/account-deletion-requests',{
    method:'POST',headers:{'Origin':'https://wootrex.cz','CF-Connecting-IP':'192.0.2.1','Content-Type':'application/json'},
    body:JSON.stringify(request),
  }),broken);
  assert.equal(failure.status,503);
});
