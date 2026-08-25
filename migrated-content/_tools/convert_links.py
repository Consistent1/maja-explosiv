#!/usr/bin/env python3
"""Stage 1 C - convert. normalized/links.json -> the exact file the site consumes.
Front matter splits into MIGRATED CONTENT and TEMPLATE CONFIGURATION; the latter is
reported, never silently carried over from the file being replaced (plan §10)."""
import json, os, sys
OUT=os.path.join(os.path.dirname(__file__),'..','links')
ROOT=os.path.join(os.path.dirname(__file__),'..','..')
UID=sys.argv[1] if len(sys.argv)>1 else '1399'
HIDDEN = UID!='1399'
src=f'{OUT}/normalized/links-{UID}.json' if HIDDEN else f'{OUT}/normalized/links.json'
d=json.load(open(src))

# --- template configuration: from the layout's requirements, NOT migrated content ---
CONFIG={'title':'Links','layout':'about-page.njk','permalink':'/about/links/'}
# --- migrated content ---
LINKS_HEADING='FRIENDS AND RELATED ARTISTS:'   # tt_content.header of uid 1399
if HIDDEN:
    CONFIG={'title':'Links — hidden content','layout':'about-page.njk','permalink':'/about/links/'}
    LINKS_HEADING=d['categories'][0]['heading'] if d['categories'] else ''

def y(s):
    """YAML double-quoted scalar. Escapes only what YAML requires."""
    return '"' + s.replace('\\','\\\\').replace('"','\\"') + '"'

L=['---']
for k,v in CONFIG.items(): L.append(f'{k}: {y(v)}')
L.append(f'linksHeading: {y(LINKS_HEADING)}')
if HIDDEN:
    L.append(f'source_uid: "{UID}"')
    L.append('source_page: "974"')
    L.append('source_path: "info/links"')
    L.append('source_state: "hidden"   # TYPO3 tt_content.hidden = 1 -- unpublished')
L.append('linkCategories:')
n=0
for c in d['categories']:
    L.append(f'  - heading: {y(c["heading"])}')
    L.append('    entries:')
    for e in c['entries']:
        first=True
        def add(k,v):
            global first
            L.append(('      - ' if first else '        ')+f'{k}: {v}'); first=False
        if e['prefix']: add('text', y(e['prefix']))
        add('name', y(e['name']))
        add('url',  y(e['url']))
        if e['suffix']: add('suffix', y(e['suffix']))
        n+=1
L.append('---')
L.append('')
if HIDDEN:
    dest=os.path.join(ROOT,'migrated-hidden-content','pages','about','links.md')
else:
    dest=f'{OUT}/converted/links.md'
os.makedirs(os.path.dirname(dest),exist_ok=True)
open(dest,'w').write('\n'.join(L))
print(f"wrote {os.path.relpath(dest,ROOT)}  categories={len(d['categories'])} entries={n}")
print("template configuration (NOT migrated content):", CONFIG)
