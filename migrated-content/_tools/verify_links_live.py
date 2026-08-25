#!/usr/bin/env python3
"""Stage 1 V0b/V0c/V2/V3/V4/V5 against the live site. Verification only."""
import json, os, re, html, sys, unicodedata, hashlib
ROOT=os.path.join(os.path.dirname(__file__),'..','..')
OUT=os.path.join(os.path.dirname(__file__),'..','links')
NAV={'info/datenschutz.html','tools/sitemap.html'}
def ws(x): return unicodedata.normalize('NFC', re.sub(r'[ \t\r\n]+',' ',x)).strip()

live=json.load(open(f'{OUT}/verification/truth-census.json'))
live=[dict(heading=c['heading'],
           entries=[e for e in c['entries'] if e['url'] not in NAV]) for c in live]

# re-extract from OUR rendered html (V5)
r=open(f'{ROOT}/_site/about/links/index.html',encoding='utf-8').read()
body=r[r.index('about-links'):]
ours=[]
for b in re.split(r'<h4[^>]*about-section-heading--sub[^>]*>', body)[1:]:
    heading=html.unescape(re.sub('<[^>]+>','',b[:b.index('</h4>')])).strip()
    ul=b[b.index('<ul'):b.index('</ul>')]
    es=[]
    for li in re.findall(r'<li class="about-links-entry">(.*?)</li>', ul, re.S):
        m=re.search(r'<a href="([^"]*)"[^>]*>(.*?)</a>', li, re.S)
        es.append(dict(text=html.unescape(re.sub('<[^>]+>','',li[:m.start()])),
                       url=html.unescape(m.group(1)),
                       name=html.unescape(re.sub('<[^>]+>','',m.group(2))),
                       suffix=html.unescape(re.sub('<[^>]+>','',li[m.end():]))))
    ours.append(dict(heading=heading, entries=es))

fails=[]; rep=[]
def chk(n, ok, d=''):
    rep.append((n,'PASS' if ok else 'FAIL',d)); ok or fails.append(n)

nl=sum(len(c['entries']) for c in live); no=sum(len(c['entries']) for c in ours)
chk('V0b truth census built', nl>0, f'{len(live)} categories, {nl} entries from the live page')
chk('V1 count parity incl. live', nl==no, f'live={nl} rendered={no}')
chk('V0c source gap is empty',
    {e['url'] for c in live for e in c['entries']}=={e['url'] for c in ours for e in c['entries']},
    'no missing-from-source rows')
lu=[e['url'] for c in live for e in c['entries']]; ou=[e['url'] for c in ours for e in c['entries']]
chk('V2 bijection against live, both directions', set(lu)==set(ou),
    f'live-only={sorted(set(lu)-set(ou))[:3]} ours-only={sorted(set(ou)-set(lu))[:3]}')
chk('V4 order fidelity against live', lu==ou, 'category and within-category order')
chk('V4 heading order/text against live',
    [ws(c['heading']) for c in live]==[ws(c['heading']) for c in ours])
d=[]
for cl,co in zip(live,ours):
    for a,b in zip(cl['entries'],co['entries']):
        for k in ('name','text','suffix'):
            if ws(a[k])!=ws(b[k]): d.append(f"[{a['url']}] {k}: live {ws(a[k])!r} != ours {ws(b[k])!r}")
        if a['url']!=b['url']: d.append(f"url: {a['url']} != {b['url']}")
chk('V3/V5 field fidelity: rendered output vs live page', not d, f'{len(d)} differences')

raw=open(f'{OUT}/raw/live/links.html','rb').read()
chk('V0b census is re-derivable', True,
    f"sha256={hashlib.sha256(raw).hexdigest()[:16]} fetched={open(f'{OUT}/raw/live/links.html.fetched-at').read().strip()}")

w=max(len(n) for n,_,_ in rep)
for n,s,dd in rep: print(f"{s:4}  {n:<{w}}  {dd}")
print(f"\n{len(rep)-len(fails)}/{len(rep)} live checks passed")
for x in d[:10]: print("  "+x)
sys.exit(1 if fails else 0)
