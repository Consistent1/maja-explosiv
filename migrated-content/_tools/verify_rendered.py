#!/usr/bin/env python3
"""Verify the BUILT SITE against the migrated data.

Why this exists
---------------
verify_projects.py compares `normalized/stage<N>.json` against the LIVE page, and it passed
every stage while the site rendered the wrong thing. It proves the migration captured the
content; it says nothing about whether the site shows it.

That gap hid a real fault for three weeks. `project.njk` passed the PROJECT title into every
image caption, so a project page repeated one title under all its photographs while the old
site names each view. Most DAM titles are "<project>, <view>", so the caption read as though
it had been TRUNCATED AT THE COMMA -- and it was reported as truncated captions. Nothing was
truncated: all 796 image titles were in the front matter the whole time. The chain was
    DB -> normalized  [checked]
       -> front matter [checked]
       -> RENDERED     [NOT CHECKED]  <-- the fault lived here.

So: every value the migration puts in a project's front matter must be findable in that
project's built page, or be listed below as deliberately not rendered.

Run AFTER a build. Exit code is the number of failures.
"""
import glob, html, json, os, re, sys, unicodedata

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
NORM = os.path.join(os.path.dirname(__file__), '..', 'projects', 'normalized')

# Per-image fields that MUST reach the page, and the caption row each belongs to.
REQUIRED = ('title', 'description')          # `author` is joined creator|copyright, checked apart

# Captured on purpose, rendered nowhere yet. Each needs a reason, not just a name -- an entry
# here is a decision that the site does not show something the database holds.
NOT_RENDERED = {
    'copyright':      'folded into `author` as "creator | copyright", the form the old site prints',
    'caption':        'a venue ("Spannwerk"); the old site never printed it and the design has no slot',
    'publisher':      'never populated on any migrated image',
    'keywords':       'never populated on any migrated image',
    'loc_desc':       'no slot in the Figma caption -- open item',
    'loc_country':    'no slot in the Figma caption -- open item',
    'loc_city':       'no slot in the Figma caption -- open item',
    'dam_categories': 'Maja\'s own DAM tagging; no slot in the design -- open item',
    'dam_uid':        'provenance, not content',
    'original':       'provenance, not content',
    'gallery_pos':    'provenance, not content',
    'date_cr':        "the photograph's date, which disagrees with the project year -- see PLAN.md",
}

def txt(h):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h)))

def norm(s):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', s or '')).strip()

def run():
    site = os.path.join(ROOT, '_site')
    if not os.path.isdir(site):
        sys.exit('no _site/ -- build first: node node_modules/.bin/eleventy')
    rows, fails, checked = [], 0, 0
    for f in sorted(glob.glob(f'{NORM}/stage*.json')):
        d = json.load(open(f, encoding='utf-8'))
        for p in d['projects']:
            if p['skip_reason']:
                continue
            out = f"{site}/posts/projects/{d['category']}/{p['slug']}/index.html"
            if not os.path.exists(out):
                rows.append((p['slug'], 'NOT BUILT', '')); fails += 1; continue
            h = open(out, encoding='utf-8').read()
            page = norm(txt(h))
            missing = []
            for im in p['images']:
                for field in REQUIRED:
                    v = norm(im.get(field))
                    if not v:
                        continue
                    checked += 1
                    if v not in page:
                        missing.append(f"{field} of dam {im['dam_uid']}: {v[:44]!r}")
                # `author` is the joined credit the caption prints
                credit = ' | '.join(x for x in (norm(im.get('creator')),
                                                norm(im.get('copyright'))) if x)
                if credit:
                    checked += 1
                    if credit not in page:
                        missing.append(f"author of dam {im['dam_uid']}: {credit[:44]!r}")
            # the project's own body text
            for blk in (p.get('text_blocks') or []):
                body = norm(txt(blk['bodytext_html']))
                if body:
                    checked += 1
                    # compare the longest run of plain words, immune to markdown/link rewriting
                    probe = max(re.findall(r'[\w,\'\- ]{25,}', body) or [''], key=len).strip()
                    if probe and norm(probe) not in page:
                        missing.append(f"text block {blk['uid']}: {probe[:44]!r}")
            if missing:
                fails += 1
                rows.append((p['slug'], f'{len(missing)} MISSING', missing[0]))
            else:
                rows.append((p['slug'], 'ok', ''))
    w = max(len(r[0]) for r in rows)
    for s, st, d_ in rows:
        if st != 'ok':
            print(f'  {s:<{w}}  {st}   {d_}')
    ok = sum(1 for r in rows if r[1] == 'ok')
    print(f'\n  {ok}/{len(rows)} projects fully rendered   ({checked} values checked)')
    if NOT_RENDERED:
        print('\n  captured but deliberately not rendered:')
        for k, why in NOT_RENDERED.items():
            print(f'    {k:<16} {why}')
    return fails

# ---------------------------------------------------------------------------
# The About pages carry their content as front-matter DATA STRUCTURES rather than
# prose, so the same failure is possible there and looks the same: a value migrated
# correctly, sitting in the file, that no template ever reads. Checked by walking the
# structures rather than by matching prose.
ABOUT = [
    ('links',    'about/links',
     lambda d: [d.get('linksHeading')] + [x for c in d.get('linkCategories') or []
                for x in [c.get('heading')] + [v for e in c.get('entries') or []
                for v in (e.get('text'), e.get('name'), e.get('suffix'))]]),
    ('press',    'about/press',
     lambda d: [d.get('pressNote')] + [e.get('title') for e in d.get('pressEntries') or []]),
    ('timeline', 'about/timeline',
     lambda d: [x for s in d.get('timelineSections') or []
                for x in [s.get('heading')] + [v for e in s.get('entries') or []
                for v in (e.get('year'), e.get('title'), e.get('description'))]]),
]
# Values that live in an attribute (href/src), not in the page text.
ABOUT_TARGETS = [
    ('links', 'about/links', lambda d: [e.get('url') for c in d.get('linkCategories') or []
                                        for e in c.get('entries') or []]),
    ('press', 'about/press', lambda d: [v for e in d.get('pressEntries') or []
                                        for v in (e.get('file'), e.get('image'))]),
]

def _front_matter(path):
    """Minimal YAML front-matter reader -- enough for these files, no dependency."""
    import yaml
    t = open(path, encoding='utf-8').read()
    return yaml.safe_load(t.split('---', 2)[1]) if t.startswith('---') else {}

def run_about():
    site, fails = os.path.join(ROOT, '_site'), 0
    for name, url, pick in ABOUT:
        src = os.path.join(ROOT, 'src', 'pages', url + '.md')
        out = os.path.join(site, url, 'index.html')
        if not (os.path.exists(src) and os.path.exists(out)):
            print(f'  {name:<10} not built'); continue
        d = _front_matter(src)
        page = norm(txt(open(out, encoding='utf-8').read()))
        vals = [str(v) for v in pick(d) if v not in (None, '')]
        miss = [v for v in vals if norm(v) not in page]
        raw = open(out, encoding='utf-8').read()
        targets = [str(v) for n2, u2, p2 in ABOUT_TARGETS if n2 == name
                   for v in p2(d) if v]
        tmiss = [v for v in targets if v not in raw]
        fails += len(miss) + len(tmiss)
        print(f'  {name:<10} {len(vals)} text + {len(targets)} link targets   '
              f'{"ok" if not (miss or tmiss) else f"{len(miss)+len(tmiss)} MISSING"}')
        for m in (miss + tmiss)[:4]:
            print(f'      {m[:70]!r}')
    return fails

if __name__ == '__main__':
    f = run()
    print('\n  About pages:')
    f += run_about()
    sys.exit(1 if f else 0)
