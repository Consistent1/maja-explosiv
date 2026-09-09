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
        if p.get('skip_reason'):
            rows.append((p['slug'], 'SKIPPED BY DESIGN', '', '', p['skip_reason'][:44]))
            continue
        f = None
        for cand in (p['slug'], p['slug'].replace('-unterfuehrung','')):
            if os.path.exists(f'{LIVE}/{cand}.html'): f = f'{LIVE}/{cand}.html'; break
        if not f:
            rows.append((p['slug'],'NO LIVE CAPTURE','','','')); fails += 1; continue
        h = open(f, encoding='utf-8', errors='replace').read()
        live = txt(h)

        # heading: the live page prints "Title, Year" exactly as tt_content.header
        head_ok = norm(p['header']) in norm(live)
        # description: compare word-for-word, tags and wrapping removed.
        # EVERY text block, not just the first -- a project can carry more than one live
        # text element and the extras are real content (Eurokot's 26 invited artists,
        # Eurokon's East/West lists). Checking only block 0 would pass while the rest were
        # silently dropped, which is exactly the failure this stage was at risk of.
        text_blocks = p.get('text_blocks') or ([{'bodytext_html': p['bodytext_html']}]
                                               if p.get('bodytext_html') else [])
        # One tolerated difference: where a link's label is the bare URL, the database
        # stores it with the scheme and the old site displays it without. Strip schemes
        # from BOTH sides before comparing. This removes only "https://"-style prefixes,
        # so it cannot hide a difference in wording. See convert_projects.py.
        def cmpable(x): return re.sub(r'\b[a-z][a-z0-9+.-]*://', '', norm(x))
        live_cmp_text = cmpable(live)
        # `and cmpable(...)` skips a block that strips to nothing -- which is precisely how
        # page 1078 passed. Its second block is a TABLE OF 12 THUMBNAIL LINKS: no text at
        # all, so it was skipped here, while body_md had already turned it into the run-on
        # uid string "107710731063...". An empty needle is trivially a substring, so the
        # check reported `body OK (2 blk)` over content that was entirely gone.
        # A block with no text is now a FAILURE, not a pass: it means the block's content
        # is carried by markup this comparison cannot see.
        empty_blocks = [b for b in text_blocks if not cmpable(txt(b['bodytext_html']))]
        missing_blocks = [b for b in text_blocks if cmpable(txt(b['bodytext_html']))
                          and cmpable(txt(b['bodytext_html'])) not in live_cmp_text]
        body_ok = not missing_blocks and not empty_blocks

        # EMBEDDED IMAGES. The gallery checks below read <div class="imageElement"> only --
        # the DAM smoothgallery -- so an image placed straight into a text element's RTE
        # markup is invisible to every other check on this page. Page 1078 has twelve of
        # them and reported `0/0 images  order OK`.
        # Gallery <img>s always carry class="full" or class="thumbnail"; page chrome is a
        # fixed short list. Anything else is embedded content that no stage handles.
        # This is a live-side heuristic and deliberately a SECOND opinion -- the exact test
        # is extract_projects.py's RTE-PAYLOAD check, which reads the bodytext itself.
        embedded = [t for t in re.findall(r'<img\b[^>]*>', h, re.I)
                    if not re.search(r'class="(full|thumbnail)"', t, re.I)
                    and not re.search(r'(fileadmin/s-maj/images/page/|clear\.gif|'
                                      r'RTEmagicC_flame4)', t, re.I)]
        # captions: each image description should appear in the page text
        caps = sum(1 for im in p['images'] if im['description'] and norm(im['description']) in norm(live))
        cap_total = sum(1 for im in p['images'] if im['description'])

        # ORDER. Presence is not order, and order failed silently once: ordering the
        # gallery by tx_dam.sorting instead of tx_dam_mm_ref.sorting_foreign produced the
        # right images with the right captions in the wrong sequence, and passed every
        # other check here. The old gallery emits one <div class="imageElement"> per image,
        # in display order, each carrying its DAM description -- compare the SEQUENCES.
        # Parse each imageElement INDEPENDENTLY. A paired `<h3>...</h3>\s*<p>(.*?)</p>`
        # regex silently skips any element that has no <p> -- an image with no DAM
        # description -- and every later element then compares against the wrong
        # position, reporting a false ORDER DIFFERS. malaga-la-vache has 15 elements of
        # which 2 have no <p>; the paired regex found 13 and mismatched from the first.
        img_blocks = re.split(r'<div class="imageElement">', h)[1:]
        live_seq = []
        for blk in img_blocks:
            m = re.match(r'\s*<h3>(.*?)</h3>', blk, re.S)
            d = re.match(r'\s*<h3>.*?</h3>\s*<p>(.*?)</p>', blk, re.S)
            live_seq.append(norm(d.group(1)) if d else '')
        ours_seq = [norm(im['description']) for im in p['images']]
        # live captions append "| creator"; ours keep the fields apart
        live_cmp = [x.split('|')[0].strip() for x in live_seq]
        order_ok = len(live_cmp) == len(ours_seq) and live_cmp == ours_seq
        first_diff = next((i+1 for i,(a,b) in enumerate(zip(live_cmp, ours_seq)) if a != b), None)

        ok = head_ok and body_ok and caps == cap_total and order_ok and not embedded
        if not ok: fails += 1
        rows.append((p['slug'],
                     'header OK' if head_ok else 'HEADER MISMATCH',
                     (f'body OK ({len(text_blocks)} blk)' if body_ok
                      else f'BODY MISMATCH {len(missing_blocks)}/{len(text_blocks)}'),
                     f'captions {caps}/{cap_total}',
                     ('order OK' if order_ok else
                      (f'ORDER DIFFERS at {first_diff}' if first_diff
                       else f'ORDER len {len(live_cmp)} vs {len(ours_seq)}'))
                     + (f'  <== {len(embedded)} EMBEDDED IMG not in any gallery'
                        if embedded else '')
                     + ('  <== %d TEXT BLOCK(S) WITH NO TEXT' % len(empty_blocks)
                        if empty_blocks else '')))
    w = max(len(r[0]) for r in rows)
    for r in rows: print(f"  {r[0]:<{w}}  {r[1]:<16} {r[2]:<14} {r[3]:<16} {r[4]}")
    print(f"\n  {len(rows)-fails}/{len(rows)} projects match live")
    return fails

if __name__ == '__main__':
    sys.exit(1 if run(int(sys.argv[1]) if len(sys.argv)>1 else 6) else 0)
