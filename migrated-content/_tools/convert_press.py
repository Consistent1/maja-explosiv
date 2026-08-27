#!/usr/bin/env python3
"""Stage 2 C+I - press. Emits press.md and copies clipping files.

JPGs go through jpegtran (lossless, identical pixels); PDFs are copied byte-for-byte.
Source is the filesystem backup; image-archive/ is not modified.
"""
import json, os, re, shutil, subprocess, sys, unicodedata
OUT=os.path.join(os.path.dirname(__file__),'..','press')
ROOT=os.path.join(os.path.dirname(__file__),'..','..')
BU=os.path.join(ROOT,'old','TYPO3BU','_')
DEST=os.path.join(ROOT,'src','assets','images','shared','press')
d=json.load(open(f'{OUT}/normalized/press.json'))

_TR = {'ä':'ae','ö':'oe','ü':'ue','ß':'ss','Ä':'Ae','Ö':'Oe','Ü':'Ue','é':'e','à':'a','ç':'c'}
def nfc(s): return unicodedata.normalize('NFC', s or '')

def slugname(fn):
    stem,ext=os.path.splitext(fn)
    stem=''.join(_TR.get(c,c) for c in unicodedata.normalize('NFC',stem))  # NFC first
    s=unicodedata.normalize('NFKD',stem).encode('ascii','ignore').decode()
    s=re.sub(r'[^A-Za-z0-9]+','-',s).strip('-').lower()
    return (s or 'clipping')+ext.lower()

# ---------------------------------------------------------------------------
# GALLERY COMPANIONS  (added 2026-08-27 -- see migrated-content/press/GALLERY-COMPANIONS.md)
#
# Five entries link a PDF. A PDF cannot be an <img>, so on its own such an entry
# appears in the text list but not in the gallery -- while the OLD SITE shows all
# three of these in its gallery, because TYPO3's DAM rasterised them into
# typo3temp/pics/ thumbnails.
#
# Three of those PDFs have a JPG counterpart already sitting in the same source
# directory. Pairing them restores the old site's gallery exactly, with no new
# asset invented and no change to what any entry LINKS to.
#
# TO REVERT: delete this table (set it to {}). Entries fall back to PDF-only,
# the gallery returns to 45, and nothing else changes.
# Values are paths relative to the backup root (old/TYPO3BU/_/), because the companion
# does not always sit beside the PDF.
GALLERY_COMPANION = {
    # 2018 pair: real clipping JPGs beside the PDFs. Verified against the live gallery's
    # own DAM titles -- our positions 0 and 1 match live exactly.
    '20180525ZürcherOberländer2.pdf':
        ('fileadmin/s-maj/images/BilderMaja/presse/2018_ZürcherOberländer2.jpg',
         '2018-zuercheroberlaender2.jpg'),
    '20180519ZürcherOberländer.pdf':
        ('fileadmin/s-maj/images/BilderMaja/presse/2018_ZürcherOberländer.jpg',
         '2018-zuercheroberlaender.jpg'),

    # Destroy HIV. CORRECTED 2026-08-27, twice.
    #   1st attempt: paired with '2013_Destroy_HIV.jpg' on the shared stem -- WRONG. That file
    #      is a 728x140 banner, a different asset, referenced nowhere on the live press page.
    #   2nd: removed the pairing, believing the live thumbnail could only be reproduced by
    #      rasterising the PDF ourselves -- also wrong.
    # TYPO3 had already rendered it, and the render is IN THE BACKUP:
    # typo3temp/pics/89d9b1aeec.jpg, 257x345, 51591 bytes -- byte-size identical to the image
    # the live gallery serves. old/TYPO3BU/ is extraction source E2, so this is a local source,
    # not a fetch from the live site.
    '2013_Destroy_HIV.pdf':
        ('typo3temp/pics/89d9b1aeec.jpg', '2013-destroy-hiv-clipping.jpg'),
}

WRITE='--write' in sys.argv
stats={'jpegtran':0,'copied-pdf':0,'missing':0}
for e in d['entries']:
    fn=os.path.basename(e['file'])
    e['target_name']=slugname(fn)
    e['target']=f"/assets/images/shared/press/{e['target_name']}"
    # a JPG companion for a PDF-linked entry, so it can appear in the gallery
    comp=GALLERY_COMPANION.get(nfc(fn))
    e['gallery_companion']=None
    if comp:
        crel, cname = comp
        csrc=os.path.join(BU, crel)
        if not os.path.exists(csrc):                      # NFD/NFC on disk
            d_,b_=os.path.split(csrc)
            if os.path.isdir(d_):
                for x in os.listdir(d_):
                    if nfc(x)==nfc(b_): csrc=os.path.join(d_,x); break
        if os.path.exists(csrc):
            e['gallery_companion']=f"/assets/images/shared/press/{cname}"
            e['gallery_companion_source']=crel
            if WRITE:
                os.makedirs(DEST,exist_ok=True)
                cdst=os.path.join(DEST,cname)
                r=subprocess.run(['jpegtran','-optimize','-progressive','-copy','none',csrc],capture_output=True)
                if r.returncode==0 and r.stdout:
                    open(cdst,'wb').write(r.stdout); stats['companion-jpegtran']=stats.get('companion-jpegtran',0)+1
                else:
                    shutil.copy2(csrc,cdst); stats['companion-copied']=stats.get('companion-copied',0)+1
        else:
            stats['companion-source-missing']=stats.get('companion-source-missing',0)+1
    if not e['file_exists']:
        stats['missing']+=1; e['target']=None; continue
    if not WRITE: continue
    os.makedirs(DEST,exist_ok=True)
    src=os.path.join(BU,e['file']); dst=os.path.join(DEST,e['target_name'])
    if e['is_pdf']:
        shutil.copy2(src,dst); stats['copied-pdf']+=1
    else:
        r=subprocess.run(['jpegtran','-optimize','-progressive','-copy','none',src],capture_output=True)
        if r.returncode==0 and r.stdout: open(dst,'wb').write(r.stdout); stats['jpegtran']+=1
        else: shutil.copy2(src,dst); stats['copied-pdf']+=1

def y(s): return '"'+s.replace('\\','\\\\').replace('"','\\"')+'"'
L=['---',
   'title: "Press"','layout: "about-page.njk"','permalink: "/about/press/"',
   f'pressNote: {y(d["note"])}',
   'pressEntries:']
for e in d['entries']:
    L.append(f'  - title: {y(e["title"])}')
    if e['target'] and not e['is_pdf']:
        L.append(f'    image: {y(e["target"])}')
    if e['target'] and e['is_pdf']:
        # a PDF cannot be an <img>; carried as `file` so the LINK is preserved.
        L.append(f'    file: {y(e["target"])}')
        # ...and its JPG companion, if one exists, so the gallery matches the old site
        if e.get('gallery_companion'):
            L.append(f'    image: {y(e["gallery_companion"])}')
            L.append(f'    image_is_companion: true')
    L.append(f'    source_file: {y(e["file"])}')
L += ['---','']
open(f'{OUT}/converted/press.md','w').write('\n'.join(L))
json.dump(d, open(f'{OUT}/normalized/press.json','w'), indent=2, ensure_ascii=False)
print(f"entries {len(d['entries'])}   stats {stats}")
print(f"  with image: {sum(1 for e in d['entries'] if e['target'] and not e['is_pdf'])}")
print(f"  with file (pdf): {sum(1 for e in d['entries'] if e['target'] and e['is_pdf'])}")
print(f"  no asset (missing): {sum(1 for e in d['entries'] if not e['target'])}")
print("  -> converted/press.md" + ("" if WRITE else "   [DRY RUN, no files copied]"))
