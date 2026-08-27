#!/usr/bin/env python3
"""Stage 4 C - bio. tt_content 1404 (pid 865) -> src/pages/about/bio.md

Split: paragraph 1 -> `excerpt` (rendered beside the portrait in the About intro),
paragraphs 2..n -> the Markdown body. Settled 2026-07-28, plan §7.
"""
import html, json, os, re
OUT=os.path.join(os.path.dirname(__file__),'..','bio')
raw=open(f'{OUT}/raw/db/tt_content-1404.bodytext.html',encoding='utf-8').read()

# the leading <img> is the portrait, embedded in bodytext; recorded, not inlined
img=re.search(r'<img[^>]+src="([^"]+)"', raw)
body=re.sub(r'<img[^>]*>','',raw)

# <br /><br /> separates paragraphs; a single <br /> is the author's manual line wrap
blocks=re.split(r'(?:<br\s*/?>\s*){2,}', body)
paras=[]
for b in blocks:
    t=re.sub(r'<br\s*/?>',' ', b)          # soft wrap -> space
    t=html.unescape(re.sub('<[^>]+>','',t))
    t=re.sub(r'[ \t\r\n]+',' ',t).strip()
    if t: paras.append(t)

def y(s): return '"'+s.replace('\\','\\\\').replace('"','\\"')+'"'
L=['---','title: "Bio"','layout: "about-page.njk"','permalink: "/about/bio/"',
   f'excerpt: {y(paras[0])}',
   'source_uid: "1404"','source_page: "865"','source_path: "info/bio"',
   f'source_portrait: {y(img.group(1) if img else "")}',
   f'source_paragraph_count: "{len(paras)}"',
   '---','']
L += ['\n\n'.join(paras[1:]), '']
open(f'{OUT}/converted/bio.md','w').write('\n'.join(L))
json.dump(dict(source='tt_content 1404 (pid 865)', portrait=img.group(1) if img else None,
               paragraphs=paras), open(f'{OUT}/normalized/bio.json','w'), indent=1, ensure_ascii=False)
print(f"paragraphs: {len(paras)}   excerpt {len(paras[0])} chars   body {sum(len(p) for p in paras[1:])} chars")
for i,p in enumerate(paras): print(f"  [{i}] {p[:88]}")
print(f"portrait (recorded, not inlined): {img.group(1) if img else '(none)'}")
