#!/usr/bin/env python3
"""Stage 1 N - normalize. TYPO3 RTE bodytext -> ordered structure. Source-shaped, not target-shaped.
hrefs are carried through byte-identically; nothing is rewritten (plan V6)."""
import json, os, re, sys, html
OUT=os.path.join(os.path.dirname(__file__),'..','links')
UID=sys.argv[1] if len(sys.argv)>1 else '1399'
FALLBACK_HEADING=sys.argv[2] if len(sys.argv)>2 else None
RAW=f'{OUT}/raw/db/tt_content-{UID}.bodytext.html'
OUTFILE=f'{OUT}/normalized/links-{UID}.json' if UID!='1399' else f'{OUT}/normalized/links.json'

text=open(RAW,'rb').read().decode('utf-8')          # already correct UTF-8, no transform
LINK=re.compile(r'<link\s+(?P<params>[^>]*?)>(?P<anchor>.*?)</link>', re.S)
BOLD=re.compile(r'<b>(?P<h>.*?)</b>', re.S)

def clean(s):
    s=re.sub(r'<br\s*/?>', '', s)
    s=html.unescape(s)
    return s.strip()

def clean_suffix(s):
    """Suffix keeps its LEADING whitespace: the template appends it straight after
    </a>, so ' /GB' and ', foo' are different renderings and both occur in the source."""
    s=re.sub(r'<br\s*/?>', '', s)
    s=html.unescape(s)
    return s.rstrip()

cats=[]; cur=None; anomalies=[]
for lineno, line in enumerate(text.split('\n'), 1):
    raw=line.rstrip('\r')
    if not raw.strip():
        continue
    m=BOLD.search(raw)
    if m:
        heading=clean(m.group('h'))   # verbatim: trailing colon is source content, not ours to tidy
        cur={'heading':heading,'source_line':lineno,'entries':[]}
        cats.append(cur); continue
    lm=list(LINK.finditer(raw))
    if not lm:
        anomalies.append({'line':lineno,'reason':'no <link> on a non-heading line','text':raw})
        continue
    if cur is None:
        # An element can carry its heading in tt_content.header rather than an inline <b>
        # (uid 1400 does). Use it rather than reporting every line as an orphan.
        if FALLBACK_HEADING is None:
            anomalies.append({'line':lineno,'reason':'entry before any heading','text':raw}); continue
        cur={'heading':FALLBACK_HEADING,'source_line':lineno,'entries':[]}; cats.append(cur)
    m0=lm[0]
    params=m0.group('params').strip()
    href=params.split()[0] if params.split() else ''
    # Consecutive <link> tags sharing one href are the RTE having split a single link
    # mid-word ("Paka the U" + "ncredible", "Hervé" + " Thiot"). Rejoin them, or the
    # anchor text is silently truncated. Anything left over is a genuine second link.
    same=[x for x in lm if (x.group('params').split() or [''])[0]==href]
    rest=[x for x in lm if x not in same]
    if rest:
        anomalies.append({'line':lineno,'reason':f'{len(rest)} additional link(s) with a different href','text':raw})
    name=clean(''.join(x.group('anchor') for x in same))  # concat raw, clean once: inner spacing survives
    prefix=clean(raw[:m0.start()])
    suffix=clean_suffix(raw[lm[-1].end():])
    cur['entries'].append({
        'source_line':lineno,
        'prefix':prefix,
        'name':name,
        'url':href,                       # byte-identical to source
        'suffix':suffix,
        'link_params':params,
        'anchor_count':len(same),
        'extra_links':[{'url':x.group('params').split()[0],'name':clean(x.group('anchor'))}
                       for x in rest],
    })

data={'source':f'tt_content uid {UID} (pid 974)','categories':cats,'anomalies':anomalies}
json.dump(data,open(OUTFILE,'w'),indent=2,ensure_ascii=False)
n=sum(len(c['entries']) for c in cats)
print(f"categories: {len(cats)}   entries: {n}   anomalies: {len(anomalies)}")
for c in cats: print(f"  {len(c['entries']):>3}  {c['heading']}")
if anomalies:
    print("\nANOMALIES:")
    for a in anomalies: print(f"  line {a['line']}: {a['reason']}\n    {a['text'][:150]}")
