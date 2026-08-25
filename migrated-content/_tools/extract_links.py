#!/usr/bin/env python3
"""Stage 1 E - extract. Database only, no live-site access."""
import base64, hashlib, json, os, subprocess, sys, datetime
DB=os.path.join(os.path.dirname(__file__),'db.sh')
OUT=os.path.join(os.path.dirname(__file__),'..','links')
PID=974
SQL=(f"SELECT uid, CType, deleted, hidden, sorting, "
     f"REPLACE(TO_BASE64(header),'\\n',''), REPLACE(TO_BASE64(bodytext),'\\n','') "
     f"FROM tt_content WHERE pid={PID} ORDER BY sorting;")
r=subprocess.run([DB,'-N','-B','-e',SQL],capture_output=True)
if r.returncode: sys.exit("QUERY FAILED\n"+r.stderr.decode())
rows=[l.split('\t') for l in r.stdout.decode().split('\n') if l]
man={'source':'database usr_p51487_2, tt_content','page_uid':PID,
     'query':SQL,'extracted_at':datetime.datetime.now().isoformat(timespec='seconds'),
     'connection_charset':'latin1 (see plan §2.3)','elements':[]}
os.makedirs(f'{OUT}/raw/db',exist_ok=True)
for uid,ct,dele,hid,sort,hdr,body in rows:
    h=base64.b64decode(hdr).decode('utf-8') if hdr not in ('','NULL') else ''
    b=base64.b64decode(body) if body not in ('','NULL') else b''
    fn=f'{OUT}/raw/db/tt_content-{uid}.bodytext.html'
    open(fn,'wb').write(b)
    man['elements'].append(dict(uid=int(uid),CType=ct,deleted=int(dele),hidden=int(hid),
        sorting=int(sort),header=h,bodytext_bytes=len(b),
        bodytext_sha256=hashlib.sha256(b).hexdigest(),
        raw_file=os.path.relpath(fn,OUT),
        published=(dele=='0' and hid=='0')))
json.dump(man,open(f'{OUT}/manifest.json','w'),indent=2,ensure_ascii=False)
for e in man['elements']:
    print(f"uid={e['uid']} published={e['published']} bytes={e['bodytext_bytes']:>6} "
          f"sha={e['bodytext_sha256'][:12]} header={e['header']!r}")
