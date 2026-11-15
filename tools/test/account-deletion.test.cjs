const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('../test-runtime/node_modules/jsdom');
const root = path.resolve(__dirname, '../..');
const script = fs.readFileSync(path.join(root, 'assets/js/account-deletion.js'), 'utf8');

for (const [status, code, message] of [
  [202, 'request_received', 'success'],
  [202, 'unexpected', 'error'],
  [503, 'unavailable', 'error'],
  [429, 'rate_limited', 'rate'],
  [0, '', 'error'],
]) {
  test(`form waits for server receipt and handles ${status} ${code}`, async t => {
    const dom = new JSDOM(fs.readFileSync(path.join(root, 'cs/delete-account.html'), 'utf8'), {
      url: 'https://wootrex.cz/cs/delete-account.html', runScripts: 'outside-only',
    });
    t.after(() => dom.window.close());
    const w = dom.window;
    const d = w.document;
    const form = d.querySelector('form');
    const button = form.querySelector('button');
    const text = JSON.parse(d.querySelector('#deletion-messages').textContent);
    let done, calls = 0;
    w.AbortSignal = AbortSignal;
    w.fetch = (url, options) => {
      calls++;
      assert.equal(url, 'https://feedback.wootrex.cz/account-deletion-requests');
      assert.deepEqual(JSON.parse(options.body), {email:'a@example.test', website:''});
      return new Promise((resolve, reject) => {
        done = () => status ? resolve(Response.json({code}, {status})) : reject(Error('offline'));
      });
    };
    w.eval(script);
    form.elements.email.value = 'a@example.test';
    for (let i = 0; i < 2; i++) form.dispatchEvent(new w.Event('submit', {cancelable:true}));
    assert.equal(calls, 1);
    assert.equal(button.disabled, true);
    assert.equal(d.querySelector('#deletion-status').textContent, text.sending);
    done();
    await new Promise(resolve => setImmediate(resolve));
    assert.equal(d.querySelector('#deletion-status').textContent, text[message]);
    assert.equal(form.elements.email.value, message === 'success' ? '' : 'a@example.test');
    assert.equal(button.disabled, false);
  });
}
