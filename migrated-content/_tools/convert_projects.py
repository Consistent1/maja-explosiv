#!/usr/bin/env python3
"""Stages 6-11 C - projects. normalized/stage<N>.json -> src Markdown.

Image paths are NOT derived here. They come from _census/site-images.json, the manifest
convert_images.py wrote when it filed the archive originals into src/assets/. Deriving
them twice is how the two sides drift apart; this joins on (page_uid, dam_uid).

FRONT MATTER -- both keys are required, and they drive different things:
  postCollections  -> collection pages   (collection.njk: allPosts|getPostsByCollection)
  tags             -> featured projects  (featured-projects.njk: collections[<name>])
The quarantined pre-migration files set `tags` only, which is why the collection pages
rendered empty while featuredProjects.json still resolved. Setting one is a silent half-fix.
"""
import json, html, os, re, sys

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
OUT  = os.path.join(os.path.dirname(__file__), '..', 'projects')
DEST = os.path.join(ROOT, 'src', 'posts', 'projects')

def y(s): return '"'+str(s).replace('\\','\\\\').replace('"','\\"')+'"'

def body_md(h):
    """TYPO3 bodytext -> Markdown.

    <br /> here is SOFT WRAP, not a paragraph break -- the text was typed to a fixed
    column ("...expeditions around <br />Europe, from Austria..."). A single <br />
    becomes a space; a doubled one becomes a paragraph break. Treating every <br /> as
    a line break, as the legal converter does, would shatter each description into
    six one-line paragraphs.
    """
    h = re.sub(r'<br\s*/?>\s*<br\s*/?>', '\x00', h)          # paragraph break
    h = re.sub(r'<br\s*/?>', ' ', h)                          # soft wrap
    # Emphasis. Whitespace INSIDE the tag must move outside the marker: the source
    # writes "<b>Zeleny Dvor </b>in", and a literal swap yields "**Zeleny Dvor **in",
    # which Markdown will not close -- it renders the asterisks.
    h = re.sub(r'<(b|strong)>(\s*)(.*?)(\s*)</\1>',
               lambda m: m.group(2) + '**' + m.group(3) + '**' + m.group(4), h, flags=re.S)
    h = re.sub(r'</?(b|strong)>', '**', h)                    # unbalanced leftovers
    paras = []
    for p in h.split('\x00'):
        p = html.unescape(re.sub(r'<[^>]+>', '', p))
        p = re.sub(r'[ \t]+', ' ', p).strip()
        if p: paras.append(p)
    return '\n\n'.join(paras) + '\n'

def run(stage, write=False):
    d   = json.load(open(f'{OUT}/normalized/stage{stage}.json'))
    cat = d['category']
    imgs_by = {}
    for r in json.load(open(f'{ROOT}/migrated-content/_census/site-images.json')):
        imgs_by[(r['page_uid'], r['dam_uid'])] = r

    os.makedirs(f'{OUT}/converted/{cat}', exist_ok=True)
    report = []
    for p in d['projects']:
        rows, missing = [], 0
        for im in p['images']:
            m = imgs_by.get((p['page_uid'], im['dam_uid']))
            if not m:                     # in the gallery but never filed into src/
                missing += 1; continue
            rows.append((m['seq'], '/' + m['target'].split('src/', 1)[1].replace('assets', 'assets', 1), im))
        rows.sort()
        # the manifest's seq is the old site's gallery order (tx_dam.sorting); keep it
        L = ['---',
             f'title: {y(p["title"])}',
             f'layout: "project.njk"',
             f'date: {(p["year"] or "1900").split("-")[0]}-01-01',
             f'year: {y(p["year"] or "")}',
             f'category: {y(cat)}',
             f'postCollections: [{cat}]',
             f'tags: [{cat}]']
        if rows:
            L.append(f'featuredImage: {y(rows[0][1])}')
            first = rows[0][2]
            L.append(f'featuredImageAlt: {y(first["description"] or first["title"] or p["title"])}')
        L += [f'source_uid: {p["page_uid"]}',
              f'source_page_title: {y(p["page_title"])}',
              f'source_header: {y(p["header"])}',
              f'source_category: {y(d["container_name"])}',
              f'source_text_uid: {p["text_uid"]}',
              f'source_list_uid: {p["list_uid"]}',
              f'source_sorting: {p["page_sorting"]}']
        if rows: L.append('images:')
        for seq, src, im in rows:
            L.append(f'  - src: {y(src)}')
            L.append(f'    alt: {y(im["description"] or im["title"] or p["title"])}')
            if im['title']:       L.append(f'    title: {y(im["title"])}')
            if im['description']: L.append(f'    description: {y(im["description"])}')
            if im['creator']:     L.append(f'    author: {y(im["creator"])}')
            L.append(f'    dam_uid: {im["dam_uid"]}')
            L.append(f'    original: {y(im["original"])}')
        L += ['---', '', body_md(p['bodytext_html'])]
        md = '\n'.join(L)
        open(f'{OUT}/converted/{cat}/{p["slug"]}.md', 'w').write(md)
        if write:
            os.makedirs(f'{DEST}/{cat}', exist_ok=True)
            open(f'{DEST}/{cat}/{p["slug"]}.md', 'w').write(md)
        report.append((p['slug'], len(rows), missing, len(p['images'])))

    print(f"stage {stage} -> {cat}")
    for slug, n, miss, total in report:
        flag = f'   {miss} GALLERY IMAGE(S) NOT IN site-images.json' if miss else ''
        print(f"  {slug:<28} {n:>3}/{total:<3} images{flag}")
    print(f"  -> converted/{cat}/  " + ("and src/posts/projects/" if write else "[DRY RUN]"))

if __name__ == '__main__':
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 6, '--write' in sys.argv)
