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
    6:  dict(container=874, category='paintings',    name='murals'),
    7:  dict(container=875, category='paintings',    name='paper work'),
    8:  dict(container=873, category='TBD',          name='event organisation'),
    9:  dict(container=872, category='performance',  name='performance'),
    10: dict(container=878, category='sculptures',   name='collaborations'),
    # 11 (sculptural work) splits across two sub-containers and is handled there.
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
    pages = q(f"""SELECT uid, {B('title')}, sorting FROM pages
                  WHERE pid={S['container']} AND deleted=0 AND hidden=0 ORDER BY sorting;""")
    projects = []
    for uid, t64, sort in pages:
        uid = int(uid); ptitle = b(t64)
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
        if len(text) != 1: anomalies.append(f'text-elements={len(text)}')
        if len(lists) > 1: anomalies.append(f'list-elements={len(lists)}')
        if other:          anomalies.append('other-ctypes=' + ','.join(c[1] for c in other))

        header = b(text[0][2]) if text else ''
        body   = b(text[0][3]) if text else ''
        title, year = split_header(header, ptitle)
        if text:
            open(f"{OUT}/raw/db/tt_content-{text[0][0]}.bodytext.html",'w',
                 encoding='utf-8').write(body)

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
            for r in q(f"""SELECT d.uid, r.sorting_foreign, {B('d.title')}, {B('d.description')},
                                  {B('d.creator')}, d.date_cr, {B('d.file_path')}, {B('d.file_name')}
                           FROM tx_dam_mm_ref r JOIN tx_dam d ON d.uid=r.uid_local
                           WHERE r.uid_foreign={lid} AND r.tablenames='tt_content'
                             AND r.ident='rgsmoothgallery' AND d.deleted=0
                           ORDER BY r.sorting_foreign;"""):
                du, dsort, dt, dd, dc, dcr, fp, fn = r
                images.append(dict(dam_uid=int(du), gallery_pos=int(dsort),
                                   title=b(dt), description=b(dd), creator=b(dc),
                                   date_cr=int(dcr) if dcr not in ('','NULL','0') else None,
                                   original=b(fp)+b(fn)))
        projects.append(dict(page_uid=uid, page_title=ptitle, page_sorting=int(sort),
                             slug=slug(ptitle), title=title, year=year,
                             header=header, bodytext_html=body,
                             text_uid=int(text[0][0]) if text else None,
                             list_uid=int(lists[0][0]) if lists else None,
                             anomalies=anomalies, images=images))
    d = dict(stage=stage, container=S['container'], container_name=S['name'],
             category=S['category'], projects=projects)
    json.dump(d, open(f'{OUT}/normalized/stage{stage}.json','w'), indent=1, ensure_ascii=False)
    print(f"stage {stage}  container {S['container']} ({S['name']}) -> {S['category']}")
    for p in projects:
        flag = ('  ANOMALY: '+'; '.join(p['anomalies'])) if p['anomalies'] else ''
        print(f"  {p['page_uid']:>4} {p['slug']:<28} {p['title']!r} year={p['year']} "
              f"body={len(p['bodytext_html']):>4}B imgs={len(p['images']):>3}{flag}")
    print(f"  -> normalized/stage{stage}.json")

if __name__ == '__main__':
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
