#!/usr/bin/env python3
"""Optimise the archive's live project images into the site's asset folders.

The archive (image-archive/) is READ-ONLY and is never modified. Output is
jpegtran -optimize -progressive -copy none: mathematically identical pixels,
smaller file, metadata stripped. Nothing is resized or re-encoded.

Category mapping per migration plan decision 13; anything undecided -> TBD/.
Live bucket only -- hidden and deleted images stay in their own stores.
"""
import base64, collections, hashlib, json, os, re, subprocess, sys, unicodedata

DB   = os.path.join(os.path.dirname(__file__), 'db.sh')
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
ARC  = os.path.join(ROOT, 'image-archive')
DEST = os.path.join(ROOT, 'src', 'assets', 'images', 'projects')

def q(sql):
    r = subprocess.run([DB,'-N','-B','-e',sql], capture_output=True)
    if r.returncode: sys.exit("QUERY FAILED\n"+sql+"\n"+r.stderr.decode())
    return [l.split('\t') for l in r.stdout.decode('utf-8').split('\n') if l]

def b(v): return '' if v in ('','NULL') else base64.b64decode(v).decode('utf-8')

# --- filename handling -------------------------------------------------------
# The live server stores umlauts in NFD (decomposed: u + combining diaeresis);
# TYPO3's database stores NFC (single codepoint). They look identical and compare
# unequal, so every path comparison must normalise to NFC first. Without this,
# recovered files look missing -- indistinguishable from actually being gone.
# See image-archive/RECOVERED-2026-08-27.md.
def nfc(s):
    return unicodedata.normalize('NFC', s or '')

# German transliteration, matching the convention the source filenames already use
# (KaetheKollwitz1_s.jpg, BernhardLuginbuehl_1_s.jpg). Without it "Kaethe" slugged
# to "k-the" -- the umlaut dropped rather than transliterated.
_TR = {'ä':'ae','ö':'oe','ü':'ue','ß':'ss','Ä':'Ae','Ö':'Oe','Ü':'Ue',
       'é':'e','è':'e','ê':'e','à':'a','á':'a','â':'a','ç':'c','ñ':'n'}

def _translit(s):
    # NFC FIRST: _TR maps composed characters (U+00E4). NFD input is 'a' + combining
    # diaeresis, which the map misses -- NFKD then drops the mark and 'Kaethe'
    # becomes 'kathe' instead of 'kaethe'.
    s = unicodedata.normalize('NFC', s or '')
    s = ''.join(_TR.get(c, c) for c in s)
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()

def slug(s,n=48):
    s=re.sub(r'[^a-zA-Z0-9]+','-',_translit((s or '').strip())).strip('-').lower()
    return s[:n] or 'untitled'

P={int(u):(int(p), b(t), int(d), int(h))
   for u,p,t,d,h in q("SELECT uid,pid,REPLACE(TO_BASE64(title),'\\n',''),deleted,hidden FROM pages;")}
def anc(u):
    o=[];seen=set()
    while u in P and u not in seen: seen.add(u);o.append(u);u=P[u][0]
    return o

# decision 13
SUB   = {1039:'sculptures', 1040:'installations'}          # sculptural-work sub-containers
DIRECT= {872:'performance', 874:'paintings', 875:'paintings',
         # collaborations -> sculptures (owner, 2026-08-27). By material these are metal
         # sculptures. Provisional: whether 'collaborations' should survive as a body of
         # work is still Maja's call (PLAN.md), and reversing this is a directory move.
         878:'sculptures'}
TBD   = {873:'TBD', 1049:'TBD'}                            # event-organisation, possibilities
SKIP  = {1041, 1042}                                       # recent-work: verified empty, not projects
CONTAINERS = set(SUB)|set(DIRECT)|set(TBD)|{877,867}

def category(pid):
    a=anc(pid)
    for x in a:
        if x in SUB:    return SUB[x]
        if x in DIRECT: return DIRECT[x]
        if x in TBD:    return 'TBD'
    return None

rows=q("""SELECT c.pid, d.uid, REPLACE(TO_BASE64(d.file_path),'\\n',''),
                 REPLACE(TO_BASE64(d.file_name),'\\n',''), d.sorting
          FROM tx_dam_mm_ref r
          JOIN tx_dam d ON d.uid=r.uid_local
          JOIN tt_content c ON c.uid=r.uid_foreign
          JOIN pages p ON p.uid=c.pid
          WHERE r.ident='rgsmoothgallery' AND d.deleted=0
            AND c.deleted=0 AND c.hidden=0 AND p.deleted=0 AND p.hidden=0
          ORDER BY c.pid, d.sorting, d.uid;""")

by_proj=collections.defaultdict(list); seen=set()
for pid,duid,fp,fn,sort in rows:
    pid=int(pid)
    if pid in SKIP or pid in CONTAINERS: continue
    cat=category(pid)
    if not cat: continue
    key=(pid,int(duid))
    if key in seen: continue
    seen.add(key)
    by_proj[(cat, slug(P[pid][1]), pid)].append((int(sort), int(duid), b(fp)+b(fn)))

# locate each source inside the archive by its original path
arc_index={}
for dp,_,fs in os.walk(ARC):
    for f in fs:
        arc_index.setdefault(nfc(f), []).append(os.path.join(dp,f))

DRY = '--write' not in sys.argv
manifest=[]; stats=collections.Counter()
for (cat, proj, pid), imgs in sorted(by_proj.items()):
    outdir=os.path.join(DEST, cat, proj)
    for n,(sort,duid,srcrel) in enumerate(sorted(imgs), 1):
        base=os.path.basename(srcrel)
        cands=[p for p in arc_index.get(nfc(base),[]) if '/live/' in p]
        if not cands: stats['source-not-in-archive']+=1; continue
        src=cands[0]
        ext=os.path.splitext(base)[1].lower()
        out=os.path.join(outdir, f"{proj}-{n:02d}{ext if ext!='.jpeg' else '.jpg'}")
        manifest.append(dict(category=cat, project=proj, page_uid=pid, dam_uid=duid,
                             seq=n, archive_source=os.path.relpath(src,ROOT),
                             original=srcrel, target=os.path.relpath(out,ROOT)))
        stats['planned']+=1
        if DRY: continue
        os.makedirs(outdir, exist_ok=True)
        if ext in ('.jpg','.jpeg'):
            r=subprocess.run(['jpegtran','-optimize','-progressive','-copy','none',src],
                             capture_output=True)
            if r.returncode==0 and r.stdout:
                open(out,'wb').write(r.stdout); stats['jpegtran']+=1
            else:
                open(out,'wb').write(open(src,'rb').read()); stats['copied-jpegtran-failed']+=1
        else:
            open(out,'wb').write(open(src,'rb').read()); stats['copied-non-jpeg']+=1

print(f"projects: {len(by_proj)}")
for cat,n in collections.Counter(c for c,_,_ in by_proj).most_common():
    imgs=sum(len(v) for k,v in by_proj.items() if k[0]==cat)
    print(f"   {cat:16} {n:>3} projects  {imgs:>4} images")
print(f"\nstats: {dict(stats)}")
if not DRY:
    json.dump(manifest, open(os.path.join(ROOT,'migrated-content','_census','site-images.json'),'w'), indent=1)
    print(f"manifest -> migrated-content/_census/site-images.json ({len(manifest)} rows)")
else:
    print("\nDRY RUN. Re-run with --write to produce files.")
