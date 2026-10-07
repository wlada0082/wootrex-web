const feedbackLabels = {"cs": ["Zpětná vazba", "Kategorie", "Chyba", "Požadavek na funkci", "Návrh", "Jiné", "Zpráva (5–4000 znaků)", "Kontaktní e-mail (nepovinný)", "Odeslat", "Odesílání…", "Děkujeme. Feedback byl odeslán.", "Odeslání se nezdařilo. Zkus to znovu.", "Příliš mnoho zpráv. Zkus to za chvíli.", "Zkontroluj zprávu a e-mail.", "Zavřít", "Zprávu, případný e-mail a jazyk odešleme do WOOTREX Feedback API a uložíme u Cloudflare. Neuváděj citlivé údaje."], "en": ["Feedback", "Category", "Bug", "Feature request", "Suggestion", "Other", "Message (5–4000 characters)", "Contact email (optional)", "Send", "Sending…", "Thank you. Your feedback has been sent.", "Unable to send. Please try again.", "Too many messages. Please try again later.", "Check your message and email.", "Close", "Your message, optional email and language are sent to the WOOTREX Feedback API and stored at Cloudflare. Do not include sensitive information."], "de": ["Feedback", "Kategorie", "Fehler", "Funktionswunsch", "Vorschlag", "Sonstiges", "Nachricht (5–4000 Zeichen)", "Kontakt-E-Mail (optional)", "Senden", "Wird gesendet…", "Danke. Dein Feedback wurde gesendet.", "Senden fehlgeschlagen. Bitte versuche es erneut.", "Zu viele Nachrichten. Bitte versuche es später erneut.", "Prüfe deine Nachricht und E-Mail.", "Schließen", "Deine Nachricht, optionale E-Mail und Sprache werden an die WOOTREX Feedback API gesendet und bei Cloudflare gespeichert. Gib keine sensiblen Informationen an."], "sk": ["Spätná väzba", "Kategória", "Chyba", "Požiadavka na funkciu", "Návrh", "Iné", "Správa (5–4000 znakov)", "Kontaktný e-mail (nepovinný)", "Odoslať", "Odosielanie…", "Ďakujeme. Spätná väzba bola odoslaná.", "Odoslanie sa nepodarilo. Skús to znova.", "Príliš veľa správ. Skús to o chvíľu.", "Skontroluj správu a e-mail.", "Zavrieť", "Správu, prípadný e-mail a jazyk odošleme do WOOTREX Feedback API a uložíme u Cloudflare. Neuvádzaj citlivé údaje."], "pl": ["Opinia", "Kategoria", "Błąd", "Prośba o funkcję", "Sugestia", "Inne", "Wiadomość (5–4000 znaków)", "E-mail kontaktowy (opcjonalny)", "Wyślij", "Wysyłanie…", "Dziękujemy. Opinia została wysłana.", "Nie udało się wysłać. Spróbuj ponownie.", "Zbyt wiele wiadomości. Spróbuj później.", "Sprawdź wiadomość i e-mail.", "Zamknij", "Wiadomość, opcjonalny e-mail i język zostaną wysłane do WOOTREX Feedback API i zapisane w Cloudflare. Nie podawaj poufnych informacji."]};

(() => {
 const lang=document.documentElement.lang.split('-')[0], t=feedbackLabels[lang]||feedbackLabels.cs;
 const localDevelopment=['http://127.0.0.1:8080','http://localhost:8080'].includes(location.origin);
 const endpoint='https://feedback.wootrex.cz/feedback';
 const triggers=document.querySelectorAll('[data-feedback]');
 if(!triggers.length)return;
 const dialog=document.createElement('dialog');dialog.className='feedback-dialog';
 dialog.innerHTML='<form novalidate><div class="feedback-heading"><h2></h2><button type="button" class="feedback-close"></button></div><label class="category-label"></label><select name="category"></select><label class="message-label"></label><textarea name="message" rows="6" maxlength="4000" required></textarea><label class="email-label"></label><input name="email" type="email" maxlength="254"><p class="feedback-notice"></p><p class="feedback-status" role="status" aria-live="polite"></p><button class="button" type="submit"></button></form>';
 document.body.append(dialog);
 const form=dialog.querySelector('form'), submit=form.querySelector('[type=submit]'), status=form.querySelector('.feedback-status');
 form.querySelector('h2').textContent=t[0];
 const titleId='feedback-title';form.querySelector('h2').id=titleId;dialog.setAttribute('aria-labelledby',titleId);
 const close=form.querySelector('.feedback-close');close.textContent=t[14];close.onclick=()=>dialog.close();
 ['category','message','email'].forEach((name,i)=>{
   const id='feedback-'+name;form.elements[name].id=id;
   const label=form.querySelector('.'+name+'-label');label.htmlFor=id;label.textContent=t[[1,6,7][i]];
 });
 ['bug','feature_request','suggestion','other'].forEach((value,i)=>{const option=document.createElement('option');option.value=value;option.textContent=t[i+2];form.elements.category.append(option)});
 form.querySelector('.feedback-notice').textContent=t[15];submit.textContent=t[8];
 triggers.forEach(button=>{button.textContent=t[0];button.addEventListener('click',()=>dialog.showModal())});
 let sending=false;
 dialog.addEventListener('cancel',event=>{if(sending)event.preventDefault()});
 form.addEventListener('submit',async event=>{
  event.preventDefault();if(sending)return;
  const message=form.elements.message.value.trim(),email=form.elements.email.value.trim();
  if([...message].length<5||[...message].length>4000||(email&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))){status.textContent=t[13];return}
  sending=true;submit.disabled=true;close.disabled=true;submit.textContent=t[9];status.textContent='';
  const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),20000);
  try {
   const url=new URL(endpoint);if(url.protocol!=='https:')throw new Error('configuration');
   const response=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({category:form.elements.category.value,message,...(email?{email}:{}),source:'website',platform:'web',language:lang}),
    credentials:'omit',signal:controller.signal,redirect:'error'});
   if(localDevelopment)form.dataset.httpStatus=String(response.status);
   if(response.status===429){status.textContent=t[12];return}
   if(response.status===400){status.textContent=t[13];return}
   if(response.status!==201)throw new Error('delivery');
   const result=await response.json();if(result.success!==true||typeof result.id!=='string')throw new Error('response');
   if(localDevelopment){form.dataset.feedbackId=result.id;form.dataset.success=String(result.success)}
   form.reset();status.textContent=t[10];
  }catch(_){status.textContent=t[11]}
  finally{clearTimeout(timeout);sending=false;submit.disabled=false;close.disabled=false;submit.textContent=t[8]}
 });
})();
