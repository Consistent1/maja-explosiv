# Press gallery: image order differs from the live site

**Recorded 2026-08-27.** Not a defect in the migration — a consequence of the new site building
one thing where the old site built two. **21 of 48 positions differ. The set is identical:
nothing missing, nothing extra, no duplicates.**

## Why it happens

The old press page has two independent content elements:

| | source | ordered by |
|---|---|---|
| gallery of 48 thumbnails | `tt_content 1455`, a DAM gallery | **`tx_dam.sorting`** — the media library's own sequence |
| list of 50 links | `tt_content 1452`, `<link>` tags in body text | **the order they were typed into the text** |

They are separate objects that happen to show overlapping material, and nothing in TYPO3 keeps
their orders aligned.

The new site derives **both** from a single `pressEntries` array, so the gallery inherits the
list's order. Every image is present and correctly captioned; some appear at a different index
than on the old site.

## What differs

Local swaps within the same year or story, never a large displacement:

| # | live | ours |
|---|---|---|
| 3 / 5 | `2007_Die-Reinpfalz.jpg` ↔ `2007_Mannheimer-Morgen.jpg` | swapped |
| 15 / 16 | `2002_elxt3.jpg` ↔ `2002_elxt4.jpg` | swapped |
| 22 / 23 | `1998_Leipzig_bimbotown.jpg` ↔ `1998_bimbotown2.jpg` | swapped |
| 24–29 | the 1996 `ru*` group | reordered within the group |

The first three positions **do** match — `2018 ZürcherOberländer2`, `2018 ZürcherOberländer`,
`2013 Destroy HIV` — which is how the companion pairing in `GALLERY-COMPANIONS.md` was verified.

Full position-by-position comparison below.

## What it would take to match exactly

The gallery needs its own ordering key rather than inheriting entry order. Roughly:

1. Emit `gallery_sort` on each entry from `tx_dam.sorting` during conversion.
2. Sort the gallery loop in `about-content.njk` by it, leaving the list loop alone.

Both are small. It is **not done** because it is a presentation decision, not a correctness one:
whether the new site should reproduce the old gallery's sequence, or order clippings by date, or
follow the list. That is Maja's call.

Note the old order is not obviously intentional — `tx_dam.sorting` reflects the sequence images
were added to the media library, which may be nothing more than upload order.

## Full comparison

| # | live (tx_dam.sorting) | ours (entry order) | |
|---|---|---|---|
| 0 | `2018_ZürcherOberländer2.jpg` | `2018-zuercheroberlaender2.jpg` |  |
| 1 | `2018_ZürcherOberländer.jpg` | `2018-zuercheroberlaender.jpg` |  |
| 2 | `2013_Destroy_HIV.pdf` | `2013-destroy-hiv.jpg` |  |
| 3 | `2007_Die-Reinpfalz.jpg` | `2007-mannheimer-morgen.jpg` | **differs** |
| 4 | `2007_Rein-Neckar-Zeitung.jpg` | `2007-rein-neckar-zeitung.jpg` |  |
| 5 | `2007_Mannheimer-Morgen.jpg` | `2007-die-reinpfalz.jpg` | **differs** |
| 6 | `2006_Rdock1.jpg` | `2006-rdock1.jpg` |  |
| 7 | `2006_Rdock2.jpg` | `2006-rdock2.jpg` |  |
| 8 | `2006_rdock3.jpg` | `2006-rdock3.jpg` |  |
| 9 | `2005_freeRadicalPula.jpg` | `2005-freeradicalpula.jpg` |  |
| 10 | `2004_casino1.jpg` | `2004-casino1.jpg` |  |
| 11 | `2004_casino2.jpg` | `2004-casino2.jpg` |  |
| 12 | `2004_casino3.jpg` | `2004-casino3.jpg` |  |
| 13 | `2003_sihlpapier.jpg` | `2003-sihlpapier.jpg` |  |
| 14 | `2003_Elxt5.jpg` | `2003-elxt5.jpg` |  |
| 15 | `2002_elxt3.jpg` | `2002-elxt4.jpg` | **differs** |
| 16 | `2002_elxt4.jpg` | `2002-elxt3.jpg` | **differs** |
| 17 | `2001_Elxt2.jpg` | `2001-elxt2.jpg` |  |
| 18 | `2001_ELXT1.jpg` | `2001-elxt1.jpg` |  |
| 19 | `1999_pfae1.jpg` | `1999-pfae1.jpg` |  |
| 20 | `1999_pfae3.jpg` | `1999-pfae3.jpg` |  |
| 21 | `1999_pfae2.jpg` | `1999-pfae2.jpg` |  |
| 22 | `1998_Leipzig_bimbotown.jpg` | `1998-bimbotown2.jpg` | **differs** |
| 23 | `1998_bimbotown2.jpg` | `1998-leipzig-bimbotown.jpg` | **differs** |
| 24 | `1996_ru-presseerklarung.jpg` | `ru6.jpg` | **differs** |
| 25 | `1996_ru3.jpg` | `1996-ru4.jpg` | **differs** |
| 26 | `1996_ru1.jpg` | `1996-ru1.jpg` |  |
| 27 | `1996_ru4.jpg` | `1996-ru3.jpg` | **differs** |
| 28 | `1996_ru7.jpg` | `1996-ru7.jpg` |  |
| 29 | `1996_rueinladung.jpg` | `1996-ru2.jpg` | **differs** |
| 30 | `ru6.jpg` | `1996-ru-ubersetzungen.jpg` | **differs** |
| 31 | `1996_ru-ubersetzungen.jpg` | `1996-ru-presseerklarung.jpg` | **differs** |
| 32 | `1996_ru2.jpg` | `1996-rueinladung.jpg` | **differs** |
| 33 | `1995_ew1.jpg` | `1995-rock-preis.jpg` | **differs** |
| 34 | `1995ew3.jpg` | `1995-ew1.jpg` | **differs** |
| 35 | `1995_ew4.jpg` | `1995-ew5.jpg` | **differs** |
| 36 | `1995_ew6.jpg` | `1995-ew6.jpg` |  |
| 37 | `1995_ew7.jpg` | `1995-ew4.jpg` | **differs** |
| 38 | `1995_ew5.jpg` | `1995-ew7.jpg` | **differs** |
| 39 | `1995_Rock-preis.jpg` | `1995ew3.jpg` | **differs** |
| 40 | `1995_denhaag2.jpg` | `1995-denhaag2.jpg` |  |
| 41 | `1995_ew2.jpg` | `1995-ew2.jpg` |  |
| 42 | `1994_prag.jpg` | `1994-prag.jpg` |  |
| 43 | `1995_felix_regula3.jpg` | `1995-felix-regula3.jpg` |  |
| 44 | `felix_regula2.jpg` | `felix-regula2.jpg` |  |
| 45 | `1994_felix_regula.jpg` | `1994-felix-regula.jpg` |  |
| 46 | `1993_wohlgrott.jpg` | `1993-wohlgrott2.jpg` | **differs** |
| 47 | `1993_wohlgrott2.jpg` | `1993-wohlgrott.jpg` | **differs** |

mismatched positions: 21 of 48
same set: True
