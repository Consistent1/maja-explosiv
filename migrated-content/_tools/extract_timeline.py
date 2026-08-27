#!/usr/bin/env python3
"""Stage 3 E+N - timeline. Source: tt_news records on page 864, rendered by two
`list_type=9` (tt_news) plugins on pages.uid 1016.

EVERY field of every record is preserved in normalized/timeline.json. The site
renders only year + title + description; the rest is kept so the presentation can
be re-derived later without going back to the database (owner, 2026-08-27).
"""
import base64, json, os, subprocess, sys, collections, datetime

DB=os.path.join(os.path.dirname(__file__),'db.sh')
OUT=os.path.join(os.path.dirname(__file__),'..','timeline')
STORAGE=864
SECTIONS=[('A partial chronology of expierience:', [17,20,21,22,23,24,25,39], 1198),
          ('Schooling:',                            [26],                      1406)]

def q(sql):
    r=subprocess.run([DB,'-N','-B','-e',sql],capture_output=True)
    if r.returncode: sys.exit("QUERY FAILED\n"+sql+"\n"+r.stderr.decode())
    return [l.split('\t') for l in r.stdout.decode('utf-8').split('\n') if l!='']
def b(v): return '' if v in ('','NULL') else base64.b64decode(v).decode('utf-8')

cols=[c[0] for c in q("""SELECT COLUMN_NAME FROM information_schema.columns
      WHERE table_schema='usr_p51487_2' AND table_name='tt_news' ORDER BY ORDINAL_POSITION;""")]
sel=', '.join(f"REPLACE(TO_BASE64(`{c}`),'\\n','')" for c in cols)
rows=q(f"SELECT {sel} FROM tt_news WHERE pid={STORAGE} AND deleted=0 AND hidden=0;")
recs={}
for r in rows:
    d={}
    for c,v in zip(cols,r):
        if v in ('','NULL'): d[c]='' if v=='' else None; continue
        raw=base64.b64decode(v)
        try: d[c]=raw.decode('utf-8')
        except UnicodeDecodeError: d[c]={'_binary_base64':base64.b64encode(raw).decode(),'_bytes':len(raw)}
    recs[int(d['uid'])]=d

cats=collections.defaultdict(list)
for ul,uf in q("SELECT uid_local, uid_foreign FROM tt_news_cat_mm;"):
    cats[int(ul)].append(int(uf))
catnames={int(u):b(t) for u,t in q("SELECT uid, REPLACE(TO_BASE64(title),'\\n','') FROM tt_news_cat;")}

def iso(ts):
    try: return datetime.datetime.utcfromtimestamp(int(ts)).isoformat()+'Z'
    except Exception: return None

sections=[]; used=set()
for heading, catsel, cuid in SECTIONS:
    ents=[]
    for uid,d in recs.items():
        if not (set(cats.get(uid,[])) & set(catsel)): continue
        used.add(uid)
        ents.append(dict(
            source_uid=uid, source_table='tt_news', source_page=STORAGE,
            source_plugin_uid=cuid,
            datetime_unix=int(d.get('datetime') or 0), datetime_iso=iso(d.get('datetime') or 0),
            date_label=(d.get('short') or '').strip(),      # verbatim, e.g. "05- 2024:"
            title=(d.get('title') or '').strip(),
            bodytext=d.get('bodytext') or '',
            categories=sorted(cats.get(uid,[])),
            category_names=[catnames.get(c,'') for c in sorted(cats.get(uid,[]))],
            all_fields={k:v for k,v in d.items() if v not in ('',None)},
        ))
    ents.sort(key=lambda e:-e['datetime_unix'])
    sections.append(dict(heading=heading, plugin_uid=cuid, categories=catsel, entries=ents))

excluded=[]
for uid,d in recs.items():
    if uid in used:
        continue
    excluded.append(dict(source_uid=uid, title=(d.get('title') or '').strip(),
        datetime_iso=iso(d.get('datetime') or 0), date_label=(d.get('short') or '').strip(),
        bodytext=d.get('bodytext') or '', categories=sorted(cats.get(uid,[])),
        category_names=[catnames.get(c,'') for c in sorted(cats.get(uid,[]))],
        reason='live record on page 864, but in no category either timeline plugin selects '
               '-- therefore not shown on the live site',
        all_fields={k:v for k,v in d.items() if v not in ('',None)}))
excluded.sort(key=lambda e:e['datetime_iso'] or '')

json.dump(dict(source=f'tt_news pid={STORAGE}, plugins 1198/1406 on pages.uid 1016',
               extracted_at=datetime.datetime.now().isoformat(timespec='seconds'),
               sections=sections, excluded=excluded),
          open(f'{OUT}/normalized/timeline.json','w'), indent=1, ensure_ascii=False)
json.dump(excluded, open(f'{OUT}/excluded/excluded-records.json','w'), indent=1, ensure_ascii=False)
print(f"live records on page {STORAGE}: {len(recs)}")
for s in sections: print(f"   {len(s['entries']):>3}  {s['heading']}")
print(f"   {len(excluded):>3}  EXCLUDED (no selected category)")
print(f"   total in sections: {sum(len(s['entries']) for s in sections)}")
