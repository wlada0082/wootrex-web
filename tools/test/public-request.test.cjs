const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM}=require('../test-runtime/node_modules/jsdom');
const root=path.resolve(__dirname,'../..'),langs=['cs','en','de','sk','pl'];
for(const lang of langs){
 test(`localized browser form exists in ${lang}`,()=>{
  const dom=new JSDOM(fs.readFileSync(path.join(root,lang,'delete-account.html'),'utf8'));
  const d=dom.window.document,form=d.querySelector('#delete-form');
  assert.equal(form.hidden,false);
  assert.equal(form.querySelector('input[name=email]').required,true);
  assert.equal(form.querySelectorAll('input[type=password]').length,0);
  assert.equal(d.querySelectorAll('a[href^="mailto:"]').length,0);
  assert.equal(d.querySelectorAll('script[src]').length,1);
  dom.window.close();
 });
 for(const file of ['privacy.html','delete-account.html'])test(`local links/assets resolve: ${lang}/${file}`,()=>{
  const current=`https://wootrex.cz/${lang}/${file}`;
  const dom=new JSDOM(fs.readFileSync(path.join(root,lang,file),'utf8'),{url:current});
  for(const n of dom.window.document.querySelectorAll('a[href],link[href],script[src]')){
   const u=new URL(n.getAttribute('href')||n.getAttribute('src'),current);
   if(u.hostname!=='wootrex.cz'||!['http:','https:'].includes(u.protocol))continue;
   assert.equal(u.protocol,'https:');let target=path.join(root,decodeURIComponent(u.pathname));
   if(u.pathname.endsWith('/'))target=path.join(target,'index.html');
   assert.ok(fs.existsSync(target),`${current}: ${u.href}`);
  }
  dom.window.close();
 });
}
test('root deletion entry is HTTPS canonical with no credential fields',()=>{
 const d=new JSDOM(fs.readFileSync(path.join(root,'delete-account.html'),'utf8')).window.document;
 assert.equal(d.querySelector('link[rel=canonical]').href,'https://wootrex.cz/cs/delete-account.html');
 assert.equal(d.querySelectorAll('input').length,0);
});
