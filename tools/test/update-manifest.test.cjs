const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
test('update manifest advertises only released Beta 4 with five translations', () => {
 const m=JSON.parse(fs.readFileSync(path.join(__dirname,'../../update.json'),'utf8'));
 assert.equal(m.build,4); assert.equal(m.version,'1.0.0');
 assert.equal(m.apk_url,'https://github.com/wlada0082/wootrex-web/releases/download/v1.0.0-beta4/Wootrex-Beta4-v1.0.0.apk');
 for (const l of ['cs','en','de','sk','pl']) assert.ok(m.changes[l].length);
});
