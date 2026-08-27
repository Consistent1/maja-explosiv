#!/usr/bin/env python3
"""Stage 5 C - contact + datenschutz. Legal text is transcribed VERBATIM, never edited
(plan §8). <b> becomes a Markdown heading only where it is the whole line -- the German
privacy policy uses 31 of them as section headings.
"""
import html, json, os, re
OUT=os.path.join(os.path.dirname(__file__),'..','legal')
RAW=f'{OUT}/raw/db'

def blocks(uid, bold_is_heading=True):
    t=open(f'{RAW}/tt_content-{uid}.bodytext.html',encoding='utf-8').read()
    # strip <br> INSIDE anchor text first, or the link label breaks across paragraphs
    def _link(m):
        href, label = m.group(1), re.sub(r'<br\s*/?>', ' ', m.group(2))
        label = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', label))).strip()
        return f'[{label}]({href})'
    t=re.sub(r'<link\s+([^ >]+)[^>]*>(.*?)</link>', _link, t, flags=re.S)
    t=re.sub(r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>', _link, t, flags=re.S)
    t=re.sub(r'<br\s*/?>', '\n', t)
    out=[]
    for line in t.split('\n'):
        m=re.fullmatch(r'\s*<(b|strong)>(.*?)</\1>\s*', line, re.S)
        if m:
            txt=html.unescape(re.sub('<[^>]+>','',m.group(2))).strip()
            # A bold line is a SECTION HEADING only where the page uses it that way.
            # The privacy policy does (31 of them). On the contact page the same markup is
            # emphasis -- "Maja Thommen" and the email address are not section headings, and
            # rendering them as <h2> misrepresents the page.
            out.append(('h' if bold_is_heading else 'b', txt))
        else:
            s=html.unescape(re.sub('<[^>]+>','',line)).strip()
            if s: out.append(('p', s))
    return out

def md(bs):
    L=[]
    for kind,txt in bs:
        L.append(f"## {txt}" if kind=='h' else (f"**{txt}**" if kind=='b' else txt))
        L.append('')
    return '\n'.join(L).strip()+'\n'

def y(s): return '"'+s.replace('\\','\\\\').replace('"','\\"')+'"'

PAGES=[
  dict(out='contact.md', title='Contact', layout='contact.njk', permalink='/contact/',
       # 1450 -- the "Webdesign and Realisation" credit for Werner Trunk -- is NOT
       # migrated to the site (owner, 2026-08-27). It is documented in full in SOURCE.md
       # and its raw bytes are kept in raw/db/tt_content-1450.bodytext.html.
       page=973, live='info/contact', uids=[1311], bold_is_heading=False,
       excluded_uids=[1450]),
  dict(out='datenschutz.md', title='Datenschutz', layout='page.njk', permalink='/datenschutz/',
       page=1065, live='info/datenschutz', uids=[1620,1619], bold_is_heading=True),
]
for p in PAGES:
    bs=[]
    for u in p['uids']: bs += blocks(u, p.get('bold_is_heading', True))
    L=['---', f'title: {y(p["title"])}', f'layout: {y(p["layout"])}',
       f'permalink: {y(p["permalink"])}',
       f'source_page: "{p["page"]}"', f'source_path: {y(p["live"])}',
       f'source_uids: {y(",".join(map(str,p["uids"])))}',
       'source_note: "Legal/contact text, transcribed verbatim. Not edited."',
       *( [f'source_excluded_uids: {y(",".join(map(str,p["excluded_uids"])))}',
           'source_excluded_note: "tt_content 1450, the Webdesign/Werner Trunk Impressum credit, '
           'is on the old site but deliberately not carried over. Full text in '
           'migrated-content/legal/SOURCE.md."'] if p.get('excluded_uids') else [] ),
       '---','', md(bs)]
    open(f'{OUT}/converted/{p["out"]}','w').write('\n'.join(L))
    heads=sum(1 for k,_ in bs if k=='h'); bolds=sum(1 for k,_ in bs if k=='b')
    paras=sum(1 for k,_ in bs if k=='p')
    print(f"  {p['out']:<18} {heads:>3} headings  {bolds:>3} bold  {paras:>4} paragraphs")
