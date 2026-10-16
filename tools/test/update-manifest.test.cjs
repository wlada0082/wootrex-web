const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
test('update manifest advertises released Beta 5 build 21 with five translations', () => {
 const m=JSON.parse(fs.readFileSync(path.join(__dirname,'../../update.json'),'utf8'));
 assert.equal(m.build,21); assert.equal(m.version,'1.0.0');
 assert.equal(m.apk_url,'https://github.com/wlada0082/wootrex-web/releases/download/v1.0.0-beta21/Wootrex-Beta5-v1.0.0.apk');
 for (const l of ['cs','en','de','sk','pl']) assert.ok(m.changes[l].length);
});

test('Android Beta 5 and iOS Beta 6 build 21 remain separate in every generated page', () => {
 const labels={cs:['sestavení 21','sestavení 21'],en:['build 21','build 21'],de:['Build 21','Build 21'],sk:['zostava 21','zostava 21'],pl:['kompilacja 21','kompilacja 21']};
 for(const [language,[android,ios]] of Object.entries(labels)) {
  const page=fs.readFileSync(path.join(__dirname,'../../',language,'index.html'),'utf8');
  assert.ok(page.includes(`Beta 5 · 1.0.0 (${android})</p>`));
  assert.ok(page.includes(`Beta 6 · 1.0.0 (${ios}) · TestFlight`));
  assert.ok(!page.includes('releases/download/v1.0.0-beta4/'));
 }
});
