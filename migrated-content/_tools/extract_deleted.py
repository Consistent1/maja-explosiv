#!/usr/bin/env python3
"""Migrate deleted content in full. Owner instruction 2026-08-25: preserve ALL information.

Every column of every deleted record is preserved, not just the renderable ones -- deleted
`image`, `menu` and `list` elements carry no bodytext at all, so a bodytext-only extraction
would silently save nothing for 39 of 103 elements.
"""
import base64, json, os, re, subprocess, sys, datetime, hashlib
DB=os.path.join(os.path.dirname(__file__),'db.sh')
ROOT=os.path.join(os.path.dirname(__file__),'..','..')
OUT=os.path.join(ROOT,'migrated-deleted-content')

def q(sql):
    r=subprocess.run([DB,'-N','-B','-e',sql],capture_output=True)
    if r.returncode: sys.exit("QUERY FAILED\n"+sql+"\n"+r.stderr.decode())
    return [l.split('\t') for l in r.stdout.decode('utf-8','surrogateescape').split('\n') if l!='']

def cols(table):
    return [c[0] for c in q(f"SELECT COLUMN_NAME FROM information_schema.columns "
                            f"WHERE table_schema='usr_p51487_2' AND table_name='{table}' "
                            f"ORDER BY ORDINAL_POSITION;")]

def fetch_all(table, where):
    """Every column, base64 on the wire so no value can corrupt the transport."""
    cs=cols(table)
    sel=', '.join(f"REPLACE(TO_BASE64(`{c}`),'\\n','')" for c in cs)
    rows=q(f"SELECT {sel} FROM `{table}` WHERE {where};")
    out=[]
    for r in rows:
        rec={}
        for c,v in zip(cs,r):
            if v in ('','NULL'):
                rec[c]=None if v=='NULL' else ''
                continue
            b=base64.b64decode(v)
            try:
                rec[c]=b.decode('utf-8')
            except UnicodeDecodeError:
                # binary column (l18n_diffsource): keep the bytes, flagged, never dropped
                rec[c]={'_binary_base64':base64.b64encode(b).decode('ascii'),
                        '_bytes':len(b), '_sha256':hashlib.sha256(b).hexdigest()}
        out.append(rec)
    return out

def slug(s, n=40):
    s=re.sub(r'[^a-zA-Z0-9]+','-', (s or '').strip()).strip('-').lower()
    return (s[:n] or 'untitled')

pages   = {int(p['uid']): p for p in fetch_all('pages','deleted=1')}
content = fetch_all('tt_content','deleted=1')
allpages= {int(p['uid']): p for p in fetch_all('pages','1=1')}

MAJA_ROOT=860
def root_of(uid):
    seen=set()
    while uid in allpages and int(allpages[uid].get('pid') or 0)!=0 and uid not in seen:
        seen.add(uid); uid=int(allpages[uid]['pid'])
    return uid
def bucket(pid):
    r=root_of(pid)
    if r==MAJA_ROOT: return 'maja', r
    t=(allpages.get(r) or {}).get('title') or f'root-{r}'
    return os.path.join('other-sites', slug(t)), r

os.makedirs(f'{OUT}/_records', exist_ok=True)
index=[]

def rte_to_text(bt):
    if not bt or isinstance(bt,dict): return ''
    t=re.sub(r'<link\s+([^ >]+)[^>]*>(.*?)</link>', r'[\2](\1)', bt, flags=re.S)
    t=re.sub(r'<b>(.*?)</b>', r'**\1**', t, flags=re.S)
    t=re.sub(r'<br\s*/?>', '\n', t)
    t=re.sub(r'<[^>]+>', '', t)
    return t.strip()

for c in content:
    uid=int(c['uid']); pid=int(c['pid'])
    page=allpages.get(pid)
    ptitle=(page or {}).get('title') or f'page-{pid}'
    on_deleted_page = pid in pages
    bk, rootuid = bucket(pid)
    sub = 'deleted-pages' if on_deleted_page else 'on-surviving-pages'
    d = f"{OUT}/{bk}/{sub}/{pid}-{slug(ptitle)}"
    os.makedirs(d, exist_ok=True)
    json.dump(c, open(f'{d}/content-{uid}.json','w'), indent=1, ensure_ascii=False)
    body=rte_to_text(c.get('bodytext'))
    hdr=c.get('header') or ''
    fields=[k for k,v in c.items() if v not in (None,'','0') and not isinstance(v,dict)]
    with open(f'{d}/content-{uid}.md','w') as f:
        f.write(f"---\nsource_table: tt_content\nsource_uid: \"{uid}\"\n"
                f"source_page: \"{pid}\"\nsource_page_title: {json.dumps(ptitle)}\n"
                f"source_state: \"deleted\"\nCType: \"{c.get('CType','')}\"\n"
                f"source_page_deleted: {str(on_deleted_page).lower()}\n"
                f"non_empty_columns: {len(fields)}\n---\n\n")
        if hdr: f.write(f"# {hdr}\n\n")
        f.write(body+"\n" if body else
                "_No bodytext. This element's content lives in other columns "
                f"(CType `{c.get('CType','')}`); see `content-{uid}.json` for the complete record._\n")
    index.append((str(uid), 'tt_content', str(pid), ptitle, c.get('CType',''),
                  'maja' if bk=='maja' else 'other-site',
                  str(len(body)), os.path.relpath(f'{d}/content-{uid}.md', OUT)))

for uid,p in sorted(pages.items()):
    bk,_=bucket(uid)
    d=f"{OUT}/{bk}/deleted-pages/{uid}-{slug(p.get('title'))}"
    os.makedirs(d, exist_ok=True)
    json.dump(p, open(f'{d}/page.json','w'), indent=1, ensure_ascii=False)
    index.append((str(uid),'pages',str(p.get('pid','')), p.get('title') or '', 'page',
                  'maja' if bk=='maja' else 'other-site','0',
                  os.path.relpath(f'{d}/page.json', OUT)))

with open(f'{OUT}/index.tsv','w') as f:
    f.write("uid\ttable\tparent_pid\ttitle\tctype\tlocation\tbody_chars\tfile\n")
    for r in sorted(index, key=lambda x:(x[1], int(x[0]))):
        f.write('\t'.join(x.replace('\t',' ').replace('\n',' ') for x in r)+'\n')

json.dump({'extracted_at':datetime.datetime.now().isoformat(timespec='seconds'),
           'deleted_pages':len(pages),'deleted_content_elements':len(content),
           'connection_charset':'latin1 (plan §2.3)',
           'note':'every column of every deleted record preserved; binary columns kept base64'},
          open(f'{OUT}/manifest.json','w'), indent=2)
print(f"deleted pages          : {len(pages)}")
print(f"deleted content elems  : {len(content)}")
print(f"  on deleted pages     : {sum(1 for c in content if int(c['pid']) in pages)}")
print(f"  on surviving pages   : {sum(1 for c in content if int(c['pid']) not in pages)}")
maja_rows=[r for r in index if r[5]=='maja']
print(f"index rows             : {len(index)}")
print(f"  belonging to MAJA    : {len(maja_rows)}")
print(f"  belonging to other sites in the same database: {len(index)-len(maja_rows)}")
