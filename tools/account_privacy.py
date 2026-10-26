from pathlib import Path
import json,re

def update(root):
 root=Path(root)
 data=json.loads((root/'tools/account_privacy_content.json').read_text(encoding='utf-8'))
 for path,languages in [(root/l/'privacy.html',[l]) for l in data]+[(root/'privacy.html',['cs','en'])]:
  text=path.read_text(encoding='utf-8')
  for lang in languages:
   item=data[lang]
   # Replace a prior generated account block, so regeneration is idempotent.
   text=re.sub(r'<div lang="'+lang+r'" id="account-data-'+lang+r'">.*?</div>','',text,flags=re.S)
   if len(languages)>1:
    # Bilingual root uses the existing stable source section IDs.
    section_id={'cs':'cesky','en':'english'}[lang]
    pattern=r'(<section id="'+section_id+r'"[^>]*>)(.*?)(</section>)'
    def body(match):
     content=match[2]
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
  text=text.replace('8. října 2026','26. října 2026').replace('8 October 2026','26 October 2026')
  path.write_text(text,encoding='utf-8')
if __name__=='__main__':update(Path(__file__).resolve().parents[1])
