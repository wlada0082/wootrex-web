const form = document.querySelector('#delete-form');
const status = document.querySelector('#deletion-status');
const messages = JSON.parse(document.querySelector('#deletion-messages').textContent);
const button = form.querySelector('button');

form.addEventListener('submit', async event => {
  event.preventDefault();
  if (button.disabled) return;
  button.disabled = true;
  status.textContent = messages.sending;
  const values = new FormData(form);
  try {
    const response = await fetch('https://feedback.wootrex.cz/account-deletion-requests', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: values.get('email'), website: values.get('website') }),
      credentials: 'omit',
      redirect: 'error',
      signal: AbortSignal.timeout(12000),
    });
    if (response.status === 429) {
      status.textContent = messages.rate;
    } else if (response.status === 202 && (await response.json()).code === 'request_received') {
      form.reset();
      status.textContent = messages.success;
    } else {
      status.textContent = messages.error;
    }
  } catch {
    status.textContent = messages.error;
  } finally {
    button.disabled = false;
  }
});

button.disabled = false;
