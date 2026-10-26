import config from './account-deletion-config.js';
const form=document.querySelector('#deletion-form'),result=document.querySelector('#result');
const receiptKey='wootrex.deletion.receipt.v1';
async function call(path,body,headers={}){
 const r=await fetch(config.url+path,{method:'POST',credentials:'omit',cache:'no-store',referrerPolicy:'no-referrer',headers:{apikey:config.publishableKey,'Content-Type':'application/json',...headers},body:JSON.stringify(body),signal:AbortSignal.timeout(45000)});
 if(!r.ok)throw Error('Žádost nelze dokončit. Zkuste pokračovat později nebo použijte e-mailovou žádost.');
 return r.json();
}
async function status(receipt){return (await call('/functions/v1/deletion-status',{receipt})).completed===true;}
if(config.enabled===true && /^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.url) && config.publishableKey){
 document.querySelector('#availability').textContent='Po přihlášení můžete nevratně odstranit vlastní účet. Heslo se neukládá do prohlížeče.';
 for(const el of form.elements)el.disabled=false;
 const pending=sessionStorage.getItem(receiptKey);
 if(pending)status(pending).then(done=>{if(done){sessionStorage.removeItem(receiptKey);sessionStorage.removeItem('wootrex.deletion.owner.v1');result.textContent='Účet a související cloudová data byly odstraněny.';}else result.textContent='Dřívější žádost zatím není dokončená. Přihlaste se ke stejnému účtu a pokračujte.';}).catch(()=>{result.textContent='Dřívější žádost vyžaduje opětovné ověření.';});
 form.addEventListener('submit',async event=>{
  event.preventDefault();if(!form.reportValidity())return;
  for(const el of form.elements)el.disabled=true;
  const password=form.elements.password.value;form.elements.password.value='';
  let accessToken;
  try{
   const login=await call('/auth/v1/token?grant_type=password',{email:form.elements.email.value,password});
   accessToken=login.access_token;
   if(!accessToken || !login.user?.id)throw Error('Přihlášení se nezdařilo.');
   // Scope retries to the same authenticated account without retaining its email.
   const previous=sessionStorage.getItem(receiptKey);
   const ownerKey='wootrex.deletion.owner.v1';
   if(previous && sessionStorage.getItem(ownerKey)!==login.user.id)throw Error('Nejdříve dokončete žádost původního účtu.');
   const receipt=previous??Array.from(crypto.getRandomValues(new Uint8Array(32)),x=>x.toString(16).padStart(2,'0')).join('');
   sessionStorage.setItem(receiptKey,receipt);sessionStorage.setItem(ownerKey,login.user.id);
   const response=await call('/functions/v1/delete-account',{confirm:'DELETE'},{Authorization:'Bearer '+accessToken,'X-Deletion-Receipt':receipt});
   if(response.code!=='account_deleted' || !await status(receipt))throw Error('Odstranění zatím není potvrzené.');
   sessionStorage.removeItem(receiptKey);sessionStorage.removeItem(ownerKey);form.reset();result.textContent='Účet a související cloudová data byly odstraněny.';
  }catch(error){result.textContent=error.message;}finally{
   // Reauthentication creates a short-lived session. Revoke it also on failure.
   if(accessToken)await fetch(config.url+'/auth/v1/logout?scope=local',{method:'POST',credentials:'omit',headers:{apikey:config.publishableKey,Authorization:'Bearer '+accessToken}}).catch(()=>{});
   accessToken=undefined;for(const el of form.elements)el.disabled=false;
  }
 });
}
