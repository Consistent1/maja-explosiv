# Press — verification report

**Stage 2 · run 2026-08-27 · status: PASSED with a recorded gap and one template limitation**

## Result

| check | result |
|---|---|
| V0a source census | 50 entries (`tt_content` 1452) + note (1456) + gallery (1455, 48 images) |
| V0b truth census | **50** anchors to press files on the live page |
| V1 count parity | source 50 = converted 50 = rendered 50 |
| V2 bijection | every live anchor text matched (20 distinct; entries repeat titles) |
| V3 field fidelity | titles match, prose suffix preserved |
| V6 assets | 48 of 50 copied — 45 JPG via jpegtran (lossless), 3 PDF byte-for-byte |
| V7 encoding | `Zürcher Oberländer` correct throughout |
| V11 provenance | installed file matches the migrated artefact |

## Two shortfalls, both recorded rather than papered over

**1. Two files missing from the backup** — `20180525ZürcherOberländer2.pdf` and
`20180519ZürcherOberländer.pdf`. Same root cause as the other 30: **the backup contains no
non-ASCII filenames at all.** Their entries migrate with title and provenance but no asset, and
render as plain text. `missing-from-source` in the ledger; resolved by the fresh backup.

**2. ~~Three PDF entries render without a link.~~ FIXED 2026-08-27.** The template keys both the gallery and the list
on `entry.image`, and a PDF cannot be an `<img>` — `<img src="....pdf">` would be a broken
image. The conversion therefore carries PDFs as **`file`** rather than `image`, so **no data is
lost**, but `about-content.njk` does not read `file`, so those three show as plain text where
the live site links them.

Affected: *Destroy HIV* (2013), *Wacken Scull* (2012), *The Alchemy Bar* (Wired, 2007).

**Fixed** in `src/_user/includes/about-content.njk`: the list loop now resolves
`entry.image or entry.file`, so the three PDFs link as they do on the old site. The gallery
still keys on `image` alone, which is correct.

**Net: the live site links 50 entries, the migrated page links 48.** The remaining 2 are the
missing files, and resolve with the fresh backup.

## Notes

- The page has **two** asset mechanisms: the DAM gallery (1455, 48 images) and the download
  links in `bodytext` (1452, 50 files). They overlap on 46. The migration follows the links,
  since those are what the entries actually reference, and the note (1456) describes them:
  *"The links below open a bigger and readable version of each press article in a new tab."*
- Clipping filenames are slugified from the originals, preserving the year prefix
  (`1993_wohlgrott.jpg` → `1993-wohlgrott.jpg`), so they stay traceable by eye.
- V8 visual comparison still needs a browser.
