#!/usr/bin/env python3
"""Stage 0 - coverage map. Source side only; joins to the live census when it exists."""
import json, os, collections
d = os.path.join(os.path.dirname(__file__),'..','_census')
P = {int(k):v for k,v in json.load(open(f'{d}/page-tree.json'))['pages'].items()}
paths={}
for line in open(f'{d}/url-to-uid.tsv'):
    if line.startswith('pagepath'): continue
    pp,pid,exp=line.rstrip('\n').split('\t'); pid=int(pid)
    if int(exp)==0 or pid not in paths: paths[pid]=pp
inv={}
for line in open(f'{d}/content-inventory.tsv'):
    if line.startswith('uid'): continue
    f=line.rstrip('\n').split('\t'); inv[int(f[0])]=f

MAJA_ROOT = 860
# category container uid -> (content_type, stage)
CAT = {872:('project/performance',9), 873:('project/event-organisation',8),
       874:('project/murals',6), 875:('project/paper-work',7),
       877:('project/sculptural-work',11), 878:('project/collaborations',10)}
PAGE = {974:('links',1), 981:('press',2), 1016:('timeline',3), 865:('bio',4),
        973:('contact',5), 1065:('datenschutz',5), 809:('impressum',5)}

def ancestors(u):
    out=[]
    while u in P and P[u]['pid'] in P:
        u=P[u]['pid']; out.append(u)
    return out

def classify(u):
    if u in PAGE: return PAGE[u]
    for a in [u]+ancestors(u):
        if a in CAT:
            return CAT[a] if a!=u else (CAT[a][0]+' (container)', CAT[a][1])
    return ('structural', 0)

rows=[]
def walk(u):
    p=P[u]
    if p['deleted']: return
    ct, stage = classify(u)
    r=inv.get(u)
    rows.append(dict(uid=u, title=p['title'], path=paths.get(u,''),
                     state='hidden' if p['hidden'] else 'active',
                     live=int(r[5]) if r else 0, shortcut=p['shortcut'],
                     ctype=ct, stage=stage))
    for c in sorted(p['children'], key=lambda x:(P[x]['sorting'],x)): walk(c)
walk(MAJA_ROOT)

def esc(v): return str(v).replace('\t','\\t').replace('\n','\\n').replace('\r','\\r')
with open(f'{d}/coverage-map.tsv','w') as f:
    f.write("uid\tstate\tlive_content_rows\tcontent_type\tstage\tpagepath\ttitle\tshortcut\n")
    for r in sorted(rows, key=lambda r:(r['stage'], r['ctype'], r['uid'])):
        f.write(f"{r['uid']}\t{r['state']}\t{r['live']}\t{r['ctype']}\t{r['stage']}\t"
                f"{esc(r['path'])}\t{esc(r['title'])}\t{r['shortcut']}\n")

# out-of-scope roots
oos=[u for u,p in P.items() if p['pid']==0 and not p['deleted'] and u!=MAJA_ROOT]
with open(f'{d}/out-of-scope-roots.tsv','w') as f:
    f.write("uid\ttitle\tdescendants_active\tnote\n")
    for u in sorted(oos):
        n=0
        stack=[u]
        while stack:
            x=stack.pop()
            if P[x]['deleted']: continue
            n+=1; stack.extend(P[x]['children'])
        f.write(f"{u}\t{esc(P[u]['title'])}\t{n}\tnot part of maja-explosiv.com\n")

by=collections.Counter((r['ctype'],r['stage']) for r in rows if r['state']=='active')
print(f"maja subtree (uid {MAJA_ROOT}): {len(rows)} pages, "
      f"{sum(1 for r in rows if r['state']=='active')} active, "
      f"{sum(1 for r in rows if r['state']=='hidden')} hidden\n")
print(f"{'content_type':38} {'stage':>5} {'pages':>6}")
for (ct,st),n in sorted(by.items(), key=lambda x:(x[0][1],x[0][0])):
    print(f"{ct:38} {st:>5} {n:>6}")
print("\nOut-of-scope roots:")
for line in open(f'{d}/out-of-scope-roots.tsv').readlines()[1:]:
    print("  "+line.rstrip())
