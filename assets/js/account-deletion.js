const expectedBackend = 'https://qsruhiewyxnhxpvnibcc.supabase.co';
const form = document.querySelector('#delete-form');
const status = document.querySelector('#deletion-status');
const button = form.querySelector('button[type=submit]');
const fields = form.querySelector('fieldset');
const messages = JSON.parse(document.querySelector('#deletion-messages').textContent);
let config, busy = false, completed = false;
function report(key, focus = true) { status.textContent = messages[key]; if (focus) status.focus(); }
async function request(url, options = {}) {
  return fetch(url, { ...options, credentials: 'omit', cache: 'no-store', redirect: 'error', signal: AbortSignal.timeout(30000) });
}
try {
  const response = await request('/assets/account-deletion-config.json');
  if (!response.ok) throw Error();
  config = await response.json();
  if (config.enabled !== true || config.url !== expectedBackend ||
      typeof config.publishableKey !== 'string' || !/^sb_publishable_[A-Za-z0-9_-]+$/.test(config.publishableKey)) throw Error();
  fields.disabled = false;
  button.disabled = false;
  report('ready', false);
} catch { config = null; report('unavailable', false); }
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!config || busy || completed || !form.reportValidity()) return;
  if (form.elements.confirm.value !== 'DELETE' || !form.elements.consent.checked) { report('confirmation'); return; }
  busy = true; button.disabled = true; form.setAttribute('aria-busy','true');
  const email = form.elements.email.value.trim();
  let password = form.elements.password.value;
  form.elements.password.value = '';
  let token;
  report('working');
  try {
    const login = await request(`${config.url}/auth/v1/token?grant_type=password`, {
      method:'POST', headers:{apikey:config.publishableKey,'content-type':'application/json'},
      body:JSON.stringify({email,password}),
    });
    password = '';
    if (!login.ok) { report('authentication'); return; }
    const session = await login.json();
    token = session.access_token;
    if (typeof token !== 'string' || !token) throw Error();
    const response = await request(`${config.url}/functions/v1/delete-account`, {
      method:'POST', headers:{apikey:config.publishableKey,authorization:`Bearer ${token}`,'content-type':'application/json'},
      body:JSON.stringify({confirm:'DELETE'}),
    });
    if (!response.ok || (await response.json()).code !== 'account_deleted') throw Error();
    completed = true;
    form.reset();
    for (const input of form.querySelectorAll('input')) input.disabled = true;
    report('success');
  } catch { report('incomplete'); }
  finally {
    password = '';
    // A failed request must not leave a new browser session behind. Tokens remain
    // in memory only; never write localStorage/cookies or put credentials in URLs.
    if (token && !completed) {
      try { await request(`${config.url}/auth/v1/logout?scope=local`, {method:'POST',headers:{apikey:config.publishableKey,authorization:`Bearer ${token}`}}); } catch {}
    }
    token = undefined; busy = false;
    form.removeAttribute('aria-busy'); button.disabled = completed;
  }
});
