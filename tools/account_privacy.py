from pathlib import Path
import html,json,re


def feedback_paragraph(text,lang,item):
 if 'feedback' not in item: return text
 pattern=r'<p id="feedback-processing-'+lang+r'">.*?</p>|<p>[^<]*Cloudflare D1[^<]*</p>'
 return re.sub(pattern,lambda m:'<p id="feedback-processing-'+lang+'">'+item['feedback']+'</p>',text,flags=re.S)

def update(root):
 root=Path(root)
 data=json.loads((root/'tools/account_privacy_content.json').read_text(encoding='utf-8'))
 for path,languages in [(root/l/'privacy.html',[l]) for l in data]+[(root/'privacy.html',['cs','en'])]:
  text=path.read_text(encoding='utf-8')
  for lang in languages:
   item=data[lang]
   if 'feedback' in item:
    # Replace the existing feedback paragraph, retaining its heading.
    if len(languages)==1: text=feedback_paragraph(text,lang,item)
   # Replace a prior generated account block, so regeneration is idempotent.
   text=re.sub(r'<div lang="'+lang+r'" id="account-data-'+lang+r'">.*?</div>','',text,flags=re.S)
   if len(languages)>1:
    # Bilingual root uses the existing stable source section IDs.
    section_id={'cs':'cesky','en':'english'}[lang]
    pattern=r'(<section id="'+section_id+r'"[^>]*>)(.*?)(</section>)'
    def body(match):
     content=match[2]
     content=feedback_paragraph(content,lang,item)
     content=re.sub(r'(<h3>[^<]+</h3><p>)([^<]*)(</p>)',lambda m:m[1]+item['future']+m[3] if any(x in m[2] for x in ['při zavedení účtů','when accounts,']) else m[0],content)
     return match[1]+content+item['html']+match[3]
    text=re.sub(pattern,body,text,count=1,flags=re.S)
   else:
    # The last existing h3 paragraph is the policy's future-changes paragraph.
    paragraphs=list(re.finditer(r'<h3>[^<]+</h3><p>([^<]*)</p>',text))
    if paragraphs:
     m=paragraphs[-1];text=text[:m.start(1)]+item['future']+text[m.end(1):]
    text=text.replace('</main>',item['html']+'</main>',1)
    text=re.sub(r'(<h1>.*?</h1>)<p>[^<]*2026</p>',lambda m:m[1]+'<p>'+item['date']+'</p>',text,count=1)
  text=text.replace('8. října 2026','27. října 2026').replace('26. října 2026','27. října 2026').replace('8 October 2026','27 October 2026').replace('26 October 2026','27 October 2026')
  text=re.sub(r'(assets/css/style\.css)(?:\?[^"]*)?(?=")',r'\1?v=20261027-policy',text)
  path.write_text(text,encoding='utf-8')
 for lang,item in data.items():
  page=root/lang/'delete-account.html'
  if page.exists(): update_deletion_page(page,item)

def update_deletion_page(page, item):
 text=page.read_text(encoding='utf-8')
 title,intro,label,button,sending,success,error,rate,nojs=item['request']
 encode=html.escape
 title,intro,label,button,nojs=map(encode,(title,intro,label,button,nojs))
 form=f'''<section id="deletion-request" aria-labelledby="request-title"><h2 id="request-title">{title}</h2><p>{intro}</p>
<form id="delete-form" method="post"><label for="email">{label}</label>
<input id="email" name="email" type="email" autocomplete="email" maxlength="254" required>
<div hidden><label for="website">Website</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
<button class="button" type="submit" disabled>{button}</button></form>
<p id="deletion-status" class="deletion-status" role="status" aria-live="polite"></p>
<noscript><p>{nojs}</p></noscript></section>'''
 scope=item['requestScope']
 start=text.index('</h1>')+5
 end=text.index('</main>',start)
 text=text[:start]+form+scope+item['requestPolicy']+text[end:]
 messages=json.dumps(dict(sending=sending,success=success,error=error,rate=rate),ensure_ascii=False).replace('<','\\u003c')
 text=re.sub(r'(<script type="application/json" id="deletion-messages">).*?(</script>)',lambda m:m[1]+messages+m[2],text,flags=re.S)
 text=text.replace('https://qsruhiewyxnhxpvnibcc.supabase.co','https://feedback.wootrex.cz')
 text=re.sub(r'(assets/(?:css/(?:style|account-deletion)\.css|js/account-deletion\.js))(?:\?[^"]*)?(?=")',r'\1?v=20261115-request',text)
 page.write_text(text,encoding='utf-8')

if __name__=='__main__':update(Path(__file__).resolve().parents[1])
