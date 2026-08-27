#!/usr/bin/env python3
"""Stages 6-11 V - compare converted output against the LIVE page.

Live is a verification source only (plan decision 1). Nothing here writes to src/.
Checks: heading text, description text, gallery image count, and per-image captions.
"""
import html, json, os, re, sys, unicodedata
OUT = os.path.join(os.path.dirname(__file__), '..', 'projects')

def txt(h):
    h = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S|re.I)
    h = re.sub(r'<br\s*/?>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()

def norm(s): return re.sub(r'\s+',' ',unicodedata.normalize('NFC', s or '')).strip()

def run(stage):
    d = json.load(open(f'{OUT}/normalized/stage{stage}.json'))
    LIVE = f'{OUT}/raw/live'
    rows, fails = [], 0
    for p in d['projects']:
        f = None
        for cand in (p['slug'], p['slug'].replace('-unterfuehrung','')):
            if os.path.exists(f'{LIVE}/{cand}.html'): f = f'{LIVE}/{cand}.html'; break
        if not f:
            rows.append((p['slug'],'NO LIVE CAPTURE','','','')); fails += 1; continue
        h = open(f, encoding='utf-8', errors='replace').read()
        live = txt(h)

        # heading: the live page prints "Title, Year" exactly as tt_content.header
        head_ok = norm(p['header']) in norm(live)
        # description: compare word-for-word, tags and wrapping removed
        body_ok = norm(txt(p['bodytext_html'])) in norm(live)
        # captions: each image description should appear in the page text
        caps = sum(1 for im in p['images'] if im['description'] and norm(im['description']) in norm(live))
        cap_total = sum(1 for im in p['images'] if im['description'])

        # ORDER. Presence is not order, and order failed silently once: ordering the
        # gallery by tx_dam.sorting instead of tx_dam_mm_ref.sorting_foreign produced the
        # right images with the right captions in the wrong sequence, and passed every
        # other check here. The old gallery emits one <div class="imageElement"> per image,
        # in display order, each carrying its DAM description -- compare the SEQUENCES.
        live_seq = [norm(m.group(1)) for m in re.finditer(
            r'<div class="imageElement">\s*<h3>.*?</h3>\s*<p>(.*?)</p>', h, re.S)]
        ours_seq = [norm(im['description']) for im in p['images']]
        # live captions append "| creator"; ours keep the fields apart
        live_cmp = [x.split('|')[0].strip() for x in live_seq]
        order_ok = len(live_cmp) == len(ours_seq) and live_cmp == ours_seq
        first_diff = next((i+1 for i,(a,b) in enumerate(zip(live_cmp, ours_seq)) if a != b), None)

        ok = head_ok and body_ok and caps == cap_total and order_ok
        if not ok: fails += 1
        rows.append((p['slug'],
                     'header OK' if head_ok else 'HEADER MISMATCH',
                     'body OK'   if body_ok else 'BODY MISMATCH',
                     f'captions {caps}/{cap_total}',
                     'order OK' if order_ok else
                     (f'ORDER DIFFERS at {first_diff}' if first_diff
                      else f'ORDER len {len(live_cmp)} vs {len(ours_seq)}')))
    w = max(len(r[0]) for r in rows)
    for r in rows: print(f"  {r[0]:<{w}}  {r[1]:<16} {r[2]:<14} {r[3]:<16} {r[4]}")
    print(f"\n  {len(rows)-fails}/{len(rows)} projects match live")
    return fails

if __name__ == '__main__':
    sys.exit(1 if run(int(sys.argv[1]) if len(sys.argv)>1 else 6) else 0)
