#!/usr/bin/env python3
"""Stage 0 - source census, from the database only. No live-site access.
Text fields travel base64 so tabs/newlines in content cannot corrupt the TSV transport."""
import base64, json, subprocess, sys, os, collections

DB = os.path.join(os.path.dirname(__file__), 'db.sh')
OUT = os.path.join(os.path.dirname(__file__), '..', '_census')

def q(sql):
    r = subprocess.run([DB, '-N', '-B', '-e', sql], capture_output=True)
    if r.returncode != 0:
        sys.exit(f"QUERY FAILED\n{sql}\n{r.stderr.decode()}")
    rows = []
    for line in r.stdout.decode('utf-8', 'strict').split('\n'):
        if line != '':
            rows.append(line.split('\t'))
    return rows

def b64(v):
    return '' if v in ('', 'NULL') else base64.b64decode(v).decode('utf-8')

def tsv(v):
    """Escape TSV-hostile characters. Census artefacts must stay parseable without
    silently altering the value -- real newlines/tabs occur in TYPO3 page titles."""
    return (v.replace('\\', '\\\\').replace('\t', '\\t')
             .replace('\r', '\\r').replace('\n', '\\n'))

# ---------- 1. page tree ----------
pages = q("""SELECT uid, pid, REPLACE(TO_BASE64(title),'\n',''), doktype, deleted, hidden, sorting,
                    shortcut, REPLACE(TO_BASE64(url),'\n',''), urltype
             FROM pages ORDER BY uid;""")
P = {}
for uid, pid, title, doktype, deleted, hidden, sorting, shortcut, url, urltype in pages:
    P[int(uid)] = dict(uid=int(uid), pid=int(pid), title=b64(title), doktype=int(doktype),
                       deleted=int(deleted), hidden=int(hidden), sorting=int(sorting),
                       shortcut=int(shortcut), url=b64(url), urltype=int(urltype),
                       children=[])
for p in P.values():
    if p['pid'] in P:
        P[p['pid']]['children'].append(p['uid'])

active = {u: p for u, p in P.items() if not p['deleted'] and not p['hidden']}
deleted = {u: p for u, p in P.items() if p['deleted']}
hidden  = {u: p for u, p in P.items() if p['hidden'] and not p['deleted']}

# ---------- 2. url -> uid ----------
paths = q("""SELECT page_id, REPLACE(TO_BASE64(pagepath),'\n',''), language_id, expire
             FROM tx_realurl_pathcache ORDER BY page_id, expire;""")
url_to_uid = collections.defaultdict(list)
for page_id, pagepath, lang, expire in paths:
    url_to_uid[b64(pagepath)].append((int(page_id), int(expire)))

# ---------- 3. content inventory ----------
content = q("""SELECT pid, uid, CType, deleted, hidden, LENGTH(bodytext), REPLACE(TO_BASE64(header),'\n','')
               FROM tt_content ORDER BY pid, sorting;""")
by_page = collections.defaultdict(list)
for pid, uid, ctype, dele, hid, blen, header in content:
    by_page[int(pid)].append(dict(uid=int(uid), CType=ctype, deleted=int(dele),
                                  hidden=int(hid), bodylen=(0 if blen in ('NULL','') else int(blen)), header=b64(header)))

# ---------- 4. other content-bearing tables ----------
others = {}
for tbl, pidcol in (('tt_news','pid'), ('tt_address','pid'),
                    ('tx_cal_event','pid'), ('tx_veguestbook_entries','pid')):
    rows = q(f"SELECT {pidcol}, COUNT(*) FROM {tbl} GROUP BY {pidcol};")
    others[tbl] = {int(a): int(b) for a, b in rows}

# ---------- 5. image census ----------
dam = q("""SELECT uid, REPLACE(TO_BASE64(file_path),'\n',''), REPLACE(TO_BASE64(file_name),'\n',''), deleted, file_size
           FROM tx_dam ORDER BY uid;""")

os.makedirs(OUT, exist_ok=True)
json.dump({'pages': {str(k): v for k, v in P.items()}}, 
          open(f'{OUT}/page-tree.json','w'), indent=1, ensure_ascii=False)

with open(f'{OUT}/url-to-uid.tsv','w') as f:
    f.write("pagepath\tpage_id\texpire\n")
    for path, entries in sorted(url_to_uid.items()):
        for pid_, exp in entries:
            f.write(f"{tsv(path)}\t{pid_}\t{exp}\n")

with open(f'{OUT}/content-inventory.tsv','w') as f:
    f.write("uid\ttitle\tdoktype\tstate\tcontent_rows\tlive_rows\tctypes\tother\n")
    for u, p in sorted(P.items()):
        rows = by_page.get(u, [])
        live = [r for r in rows if not r['deleted'] and not r['hidden']]
        oth = ';'.join(f"{t}={d[u]}" for t, d in others.items() if u in d)
        state = 'deleted' if p['deleted'] else ('hidden' if p['hidden'] else 'active')
        ctypes = ','.join(sorted({r['CType'] for r in live})) or '-'
        f.write(f"{u}\t{tsv(p['title'])}\t{p['doktype']}\t{state}\t{len(rows)}\t{len(live)}\t{ctypes}\t{oth}\n")

nocontent = [(u, p) for u, p in sorted(active.items())
             if not [r for r in by_page.get(u, []) if not r['deleted'] and not r['hidden']]
             and u not in others['tt_news'] and p['doktype'] == 1]
with open(f'{OUT}/pages-without-content.tsv','w') as f:
    f.write("uid\ttitle\tdoktype\tshortcut\n")
    for u, p in nocontent:
        f.write(f"{u}\t{tsv(p['title'])}\t{p['doktype']}\t{p['shortcut']}\n")

with open(f'{OUT}/image-census-db.tsv','w') as f:
    f.write("uid\tfile_path\tfile_name\tdeleted\tfile_size\n")
    for uid, fp, fn, dele, size in dam:
        f.write(f"{uid}\t{tsv(b64(fp))}\t{tsv(b64(fn))}\t{dele}\t{size}\n")

print(f"pages           : {len(P)} total | {len(active)} active | {len(hidden)} hidden | {len(deleted)} deleted")
print(f"realurl paths   : {len(paths)} rows -> {len(url_to_uid)} distinct paths")
print(f"tt_content      : {len(content)} rows | {sum(1 for c in content if c[3]=='0' and c[4]=='0')} live")
print(f"other tables    : " + ', '.join(f"{t}={sum(d.values())}" for t,d in others.items()))
print(f"tx_dam          : {len(dam)} rows | {sum(1 for d in dam if d[3]=='0')} not deleted")
print(f"active doktype=1 pages with NO live content: {len(nocontent)}")
