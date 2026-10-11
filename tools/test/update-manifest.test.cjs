const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
test('update manifest advertises only released Beta 4 build 5 with five translations', () => {
 const m=JSON.parse(fs.readFileSync(path.join(__dirname,'../../update.json'),'utf8'));
 assert.equal(m.build,5); assert.equal(m.version,'1.0.0');
 assert.equal(m.apk_url,'https://github.com/wlada0082/wootrex-web/releases/download/v1.0.0-beta5/Wootrex-Beta4-v1.0.0.apk');
 for (const l of ['cs','en','de','sk','pl']) assert.ok(m.changes[l].length);
});

test('Android build 5 and iOS build 4 remain separate in every generated page', () => {
 const labels={cs:['sestavení 5','sestavení 4'],en:['build 5','build 4'],de:['Build 5','Build 4'],sk:['zostava 5','zostava 4'],pl:['kompilacja 5','kompilacja 4']};
 for(const [language,[android,ios]] of Object.entries(labels)) {
  const page=fs.readFileSync(path.join(__dirname,'../../',language,'index.html'),'utf8');
  assert.ok(page.includes(`Beta 4 · 1.0.0 (${android})</p>`));
  assert.ok(page.includes(`Beta 4 · 1.0.0 (${ios}) · TestFlight`));
  assert.ok(!page.includes('releases/download/v1.0.0-beta4/'));
 }
});
