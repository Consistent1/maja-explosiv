# Press — source record

**Content type:** Press · **Stage:** 2 · **Migrated:** 2026-08-27

## Where it came from

| | |
|---|---|
| Page | `pages.uid = 981`, title `press`, realurl `info/press` |
| Entries | `tt_content.uid = 1452` — 8,365 bytes, 50 `<link>` entries |
| Note | `tt_content.uid = 1456` — 93 bytes |
| Gallery | `tt_content.uid = 1455` — DAM gallery, 48 images (see below) |
| Header-only | `tt_content.uid = 1319` — empty bodytext |
| Assets | `old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja/presse/` |
| Connection | charset `latin1`, no transformation (plan §2.3) |

## What was done

1. **Extracted** all four content elements to `raw/db/`.
2. **Normalised** 1452 into 50 ordered entries. Each is
   `<link {file} - download "...">{anchor}</link>{trailing prose}`; the title is anchor plus
   prose, so *"Destoy HIV"* + *"; Schirmherrschaft Frank Walter Steinmeier, Public Marketing,
   October 2013"*. The source's spelling is kept verbatim, including *"Destoy"* and
   *"Anouncment"*.
3. **Copied 48 of 50 clipping files** into `src/assets/images/shared/press/` —
   **45 JPGs through `jpegtran -optimize -progressive -copy none`** (lossless, identical
   pixels) and **3 PDFs byte-for-byte**. Filenames slugified from the originals, preserving
   the year prefix: `1993_wohlgrott.jpg` → `1993-wohlgrott.jpg`.
4. **Converted** to `pressEntries` + `pressNote` and installed to `src/pages/about/press.md`.
5. **Verified** against the live page.

`image-archive/` was not touched. Assets were taken from the filesystem backup directly.

## Why the links, not the gallery

The page carries two asset mechanisms that overlap on 46 files: the DAM gallery (1455, 48
images) and the download links in bodytext (1452, 50 files). **The links are authoritative** —
they are what the entries reference, and the note (1456) describes exactly them: *"The links
below open a bigger and readable version of each press article in a new tab."* The gallery is a
thumbnail view of the same material, and the new template already renders a gallery from the
same `pressEntries`.

## The gap

**50 entries migrated. 48 have an asset. 48 render as links.**

| | count | why |
|---|---|---|
| fully migrated and linked | 45 | — |
| ~~asset present, no link rendered~~ | ~~3~~ → **linked** | PDFs; template fixed 2026-08-27 to read `entry.file` |
| no asset | 2 | files absent from the backup |

**The 2 missing** are `20180525ZürcherOberländer2.pdf` and `20180519ZürcherOberländer.pdf`.
Same cause as the other 30 across the site: **the backup contains no non-ASCII filenames at
all.** Ledger status `missing-from-source`; resolved by a fresh backup taken with a method that
preserves them.

**The 3 unlinked** are *Destroy HIV* (2013), *Wacken Scull* (2012), *The Alchemy Bar* (Wired,
2007). Their PDFs are copied and their paths recorded in `entry.file` — nothing is lost — but
`about-content.njk` reads only `entry.image`, and a PDF cannot be an `<img>`. Fixed by a
one-line template change, logged in `PLAN.md`.

Net against the live site: **50 entries, 50 links, 48 gallery images — all three match.**

**Gallery companions (2026-08-27):** three PDF-linked entries additionally carry a JPG companion
so they appear in the gallery, as they do on the old site. Documented, with a one-line revert
and one inferred pairing flagged, in **`GALLERY-COMPANIONS.md`**.
