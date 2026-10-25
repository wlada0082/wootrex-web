const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
test('update manifest advertises released Beta 136 build 136 with five translations', () => {
 const m=JSON.parse(fs.readFileSync(path.join(__dirname,'../../update.json'),'utf8'));
 assert.equal(m.build,136); assert.equal(m.version,'1.0.0');
 assert.equal(m.apk_url,'https://github.com/wlada0082/wootrex-web/releases/download/v1.0.0-beta136/Wootrex-Beta136-v1.0.0.apk');
 for (const l of ['cs','en','de','sk','pl']) assert.ok(m.changes[l].length);
});

test('Android Beta 136 and iOS Beta 6 build 21 remain separate in every generated page', () => {
 const labels={cs:['sestavení 136','sestavení 21'],en:['build 136','build 21'],de:['Build 136','Build 21'],sk:['zostava 136','zostava 21'],pl:['kompilacja 136','kompilacja 21']};
 for(const [language,[android,ios]] of Object.entries(labels)) {
  const page=fs.readFileSync(path.join(__dirname,'../../',language,'index.html'),'utf8');
  assert.ok(page.includes(`Beta 136 · 1.0.0 (${android})</p>`));
  assert.ok(page.includes(`Beta 6 · 1.0.0 (${ios}) · TestFlight`));
  assert.ok(!page.includes('releases/download/v1.0.0-beta4/'));
 }
});

// This exact shape is accepted by the installed app's download allowlist.
test('release URL remains compatible with the native update allowlist', () => {
 const m=JSON.parse(fs.readFileSync(path.join(__dirname,'../../update.json'),'utf8'));
 const u=new URL(m.apk_url);
 assert.equal(u.protocol,'https:'); assert.equal(u.host,'github.com');
 assert.equal(u.search,''); assert.equal(u.hash,''); assert.equal(u.username,'');
 assert.match(u.pathname,/^\/wlada0082\/wootrex-web\/releases\/download\/v[0-9]+\.[0-9]+\.[0-9]+-beta[0-9]+\/Wootrex-Beta[0-9]+-v[0-9]+\.[0-9]+\.[0-9]+\.apk$/);
 assert.ok(m.build>130);
});
