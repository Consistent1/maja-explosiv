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

## Destroy HIV — got wrong twice, then fixed

Worth recording in full, because both errors were confident.

**Attempt 1.** `2013_Destroy_HIV.pdf` was paired with `2013_Destroy_HIV.jpg` on the strength of
the shared filename stem, and this document called it *"certain"* while flagging the two 2018
pairings as the doubtful ones. **Exactly backwards.** `2013_Destroy_HIV.jpg` is **728×140 — a
wide banner**, a different asset entirely, referenced **nowhere** on the live press page. The
live gallery shows a **257×345 portrait**. The DAM gallery holds exactly one Destroy record,
`uid 2645`, and it points at the **PDF**.

**Attempt 2.** The pairing was removed, on the reasoning that matching the live thumbnail would
mean rasterising the PDF ourselves and inventing an asset. Also wrong.

**The fix.** TYPO3 had already rendered that thumbnail, and **the render is in the backup**:

| | |
|---|---|
| `old/TYPO3BU/_/typo3temp/pics/89d9b1aeec.jpg` | 257×345, 51,591 bytes |
| the live gallery's image | 257×345, 51,591 bytes |

`old/TYPO3BU/` is extraction source **E2**. Using it is a local source, not a fetch from the live
site, so decision 1 is not engaged. It ships as
`/assets/images/shared/press/2013-destroy-hiv-clipping.jpg`; the entry still links the PDF.

**`typo3temp/pics/` holds 3,766 rendered derivatives.** It is a fourth asset source, unconsidered
until now, and it is how *any* PDF-backed gallery item gets its thumbnail. Stages 6–11 may hit
the same case.

**The lesson, since it cost two rounds:** the pairings that were doubted got verified and were
right; the one asserted as certain was never checked and was wrong.

## Current state

| entry links | gallery shows | source |
|---|---|---|
| `20180525ZürcherOberländer2.pdf` | `2018-zuercheroberlaender2.jpg` | clipping JPG beside the PDF |
| `20180519ZürcherOberländer.pdf` | `2018-zuercheroberlaender.jpg` | clipping JPG beside the PDF |
| `2013_Destroy_HIV.pdf` | `2013-destroy-hiv-clipping.jpg` | **TYPO3 render from `typo3temp/pics/`** |

Gallery renders **48**, matching the live site exactly. All 53 press source files are in
`image-archive/live/about/press/` with `PROVENANCE.json` recording each one's original path and
role.

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
