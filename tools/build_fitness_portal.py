from pathlib import Path
import re, html, hashlib, json
from urllib.parse import urlsplit
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1]

def build(base_url, legacy_cs):
    base_url=base_url.rstrip('/')+'/'
    prefix=urlsplit(base_url).path.rstrip('/')
    templates=ROOT/'tools/fitness_portal/pages'
    beta=re.search(r'<section class="section beta" id="beta">.*?</section>',legacy_cs,re.S)
    if not beta:raise ValueError('Generated Czech download section is required')
    beta=beta.group(0).replace('class="section beta"','class="download-box beta"')
    beacon=re.search(r'<!-- Cloudflare Web Analytics -->.*?<!-- End Cloudflare Web Analytics -->',legacy_cs,re.S).group(0)
    language_links='<div class="public-languages" role="group" aria-label="Jazyk">'+''.join(f'<a href="{prefix}/{code}/" data-language="{code}" lang="{code}" hreflang="{code}"'+(' aria-current="page"' if code=='cs' else '')+f'>{label}</a>' for code,label in [('cs','CZ'),('en','EN'),('de','DE'),('sk','SK'),('pl','PL')])+'</div>'
    about='''<div class="wrap"><section class="page-head"><p class="eyebrow">O WOOTREX</p><h1>Pohyb, jídlo<br>a tvoje další verze.</h1><p class="lead">Inspirace pro běžný den a aplikace, ve které máš přehled o svém tréninku.</p></section><section class="section about-layout" style="padding-top:10px"><h2>Co tu najdeš</h2><p>Praktické články o zapisování a plánování tréninku, srozumitelné pojmy, inspiraci pro přípravu jídla a přehled aplikace WOOTREX. Obsah postupně rozšiřujeme.</p><h2>Jak přemýšlíme o tréninku</h2><p>Jednoduchý rozvrh, stálý základ cviků, pravidelnost a postupné přetížení. Místo hledání zázračného splitu sledujeme vlastní výkon. Pracovní váhy a opakování doplňujeme mírami a vývojem postavy; tělesnou hmotnost hodnotíme v kontextu cíle. Plán upravujeme z konkrétního důvodu, ne kvůli neustálému střídání.</p><a class="text-link" href="/treninky/jak-si-nastavit-trenink/">Jak si nastavit trénink a cíle ↗</a><h2>Aplikace WOOTREX</h2><p>Silový trénink, vlastní plány, historie, statistiky, outdoor aktivity a sledování postavy. Aktuální dostupné verze a postup instalace najdeš v části stažení.</p><a class="text-link" href="/aplikace/#stazeni">Poznat aplikaci a dostupnou betu ↗</a><h2>Jak označujeme obsah</h2><p>Vzdělávací články redakce WOOTREX odkazují na odborné zdroje a rozlišují jejich výsledky od praktických příkladů. Jde o obecné informace, nikoli individuální zdravotní doporučení. U plánů uvádíme původ v katalogu aplikace.</p><p>Články označené jako redakční koncept zatím neprošly odbornou kontrolou. U návrhu receptu uvádíme, že nebyl kuchyňsky ověřen, a neuvádíme neověřené nutriční výpočty. Koncepty zatím nenabízíme k indexaci vyhledávačům.</p><p>Výživové články a recepty jsou obsah webu. Výživový deník ani jídelníčky jako současnou funkci aplikace neslibujeme.</p><h2>Ukázky a vizuální podklady</h2><p>Snímky obrazovek zachycují aplikaci WOOTREX. Krátké video je sestřih těchto obrazovek, nikoli záznam ovládání. Fotografie činek je ilustrační obrázek vytvořený pomocí AI; grafický motiv u receptu nenahrazuje fotografii připraveného jídla.</p><h2>Kontakt</h2><p>Zpětnou vazbu nebo námět můžeš poslat přes kontaktní část webu.</p><a class="btn" href="/cs/stazeni/#kontakt">Přejít na kontakt <span>↗</span></a></section></div>'''
    css_version=hashlib.sha256((ROOT/'assets/fitness/style.css').read_bytes()).hexdigest()[:12]
    js_version=hashlib.sha256((ROOT/'assets/fitness/main.js').read_bytes()).hexdigest()[:12]
    indexable=[]
    all_templates={source.relative_to(templates):source.read_text(encoding='utf-8') for source in templates.rglob('*.html')}
    from training_content import extend_templates
    published_content=extend_templates(all_templates)
    for rel,s in sorted(all_templates.items()):
        route='/'+str(rel.parent).replace('\\','/').strip('.')
        route=route.rstrip('/')+'/' if route!='/' else '/'
        if route=='/o-webu/':
            s=re.sub(r'<main id="main">.*?</main>',lambda m:'<main id="main">'+about+'</main>',s,flags=re.S)
            s=s.replace('O návrhu fitness webu','O fitness webu').replace('O návrhu webu','O webu').replace('Obsahový a produktový směr samostatného webu WOOTREX.','Trénink, jídlo, aplikace a redakční pravidla webu WOOTREX.')
        s=re.sub(r'<div class="draft-bar">.*?</div></div>','',s,count=1,flags=re.S)
        s=s.replace('© 2026 WOOTREX · Pracovní návrh','© 2026 WOOTREX')
        s=s.replace('O návrhu webu','O webu')
        s=s.replace('V tomto návrhu jde o obsah webu.','Jde o obsah webu.')
        s=s.replace('Tlačítko stažení vede na hlavní web WOOTREX, který slouží jako společný rozcestník dostupných verzí.','Aktuální verze najdeš v sekci stažení na této stránce. Odkazy pro Android a iOS jsou uvedené samostatně.')
        s=s.replace('Texty jsou ukázky k redakčnímu ověření. Fotografie vybavení je ilustrace vytvořená AI.','Články označené jako koncept čekají na redakční ověření. Fotografie vybavení je ilustrace vytvořená AI.')
        s=s.replace('Redakční návrh · 25. října 2026 · Autor a odborná kontrola budou doplněni před veřejným vydáním.','Redakční koncept · 25. října 2026 · Zatím bez odborné kontroly.')
        s=s.replace('Návrh receptu pro ukázku webu.','Redakční koncept receptu.')
        s=s.replace('MAGAZÍN / PRVNÍ TÉMATA','MAGAZÍN / INSPIRACE PRO TEBE')
        s=s.replace('První recept jako ukázka budoucí kuchařky WOOTREX.','Recepty a inspirace pro každodenní vaření.')
        s=s.replace('Finální video doplníme záznamem skutečného ovládání.','Sestřih zachycuje skutečné obrazovky aplikace.')
        if route=='/':
            s=s.replace('<a class="text-link" href="/aplikace/">Poznat WOOTREX <span>→</span></a>','<a class="text-link" href="#beta" data-beta-cta data-cta="hero">Získat aplikaci <span>→</span></a>',1)
            s=s.replace('</main>',beta+'</main>')
        if route=='/aplikace/':
            s=re.sub(r'<section class="download-box" id="stazeni">.*?</section>',lambda m:'<div id="stazeni">'+beta+'</div>',s,flags=re.S)
            s=s.replace('<a class="btn" href="#stazeni">Získat betu','<a class="btn" href="#beta" data-beta-cta data-cta="hero">Získat betu')
        if route in ('/','/aplikace/'):
            s=s.replace('<a class="nav-cta" href="/aplikace/#stazeni">','<a class="nav-cta" href="#beta" data-beta-cta data-cta="nav">')
            s=s.replace('</head>',f'<script src="{prefix}/assets/js/beta-cta.js" defer></script></head>')
        for name in ['training.png.jpg','statistics.png.jpg','physique.png.jpg','wootrex-splash-logo.png']:
            s=s.replace('/assets/'+name,prefix+'/assets/images/'+name)
        for name in ['style.css','main.js','wootrex-ukazka.mp4','video-poster.jpg','captions.vtt']:
            s=s.replace('/assets/'+name,prefix+'/assets/fitness/'+name+('?v='+css_version if name=='style.css' else '?v='+js_version if name=='main.js' else ''))
        s=s.replace('/assets/gym-editorial.png',prefix+'/assets/fitness/gym-editorial.webp')
        # Rewrite the prototype root routes to Czech public routes. Asset paths are already final.
        def rewrite(match):
            attr,u=match.groups()
            if u.startswith('/assets/') or (prefix and u.startswith(prefix+'/assets/')):return match.group(0)
            if u.startswith('/cs/'):return f'{attr}="{prefix}{u}"'
            return f'{attr}="{prefix}/cs'+u+'"'
        s=re.sub(r'(href|src|poster)="(/[^\"]*)"',rewrite,s)
        s=s.replace('https://wootrex.cz/cs/privacy.html',base_url+'cs/privacy.html')
        s=s.replace('</head>',f'<script src="{prefix}/assets/js/language.js" defer></script></head>')
        footer_contact=f'<a href="{prefix}/cs/stazeni/#kontakt">Kontakt</a>'
        s=s.replace('<div class="footer-links">','<div class="footer-links" id="kontakt">'+footer_contact,1)
        s=s.replace('<div class="footer-bottom">',language_links+'<div class="footer-bottom">',1)
        draft=len(rel.parts)>2 and route not in published_content
        s=s.replace('<meta name="robots" content="noindex,nofollow">','<meta name="robots" content="noindex,follow">' if draft else '<meta name="robots" content="index,follow">')
        canonical=base_url+'cs/'+(route.lstrip('/') if route!='/' else '')
        title=re.search(r'<title>(.*?)</title>',s,re.S).group(1)
        desc=re.search(r'<meta name="description" content="([^"]*)"',s).group(1)
        seo=f'<link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{html.escape(html.unescape(title),quote=True)}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{base_url}assets/fitness/gym-editorial.webp"><meta property="og:locale" content="cs_CZ">'
        if route=='/':
            seo+=''.join(f'<link rel="alternate" hreflang="{l}" href="{base_url}{l}/">' for l in ['cs','en','de','sk','pl'])+f'<link rel="alternate" hreflang="x-default" href="{base_url}cs/">'
        if route in published_content and published_content[route]['kind']=='article':
            content=published_content[route]
            structured={'@context':'https://schema.org','@type':'Article','headline':content['title'],'description':content['description'],'datePublished':content['datePublished'],'dateModified':content['datePublished'],'author':{'@type':'Organization','name':'Redakce WOOTREX','url':base_url+'cs/o-webu/'},'publisher':{'@type':'Organization','name':'WOOTREX'},'mainEntityOfPage':canonical,'inLanguage':'cs','citation':[x['url'] for x in content['sources']]}
            seo+='<script type="application/ld+json">'+json.dumps(structured,ensure_ascii=False).replace('<','\\u003c')+'</script>'
            s=s.replace('property="og:type" content="website"','property="og:type" content="article"')
            seo=seo.replace('property="og:type" content="website"','property="og:type" content="article"')
        s=s.replace('</head>',seo+'</head>')
        s=s.replace('</body>',beacon+'</body>')
        target=ROOT/'cs'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(s+'\n',encoding='utf-8')
        if not draft:indexable.append(canonical)
        if route=='/':
            root=s.replace('<body>','<body data-language-entry="true">',1)
            (ROOT/'index.html').write_text(root+'\n',encoding='utf-8')
    # Preserve the full established landing page and contact flow on a stable standalone URL.
    archive=re.sub(r'(src|href)="(\.\./[^"]*)"', lambda m: m[1]+'="../'+m[2]+'"', legacy_cs).replace('href="privacy.html"','href="../privacy.html"')
    archive=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{base_url}cs/aplikace/">',archive,count=1)
    archive=archive.replace('</head>','<meta name="robots" content="noindex,follow"></head>')
    folder=ROOT/'cs/stazeni';folder.mkdir(parents=True,exist_ok=True);(folder/'index.html').write_text(archive,encoding='utf-8')
    extra=['privacy.html']+[l+'/'+f for l in ['cs','en','de','sk','pl'] for f in ['','privacy.html'] if l!='cs' or f!='']
    urls=sorted(set(indexable+[base_url+p for p in extra]))
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+escape(u)+'</loc></url>\n' for u in urls)+'</urlset>\n',encoding='utf-8')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /tools/\nSitemap: '+base_url+'sitemap.xml\n',encoding='utf-8')
    print('Built Czech fitness portal, preserved download/contact flow and generated public sitemap.')
