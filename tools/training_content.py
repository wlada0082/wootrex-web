from pathlib import Path
import re, json, html, unicodedata
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'tools/fitness_portal'
CATEGORIES={'gym':'Posilovna','home':'Doma','street':'Street workout','conditioning':'Kondice','running':'Běh'}
LEVELS={'beginner':'Začátečník','intermediate':'Středně pokročilý','advanced':'Pokročilý'}
def esc(x):return html.escape(str(x),quote=True)
def slug(x):return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode().lower()).strip('-')
def extend_templates(templates):
    catalog=json.loads((DATA/'training_plans.json').read_text(encoding='utf-8'))
    publication=json.loads((DATA/'training_articles.json').read_text(encoding='utf-8'))
    plans=catalog['plans'];articles=publication['articles'];public={}
    base=templates[Path('treninky/treninkovy-denik/index.html')]
    def page(title,description,body):
        s=re.sub(r'<title>.*?</title>',lambda m:'<title>'+esc(title)+' · WOOTREX</title>',base,count=1,flags=re.S)
        s=re.sub(r'<meta name="description" content="[^"]*">',lambda m:'<meta name="description" content="'+esc(description)+'">',s,count=1)
        return re.sub(r'<main id="main">.*?</main>',lambda m:'<main id="main">'+body+'</main>',s,flags=re.S)
    def add(route,title,description,body,kind='page',sources=None):
        templates[Path(route.strip('/'))/'index.html']=page(title,description,body)
        public[route]={'kind':kind,'title':title,'description':description,'sources':sources or [],'datePublished':publication['publishedAt']}
    def article_card(a):
        cover=esc(a['cover']).replace('\n','<br>')
        return '<a class="article-card" href="/treninky/'+a['slug']+'/"><div class="cover editorial-cover" aria-hidden="true"><span>'+esc(a['label'])+'</span><strong>'+cover+'</strong><b>↗</b></div><div class="meta"><span class="category">Tréninky</span><span>'+str(a['minutes'])+' min čtení</span></div><h3>'+esc(a['title'])+'</h3><p>'+esc(a['description'])+'</p><span class="read">Číst článek <span>↗</span></span></a>'
    def plan_card(p):
        all_names=' '.join(x['name'] for x in p['exercises'])
        search=p['name']+' '+p['description']+' '+all_names+' '+' '.join(p['equipment'])
        return '<article class="plan-card" data-plan-category="'+p['category']+'" data-plan-level="'+p['level']+'" data-plan-search="'+esc(search)+'"><div class="meta"><span class="category">'+CATEGORIES[p['category']]+'</span><span>≈ '+str(p['estimatedMinutes'])+' min</span></div><h2>'+esc(p['name'])+'</h2><p class="plan-level">'+LEVELS[p['level']]+'</p><p>'+esc(p['description'])+'</p><p class="plan-exercises">'+esc(', '.join(x['name'] for x in p['exercises'][:3]))+('…' if len(p['exercises'])>3 else '')+'</p><a class="text-link" href="/treninky/plany/'+p['id']+'/">Prohlédnout plán <span>↗</span></a></article>'
    plan_banner='''<section class="training-promo"><div><p class="eyebrow">HOTOVÉ PŘEDLOHY Z WOOTREX</p><h2>Vyber plán. Drž se ho. Sleduj progres.</h2><p>19 předloh pro posilovnu, domácí cvičení, street workout, kondici i běh. S konkrétními cviky a předepsanými sériemi nebo úseky.</p></div><a class="btn" href="/treninky/plany/">Prohlédnout plány <span>↗</span></a></section>'''
    training=Path('treninky/index.html')
    s=templates[training].replace('Začni přehledným zápisem. Vrať se k historii. Dej svým tréninkům souvislosti.','Jednoduchý plán, stálé cviky a postupné přetížení. Sleduj vlastní výkon a dej konzistenci čas.')
    s=s.replace('<section class="section magazine"',plan_banner+'<section class="section magazine"',1)
    s=s.replace('<div class="cards">','<div class="cards">'+''.join(article_card(a) for a in articles),1)
    s=s.replace('Zobrazené články: 3','Zobrazené články: '+str(3+len(articles)))
    templates[training]=s
    magazine=Path('magazin/index.html');s=templates[magazine].replace('<div class="cards">','<div class="cards">'+''.join(article_card(a) for a in articles),1).replace('Zobrazené články: 6','Zobrazené články: '+str(6+len(articles)));templates[magazine]=s
    home=templates[Path('index.html')]
    home=re.sub(r'(<div class="cards">).*?(</div></section></div><section class="section app-band")',lambda m:m[1]+''.join(article_card(a) for a in articles[:3])+m[2],home,count=1,flags=re.S)
    templates[Path('index.html')]=home
    for a in articles:
        body=(DATA/'articles'/(a['slug']+'.html')).read_text(encoding='utf-8')
        headings=[]
        def heading(m):
            text=m[1];sid=slug(re.sub('<[^>]+>','',text));headings.append((sid,text));return '<h2 id="'+sid+'">'+text+'</h2>'
        body=re.sub(r'<h2>(.*?)</h2>',heading,body)
        contents='<nav class="article-contents" aria-label="V článku"><strong>V článku</strong><ul>'+''.join('<li><a href="#'+sid+'">'+text+'</a></li>' for sid,text in headings)+'</ul></nav>'
        refs='<section class="references" aria-labelledby="zdroje"><h2 id="zdroje">Z čeho článek vychází</h2><ol>'+''.join('<li id="zdroj-'+str(i+1)+'"><a href="'+esc(r['url'])+'" target="_blank" rel="noopener">'+esc(r['title'])+' ↗</a><p>'+esc(r['note'])+'</p></li>' for i,r in enumerate(a['sources']))+'</ol></section>'
        if not a['sources']: refs=''
        publication_meta=esc(a.get('editorialLabel','Redakce WOOTREX'))+' · '+esc(a.get('displayDate','25. října 2026'))+' · '+str(a['minutes'])+' min čtení'+(' · Studie a další zdroje najdeš na konci' if a['sources'] else '')
        aside='''<aside class="article-aside"><img src="/assets/wootrex-splash-logo.png" width="55" height="55" alt=""><h3>Od čtení<br>k tréninku.</h3><p>Vyber si předlohu, prohlédni cviky a ve WOOTREX sleduj vlastní záznamy.</p><a class="btn" href="/treninky/plany/">Vybrat plán <span>↗</span></a></aside>'''
        related='<section class="section related-articles"><p class="eyebrow">DALŠÍ SOUVISLOSTI</p><h2>Čti dál.</h2><div class="cards">'+''.join(article_card(x) for x in articles if x!=a)+'</div></section>'
        main='<div class="wrap"><header class="page-head article-head"><div class="crumb"><a href="/treninky/">Tréninky</a><span>/</span><span>Články</span></div><p class="eyebrow">'+esc(a['label'])+'</p><h1>'+esc(a['title'])+'</h1><p class="lead">'+esc(a['description'])+'</p><p class="publication-meta">'+publication_meta+'</p></header><div class="article-layout"><article class="prose">'+contents+body+refs+'<div class="callout"><h2>Přenes to do svého tréninku</h2><p>Mrkni na <a href="/treninky/plany/">plány z katalogu aplikace</a> nebo si prohlédni <a href="/aplikace/">WOOTREX</a>. Zapiš, co jsi odcvičil, a příště máš na co navázat.</p></div></article>'+aside+'</div>'+related+'</div>'
        add('/treninky/'+a['slug']+'/',a['title'],a['description'],main,'article',a['sources'])
        public['/treninky/'+a['slug']+'/']['datePublished']=a.get('publishedAt',publication['publishedAt'])
    chips='<div class="plan-categories" role="group" aria-label="Prostředí tréninku"><button type="button" class="filter active" data-plan-filter="all" aria-pressed="true">Vše</button>'+''.join('<button type="button" class="filter" data-plan-filter="'+k+'" aria-pressed="false">'+v+'</button>' for k,v in CATEGORIES.items())+'</div>'
    controls='<div class="plan-filter-controls" hidden>'+chips+'<div class="plan-search-row"><label for="plan-search">Hledat plán nebo cvik<input id="plan-search" type="search" placeholder="Např. full body nebo kliky…"></label><label for="plan-level">Náročnost<select id="plan-level"><option value="all">Všechny úrovně</option>'+''.join('<option value="'+k+'">'+v+'</option>' for k,v in LEVELS.items())+'</select></label></div></div>'
    weeks='''<section class="section prose weekly-examples" id="tyden"><h2>Příklady rozvržení týdne</h2><p>Šablona je jedna tréninková jednotka. Následující rozvrhy jsou organizační příklady, ne osobní předpis podle věku nebo pohlaví.</p><div class="table-scroll"><table><thead><tr><th>Kolikrát týdně</th><th>Příklad</th><th>Pro koho může být praktický</th></tr></thead><tbody><tr><td>2×</td><td>Pondělí a čtvrtek: Full Body – začátečník</td><td>Zdravý začátečník, který se učí základům</td></tr><tr><td>3×</td><td>Po / st / pá: Full Body A / B / A, další týden B / A / B</td><td>Člověk se zkušeností s uvedenými cviky a prostorem pro regeneraci</td></tr><tr><td>4×</td><td>Po Upper, út Lower, čt Upper, pá Lower</td><td>Cvičící, kterému rozdělení horní a dolní části vyhovuje</td></tr></tbody></table></div><p>PUSH, PULL a LEGS jsou také jednotlivé jednotky. Výběr jedné z nich neznamená vyvážený celotýdenní program. U domácích šablon si v celém týdnu pohlídej i dřepový pohyb pro nohy a tahy pro záda.</p><p>Obecná doporučení počítají s procvičením hlavních svalových skupin alespoň dva dny týdně. <a href="https://www.ncbi.nlm.nih.gov/books/NBK566046/" target="_blank" rel="noopener">WHO: doporučení pro dospělé ↗</a> Rozvržení přizpůsob tomu, co skutečně zvládáš.</p></section>'''
    main='<div class="wrap"><header class="page-head"><div class="crumb"><a href="/treninky/">Tréninky</a><span>/</span><span>Plány</span></div><p class="eyebrow">PŘEDLOHY Z KATALOGU WOOTREX</p><h1>Tréninkové plány</h1><p class="lead">Vyber si prostředí a náročnost. U každého plánu najdeš cviky, série a opakování nebo časové úseky tak, jak jsou uvedené v katalogu aplikace.</p><div class="actions"><a class="text-link" href="/treninky/jak-si-nastavit-trenink/">Jak si nastavit trénink <span>↗</span></a><a class="text-link" href="#tyden">Příklady tréninkového týdne <span>↓</span></a><a class="text-link" href="/treninky/progresivni-pretizeni/">Jak postupně přidávat <span>↗</span></a></div></header><section class="section plans-section">'+controls+'<p class="plan-result-count" id="plan-results" role="status" aria-live="polite">Zobrazené plány: 19</p><div class="plan-grid">'+''.join(plan_card(p) for p in plans)+'</div><p id="plan-empty" class="empty" hidden>Takový plán tu zatím není. Zkus jiný název, prostředí nebo náročnost.</p><p class="catalog-note">Obsah katalogu ověřen 25. října 2026. Časy jsou orientační; nabídka aplikace se může lišit podle verze. Jde o předlohy k přizpůsobení, ne individuální plán pro každého.</p></section>'+weeks+'</div>'
    add('/treninky/plany/','Tréninkové plány z aplikace WOOTREX','19 hotových předloh: cviky, série, opakování, vybavení a náročnost. Vyber si plán pro posilovnu, domov nebo venek.',main)
    for p in plans:
        rows=''
        for i,e in enumerate(p['exercises']):
            if e['isCardio']:sets='—';reps='Časové úseky níže'
            else:sets=p['setCounts'].get(e['id'],p['sets']);reps=str(p['minReps'])+'–'+str(p['maxReps'])
            rows+='<tr><td>'+str(i+1)+'</td><td>'+esc(e['name'])+'</td><td>'+str(sets)+'</td><td>'+reps+'</td></tr>'
        table='<div class="table-scroll" tabindex="0" role="region" aria-label="Cviky a parametry plánu"><table class="plan-table"><caption>Parametry předlohy z katalogu aplikace</caption><thead><tr><th>Pořadí</th><th>Cvik</th><th>Série</th><th>Opakování / čas</th></tr></thead><tbody>'+rows+'</tbody></table></div>'
        def duration(seconds):return str(seconds//60)+' min' if seconds%60==0 else str(seconds)+' s'
        intervals=''
        if p['intervals']:
            intervals='<h2>Časové úseky</h2><ul>'+''.join('<li>'+str(x.get('repetitions',1))+' × '+duration(x['durationSeconds'])+' '+esc(x['label'])+(' / '+duration(x['recoverySeconds'])+' lehce' if x.get('recoverySeconds') else '')+'</li>' for x in p['intervals'])+'</ul>'
        special={
          'full-body-start':'Před první sérií si nech ukázat nastavení strojů. Dvě pracovní série jsou výchozí hodnota předlohy; rozcvičení eviduj odděleně podle potřeby.',
          'home-full':'Tato krátká domácí šablona nemá samostatný dřepový ani tahový cvik pro záda. Pro vyvážený týden ji doplň vhodným pohybem pro nohy a přítahy podle vybavení.',
          'home-upper':'Odporovou gumu bezpečně upevni a zkontroluj její stav. Zvol odpor, který zvládáš v kontrolovaném pohybu.',
          'circuit':'Dvě série u každého cviku zde znamenají dvě kola. V jednom kole projdi cviky po jedné sérii; odpočinek přizpůsob potřebě.',
          'conditioning':'Silovou část projdi ve třech kolech. Deset minut lehkého rotopedu následuje až po ní.',
          'street-pull':'Pokročilá předloha. Počty opakování nejsou důvodem pokračovat po ztrátě techniky; zvol lehčí variantu, pokud ji potřebuješ.'
        }.get(p['id'],'Jde o jednu tréninkovou jednotku. Rozložení celého týdne a zátěž zvol podle zkušeností, ostatního pohybu a zotavení.')
        instructions='''<h2>Jak s předlohou pracovat</h2><ol><li>Začni zahřátím a nácvikem pohybů. U silových cviků zvol zátěž, kterou ovládáš s rezervou; kilogramy šablona nepředepisuje.</li><li>Uvedené série a opakování ber jako výchozí rámec. Pauzu přizpůsob tak, abys další sérii zvládl kontrolovaně. U cviků na jednu stranu procvič obě strany a drž stejný způsob zápisu.</li><li>Zapisuj skutečný výkon. Když rozsah nezvládáš bez ztráty techniky, uprav zátěž nebo variantu cviku.</li></ol>''' if p['category']!='running' else '<h2>Jak s předlohou pracovat</h2><p>Řiď se popisem jednotlivých úseků a svou současnou kondicí. Rychlejší běžecké předlohy jsou označené pro středně pokročilé; nejde o pokyn začínat intervaly po dlouhé neaktivitě.</p>'
        facts='<dl class="plan-facts"><div><dt>Prostředí</dt><dd>'+CATEGORIES[p['category']]+'</dd></div><div><dt>Náročnost</dt><dd>'+LEVELS[p['level']]+'</dd></div><div><dt>Orientační čas</dt><dd>'+str(p['estimatedMinutes'])+' minut</dd></div><div><dt>Vybavení</dt><dd>'+esc(', '.join(p['equipment']) or 'Bez speciálního vybavení')+'</dd></div></dl>'
        other=[x for x in plans if x['category']==p['category'] and x['id']!=p['id']][:2]
        main='<div class="wrap"><header class="page-head article-head"><div class="crumb"><a href="/treninky/">Tréninky</a><span>/</span><a href="/treninky/plany/">Plány</a></div><p class="eyebrow">PŘEDLOHA Z APLIKACE</p><h1>'+esc(p['name'])+'</h1><p class="lead">'+esc(p['description'])+'</p><p class="publication-meta">Přepis katalogu WOOTREX · ověřeno 25. října 2026</p></header>'+facts+'<div class="article-layout"><article class="prose"><h2>Cviky a parametry</h2>'+table+intervals+'<h2>Zaměření a četnost</h2><p>'+esc(p['goal'])+'. '+esc(p['frequency'])+'</p><div class="callout"><p>'+esc(special)+'</p></div>'+instructions+'<p>Další postup vysvětluje <a href="/treninky/progresivni-pretizeni/">článek o progresivním přetížení</a>. Zdravotní omezení nebo návrat po úrazu mohou vyžadovat individuální úpravu; označení „začátečník“ samo vhodnost neposuzuje.</p><h2>Kde plán najdeš ve WOOTREX</h2><p>Otevři v aplikaci <strong>Trénink → Katalog tréninků</strong> a vyhledej <strong>'+esc(p['name'])+'</strong>. Předlohu přidej do svých tréninků. Vlastní kopii pak můžeš upravit a zapisovat skutečně odcvičené série; web ji do aplikace nepřenáší automaticky.</p><div class="actions"><a class="btn" href="/aplikace/#stazeni">Získat WOOTREX <span>↗</span></a><a class="text-link" href="/treninky/plany/">Další plány <span>→</span></a></div><p class="catalog-note">Cviky, pořadí, série, rozsahy a intervaly pocházejí z katalogu aplikace. Vysvětlení použití je doplněné pro web. Dostupnost se může lišit podle verze.</p></article><aside class="article-aside"><h3>Vyber plán<br>pro svůj týden.</h3><p>Podívej se také na příklady rozvržení. Jedna šablona nenahrazuje rozvrh všech aktivit.</p><a class="btn" href="/treninky/plany/#tyden">Příklady týdne <span>↗</span></a></aside></div>'+('<section class="section"><h2>Další předlohy</h2><div class="plan-grid">'+''.join(plan_card(x) for x in other)+'</div></section>' if other else '')+'</div>'
        add('/treninky/plany/'+p['id']+'/',p['name']+' — plán z aplikace',p['description'],main)
    return public
