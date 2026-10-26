const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const {webcrypto}=require('node:crypto');
const script=fs.readFileSync(path.join(__dirname,'../../assets/js/account-deletion.js'),'utf8').replace("import config from './account-deletion-config.js';",'');
async function harness({enabled=true,valid=true,pendingOwner=null}={}){
 const calls=[],data=new Map(),handlers={};
 if(pendingOwner){data.set('wootrex.deletion.receipt.v1','a'.repeat(64));data.set('wootrex.deletion.owner.v1',pendingOwner);}
 const elements=Object.assign([{value:'test@example.invalid',disabled:true},{value:'test password',disabled:true},{checked:true,disabled:true},{disabled:true}],{});
 elements.email=elements[0];elements.password=elements[1];elements.confirm=elements[2];
 const form={elements,reportValidity:()=>valid,addEventListener:(type,f)=>handlers[type]=f,reset:()=>{elements.email.value='';elements.password.value='';}};
 const result={textContent:''},availability={textContent:''};
 vm.runInNewContext(script,{config:{enabled,url:'https://test.supabase.co',publishableKey:'public'},document:{querySelector:s=>s==='#deletion-form'?form:s==='#result'?result:availability},sessionStorage:{getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,v),removeItem:k=>data.delete(k)},crypto:webcrypto,AbortSignal,Error,
 fetch:async(url,options)=>{
  calls.push({url,options,secretStillInForm:elements.password.value});
  if(url.includes('/auth/v1/token'))return {ok:true,json:async()=>({access_token:'synthetic-token',user:{id:'A'}})};
  if(url.includes('/deletion-status'))return {ok:true,json:async()=>({completed:!pendingOwner})};
  return {ok:true,json:async()=>({code:'account_deleted'})};
 }});
 await new Promise(setImmediate);
 return {calls,data,handlers,form,result};
}
test('disabled automatic form never registers a submission or contacts server',async()=>{const h=await harness({enabled:false});assert.equal(h.handlers.submit,undefined);assert.equal(h.calls.length,0);assert.ok(h.form.elements.every(x=>x.disabled));});
test('invalid confirmation cannot start authentication or deletion',async()=>{const h=await harness({valid:false});await h.handlers.submit({preventDefault(){}});assert.equal(h.calls.length,0);});
test('successful flow clears password before network, pins request and confirms before claiming success',async()=>{const h=await harness();await h.handlers.submit({preventDefault(){}});assert.equal(h.calls[0].secretStillInForm,'');const deletion=h.calls.find(x=>x.url.endsWith('/delete-account'));assert.deepEqual(JSON.parse(deletion.options.body),{confirm:'DELETE'});assert.equal(deletion.options.headers.Authorization,'Bearer synthetic-token');assert.ok(!deletion.options.body.includes('password'));assert.equal(deletion.options.credentials,'omit');assert.equal(h.data.size,0);assert.match(h.result.textContent,/byly odstraněny/);assert.ok(h.calls.some(x=>x.url.includes('/logout?scope=local')));});
test('pending receipt cannot be reused by a different account',async()=>{const h=await harness({pendingOwner:'B'});await h.handlers.submit({preventDefault(){}});assert.ok(!h.calls.some(x=>x.url.endsWith('/delete-account')));assert.match(h.result.textContent,/původního účtu/);assert.equal(h.data.get('wootrex.deletion.owner.v1'),'B');});
