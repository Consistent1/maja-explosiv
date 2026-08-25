#!/usr/bin/env python3
"""Stage 1 V0b - truth census from the live page. VERIFICATION ONLY."""
import re, html, json, os
OUT=os.path.join(os.path.dirname(__file__),'..','links')
t=open(f'{OUT}/raw/live/links.html','rb').read().decode('utf-8')
# isolate the content cell: from the first category heading to the footer email
start=t.index('<b>ROBOTIC')
end=t.index('m-e@maja-explosiv.com')
body=t[start:end]
# split on <b>...</b> headings
parts=re.split(r'<b>(.*?)</b>', body, flags=re.S)
cats=[]
for i in range(1,len(parts),2):
    heading=html.unescape(re.sub('<[^>]+>','',parts[i])).strip()
    chunk=parts[i+1] if i+1<len(parts) else ''
    entries=[]
    # each entry is one <p class="bodytext">
    for para in re.findall(r'<p class="bodytext">(.*?)</p>', chunk, re.S):
        anchors=list(re.finditer(r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>', para, re.S))
        if not anchors: continue
        # consecutive anchors sharing one href are an RTE split of a single link
        # (e.g. "Paka the U" + "ncredible"); rejoin them.
        first, last = anchors[0], anchors[-1]
        name=''.join(html.unescape(re.sub('<[^>]+>','',a.group(2))) for a in anchors
                     if a.group(1)==first.group(1))
        pre=html.unescape(re.sub('<[^>]+>','',para[:first.start()]))
        suf=html.unescape(re.sub('<[^>]+>','',para[last.end():]))
        entries.append(dict(text=pre.strip(), url=html.unescape(first.group(1)),
                            name=name.strip(), suffix=suf.rstrip(),
                            anchor_count=len(anchors)))
    cats.append(dict(heading=heading, entries=entries))
json.dump(cats, open(f'{OUT}/verification/truth-census.json','w'), indent=2, ensure_ascii=False)
n=sum(len(c['entries']) for c in cats)
print(f"live categories: {len(cats)}  entries: {n}")
for c in cats: print(f"  {len(c['entries']):>3}  {c['heading']}")
