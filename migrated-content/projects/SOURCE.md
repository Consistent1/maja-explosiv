# Projects — source and method (Stages 6–11)

Machinery shared by every project stage. Stage 6 (murals) is the proving run; adding a
stage is one row in `_tools/extract_projects.py` → `STAGES`.

## Where the content comes from

| Piece | Source |
|---|---|
| Project list | `pages` rows whose `pid` is the stage's container, `deleted=0 AND hidden=0`, ordered by `sorting` |
| Title, year | `tt_content.header` of the `text` element — always `"Title, Year"` |
| Description | `tt_content.bodytext` of the same element |
| Gallery order | **`tx_dam_mm_ref.sorting_foreign`** — see the warning below |
| Image captions | `tx_dam.description`; `tx_dam.title` is the project name, `tx_dam.creator` the photographer |
| Image files | **not resolved here** — joined from `_census/site-images.json` on `(page_uid, dam_uid)` |

`tx_dam_mm_ref.uid_local` is the **image** and `uid_foreign` the **content element**, which is
backwards from the column names. Joined the other way the query returns plausible nonsense
rather than an error.

### Gallery order is `tx_dam_mm_ref.sorting_foreign` — corrected 2026-08-27

The first Stage 6 run ordered galleries by `tx_dam.sorting` and **every one came out
scrambled**. The earlier note that `tx_dam_mm_ref.sorting` is zero on every row is true —
all 1745 rows — but the conclusion drawn from it, that `tx_dam.sorting` must therefore be
the gallery order, was never tested. `tx_dam.sorting` is the DAM record's own sorting and
carries no gallery meaning.

`sorting_foreign` is populated on all **1745 rows across 118 galleries**, runs 1..N, and has
**no duplicate inside any gallery**. It reproduces the live order exactly.

**Why it survived the first pass:** every other check passed. The right images appeared, each
with the right caption, in the right count — only the sequence was wrong, and nothing about
the output looks broken when you read it. It was caught only by comparing the *order* against
the live page, which `verify_projects.py` now does as a first-class check for every stage.
`_tools/convert_images.py` had the same defect and was corrected with it; the site's image
files were renumbered.

**The renumbering run was interrupted** (the machine froze) after 635 of 1006 files. It was
resumed with a new `--projects <file>` flag, which restricts which files are *written* to the
`category/project` lines in that file while still building the manifest for every project, so
`site-images.json` stays complete either way.

Correctness was then established independently of any reasoning about where the run stopped:
`jpegtran` is lossless, so **every one of the 1006 targets was decoded and hashed against the
archive source the manifest assigns it — 1006/1006 identical, 0 missing.** A file left holding
its old-order image would have hashed against a different source and failed. Use this check
after any future renumbering; do not rely on file timestamps.

Verification is `maja-explosiv.com`, read-only, never an extraction source.

## Decisions

1. **`title` comes from the content header, not the page title.** Page 918 is titled
   *Felix und Regula*; its heading, and the live page, say *Felix und Regula Unterführung*.
   The page title still drives the **slug**, so the URL and the image directory agree with
   `site-images.json`. Both are recorded as `source_page_title` / `source_header`.
2. **`<br />` is a soft wrap, not a paragraph break.** The descriptions were typed to a fixed
   column: `"...expeditions around <br />Europe, from Austria..."`. A single `<br />` becomes a
   space; a doubled one becomes a paragraph break. Treating every `<br />` as a line break —
   which is what the Stage 5 legal converter does, correctly, for its own source — would
   shatter each description into six one-line paragraphs.
3. **Whitespace inside `<b>` moves outside the marker.** The source writes
   `<b>Zeleny Dvor </b>in`; a literal swap gives `**Zeleny Dvor **in`, which Markdown does not
   close and renders as visible asterisks.
4. **Both `postCollections` and `tags` are emitted.** They drive different things —
   `postCollections` the collection pages, `tags` the featured-projects lookup. The
   pre-migration files set `tags` only. See *Known defects* below.
5. **`date` is the first year of the range**, `year` keeps the range as displayed
   (`year: "1994-1995"`, `date: 1994-01-01`). The pre-migration file used the last year.
6. **Beyond nine images, the layout repeats.** The Figma project page draws nine cards;
   Stage 6 alone has projects with 10, 12 and 18. Owner's decision, 2026-08-27: *"if a
   project has more images, do more of the same."* The row pattern cycles rather than
   stopping. Spec and geometry: `project_docs/PLAN.md` § *Project Page — extracted spec*.
7. **Anomalies are recorded, not guessed past.** A project without exactly one `text` element,
   or with more than one `list`, or with an unexpected CType, lands in `anomalies[]` rather
   than being silently reduced to `[0]`. Stage 6 produced none.

## Stage 6 — murals (container 874) → `paintings`

| page | slug | year | images | live |
|---|---|---|---|---|
| 919 | `wohlgroth` | 1993 | 10 | `2d/murals/wohlgroth` |
| 918 | `felix-und-regula` | 1994 | 18 | `paintings/murals/felix-und-regula` |
| 866 | `murals-europe` | 1994-1995 | 12 | `2d/murals/murals-europe` |

**Verified 3/3 against live**: heading text, description text, and **every image caption**
(10/10, 18/18, 12/12) present in the live HTML.

The `live img refs` figure printed by `verify_projects.py` is lower (8/8/7) and is **not** a
gap: the old site's smoothgallery loads most thumbnails from JSON after page load, so only the
first few appear as inline `<img>`. The caption check is the one that proves coverage.

## Stage 7 — paper work (container 875) → `paintings`

| page | slug | year | images | live |
|---|---|---|---|---|
| 923 | `concept-illustration` | — | 12 | `paintings/paper-work/concepts` |
| 920 | `graphical-work` | — | 18 | `paintings/paper-work/graphics` |
| 921 | `akwa` | 2005 | 7 | `content/2d/paper-work/akwa` |
| 922 | `malaga-la-vache` | 2006 | 15 | `content/2d/paper-work/malaga-la-vache` |
| 982 | *(skipped)* | — | 0 | `content/recent-work/the-whale` |

**Verified 5/5 against live** — heading, description, every caption, and gallery order.

### 982 "Breath under Water" is a shortcut, and is deliberately not migrated here

It sits under paper work but has **zero `tt_content` rows in any state** — not live, not
hidden, not deleted — and carries `pages.shortcut = 924`. The live site renders it by
following that shortcut to page **924 "Breath Under Water"**, which holds the real content
(a 1,399-byte text, a 38-image gallery, and a second text block of video links) and lives
under container **1049**, not 875.

So the work is real and live, but it belongs to whichever stage owns 1049. Emitting a
project here would either publish an empty page or migrate the same content twice. The
extractor now reads `pages.shortcut` and records a `skip_reason`; the converter writes no
Markdown for such a page and reports it; the verifier reports it as *skipped by design*
rather than as a missing capture.

Note for that later stage: page 924 has **multiple live text elements** and a **hidden
39-image gallery** beside its live 38-image one — the "live page, hidden gallery" case.

### Titles: the header is the heading, even when it does not look like one

Page 920's page title is *Graphical Work* but its content header is
`graphics, illustration and sketches`. **The live site displays the header**, verbatim and
lowercase, so that is what `title` carries. The page title still drives the slug, so the URL
and the image directory stay `graphical-work` and agree with `site-images.json`. Both are
recorded as `source_page_title` and `source_header`.

### Two pipeline bugs this stage exposed

**The verifier's live parser mis-read galleries containing an image with no description.**
It matched `<h3>…</h3>\s*<p>(.*?)</p>` as a pair, which silently skips any `imageElement`
lacking a `<p>` and compares everything after it against the wrong position — reporting a
false `ORDER DIFFERS`. `malaga-la-vache` has 15 elements, 2 without a description; the old
parser found 13 and mismatched from position 1. It now splits on `<div class="imageElement">`
and parses each block independently. **Stage 6 passed only because every one of its images
had a description** — re-verified after the fix, still 3/3.

**Sub-containers were invisible to the extractor.** It treated every child of a container as
a leaf project. The old site nests deeper in two places: 877 "sculptural work" splits into
1039 Sculptures / 1040 Installations (known, and handled by the category map), and **inside
1039, page 1068 "Portraits" is itself a container** holding *Alberto* (22 images), *Käthe*
(16) and *Bernhard* (12) while carrying its own intro text and no gallery of its own. Stage 11
would have emitted one project and silently lost three. The extractor now counts child pages
and raises `SUB-CONTAINER: n child page(s) not walked by this stage`. Stage 7 has none.
`convert_images.py` was never affected — it resolves a category by walking ancestors, so
image filing is correct at any depth, and all three portrait directories exist already.

## Stage 8 — event organisation (container 873) → `installations`

| page | slug | year | images | text blocks |
|---|---|---|---|---|
| 934 | `dada-festwochen` | 2003 | 12 | 1 |
| 935 | `eurokon` | 1996 | 26 | **2** |
| 936 | `eurokot` | 1995 | 40 | **2** |

**Verified 3/3 against live** — heading, *every* text block, every caption, and gallery order.

### Category: `installations`, not `TBD`

Owner's decision, 2026-08-27. The stage table and `convert_images.py` both changed, and the
**78 image files moved** from `src/assets/images/projects/TBD/` to `installations/`.

The move was done as a **rename, not a re-encode**: `git mv` on the three directories, then
`convert_images.py --write --projects <empty list>` to rebuild the manifest while writing no
image files. Re-running the pipeline properly would have re-encoded 1006 images for a change
that alters no pixels. Verified afterwards: 1006/1006 manifest targets present on disk, and
all 78 moved files **pixel-identical** to their archive source.

`TBD/` now holds only container 1049 — `breath-under-water` (page 924) and `alchemy-bar`
(page 937), neither of which any stage currently owns. See PLAN.md.

### Multiple text elements are concatenated, not dropped

**This is the decision most likely to need revisiting, so it is spelled out.**

A project can carry more than one live `text` element. Eurokot and Eurokon each carry two,
and the second is not incidental:

| page | 2nd block | content |
|---|---|---|
| 936 Eurokot | uid **1458** | `Invited artists:` — 26 artists with nationalities |
| 935 Eurokon | uid **1459** | `Artists East:` / `Artists West:` — 22 artists |

Both are on the live page, and both are Maja's collaborators by name. The previous extractor
took `text[0]` and would have **silently dropped them**.

Now: **every live `text` element is captured in `sorting` order**, and the body is their
concatenation. The first block's `header` is the project's `"Title, Year"` line and is not
repeated in the body — it is already the page title. A *later* block whose header is
non-empty gets that header rendered as an `##` heading, because on the old site it reads as a
sub-section; page 926 (`Elxt 90`, Stage 9) has `Elxt 90 Videos:` in exactly that shape.
Blocks 1458 and 1459 have empty headers, so they join as further paragraphs.

Traceability: `source_text_uids` in the front matter lists **every** contributing uid
(`"1238,1458"`), `source_text_uid` keeps the first for compatibility, `normalized/stage8.json`
holds each block with its own uid, header, bodytext and sorting, and **every block's raw bytes
are written to `raw/db/tt_content-<uid>.bodytext.html`**.

Stages 6 and 7 were re-extracted and re-converted so all stages carry the new fields.

### The verifier only checked the first block — fixed

`body_ok` compared `bodytext_html` (block 0) against the live page. It would have reported
`body OK` for Eurokot while the 26-artist list was missing from the output. It now checks
**every** block and reports the count (`body OK (2 blk)`). A shadowed local (`blocks`, reused
by the gallery-order check) initially made it print image counts instead — renamed to
`img_blocks`.

### Live URLs need the redirect followed

`url-to-uid.tsv` holds several historical paths per page. `show/event-organisation/eurokot`
returns **301** to `content/show/event-organisation/eurokot.html`, and `fetch.sh` does not
follow redirects, so the first fetch recorded **0 bytes** and every check failed at once.
That is loud rather than silent, but worth knowing: **check `*.headers` for a 301 before
concluding a page is gone.** The `.html` suffixed, `content/`-prefixed form is the one that
serves.

## Stage 9 — performance (container 872) → `performance` — **PARTIAL, 4 of 6**

| page | slug | year | images | text blocks | |
|---|---|---|---|---|---|
| 1056 | `the-sea-monster` | — | 15 | 1 | done |
| 932 | `trojan-fire` | 2004 | 8 | 1 | done |
| 927 | `free-radicals` | 2002-2004 | 16 | 2 | done |
| 928 | `bagger` | 1997-2001 | 50 | 3 | done |
| 933 | `casino-gitano` | 2003-2012 | 39 | — | **HELD** |
| 926 | `elxt-90` | 1999-2003 | 49 | — | **HELD** |

**Verified 6/6 against live** (4 migrated + 2 correctly reported as held).

### Two projects are HELD, not skipped

Owner's decision, 2026-08-27: migrate what can be migrated, hold what needs a decision.
`STAGES[9]['hold']` names each page and the reason. **A held page is still extracted** and
still appears in `normalized/stage9.json` with all its content — only the Markdown is
withheld. Delete the entry to migrate it; nothing else changes.

| page | why held |
|---|---|
| 926 Elxt 90 | 4 text blocks, **2 `list` elements** (the second is `Bio ShortList` with **0 images** — a gallery element with no gallery), **2 live `html` video embeds**, and 6 hidden elements |
| 933 Casino Gitano | a live `Casino Gitano Videos:` text block and **8 hidden elements** — 4 `html` video embeds plus their captions |

### The unresolved question behind both: video

Six pages across the old site carry video content as `CType: html` embeds (926, 928, 933,
946, 1054, 1064). **No stage in the plan handles video, and the Figma project page has no
video component**, so there is nowhere to put it even once extracted. The extractor reports
these as `other-ctypes=html` and does not migrate them.

Note the wrinkle: Bagger's video block is **not** an embed — it is a `text` element in which
Maja explains that she took the videos down under GDPR and links her YouTube channel. That
migrated normally, and is the first real test of the headed-block rule.

### Links, and following the live site

Bagger's note contains the only link in the project content so far, and it exposed two gaps.

**`body_md` had no link handling at all.** It stripped tags, which would have left the label
as unlinked text and lost the target entirely. It now converts both TYPO3's `<link>` syntax
and plain `<a href>` to Markdown links, before any tag stripping.

**The label follows the live site, not the database.** The database stores the label as the
full URL, `http://t1p.de/maja-explosiv`; the old site displays it **without the scheme**,
`t1p.de/maja-explosiv`. The href is byte-identical on both sides — only the visible label
differs, and it differs because of TYPO3's own display convention. Per the owner
(2026-08-27), *the live site is the source of truth for how a link reads*, so where a
label **is** its own bare URL the scheme is dropped. The original label is preserved verbatim
in `raw/db/` and `normalized/`. `verify_projects.py` strips URL schemes from both sides
before comparing — a tolerance narrow enough that it cannot mask a difference in wording.

(The live page actually emits a *nested* `<a>` inside `<a>` here — a TYPO3 link-parsing bug.
Not reproduced.)

### Page 1056's live path is under `installations`, not performance

`url-to-uid.tsv` gives `content/sculptures/sculptural-work/installations/the-sea-monster`,
while the page tree has it under container 872 (performance). realurl records historical
paths, so this is where the page **used to** live. The page tree is authoritative for
category; the stale path still serves and is what was fetched for verification.

## The original stays intact

Nothing is edited in place and nothing is normalised away. Three layers hold the source
exactly as the database has it, and each is verifiable:

| layer | what it holds | check |
|---|---|---|
| `raw/db/tt_content-<uid>.bodytext.html` | the description's **raw bytes**, straight from `bodytext` | byte-identical to the database (139 / 123 / 642 B for uids 1212 / 1213 / 1214) |
| `normalized/stage<N>.json` | every DAM field **unmodified** — `title`, `description`, `creator`, `date_cr`, and the original `file_path + file_name` | 40/40 Stage 6 images match the database with 0 alterations |
| the Markdown front matter | `source_uid`, `source_page_title`, `source_header`, `source_category`, `source_text_uid`, `source_list_uid`, `source_sorting`, and per image `dam_uid` + `original` | every row traceable back to its record |

Derived values are **added beside** the originals, never over them. `title` and `year` are
parsed out of `source_header`, which is itself kept whole; `alt` falls back through
`description` → `title` without overwriting either. Any project can be re-derived from the
database, or audited against it, without re-running the pipeline.

The image files are a fourth layer: `image-archive/` holds the untouched originals and is
never written to. Every file under `src/assets/images/projects/` was verified **pixel-identical**
to its archive source — 1006/1006, 0 missing.

## Known defects — NOT introduced by this stage

Both are pre-existing and block the result from being *seen*, not from being *correct*.

1. **Image captions render empty.** `src/_user/layouts/project.njk` includes
   `project-image-caption.njk` without setting `projectTitle`, `projectYear`,
   `imageDescription` or `imageAuthor`, so the include logs `ERROR: Missing project title for
   image caption` and emits an empty `<div>`. 80 such errors for Stage 6's 40 images. The data
   is present in the front matter; only the hand-off is missing. This is the build noise
   `CLAUDE.md` §7b recorded as "gone" — it was gone only because the content was quarantined.
2. **The four collection pages produce 0-byte files.** `src/collections/{paintings,sculptures,
   installations,performance}.md` carry `title` and `description` but no `layout`,
   `collectionName` or `permalink`, unlike the template's own `blog.md`. So
   `/collections/paintings/` is empty regardless of how many projects exist.

## Reproducing

```bash
python3 migrated-content/_tools/extract_projects.py 6            # DB  -> normalized/stage6.json
python3 migrated-content/_tools/convert_projects.py 6            # dry run
python3 migrated-content/_tools/convert_projects.py 6 --write    # -> src/posts/projects/
python3 migrated-content/_tools/verify_projects.py 6             # against raw/live/
```
