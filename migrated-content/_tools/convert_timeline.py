#!/usr/bin/env python3
"""Stage 3 C - timeline. normalized/timeline.json -> src/pages/about/timeline.md

Rendered by the design: `year` (37px column -- year only, per Figma), `title`, `description`.
Everything else the source carried is emitted alongside as metadata so the presentation can
be re-derived without returning to the database (owner, 2026-08-27).
"""
import html, json, os, re, sys
OUT=os.path.join(os.path.dirname(__file__),'..','timeline')
d=json.load(open(f'{OUT}/normalized/timeline.json'))

def text(x):
    """RTE bodytext -> plain text. <br> becomes a space; nothing else is altered."""
    x=re.sub(r'<br\s*/?>',' ',x or '')
    return re.sub(r'[ \t\r\n]+',' ',html.unescape(re.sub('<[^>]+>','',x))).strip()

YEAR=re.compile(r'(\d{4})')
def year_of(e):
    """The 37px column fits a year, so labels are reduced to one -- with ONE exception.

    "since YYYY:" renders as "Since YYYY" (owner, 2026-08-27). Reducing it to a bare year
    is actively misleading: entries sort by timestamp, and `since 2020:` carries a 2022
    timestamp, so it would show "2020" sitting between 2023 and 2022 and read as a sorting
    fault. "Since 2020" explains its own position. It does not fit the 37px column and will
    wrap -- accepted, and flagged for Maja.

    Everything else takes the FIRST 4-digit year ("05- 2024:" -> 2024, "1997-2001:" -> 1997);
    source_date_label keeps the original verbatim either way."""
    lab=(e['date_label'] or '').strip()
    m=YEAR.search(lab)
    if re.match(r'(?i)^since\b', lab) and m:
        return f"Since {m.group(1)}"
    if m: return m.group(1)
    return (e['datetime_iso'] or '')[:4]

def y(s): return '"'+str(s).replace('\\','\\\\').replace('"','\\"')+'"'

L=['---','title: "Timeline"','layout: "about-page.njk"','permalink: "/about/timeline/"',
   'timelineSections:']
n=0; odd=[]
for s in d['sections']:
    L.append(f'  - heading: {y(s["heading"])}')
    L.append(f'    source_plugin_uid: {y(s["plugin_uid"])}')
    L.append(f'    source_categories: {y(",".join(map(str,s["categories"])))}')
    L.append('    entries:')
    for e in s['entries']:
        yr=year_of(e); body=text(e['bodytext']); ti=e['title']
        L.append(f'      - year: {y(yr)}')
        L.append(f'        title: {y(ti)}')
        L.append(f'        description: {y(body)}')
        # --- preserved source metadata (not rendered) ---
        L.append(f'        source_uid: {y(e["source_uid"])}')
        L.append(f'        source_date_label: {y(e["date_label"])}')
        L.append(f'        source_datetime: {y(e["datetime_iso"] or "")}')
        L.append(f'        source_categories: {y(",".join(map(str,e["categories"])))}')
        L.append(f'        source_category_names: {y(", ".join(e["category_names"]))}')
        L.append(f'        source_bodytext_html: {y(e["bodytext"])}')
        if e['date_label'] and not re.fullmatch(r'\d{4}:?', e['date_label'].strip()) and not yr.startswith('Since'):
            odd.append((e['source_uid'], e['date_label'], yr))
        n+=1
L += ['---','']
open(f'{OUT}/converted/timeline.md','w').write('\n'.join(L))
print(f"entries: {n}   sections: {len(d['sections'])}")
print(f"labels reduced to a bare year for display: {len(odd)}  (originals kept in source_date_label)")
for u,lab,yr in odd[:6]: print(f"    uid {u}: {lab!r} -> year {yr}")
