#!/usr/bin/env python3
"""Build image-archive/ : every file the old site referenced, in ORIGINAL form,
arranged by the old site's category/project.

Owner instruction 2026-08-26: an archive of all original content from the site,
unmodified, to hand to Maja and to use as the master for producing site images.
Includes files referenced by hidden and deleted content, bucketed separately,
mirroring the migrated-hidden-content / migrated-deleted-content convention.
"""
import base64, hashlib, json, os, re, shutil, subprocess, sys, collections, datetime

DB = os.path.join(os.path.dirname(__file__), 'db.sh')
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
BU = os.path.join(ROOT, 'old', 'TYPO3BU', '_')
OUT = os.path.join(ROOT, 'image-archive')

def q(sql):
    r = subprocess.run([DB, '-N', '-B', '-e', sql], capture_output=True)
    if r.returncode: sys.exit("QUERY FAILED\n" + sql + "\n" + r.stderr.decode())
    return [l.split('\t') for l in r.stdout.decode('utf-8').split('\n') if l != '']

def b64(v): return '' if v in ('', 'NULL') else base64.b64decode(v).decode('utf-8')
def slug(s, n=48):
    s = re.sub(r'[^a-zA-Z0-9]+', '-', (s or '').strip()).strip('-').lower()
    return s[:n] or 'untitled'

# ---- page tree, for category ancestry -------------------------------------
pages = {int(u): dict(pid=int(p), title=b64(t), deleted=int(d), hidden=int(h))
         for u, p, t, d, h in q("""SELECT uid,pid,REPLACE(TO_BASE64(title),'\\n',''),deleted,hidden
                                   FROM pages;""")}
OLD_CAT = {872:'performance', 873:'event-organisation', 874:'murals',
           875:'paper-work', 877:'sculptural-work', 878:'collaborations',
           # Not part of the old site's six categories, but they hold real projects:
           # 'Breath Under Water' (77 images), 'Alchemy Bar' (36), 'Sculptures' (32).
           # Found 2026-08-26 -- the stage table in the plan assumes the six are
           # exhaustive and they are not.
           867:'recent-work', 1049:'possibilities'}
# proposed six -> four, RECORDED ONLY. D5 is owner-reviewed and not yet settled.
PROPOSED = {'performance':'performance', 'event-organisation':'performance',
            'murals':'paintings', 'paper-work':'paintings',
            'sculptural-work':'sculptures-or-installations', 'collaborations':'UNMAPPED',
            'recent-work':'UNMAPPED', 'possibilities':'UNMAPPED'}
NAMED = {974:'links', 981:'press', 1016:'timeline', 865:'bio', 973:'contact',
         1065:'datenschutz', 809:'impressum'}

def ancestry(uid):
    out, seen = [], set()
    while uid in pages and uid not in seen:
        seen.add(uid); out.append(uid); uid = pages[uid]['pid']
    return out

def categorise(pid):
    if pid in NAMED: return 'about', NAMED[pid]
    for a in ancestry(pid):
        if a in OLD_CAT:
            return OLD_CAT[a], slug(pages[pid]['title'])
    root = ancestry(pid)[-1] if ancestry(pid) else pid
    if root != 860: return 'other-sites', slug(pages.get(root,{}).get('title','unknown'))
    return 'uncategorised', slug(pages.get(pid, {}).get('title', 'unknown'))

# ---- every image reference, from every path -------------------------------
refs = []   # (dam_uid, path, name, content_uid, pid, ident)
for uid_local, uid_foreign, ident, fp, fn in q("""
        SELECT r.uid_local, r.uid_foreign, r.ident,
               REPLACE(TO_BASE64(d.file_path),'\\n',''), REPLACE(TO_BASE64(d.file_name),'\\n','')
        FROM tx_dam_mm_ref r JOIN tx_dam d ON d.uid=r.uid_local
        WHERE r.tablenames='tt_content';"""):
    refs.append((int(uid_local), b64(fp), b64(fn), int(uid_foreign), None, ident))

# tt_content.image -> uploads/pics/
for cuid, imgs in q("""SELECT uid, REPLACE(TO_BASE64(image),'\\n','') FROM tt_content
                       WHERE image IS NOT NULL AND image<>'';"""):
    for nm in [x for x in b64(imgs).split(',') if x.strip()]:
        refs.append((None, 'uploads/pics/', nm.strip(), int(cuid), None, 'tt_content.image'))

content = {int(u): dict(pid=int(p), deleted=int(d), hidden=int(h))
           for u, p, d, h in q("SELECT uid,pid,deleted,hidden FROM tt_content;")}

def bucket(cuid):
    c = content.get(cuid)
    if not c: return 'orphaned'
    pg = pages.get(c['pid'], {})
    if c['deleted'] or pg.get('deleted'): return 'deleted'
    if c['hidden'] or pg.get('hidden'):   return 'hidden'
    return 'live'

rows, seen_targets = [], {}
stats = collections.Counter()
for dam, fp, fn, cuid, _, ident in refs:
    c = content.get(cuid)
    if not c: stats['ref-to-missing-content'] += 1; continue
    bk = bucket(cuid)
    cat, proj = categorise(c['pid'])
    src = os.path.join(BU, fp, fn)
    dest_dir = os.path.join(OUT, bk, cat, proj)
    target = os.path.join(dest_dir, fn)
    # collision inside one project folder -> disambiguate with the dam uid
    key = (bk, cat, proj, fn)
    if key in seen_targets and seen_targets[key] != (fp + fn):
        stem, ext = os.path.splitext(fn)
        target = os.path.join(dest_dir, f"{stem}__dam{dam}{ext}")
        stats['renamed-on-collision'] += 1
    seen_targets.setdefault(key, fp + fn)
    ok = os.path.exists(src)
    stats['missing-from-backup' if not ok else 'resolved'] += 1
    rows.append(dict(bucket=bk, category=cat, project=proj, dam_uid=dam, ident=ident,
                     content_uid=cuid, page_uid=c['pid'],
                     page_title=pages.get(c['pid'], {}).get('title', ''),
                     source=fp + fn, target=os.path.relpath(target, OUT),
                     exists=ok, src_abs=src, target_abs=target,
                     proposed_new_category=PROPOSED.get(cat, '')))
json.dump({'rows': rows, 'stats': dict(stats)},
          open('/tmp/claude-1000/-home-miichael-Code-maja-explosiv/86595204-792e-49ea-bced-c238f1b6976e/scratchpad/archive_plan.json', 'w'))
print(f"references found      : {len(refs)}")
for k, v in sorted(stats.items()): print(f"  {k:24} {v}")
print(f"\nby bucket : {dict(collections.Counter(r['bucket'] for r in rows))}")
print(f"by category:")
for c, n in collections.Counter(r['category'] for r in rows).most_common():
    print(f"   {c:22} {n}")

# ---------------------------------------------------------------- copy phase
if '--copy' in sys.argv:
    copied = failed = 0
    manifest = []
    for r in rows:
        if not r['exists']:
            manifest.append(r); failed += 1; continue
        os.makedirs(os.path.dirname(r['target_abs']), exist_ok=True)
        if not os.path.exists(r['target_abs']):
            shutil.copy2(r['src_abs'], r['target_abs'])   # copy2 keeps mtime
        h = hashlib.sha256(open(r['target_abs'], 'rb').read()).hexdigest()
        r['sha256'] = h
        r['bytes'] = os.path.getsize(r['target_abs'])
        manifest.append(r); copied += 1

    def esc(v): return str(v).replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
    cols = ['bucket','category','project','page_uid','page_title','content_uid','ident',
            'dam_uid','source','target','sha256','bytes','exists','proposed_new_category']
    with open(os.path.join(OUT, 'manifest.tsv'), 'w') as f:
        f.write('\t'.join(cols) + '\n')
        for r in manifest:
            f.write('\t'.join(esc(r.get(c, '')) for c in cols) + '\n')

    uniq = {r['sha256'] for r in manifest if r.get('sha256')}
    total = sum(os.path.getsize(os.path.join(dp, fn))
                for dp, _, fs in os.walk(OUT) for fn in fs)
    json.dump({'built_at': datetime.datetime.now().isoformat(timespec='seconds'),
               'references': len(refs), 'copied': copied,
               'missing_from_backup': failed,
               'distinct_files_by_sha256': len(uniq),
               'bytes': total,
               'source': 'old/TYPO3BU/_/ (filesystem backup, 2025-01-02)',
               'note': 'Files are byte-identical originals. Nothing resized or re-encoded.'},
              open(os.path.join(OUT, 'manifest.json'), 'w'), indent=2)
    print(f"\ncopied {copied} files ({total/1e6:.0f} MB), {len(uniq)} distinct by sha256")
    print(f"missing from backup: {failed}")
