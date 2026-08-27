# Press gallery companions — what was changed, and how to undo it

**Date:** 2026-08-27 · **Owner-requested:** make the press page's gallery match the live site.
**Status:** applied, and reversible in one edit — see *Reverting* at the end.

---

## The problem

The old press page shows **two** things built from **two different content elements**:

| | source | shows |
|---|---|---|
| a gallery of thumbnails | `tt_content 1455` — a TYPO3 DAM gallery | **48 images** |
| a list of links | `tt_content 1452` — 50 `<link>` tags in body text | **50 links**, 45 to JPGs and 5 to PDFs |

The new site builds **both** from a single `pressEntries` list. An entry shows in the gallery
only if it has an `image`, and a **PDF cannot be an `<img>`** — so the five PDF-linked entries
appeared in the list but not the gallery, giving **45** where the old site shows **48**.

The old site manages it because TYPO3's DAM rasterised those PDFs into `typo3temp/pics/`
thumbnails at render time. We do not have that machinery, and generating one would mean
creating an asset that does not exist in the source.

## What was actually missing

The three-image gap breaks down as:

| file | why it was absent from our gallery |
|---|---|
| `2013_Destroy_HIV.pdf` | a **PDF that DAM indexed into the gallery** — surprising, but DAM handles any media type |
| `2018_ZürcherOberländer.jpg` | a **JPG in the gallery that no entry links** |
| `2018_ZürcherOberländer2.jpg` | same |

## The change

**No asset was invented.** All three PDFs turned out to have a **JPG counterpart already
sitting in the same source directory**, so the fix is to pair them:

| the entry links this PDF | now also shows this JPG in the gallery |
|---|---|
| `2013_Destroy_HIV.pdf` | `2013_Destroy_HIV.jpg` (21 KB) |
| `20180525ZürcherOberländer2.pdf` | `2018_ZürcherOberländer2.jpg` (2.0 MB) |
| `20180519ZürcherOberländer.pdf` | `2018_ZürcherOberländer.jpg` (5.6 MB) |

Result: gallery **45 → 48**, list unchanged at 50, PDF links unchanged at 5. All three now
match the live site exactly.

### Files changed

**1. `migrated-content/_tools/convert_press.py`**

- Added the `GALLERY_COMPANION` table (the three pairs above), marked with a revert note.
- Each companion JPG is copied to `src/assets/images/shared/press/` through
  `jpegtran -optimize -progressive -copy none` — lossless, identical pixels.
- A PDF-linked entry now emits **both** `file` (the PDF, what it links) and `image` (the
  companion JPG, what the gallery shows), plus `image_is_companion: true` as a marker.

**2. `src/_user/includes/about-content.njk`** — precedence reversed in the list loop:

```njk
{% set target = entry.file or entry.image %}   {# was: entry.image or entry.file #}
```

**This line matters more than it looks.** With the old precedence, an entry carrying both would
have linked its **preview JPG instead of the PDF**, silently swapping three downloadable press
articles for pictures of them. The gallery loop is untouched and still keys on `image` alone.

**3. Three new files** in `src/assets/images/shared/press/`:
`2013-destroy-hiv.jpg`, `2018-zuercheroberlaender.jpg`, `2018-zuercheroberlaender2.jpg`.
Press assets went 50 → 53.

## The one inference — CONFIRMED 2026-08-27

`2013_Destroy_HIV.pdf` → `2013_Destroy_HIV.jpg` was certain (identical stem).

The two 2018 pairings were inferred from a trailing "2", and an earlier version of this document
said the live gallery offered no way to check because it renders hashed `typo3temp/pics/`
filenames. **That was wrong.** Each gallery element carries an `<h3>` with the DAM record's
title, which resolves to a filename via `tx_dam`. The live gallery's first three positions are:

```
0  2018 ZürcherOberländer2
1  2018 ZürcherOberländer
2  2013 Destroy HIV
```

Our gallery renders `2018-zuercheroberlaender2.jpg`, `2018-zuercheroberlaender.jpg`,
`2013-destroy-hiv.jpg` in those same positions. **The pairing is correct**, not a guess.

There is also a third 2018 PDF, `20180525ZürcherOberländer_1.pdf` (610 KB), which **no entry
links and no gallery shows**. Preserved in the archive, left out of the site, matching live.

## A remaining difference: gallery ORDER

The 48 images are the same set, but **21 of 48 sit in a different position** than on the live
site. Two different orderings of one set:

| | ordered by |
|---|---|
| live gallery | `tx_dam.sorting` — the DAM element's own sequence |
| our gallery | the press-entry sequence, since we derive both from `pressEntries` |

The differences are local swaps within a year — `2002_elxt3`/`elxt4`, `2007_Die-Reinpfalz`/
`Mannheimer-Morgen`, `1996_ru3`/`ru4`. Nothing is missing or extra.

Fixing it would mean giving the gallery its own ordering key from `tx_dam.sorting` rather than
inheriting entry order, which is a change to how the template consumes `pressEntries`.
**Logged in `PLAN.md` rather than done**, since it is a presentation decision.

## Reverting

**One edit.** In `migrated-content/_tools/convert_press.py`:

```python
GALLERY_COMPANION = {}      # was: the three pairs
```

Then:

```bash
python3 migrated-content/_tools/convert_press.py --write
cp migrated-content/press/converted/press.md src/pages/about/press.md
rm src/assets/images/shared/press/2013-destroy-hiv.jpg \
   src/assets/images/shared/press/2018-zuercheroberlaender.jpg \
   src/assets/images/shared/press/2018-zuercheroberlaender2.jpg
```

Gallery returns to 45; list, links and every other entry are unaffected.

**Leave the template precedence as it is** even if reverting — `entry.file or entry.image` is
correct regardless, and reversing it is what would break the PDF links.

To change only the 2018 pairing rather than revert, swap the two JPG values in the table and
re-run the same two commands.
