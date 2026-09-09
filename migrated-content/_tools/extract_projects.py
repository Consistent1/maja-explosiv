#!/usr/bin/env python3
"""Stages 6-11 E+N - projects. One container per stage; the shape is identical
throughout (plan H4), so adding a stage is one row in STAGES.

Each project page carries exactly two live content elements:
  - CType 'text' -- the description. `header` is "Title, Year".
  - CType 'list' -- the DAM gallery. bodytext is empty; images resolve through
    tx_dam_mm_ref (uid_local = image, uid_foreign = content element -- backwards
    from the column names).

Writes raw bodytext bytes per uid, then normalized/<stage>.json. No Markdown here.
"""
import base64, json, os, re, subprocess, sys, unicodedata

DB   = os.path.join(os.path.dirname(__file__), 'db.sh')
OUT  = os.path.join(os.path.dirname(__file__), '..', 'projects')

# container pid -> (stage, new category). Category per plan decision 13, and it must
# agree with convert_images.py -- the images are already filed under it.
STAGES = {
    '6': dict(container=874, category='paintings',    name='murals'),
    '7': dict(container=875, category='paintings',    name='paper work'),
    '8': dict(container=873, category='installations', name='event organisation'),
    # HOLD: pages deliberately not migrated yet, with the reason. They are still extracted
    # and still appear in normalized/, so nothing is lost -- the converter writes no Markdown
    # for them. Remove the entry to migrate. (owner, 2026-08-27)
    '9': dict(container=872, category='performance',  name='performance',
            hold={926: 'Elxt 90: 2 list elements (one is "Bio ShortList" with 0 images), '
                       '4 text blocks and 2 live html video embeds, plus 6 hidden elements. '
                       'Video content has no home in the plan and no Figma component.',
                  933: 'Casino Gitano: a live "Casino Gitano Videos:" text block and 8 hidden '
                       'elements (4 html video embeds + their captions). Same video question.'}),
    '10': dict(container=878, category='sculptures',   name='collaborations',
            hold={1078: 'Metal Group XIX: text uid 1654 is a 4-column TABLE of 12 thumbnail '
                        'images, each an internal link to another project -- a hand-built '
                        'index, not a DAM gallery. body_md strips it and there is no Figma '
                        'component for it. Migrated at Stage 10 and CORRUPTED before this '
                        'hold was added; see SOURCE.md.',
                  946: 'Wheel of Power: a live "Wheel of Power videos:" text block (uid 1446) '
                       'plus 2 hidden html video embeds and 2 hidden captions. Same video '
                       'question as stage 9.',
                  1054: 'Destroy HIV: a live "Videos" text block (uid 1572) plus 6 hidden html '
                        'video embeds, each captioned "Zerstoere HIV - Tag 1..6". Same video '
                        'question as stage 9.'}),
    # STAGE 11 -- sculptural work (877). It carries no projects of its own: it splits into
    # 1039 Sculptures and 1040 Installations, which map to DIFFERENT categories, and 1039
    # nests a third container (1068 Portraits) holding three more projects. One row per
    # container is what the rest of this pipeline expects -- a stage is one container and
    # one category -- so 11 is three rows, not one. Stage keys are strings for this reason.
    '11a': dict(container=1039, category='sculptures',   name='sculptures',
            hold={1050: 'The Birds: text uid 1557 is a multi-work page -- 11 RTE images in 5 '
                        'tables, each a photo pair captioned under a bold work title. Not a '
                        'DAM gallery and not one project. body_md cannot represent it. Same '
                        'class as metal-group-xix (stage 10).',
                  1068: 'Portraits: a SUB-CONTAINER holding 1067 Alberto, 1070 Kaethe and '
                        '1069 Bernhard (migrated as stage 11c), while carrying its own intro '
                        'text with 2 RTE images and no gallery of its own. Two open questions '
                        'at once -- what a container page becomes, and RTE payload.'}),
    '11b': dict(container=1040, category='installations', name='installations',
            hold={1064: 'The Helixes: a live "Videos" text block (uid 1616) plus 6 hidden html '
                        'video embeds. Same video question as stages 9 and 10.'}),
    '11c': dict(container=1068, category='sculptures',   name='portraits'),
}

def q(sql):
    r = subprocess.run([DB,'-N','-B','-e',sql], capture_output=True)
    if r.returncode: sys.exit("QUERY FAILED\n"+sql+"\n"+r.stderr.decode())
    return [l.split('\t') for l in r.stdout.decode('utf-8').split('\n') if l]

def b(v): return '' if v in ('','NULL') else base64.b64decode(v).decode('utf-8')
def B(col): return f"REPLACE(TO_BASE64({col}),'\\n','')"

_TR = {'ä':'ae','ö':'oe','ü':'ue','ß':'ss','Ä':'Ae','Ö':'Oe','Ü':'Ue',
       'é':'e','è':'e','ê':'e','à':'a','á':'a','â':'a','ç':'c','ñ':'n'}
def slug(s, n=48):
    # NFC before transliterating: _TR maps composed codepoints. NFD input would slip
    # past it and NFKD would then drop the mark -- 'Kaethe' becomes 'kathe'.
    s = unicodedata.normalize('NFC', s or '')
    s = ''.join(_TR.get(c, c) for c in s)
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()
    return (re.sub(r'[^a-zA-Z0-9]+','-',s).strip('-').lower()[:n]) or 'untitled'

# "Wohlgroth, 1993" / "Murals Europe, 1994-1995" -> (title, year)
_HDR = re.compile(r'^(?P<t>.+?),\s*(?P<y>\d{4}(?:\s*[-–/]\s*\d{2,4})?)\s*$')
def split_header(header, page_title):
    m = _HDR.match((header or '').strip())
    if m:
        return m.group('t').strip(), re.sub(r'\s*[-–]\s*','-',m.group('y').strip())
    return (header or page_title).strip(), None

def run(stage):
    S = STAGES[stage]
    # `shortcut` matters: a TYPO3 page can be an alias that carries no content of its own
    # and resolves to another page. Page 982 "Breath under Water" is one -- it sits under
    # paper work, has zero tt_content rows in ANY state, and points at 924, which lives
    # under a different container. The live site renders it by following the shortcut.
    # Without reading this column such a page looks like a project with no content.
    # `kids` catches SUB-CONTAINERS. The old site nests deeper than one level in places:
    # 877 "sculptural work" splits into 1039 Sculptures / 1040 Installations (known), and
    # inside 1039, page 1068 "Portraits" is itself a container holding Alberto, Kaethe and
    # Bernhard while carrying its own intro text and no gallery. A model that treats every
    # child of a container as a leaf project silently loses those three. Flagged, never
    # guessed past. (convert_images.py was never affected: it walks ancestors, so image
    # filing is correct at any depth.)
    # `content_from_pid` is a THIRD mechanism, and it bites harder than the other two
    # because the page looks populated. TYPO3 lets a page render ANOTHER page's content
    # while keeping its own. Page 949 "The Alchemy Bar" (container 1040) sets it to 937:
    # its own text and gallery are hidden=1, its only live element is the GDPR video note,
    # and it therefore reads as an almost-empty page -- while the live site serves a full
    # 36-image project, page 937's, which lives under container 1049. Read at Stage 11
    # only because the live capture came back 8 kB larger than its siblings.
    # Site-wide there are five such pages; 982 also sets `shortcut`, so it was already
    # caught, but 949 sets ONLY this column and nothing saw it.
    pages = q(f"""SELECT p.uid, {B('p.title')}, p.sorting, p.shortcut, p.content_from_pid,
                        (SELECT COUNT(*) FROM pages g
                          WHERE g.pid=p.uid AND g.deleted=0 AND g.hidden=0) AS kids
                  FROM pages p
                  WHERE p.pid={S['container']} AND p.deleted=0 AND p.hidden=0
                  ORDER BY p.sorting;""")
    projects = []
    for uid, t64, sort, shortcut, from_pid, kids in pages:
        uid = int(uid); ptitle = b(t64); shortcut = int(shortcut or 0); kids = int(kids)
        from_pid = int(from_pid or 0)
        ces = q(f"""SELECT uid, CType, {B('header')}, {B('bodytext')}, sorting
                    FROM tt_content WHERE pid={uid} AND deleted=0 AND hidden=0
                    ORDER BY sorting;""")
        text = [c for c in ces if c[1] == 'text']
        lists= [c for c in ces if c[1] == 'list']
        other= [c for c in ces if c[1] not in ('text','list')]
        # A project with no text, two texts, or an unexpected CType is not the shape
        # this stage assumes. Record it rather than guessing -- silently taking [0]
        # is how content goes missing.
        anomalies = []
        if len(text) == 0: anomalies.append('text-elements=0')
        elif len(text) > 1: anomalies.append(f'text-elements={len(text)} '
                                             f'(all captured and concatenated in sorting order)')
        if len(lists) > 1: anomalies.append(f'list-elements={len(lists)}')
        if other:          anomalies.append('other-ctypes=' + ','.join(c[1] for c in other))
        if kids:           anomalies.append(f'SUB-CONTAINER: {kids} child page(s) not walked '
                                            f'by this stage -- they need their own handling')
        # RTE PAYLOAD. A `text` element's bodytext can carry markup this pipeline has no
        # model for -- images, tables, and links wrapping an image rather than a label.
        # Page 1078 "Metal Group XIX" is 12 thumbnails in a 4-column table, each an
        # internal link to another project: a hand-built index, not a DAM gallery.
        #
        # It was migrated at Stage 10 and came out CORRUPTED, and nothing caught it:
        #   - the gallery count reads tx_dam_mm_ref only, so it said `imgs=0`;
        #   - the live check counts <div class="imageElement"> only, so it said 0/0 too;
        #   - body_md strips tags, and a <link> around an <img> has no text label, so it
        #     fell through to the bare href -- emitting the twelve page uids as the run-on
        #     string "107710731063...". The verifier's body check then PASSED, because it
        #     strips tags from both sides and an empty needle is trivially a substring.
        # Three independent checks agreed on a page whose entire second block was gone.
        # Detect it at the SOURCE, where it is exact, rather than inferring it downstream.
        for c in text:
            bt = b(c[3])          # c[3] is base64 out of the query -- decode it
            n_img = len(re.findall(r'<img\b', bt, re.I))
            n_tbl = len(re.findall(r'<table\b', bt, re.I))
            # a link whose content has no text once tags are stripped -- an image link
            n_imglink = sum(1 for m in re.finditer(
                r'<(?:link\s[^>]*|a\s[^>]*)>(.*?)</(?:link|a)>', bt, re.S | re.I)
                if not re.sub(r'<[^>]+>', '', m.group(1)).strip())
            if n_img or n_tbl or n_imglink:
                anomalies.append(
                    f'RTE-PAYLOAD in text uid {c[0]}: {n_img} img, {n_tbl} table, '
                    f'{n_imglink} image-link -- body_md CANNOT represent this, and will '
                    f'silently drop it. Do not migrate this page without a decision.')

        # A project can carry MORE THAN ONE live text element, and the extra ones are real
        # content, not noise: Eurokot's second block (uid 1458) is the list of 26 invited
        # artists, Eurokon's (1459) the East/West artist lists. Taking text[0] and moving on
        # would silently drop them. All blocks are captured in `sorting` order; the FIRST
        # supplies the header (the "Title, Year" line), the rest are continuation blocks.
        # A later block with a non-empty header keeps it -- page 926 has "Elxt 90 Videos:".
        # Every block's raw bytes are written to raw/db/ so the original stays available.
        text_blocks = []
        for tid, _ct, thdr, tbody, tsort in text:
            hdr, bdy = b(thdr), b(tbody)
            text_blocks.append(dict(uid=int(tid), header=hdr, bodytext_html=bdy,
                                    sorting=int(tsort)))
            open(f"{OUT}/raw/db/tt_content-{tid}.bodytext.html",'w',
                 encoding='utf-8').write(bdy)

        header = text_blocks[0]['header'] if text_blocks else ''
        body   = text_blocks[0]['bodytext_html'] if text_blocks else ''
        title, year = split_header(header, ptitle)

        images = []
        if lists:
            lid = lists[0][0]
            # GALLERY ORDER IS r.sorting_foreign. tx_dam_mm_ref.sorting is zero on all
            # 1745 rows -- which is true and was recorded -- but the conclusion drawn from
            # it, that tx_dam.sorting must therefore be the gallery order, was wrong.
            # tx_dam.sorting is the DAM record's own sorting. Ordering by it scrambles
            # every gallery, and nothing about the output looks broken: the right images
            # appear with the right captions, in the wrong sequence. Caught only by
            # comparing the ORDER against the live page. See verify_projects.py.
            # THE WHOLE DAM RECORD, not just the parts the old site prints. `creator`
            # alone was being read; `copyright` is a second credit and IS rendered, after
            # it ("Berlin 2008 | Maja Thommen | Erico Moreira", page 995 Soldier). But
            # rendering is not the test -- metadata that exists only in the database is
            # still content and still migrates (owner, 2026-09-09). On live galleries:
            # 447 images carry loc_country, 192 loc_city, 87 a DAM category, 16 caption,
            # 16 loc_desc, 12 copyright, 2 keywords, 2 publisher.
            # Deliberately NOT taken: alt_text, abstract, language, pages, instructions,
            # file_creator, file_orig_loc_desc, meta and ident are empty on all 2312
            # records; `date_mod` is a bookkeeping timestamp; and `tx_dam.category` is a
            # COUNT of assigned categories, not a category -- the real ones are the
            # tx_dam_mm_cat -> tx_dam_cat join below (2D, poster, concept illustration,
            # current work, 1.Mai).
            # `loc_country` uses the literal string '0' for unset, not '' -- treat it as
            # empty or every second image acquires a country of "0".
            for r in q(f"""SELECT d.uid, r.sorting_foreign, {B('d.title')}, {B('d.description')},
                                  {B('d.creator')}, d.date_cr, {B('d.file_path')}, {B('d.file_name')},
                                  {B('d.copyright')}, {B('d.caption')}, {B('d.publisher')},
                                  {B('d.keywords')}, {B('d.loc_desc')}, {B('d.loc_country')},
                                  {B('d.loc_city')},
                                  (SELECT GROUP_CONCAT(k.title ORDER BY k.title SEPARATOR '|')
                                     FROM tx_dam_mm_cat mm JOIN tx_dam_cat k ON k.uid=mm.uid_foreign
                                    WHERE mm.uid_local=d.uid AND k.deleted=0) AS cats
                           FROM tx_dam_mm_ref r JOIN tx_dam d ON d.uid=r.uid_local
                           WHERE r.uid_foreign={lid} AND r.tablenames='tt_content'
                             AND r.ident='rgsmoothgallery' AND d.deleted=0
                           ORDER BY r.sorting_foreign;"""):
                (du, dsort, dt, dd, dc, dcr, fp, fn, dcp,
                 dcap, dpub, dkw, dld, dlco, dlci, dcats) = r
                def _v(x):
                    x = b(x).strip()
                    return '' if x in ('', '0') else x
                images.append(dict(dam_uid=int(du), gallery_pos=int(dsort),
                                   title=b(dt), description=b(dd), creator=b(dc),
                                   copyright=b(dcp),
                                   caption=b(dcap), publisher=b(dpub), keywords=b(dkw),
                                   loc_desc=b(dld), loc_country=_v(dlco), loc_city=b(dlci),
                                   # q() renders SQL NULL as the STRING 'NULL' -- the same
                                   # trap b() already guards. Unfiltered, every image with
                                   # no category acquires one called "NULL".
                                   dam_categories=[c for c in (dcats or '').split('|')
                                                   if c and c != 'NULL'],
                                   date_cr=int(dcr) if dcr not in ('','NULL','0') else None,
                                   original=b(fp)+b(fn)))
        # Nothing to migrate: no text, no gallery. Record WHY, and where the content
        # actually lives, so the page is not silently dropped and not double-migrated.
        skip_reason = None
        held = (S.get('hold') or {}).get(uid)
        if held:
            skip_reason = 'HELD -- ' + held
        elif from_pid:
            # Checked BEFORE the empty test: such a page can carry live elements of its
            # own (949 carries the GDPR note) and so would not look empty at all.
            skip_reason = (f'content_from_pid={from_pid}: this page RENDERS PAGE {from_pid}\'s '
                           f'content, not its own. Whatever it holds locally is not what the '
                           f'live site shows. The content belongs to page {from_pid} and is '
                           f'migrated by whichever stage owns it.')
        elif not text and not images:
            skip_reason = (f'shortcut to page {shortcut}: no content of its own; the content '
                           f'belongs to that page and is migrated by whichever stage owns it'
                           if shortcut else 'no text element and no gallery')

        projects.append(dict(page_uid=uid, page_title=ptitle, page_sorting=int(sort),
                             shortcut=shortcut or None, content_from_pid=from_pid or None,
                             skip_reason=skip_reason,
                             child_pages=kids,
                             slug=slug(ptitle), title=title, year=year,
                             header=header, bodytext_html=body,
                             text_uid=int(text[0][0]) if text else None,
                             text_uids=[t['uid'] for t in text_blocks],
                             text_blocks=text_blocks,
                             list_uid=int(lists[0][0]) if lists else None,
                             anomalies=anomalies, images=images))
    d = dict(stage=stage, container=S['container'], container_name=S['name'],
             category=S['category'], projects=projects)
    json.dump(d, open(f'{OUT}/normalized/stage{stage}.json','w'), indent=1, ensure_ascii=False)
    print(f"stage {stage}  container {S['container']} ({S['name']}) -> {S['category']}")
    for p in projects:
        flag = ('  ANOMALY: '+'; '.join(p['anomalies'])) if p['anomalies'] else ''
        if p['skip_reason']: flag = '  SKIP -- ' + p['skip_reason']
        print(f"  {p['page_uid']:>4} {p['slug']:<28} {p['title']!r} year={p['year']} "
              f"body={len(p['bodytext_html']):>4}B imgs={len(p['images']):>3}{flag}")
    print(f"  -> normalized/stage{stage}.json")

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else '6')
