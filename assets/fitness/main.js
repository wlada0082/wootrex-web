
document.documentElement.classList.add('js');
const menu=document.querySelector('.menu'), nav=document.querySelector('.nav');
if(menu&&nav){menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.textContent=open?'Zavřít ×':'Menu +';nav.classList.toggle('open',open)});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){menu.click();menu.focus()}})}
const input=document.querySelector('#article-search');
if(input){const cards=[...document.querySelectorAll('.article-card')],count=document.querySelector('#result-count'),empty=document.querySelector('#no-results');const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();input.addEventListener('input',()=>{const q=normalize(input.value.trim());let n=0;cards.forEach(card=>{const show=normalize(card.textContent).includes(q);card.hidden=!show;if(show)n++});count.textContent='Zobrazené články: '+n;empty.hidden=n!==0})}
