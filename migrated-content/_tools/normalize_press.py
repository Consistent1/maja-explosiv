#!/usr/bin/env python3
"""Stage 2 N - press. tt_content 1452 -> ordered entries; 1456 -> the note."""
import json, os, re, html, sys, unicodedata
OUT=os.path.join(os.path.dirname(__file__),'..','press')
BU=os.path.join(os.path.dirname(__file__),'..','..','old','TYPO3BU','_')
raw=open(f'{OUT}/raw/db/tt_content-1452.bodytext.html',encoding='utf-8').read()
note=open(f'{OUT}/raw/db/tt_content-1456.bodytext.html',encoding='utf-8').read()

def clean(s):
    s=re.sub(r'<br\s*/?>',' ',s); s=html.unescape(re.sub('<[^>]+>','',s))
    return re.sub(r'[ \t\r\n]+',' ',s).strip()

def _exists(href):
    """The server stores umlauts in NFD, the database in NFC. A plain os.path.exists
    on the DB form reports every umlaut file as missing even when it is present."""
    p=os.path.join(BU,href)
    if os.path.exists(p): return True
    d,b=os.path.split(p)
    if not os.path.isdir(d): return False
    tgt=unicodedata.normalize('NFC',b)
    return any(unicodedata.normalize('NFC',x)==tgt for x in os.listdir(d))

LINK=re.compile(r'<link\s+([^>]*?)>(.*?)</link>', re.S)
entries=[]; anomalies=[]
# entries are separated by newlines, but a line may hold more than one <link>
pos=0
for m in LINK.finditer(raw):
    href=m.group(1).split()[0]
    title_anchor=clean(m.group(2))
    # trailing prose up to the next <link> or end of line
    tail=raw[m.end():]
    nxt=LINK.search(tail)
    seg=tail[:nxt.start()] if nxt else tail
    seg=seg.split('\n')[0]
    suffix=clean(seg)
    title=(title_anchor+suffix) if suffix.startswith((';',',')) else (title_anchor+' '+suffix).strip()
    entries.append(dict(title=re.sub(r'\s+',' ',title).strip(),
                        file=href,
                        file_exists=_exists(href),
                        is_pdf=href.lower().endswith('.pdf')))
data=dict(source='tt_content 1452 (entries) + 1456 (note), pid 981',
          note=clean(note), entries=entries, anomalies=anomalies)
json.dump(data, open(f'{OUT}/normalized/press.json','w'), indent=2, ensure_ascii=False)
print(f"entries: {len(entries)}   pdf: {sum(1 for e in entries if e['is_pdf'])}   "
      f"missing file: {sum(1 for e in entries if not e['file_exists'])}")
print(f"note: {data['note'][:80]!r}")
for e in entries[:4]: print(f"   {e['title'][:70]}")
