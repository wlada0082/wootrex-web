const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM}=require('../test-runtime/node_modules/jsdom');
const source=fs.readFileSync(path.join(__dirname,'../../assets/js/feedback.js'),'utf8');
async function fixture(t,status=201,result={success:true,id:'synthetic-receipt'}){
 const dom=new JSDOM('<html lang="cs"><body><button data-feedback>Feedback</button></body></html>',{url:'https://wootrex.cz/cs/',runScripts:'outside-only'});t.after(()=>dom.window.close());
 const w=dom.window,calls=[];w.fetch=async(url,options)=>{calls.push({url,options});return Response.json(result,{status})};
 w.HTMLDialogElement.prototype.showModal=function(){this.open=true};
 w.HTMLDialogElement.prototype.close=function(){this.open=false};w.eval(source);
 const form=w.document.querySelector('form');form.elements.message.value='Synthetic feedback';
 async function submit(){form.dispatchEvent(new w.Event('submit',{cancelable:true}));for(let i=0;i<30;i++){await new Promise(setImmediate);if(!form.querySelector('[type=submit]').disabled)return}throw Error('Timeout')}
 return {w,form,calls,submit,status:()=>form.querySelector('[role=status]').textContent};
}
test('feedback confirms only exact201 receipt, sends limited fields without credentials',async t=>{
 const x=await fixture(t);await x.submit();assert.equal(x.form.elements.message.value,'');assert.equal(x.calls.length,1);
 const c=x.calls[0];assert.equal(String(c.url),'https://feedback.wootrex.cz/feedback');assert.equal(c.options.credentials,'omit');assert.equal(c.options.redirect,'error');
 assert.deepEqual(Object.keys(JSON.parse(c.options.body)).sort(),['category','language','message','platform','source']);
 assert.equal(x.w.localStorage.length,0);assert.match(x.status(),/Děkujeme/);
});
for(const r of [{success:true,id:''},{success:true,id:'   '},{success:false,id:'x'},{success:true,id:1}])test('unconfirmed feedback preserves draft for retry',async t=>{
 const x=await fixture(t,201,r);await x.submit();assert.equal(x.form.elements.message.value,'Synthetic feedback');assert.doesNotMatch(x.status(),/Děkujeme/);assert.equal(x.calls.length,1);
});
for(const status of [400,429,500])test(`feedback HTTP${status} never claims success`,async t=>{
 const x=await fixture(t,status);await x.submit();assert.equal(x.form.elements.message.value,'Synthetic feedback');assert.doesNotMatch(x.status(),/Děkujeme/);
});
