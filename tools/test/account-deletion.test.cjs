const test=require('node:test'), assert=require('node:assert/strict');
const {readFileSync}=require('node:fs');const path=require('node:path');
const {JSDOM}=require('../test-runtime/node_modules/jsdom');
const root=path.resolve(__dirname,'../..');
const source=readFileSync(path.join(root,'assets/js/account-deletion.js'),'utf8');
const backend='https://qsruhiewyxnhxpvnibcc.supabase.co';
async function fixture(t,{config={enabled:true,url:backend,publishableKey:'sb_publishable_synthetic'},login=200,deletion=200,code='account_deleted',networkError=false,lang='cs'}={}) {
 const dom=new JSDOM(readFileSync(path.join(root,lang,'delete-account.html'),'utf8'),{url:`https://wootrex.cz/${lang}/delete-account.html`,runScripts:'outside-only'});
 t.after(()=>dom.window.close()); const w=dom.window,calls=[];
 w.AbortSignal=AbortSignal;
 w.fetch=async(url,options)=>{
  calls.push({url,options});
  if(url.startsWith('/assets/'))return Response.json(config);
  if(url.includes('/token'))return Response.json({access_token:'synthetic-token',refresh_token:'never-store'}, {status:login});
  if(url.includes('/logout'))return new Response(null,{status:204});
  if(networkError)throw Error('private details');
  return Response.json({code},{status:deletion});
 };
 await w.eval(`(async()=>{${source}})()`);
 const f=w.document.querySelector('form');
 f.elements.email.value='a@example.test';f.elements.password.value='synthetic-password';
 f.elements.confirm.value='DELETE';f.elements.consent.checked=true;
 const submit=async()=>{f.dispatchEvent(new w.Event('submit',{cancelable:true}));
  for(let i=0;i<50;i++){await new Promise(setImmediate);if(!f.hasAttribute('aria-busy'))return;}throw Error('Form did not finish');};
 return {w,f,calls,submit,status:()=>w.document.querySelector('[role=status]').textContent};
}
for(const lang of ['cs','en','de','sk','pl'])test(`localized accessible page ${lang} has no trackers`,async t=>{
 const {w,f}=await fixture(t,{lang});
 assert.equal(w.document.documentElement.lang,lang);
 assert.equal(f.querySelector('button').disabled,false);
 assert.equal(w.document.querySelectorAll('script[src]').length,1);
 assert.ok(w.document.querySelector('meta[http-equiv="Content-Security-Policy"]').content.includes("form-action 'none'"));
 assert.equal(w.document.querySelectorAll('input[type=password]').length,1);
 assert.equal(w.document.querySelectorAll('nav a').length,5);
});
for(const config of [{enabled:false},{enabled:true,url:'https://evil.example',publishableKey:'sb_publishable_test'}, {enabled:true,url:backend,publishableKey:'service-role-secret'}])test('unsafe/disabled config sends no credentials',async t=>{
 const {f,calls,submit}=await fixture(t,{config});await submit();
 assert.equal(f.querySelector('button').disabled,true);assert.equal(calls.length,1);
});
test('explicit confirmation required before authentication',async t=>{
 const {f,calls,submit}=await fixture(t);f.elements.consent.checked=false;await submit();assert.equal(calls.length,1);
 f.elements.consent.checked=true;f.elements.confirm.value='delete';await submit();assert.equal(calls.length,1);
});
test('success sends exact confirmation, clears credentials and cannot submit twice',async t=>{
 const {w,f,calls,submit,status}=await fixture(t);await submit();
 assert.equal(calls.length,3);
 assert.equal(calls[2].options.body,JSON.stringify({confirm:'DELETE'}));
 assert.equal(JSON.parse(calls[1].options.body).password,'synthetic-password');
 assert.equal(f.elements.password.value,'');assert.equal(w.localStorage.length,0);assert.equal(w.document.cookie,'');
 assert.equal(f.querySelector('button').disabled,true);assert.match(status(),/byly smazány/);
 await submit();assert.equal(calls.length,3);
 for(const call of calls){assert.equal(call.options.credentials,'omit');assert.equal(call.options.redirect,'error');assert.ok(!call.url.includes('synthetic'));}
});
for(const options of [{deletion:503},{code:'unexpected'},{networkError:true}])test('failure never claims deletion and logs out temporary session',async t=>{
 const {f,calls,submit,status}=await fixture(t,options);await submit();
 assert.match(status(),/nepodařilo potvrdit/);assert.ok(calls.at(-1).url.includes('/logout?scope=local'));
 assert.equal(f.querySelector('button').disabled,false);assert.equal(f.elements.password.value,'');
});
test('failed login does not invoke deletion',async t=>{
 const {calls,submit,status}=await fixture(t,{login:400});await submit();
 assert.equal(calls.length,2);assert.match(status(),/nepodařilo ověřit/);
});
test('published config stays disabled until reviewed backend deployment',()=>{
 const config=JSON.parse(readFileSync(path.join(root,'assets/account-deletion-config.json'),'utf8'));
 assert.equal(config.enabled,false);assert.equal(config.publishableKey,'');
});
