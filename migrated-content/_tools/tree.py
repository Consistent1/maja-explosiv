#!/usr/bin/env python3
import json, sys, os
d = os.path.join(os.path.dirname(__file__),'..','_census')
P = {int(k):v for k,v in json.load(open(f'{d}/page-tree.json'))['pages'].items()}
paths = {}
for line in open(f'{d}/url-to-uid.tsv'):
    if line.startswith('pagepath'): continue
    pp, pid, exp = line.rstrip('\n').split('\t')
    pid=int(pid)
    # keep the non-expiring (expire=0) path as canonical
    if int(exp)==0 or pid not in paths: paths.setdefault(pid, pp)
    if int(exp)==0: paths[pid]=pp
inv={}
for line in open(f'{d}/content-inventory.tsv'):
    if line.startswith('uid'): continue
    f=line.rstrip('\n').split('\t'); inv[int(f[0])]=f
def walk(uid, depth=0):
    p=P[uid]
    if p['deleted']: return
    row=inv.get(uid)
    live=row[5] if row else '0'
    mark='' if not p['hidden'] else ' [hidden]'
    sc=f" ->{p['shortcut']}" if p['shortcut'] else ''
    url=paths.get(uid,'')
    print(f"{'  '*depth}{p['title'][:38]:<40} uid={uid:<5} live={live:<3}{sc}{mark}  {url}")
    for c in sorted(p['children'], key=lambda u:(P[u]['sorting'],u)):
        walk(c, depth+1)
roots=[u for u,p in P.items() if p['pid']==0 and not p['deleted']]
for r in sorted(roots): walk(r)
