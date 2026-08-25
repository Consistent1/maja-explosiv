#!/usr/bin/env python3
"""Stage 1 V - local checks only (V1a, V2, V3, V6, V7, V11).
V0b/V0c/V4-vs-live/V5-vs-live/V8 need the live site and are NOT run here."""
import json, os, re, html, sys, hashlib, unicodedata

def ws(x):
    """V3 normalization: collapse ASCII whitespace runs, NFC, drop trailing space.
    U+00A0 is deliberately NOT collapsed -- it is a real character in this content
    and collapsing it would hide a genuine difference."""
    return unicodedata.normalize('NFC', re.sub(r'[ \t\r\n]+', ' ', x)).rstrip(' ')
ROOT=os.path.join(os.path.dirname(__file__),'..','..')
OUT=os.path.join(os.path.dirname(__file__),'..','links')
norm=json.load(open(f'{OUT}/normalized/links.json'))
rendered=open(f'{ROOT}/_site/about/links/index.html',encoding='utf-8').read()

# re-extract structure from the RENDERED html
body=rendered[rendered.index('about-links'):]
blocks=re.split(r'<h4[^>]*class="[^"]*about-section-heading--sub[^"]*"[^>]*>', body)
rend=[]
for b in blocks[1:]:
    heading=html.unescape(re.sub('<[^>]+>','',b[:b.index('</h4>')])).strip()
    ul=b[b.index('<ul'):b.index('</ul>')]
    entries=[]
    for li in re.findall(r'<li class="about-links-entry">(.*?)</li>', ul, re.S):
        m=re.search(r'<a href="([^"]*)"[^>]*>(.*?)</a>', li, re.S)
        pre=html.unescape(re.sub('<[^>]+>','',li[:m.start()]))
        suf=html.unescape(re.sub('<[^>]+>','',li[m.end():]))
        entries.append(dict(text=pre, url=html.unescape(m.group(1)),
                            name=html.unescape(re.sub('<[^>]+>','',m.group(2))), suffix=suf))
    rend.append(dict(heading=heading, entries=entries))

src=[dict(heading=c['heading'],
          entries=[dict(text=(e['prefix']+' ') if e['prefix'] else '',
                        url=e['url'], name=e['name'], suffix=e['suffix'])
                   for e in c['entries']]) for c in norm['categories']]

fails=[]; report=[]
def chk(name, ok, detail=''):
    report.append((name, 'PASS' if ok else 'FAIL', detail))
    if not ok: fails.append(name)

ns=sum(len(c['entries']) for c in src); nr=sum(len(c['entries']) for c in rend)
conv=open(f'{OUT}/converted/links.md').read().count('\n        url:')+open(f'{OUT}/converted/links.md').read().count('\n        url: ')
nc=len(re.findall(r'^\s+url: ', open(f'{OUT}/converted/links.md').read(), re.M))
chk('V1a count parity (source=normalized=converted=rendered)',
    ns==nc==nr, f'source={ns} converted={nc} rendered={nr}')
chk('V1a category parity', len(src)==len(rend), f'source={len(src)} rendered={len(rend)}')

su={e['url'] for c in src for e in c['entries']}; ru={e['url'] for c in rend for e in c['entries']}
chk('V2 bijection on url (both directions)', su==ru,
    f'source-only={sorted(su-ru)[:3]} rendered-only={sorted(ru-su)[:3]}')

diffs=[]
for cs, cr in zip(src, rend):
    if ws(cs['heading'])!=ws(cr['heading']): diffs.append(f"heading: {cs['heading']!r} != {cr['heading']!r}")
    for a,b in zip(cs['entries'], cr['entries']):
        for k in ('text','url','name','suffix'):
            av, bv = (a[k], b[k]) if k=='url' else (ws(a[k]), ws(b[k]))
            if av!=bv: diffs.append(f"[{a['url']}] {k}: {av!r} != {bv!r}")
chk('V3 field fidelity (source vs rendered)', not diffs, f'{len(diffs)} differences')

order_ok=all(cs['heading']==cr['heading'] for cs,cr in zip(src,rend)) and all(
    [e['url'] for e in cs['entries']]==[e['url'] for e in cr['entries']] for cs,cr in zip(src,rend))
chk('V4 order fidelity (source vs rendered)', order_ok)

raw=open(f'{OUT}/raw/db/tt_content-1399.bodytext.html',encoding='utf-8').read()
missing=[u for u in su if u not in raw]
chk('V6 every url byte-identical to the database bodytext', not missing, f'missing={missing[:3]}')
chk('V6 no silent http->https rewriting',
    all(e['url'] in raw for c in rend for e in c['entries']))

moji=[s for s in ('Ã','Â','â€','ï»¿','Ã¤') if s in rendered]
chk('V7 no mojibake in rendered html', not moji, f'found={moji}')
# Positive encoding test derived from the source, not hardcoded: every non-ASCII
# string the source carries must appear intact in the rendered output. A hardcoded
# list rots -- 'Château de Monthelon' was a valid test until the entry was removed.
acc=set()
for c in norm['categories']:
    for e in c['entries']:
        for fld in (e['prefix'], e['name'], e['suffix']):
            if any(ord(ch)>127 for ch in fld): acc.add(fld.strip())
absent=[a for a in acc if a and a not in rendered]
chk('V7 every non-ASCII source string renders intact', not absent,
    f'{len(acc)} checked: {sorted(acc)} | absent={absent}')

art=os.path.exists(f'{OUT}/converted/links.md')
inst=os.path.exists(f'{ROOT}/src/pages/about/links.md')
same=art and inst and open(f'{OUT}/converted/links.md','rb').read()==open(f'{ROOT}/src/pages/about/links.md','rb').read()
chk('V11 installed file matches the migrated artefact', same)
stray=[p for p in os.popen(f'find {ROOT}/src/pages {ROOT}/src/posts -name "*.md"').read().split() if p]
chk('V11 src/ contains only migration output', len(stray)==1, f'{len(stray)} files: {[os.path.basename(x) for x in stray]}')

w=max(len(n) for n,_,_ in report)
for n,s,d in report: print(f"{s:4}  {n:<{w}}  {d}")
print(f"\n{len(report)-len(fails)}/{len(report)} local checks passed")
if diffs:
    print("\nV3 differences:"); [print('  '+d) for d in diffs[:10]]
sys.exit(1 if fails else 0)
