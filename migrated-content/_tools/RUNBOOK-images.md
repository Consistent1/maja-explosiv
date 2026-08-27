# Runbook — processing images, and what to do when a new backup arrives

Written 2026-08-27, after Stages 1–2. Policy lives in the migration plan (decision 14); this
is the procedure.

## The rules that do not change

1. **`old/TYPO3BU/_/` and `image-archive/` are read-only.** Nothing writes to either.
2. **Lossless only.** `jpegtran -optimize -progressive -copy none` — identical pixels, smaller
   file, metadata stripped. **Never** resize, never re-encode, never convert format.
3. **Native size**, including the large ones (owner, explicit).
4. **PDFs and non-JPEG files are copied byte-for-byte.** jpegtran only understands JPEG.
5. **Live content only** reaches `src/`. Hidden and deleted stay in their own stores.

## Order of operations

```
old/TYPO3BU/_/  ──build_archive.py──▶  image-archive/  ──convert_images.py──▶  src/assets/images/projects/
       └────────────────────────────convert_press.py───────────────────────▶  src/assets/images/shared/press/
```

**Note the asymmetry, it is deliberate but easy to trip over:** `convert_images.py` reads from
`image-archive/`, `convert_press.py` reads from `old/TYPO3BU/_/` directly. Press clippings are
referenced by path from `bodytext` rather than through a DAM gallery, so they are not routed
through the archive's gallery-derived structure. **If you change one, check the other.**

## When a new backup arrives

The known reason for needing one: **the January 2025 backup contains no non-ASCII filenames at
all** — 30 files across the site, and 2 press clippings, were silently dropped by whatever
transferred it. `Käthe` (16 images) and `Bernhard` (12) have none at all.

**Get the backup right first.** Use `rsync` or `tar` over SSH with a UTF-8 locale. FTP clients
and legacy-codepage zip tools will drop exactly the same files again, just as silently.

Then:

```bash
# 0. Sanity-check the new backup BEFORE trusting it
find <new-backup>/fileadmin -depth | LC_ALL=C grep -cP '[\x80-\xff]'
#    Must be > 0. If it returns 0, the umlaut files were dropped again -- stop here.

# 1. Put it in place (keep the old one until the new is verified)
# 2. Rebuild the archive. Idempotent: existing files are not re-copied.
python3 migrated-content/_tools/build_archive.py --copy

# 3. Regenerate project images. Existing outputs are overwritten with identical bytes.
python3 migrated-content/_tools/convert_images.py --write

# 4. Regenerate press assets and page
python3 migrated-content/_tools/convert_press.py --write
cp migrated-content/press/converted/press.md src/pages/about/press.md

# 5. Rebuild and check
npx eleventy
```

**Expect `source-not-in-archive` to fall from 28 to 0** in step 3, and the 2 press
`missing-from-source` rows to clear in step 4.

## Filenames: NFC vs NFD

**The live server stores umlauts decomposed (NFD); TYPO3's database stores them composed
(NFC).** `ü` is one codepoint in the database and two on disk. They render identically and
compare unequal.

Every path comparison in these tools normalises to NFC first — `nfc()` in `build_archive.py`,
`convert_images.py` and `convert_press.py`, and an NFC-comparing directory scan in
`normalize_press.py`. **Do not remove it.** Without it, files that are present report as
missing, and that looks exactly like the original backup problem.

Two rules if you touch this code:

1. **Normalise to NFC before transliterating**, never after. The transliteration table maps
   composed characters, so NFD input slips past it and the umlaut is then dropped —
   `Käthe` becomes `kathe` instead of `kaethe`, quietly creating a second folder for one project.
2. **Test both forms.** `unicodedata.normalize('NFD', name)` and the NFC form must produce the
   same slug and resolve to the same file.

## Verifying a conversion is really lossless

Decode both to raw RGB and compare. This is the only check that proves it:

```bash
convert <source> -depth 8 rgb:- | sha256sum
convert <output> -depth 8 rgb:- | sha256sum
```

File sizes will differ — that is the point. **Pixel hashes must match exactly.** Run it on a
sample of a dozen after any bulk pass.

## Known measurements, for comparison against a re-run

| | |
|---|---|
| archive | 1,661 files, 562,019,142 bytes, 1,198 distinct by sha256 |
| project images | 978 files, 346.0 MB in → 310.4 MB out, **10.3% saved, zero pixel change** |
| press | 48 of 50 assets — 45 via jpegtran, 3 PDFs copied |
| source profile | median longest edge 1000px, 34% ≥1200px, max 2480px, 68% at 4:4:4, q86–99 |

If a re-run produces materially different numbers, something changed — investigate before
committing.

## Not covered by these tools

- **Images embedded in `bodytext` HTML** (`<img src=...>`, including `uploads/RTEmagicC_*`):
  70 elements, 38 live, 163 distinct files. Unaudited, not in the archive.
- **`fileadmin/.../thumbs/` and the 1,378 `uploads/RTEmagic*` derivatives** — regenerable, not
  referenced by any gallery, deliberately excluded.
- **Delivery variants** (WebP/AVIF, responsive widths). A later bandwidth decision, to be
  generated from these preserved originals, never from a lossy intermediate.
