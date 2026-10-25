
document.documentElement.classList.add('js');
const menu=document.querySelector('.menu'), nav=document.querySelector('.nav');
if(menu&&nav){menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.textContent=open?'Zavřít ×':'Menu +';nav.classList.toggle('open',open)});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){menu.click();menu.focus()}})}
const input=document.querySelector('#article-search');
if(input){const cards=[...document.querySelectorAll('.article-card')],count=document.querySelector('#result-count'),empty=document.querySelector('#no-results');const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();input.addEventListener('input',()=>{const q=normalize(input.value.trim());let n=0;cards.forEach(card=>{const show=normalize(card.textContent).includes(q);card.hidden=!show;if(show)n++});count.textContent='Zobrazené články: '+n;empty.hidden=n!==0})}

const planControls=document.querySelector('.plan-filter-controls');
if(planControls){
  const plans=[...document.querySelectorAll('.plan-card')],buttons=[...document.querySelectorAll('[data-plan-filter]')],search=document.querySelector('#plan-search'),level=document.querySelector('#plan-level'),count=document.querySelector('#plan-results'),empty=document.querySelector('#plan-empty');
  const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  let category='all';
  const update=()=>{let visible=0;const query=normalize(search.value.trim());plans.forEach(card=>{const show=(category==='all'||card.dataset.planCategory===category)&&(level.value==='all'||card.dataset.planLevel===level.value)&&normalize(card.dataset.planSearch).includes(query);card.hidden=!show;if(show)visible++});count.textContent='Zobrazené plány: '+visible;empty.hidden=visible!==0};
  buttons.forEach(button=>button.addEventListener('click',()=>{category=button.dataset.planFilter;buttons.forEach(item=>{const selected=item===button;item.classList.toggle('active',selected);item.setAttribute('aria-pressed',String(selected))});update()}));
  search.addEventListener('input',update);level.addEventListener('change',update);planControls.hidden=false;update();
}
