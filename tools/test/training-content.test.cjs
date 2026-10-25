const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const plans = JSON.parse(read('tools/fitness_portal/training_plans.json')).plans;
const articles = JSON.parse(read('tools/fitness_portal/training_articles.json')).articles;
const decode = s => s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");

test('published plans preserve catalog exercise order and prescription', () => {
  for (const p of plans) {
    const html = read(`cs/treninky/plany/${p.id}/index.html`);
    const table = html.match(/<table class="plan-table">([\s\S]*?)<\/table>/)[1];
    const rows = [...table.matchAll(/<tr>([\s\S]*?)<\/tr>/g)].slice(1).map(r => [...r[1].matchAll(/<td>([\s\S]*?)<\/td>/g)].map(c => decode(c[1])));
    assert.equal(rows.length, p.exercises.length, p.id);
    p.exercises.forEach((e, i) => {
      assert.equal(rows[i][1], e.name, p.id);
      assert.equal(rows[i][2], e.isCardio ? '—' : String(p.setCounts[e.id] ?? p.sets), p.id);
      assert.equal(rows[i][3], e.isCardio ? 'Časové úseky níže' : `${p.minReps}–${p.maxReps}`, p.id);
    });
  }
});

test('published articles have matching references and valid discovery metadata', () => {
  const sitemap = read('sitemap.xml');
  for (const a of articles) {
    const route = `https://wootrex.cz/cs/treninky/${a.slug}/`;
    const html = read(`cs/treninky/${a.slug}/index.html`);
    const data = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(m => JSON.parse(m[1])).find(d => d['@type'] === 'Article');
    assert.equal(data.headline, a.title);
    assert.equal(data.mainEntityOfPage, route);
    assert.deepEqual(data.citation, a.sources.map(s => s.url));
    assert.ok(sitemap.includes(route));
    assert.ok(!html.includes('noindex'));
    for (const m of html.matchAll(/class="citation" href="#(zdroj-\d+)"/g)) assert.ok(html.includes(`id="${m[1]}"`));
  }
  const draft = read('cs/treninky/treninkovy-denik/index.html');
  assert.ok(draft.includes('noindex,follow'));
  assert.ok(!sitemap.includes('https://wootrex.cz/cs/treninky/treninkovy-denik/'));
});
