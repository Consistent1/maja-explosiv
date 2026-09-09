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

## Stage 10 — collaborations (container 878) → `sculptures` — **PARTIAL, 5 of 8**

| page | slug | title | year | images | text blocks | |
|---|---|---|---|---|---|---|
| 1058 | `gong-trophy` | The Gong Trophies | — | 8 | 1 | done |
| 1031 | `elephant` | Elephants Head | — | 10 | 1 | done |
| 994 | `throne` | The Throne | — | 6 | 1 | done |
| 945 | `hand-of-man` | Hand of Man | 2007 | 12 | 1 | done |
| 947 | `forget-me-not` | Forget Me Not | 2003 | 10 | 1 | done |
| 1078 | `metal-group-xix` | Metal group XIX, since 1995 | — | **0 DAM + 12 RTE** | 2 | **HELD** |
| 1054 | `destroy-hiv` | Destroy HIV | — | 8 | — | **HELD** |
| 946 | `wheel-of-power` | Derevo, Wheel of Power | 2007 | 40 | — | **HELD** |

**Verified 8/8 against live** (5 migrated + 3 correctly reported as held) — heading, every text
block, every caption, and gallery order. 46 image references, all present on disk; no image
file was written, because `convert_images.py` walks ancestors and had already filed them.

### The two HELD pages are the same video question, in the same shape

`STAGES[10]['hold']` names each. Both carry a **live** text block of video links plus **hidden**
`html` embeds:

| page | live video block | hidden |
|---|---|---|
| 946 Wheel of Power | uid **1446** `Wheel of Power videos:` (318 B) | 2 `html` embeds (1448, 1468) + 2 captions (1447, 1467) |
| 1054 Destroy HIV | uid **1572** `Videos` (287 B) | 6 `html` embeds (1566–1571), captioned `Zerstöre HIV - Tag 1`–`6` |

This is Casino Gitano's shape exactly. The hidden embeds were never at risk — the extractor
walks live rows only. What is withheld is the **live** headed block, which the headed-block rule
would otherwise render as an `##` sub-section of bare video links with no component behind them.

Note that both pages migrate *cleanly* apart from that block — Wheel of Power is the largest
gallery in the stage at 40 images. One line out of `STAGES[10]['hold']` releases each.

### 1078 Metal Group XIX — migrated CORRUPTED, then held. Read this one.

**This page was reported as "no gallery, and that is correct". It was not correct**, and the
way it passed is the most useful thing in this file.

Its DAM `list` element (uid 1655) really is `hidden = 1`, so there is no smoothgallery. But its
second `text` element (uid **1654**, 2156 B) is a **4-column HTML table of 12 thumbnail images,
each wrapped in an internal `<link>` to another project** — Bächtel, Affenbande, Weglampen,
Lionfish Door, ELXT 90, Bagger, Dorfbachschiff, 17 Ton Bar, Iron Eagle, Torso, Nailed Tanks,
Iron Channel. A hand-built index of the group's work, sitting in RTE markup.

`body_md` strips tags. `<link 1077 - internal-link "…">` wrapping an `<img>` has **no text
label**, so `_link` fell through to `return … href` and emitted the *target page uid* as bare
text. The published page ended with:

```
107710731063105792692894210041005100610071008
```

— twelve uids run together, and the twelve images and twelve links gone.

**Three independent checks all passed on it**, which is why this is worth spelling out:

| check | what it looks at | why it missed |
|---|---|---|
| extractor `imgs=` | `tx_dam_mm_ref` | RTE images are not DAM records → `imgs=0` |
| verifier captions/order | `<div class="imageElement">` | RTE images are not in that markup → `0/0`, `order OK` |
| verifier `body_ok` | block text ∈ live text | the block strips to **nothing**, and an empty needle is trivially a substring → `body OK (2 blk)` |

Every check agreed, and every check was asking the wrong question. Caught only by the owner
looking at the live page.

**Three guards were added, at three different layers, and each was regression-tested by
lifting the hold and confirming it fires:**

1. **`extract_projects.py` — `RTE-PAYLOAD` anomaly.** Counts `<img>`, `<table>` and
   text-less `<link>`/`<a>` in each block's *decoded* bodytext. Source-side and exact.
   (First cut read `c[3]` straight from the query and silently found nothing — that column is
   base64. It needs `b(c[3])`.)
2. **`convert_projects.py` — `body_md` now raises** rather than degrading: an empty link label
   is a `ValueError`, and so is any `<img>`/`<table>` in bodytext. There is no correct silent
   answer, so it refuses.
3. **`verify_projects.py` — two new live-side checks.** Any `<img>` that is not page chrome and
   carries neither `class="full"` nor `class="thumbnail"` is embedded content and fails the
   page; and a text block that strips to no text is now a failure rather than a skip.
   Tested across all 23 captured live pages: **12 hits on 1078, zero elsewhere** — the gallery
   `<img>`s are all class-tagged, so there are no false positives.

**Scope of the damage: one page.** Re-running the `RTE-PAYLOAD` check over Stages 6–10 finds
1078 and nothing else. The corrupted Markdown was deleted and the page is now in
`STAGES[10]['hold']`.

**Ahead in Stage 11, the same shape, larger:** live text blocks with embedded thumbnail tables
on **1039 Sculptures (25 img, 24 links)**, **1040 Installations (21 img, 21 links)**,
**1050 The Birds (11 img, 5 tables)** and **1068 Portraits (2 img)**. The category *container*
pages (860–878) carry them too. None of these can go through `body_md` as it stands — they will
now fail loudly instead of corrupting.

**What it should become is undecided and is the owner's call** — an index of internal links has
no Figma component. Logged in PLAN.md.

### The header carries a year the parser cannot use, and is left alone

(This one is about 1078 too, and still stands — it is a separate issue from the table above.)

Page 1078's header is `Metal group XIX, since 1995`. `_HDR` matches `Title, YYYY`; *"since 1995"*
does not match, so `year` stays null and the **whole string becomes the title** — which is what
the live page prints as its heading, verbatim. Correct by decision 1, and deliberately not
"fixed": widening the regex to swallow `since` would start guessing at prose. It is one more
row for the project-years open item, not a parser bug.

### Four of the eight live under `sculptural-work/`, not `collaborations/`

`url-to-uid.tsv` gives 994, 1031, 1054 and 1058 paths under
`content/sculptures/sculptural-work/…` while the page tree has all eight under container 878.
Same realurl-history effect as page 1056 in Stage 9: **the page tree is authoritative for
category**, the stale paths still serve, and those are the URLs fetched for verification. All
eight returned `HTTP/2 200` on first request — no 301 chase needed this time.

### `gong-trophy` reports `captions 7/7` on 8 images — not a gap

`cap_total` counts only images that *have* a DAM description; one of the eight has none. Coverage
is proven by the order check instead, which compares full sequences: 8 live `imageElement`s
against 8 of ours, identical. Same situation as `malaga-la-vache` in Stage 7.

## Stage 11 — sculptural work (container 877) — **40 of 44**

877 carries no projects of its own. It splits into two sub-containers that map to **different
categories**, and one of those nests a third. A stage is one container and one category
everywhere else in this pipeline, so **11 is three rows, not one** — and stage keys became
strings to allow it (`extract_projects.py 11a`). Existing `stage6.json`…`stage10.json`
filenames are unchanged.

| sub-stage | container | category | pages | migrated | held / skipped |
|---|---|---|---|---|---|
| `11a` | 1039 Sculptures | `sculptures` | 25 | **23**, 272 images | 1068 Portraits, 1050 The Birds |
| `11b` | 1040 Installations | `installations` | 16 | **14**, 169 images | 1064 The Helixes, 949 The Alchemy Bar |
| `11c` | 1068 Portraits | `sculptures` | 3 | **3**, 50 images | — |

**Verified 44/44 against live** — heading, every text block, every caption *including both
credit fields*, and gallery order. 491 images, every one resolving 1:1 from
`site-images.json`; no image file was written.

### Held: video, and RTE payload — the two classes already known

| page | class | why |
|---|---|---|
| 1064 The Helixes | video | live `Videos` text block (uid 1616) + 6 hidden `html` embeds. Same shape as Destroy HIV |
| 1050 The Birds | RTE payload | text uid 1557 is a **multi-work page**: 11 RTE images in 5 tables, each a photo pair captioned under a bold work title. Not one project, and not a DAM gallery |
| 1068 Portraits | RTE payload + sub-container | its own intro text carries 2 RTE images and no gallery, *and* it is the container for 11c |

Note 1050 is a different animal from `metal-group-xix`: no links, no index — it is several
distinct sculptures sharing one page. Whatever is decided for one may not fit the other.

### 949 The Alchemy Bar — `content_from_pid`, a THIRD structural mechanism

Not held: **skipped by design**, and it exposed a gap that had been open since Stage 6.

`pages.content_from_pid = 937` means page 949 **renders page 937's content instead of its
own**. Its own description and gallery are `hidden = 1` and its only live element is the GDPR
video note, so to the extractor it looked like a near-empty page — while the live site serves a
full **36-image project**, page 937's, which lives under container **1049**, a container no
stage owns.

Caught only because the live capture came back **29 kB against ~18 kB for its siblings**. Nothing
in the pipeline read the column.

Site-wide, five live pages set `content_from_pid`: 733 (other site), 1041 and 1042 (the
`recent work` mirrors of 1040/1039), **982 Breath under Water**, and **949**. 982 also sets
`shortcut`, which is why Stage 7 caught it; **949 sets only this column, and nothing saw it.**
The extractor now reads it and skips such a page with the source page named — checked *before*
the empty test, because such a page can carry live elements of its own and so never looks empty.

### The DAM record was being read for five fields out of a dozen — **fixed across all stages**

Found as `copyright`, then widened on the owner's instruction (2026-09-09): *information that
doesn't render live and exists only as metadata should also be migrated.* **Rendering is not the
test.** The first pass here judged `caption` and `publisher` unnecessary because the old site
does not print them, and recorded that as a deliberate decision. That was the wrong call and it
is corrected below.

`copyright` was the way in: the live caption is `description | creator | copyright`, page **995
Soldier** renders `Berlin 2008 | Maja Thommen | Erico Moreira`, and reading `creator` alone lost
the co-credit. Auditing the rest of `tx_dam` then showed the loss was much wider, and **spread
across every project stage, not just this one**:

| field | images on migrated projects | note |
|---|---|---|
| `loc_country` | **170** | ISO-3166 alpha-3. Unset is the literal string `'0'`, not `''` |
| `loc_city` | **147** | |
| `dam_categories` | **71** | resolved join `tx_dam_mm_cat` → `tx_dam_cat`: *2D*, *poster*, *concept illustration*, *current work*, *1.Mai* |
| `caption` | 16 | a venue — `Spannwerk`, on Free Radicals' 16 images |
| `loc_desc` | 16 | `Rodellar`, `les Prés d'Orvin`, `Tacheles Freifläche` |
| `copyright` | 7 | |

**15 projects across Stages 6–11 were affected** — akwa, bagger, concept-illustration,
dada-festwochen, dorfbachschiff, felix-und-regula, forget-me-not, free-radicals, graphical-work,
malaga-la-vache, murals-europe, soldier, trojan-fire, vulture, wohlgroth. All stages were
re-extracted and re-converted; **427 values now in `src/`**.

Deliberately not taken, and why: `alt_text`, `abstract`, `language`, `pages`, `instructions`,
`file_creator`, `file_orig_loc_desc`, `meta` and `ident` are **empty on all 2312 records**;
`date_mod` is a bookkeeping timestamp; and **`tx_dam.category` is a *count* of assigned
categories, not a category** — reading it would put `0`, `1` or `2` in the front matter. The
real categories are the `tx_dam_mm_cat` join.

Two traps in the data itself, both of which produced wrong output before being caught:

- **`loc_country` stores `'0'` for unset.** Untreated, 619 images acquire a country of `"0"`.
- **`q()` renders SQL `NULL` as the string `'NULL'`** — the same trap `b()` already guards. The
  categories subquery returns `NULL` for an uncategorised image, so every one of them briefly
  acquired a category called `NULL`. Caught on the first run.

Field names in the front matter are the **DAM column names verbatim**, so a value is always
traceable to its source. `author` is the single rename and predates this; it carries the joined
`creator | copyright` form the live site prints, with `copyright` emitted separately beside it so
the field is never available only in joined form. `dam_categories` is a resolved join and so has
a name of its own.

**The other stages were checked for the same class of gap and have none.** Stages 1–5 read
`tt_content`, and `subheader`, `image`, `imagecaption`, `header_link`, `altText`, `titleText`,
`longdescURL`, `records` and `pi_flexform` are all empty on every element they use. Stage 3
reads `tt_news` and already captures **all 33 columns** per entry in `all_fields`.

### The order check was comparing the wrong thing, and passed two pages it should not have

`ORDER DIFFERS at 1` on `flower-power` was the first Stage 11 failure, and it was the *check*
that was wrong. Three faults, all in one line — `live_cmp = [x.split('|')[0].strip() …]`:

1. **A description containing `||` was truncated.** `flower-power`'s captions read
   `Close Up Bouquet Nr. 1 || Berlin, October 2019`. Splitting on the first `|` cut the live
   side down to `Close Up Bouquet Nr. 1` and failed a page that was correct.
2. **Comparing descriptions alone made the check vacuous where there are none.**
   `hafenszene` has **7 images and not one description** — both sequences were `['', '', …]`
   and `order OK` proved nothing. Its `<h3>` titles are distinct, so including the title makes
   the check real. Same empty-needle shape as the body check that let page 1078 through.
3. **It hid the missing `copyright`**, and a second convention: where the description is empty
   but a credit exists, the old site still prints the separator — bagger's image 32 renders as
   `| Kati Bitzer`. "Tidying" that leading `|` away fails a correct page.

The check now reconstructs the live `<p>` exactly — `description`, then each credit field that
is set, joined by `" | "` — and compares `(title, caption)` tuples. A page whose live captions
are *all* blank now reports **`ORDER UNVERIFIABLE (no captions at all)`** rather than `order OK`.

All eight stages were re-extracted, re-converted and re-verified under it: **8/8 stages,
73 pages, all match live.**

### Sub-containers: `1068 Portraits` resolved as `11c`

The `SUB-CONTAINER` anomaly added at Stage 7 fired exactly as intended. Its three children —
Alberto (22 images), Käthe (16), Bernhard (12) — are ordinary projects and migrate cleanly as
`11c` into `sculptures`, agreeing with where `convert_images.py` had already filed their files.
**What the Portraits page itself becomes is still open** and is why 1068 is held: a page of its
own, a grouping in the listing, or nothing.

## "A column named like content that holds a number" — audited 2026-09-09

The same mistake turned up twice in one day: **`tx_dam.category`** and **`tt_news.category`** are
both `int`, and both hold a *count of assigned categories* (1, 2 or 3), not a category. Read as
content they yield `0`/`1`/`2` and look meaningful. The real categories are join tables —
`tx_dam_mm_cat` → `tx_dam_cat`, and `tt_news_cat_mm` → `tt_news_cat`.

**It never reached the output**, and that was checked rather than assumed:

- **Every column the tools read as text is genuinely a text type.** The 14 columns passed through
  `B()` — `bodytext, caption, copyright, creator, description, file_name, file_path, header,
  keywords, loc_city, loc_country, loc_desc, publisher, title` — are all `text`/`varchar`/
  `tinytext`/`char`. Neither `category` column is read at all.
- **No migrated file carries a count in a content slot.** Sweeping all of `src/posts/` and
  `src/pages/`, every bare-number value is either a real `year` or a deliberate `source_*_uid`,
  and there are **no digit-run bodies** — the `107710731063…` signature from page 1078 is gone.
- The two occurrences were caught before emitting: `tx_dam.category` while widening the DAM
  metadata capture, `tt_news.category` in a *documentation* sentence about Stage 12 that no code
  depended on. Both are corrected in place.

**The inverse was checked at the same time** — content-bearing columns that nobody reads — and is
also clean. On the 69 live pages and 147 live `text`/`list` elements the project stages migrate:
`pages.keywords`, `description`, `abstract`, `author`, `subtitle`, `nav_title`, `media` and
`tt_content.subheader`, `header_link`, `imagecaption`, `image`, `altText`, `titleText` are **empty
on every row**. The only populated one is `tt_content.spaceBefore` (71 elements), a layout value
in pixels, correctly ignored.

**Columns to be careful with if you extend any extractor** — numeric, but named as though they
carry content:

| table | column | what it really is |
|---|---|---|
| `tx_dam` | `category` | count of assigned categories |
| `tx_dam` | `media_type`, `file_status`, `file_usage`, `fe_group` | enums / flags |
| `tt_news` | `category` | count of assigned categories |
| `tt_news` | `type` | enum |
| `tt_content` | `layout`, `sectionIndex`, `section_frame` | display flags |
| `pages` | `doktype`, `urltype`, `shortcut_mode`, `layout`, `fe_login_mode` | enums — but `doktype` and `shortcut_mode` matter structurally, see `content_from_pid` above |

The rule that catches all of it: **check the column's SQL type before treating a value as text**,
and where a name suggests a taxonomy, look for the `_mm_` join table before believing the column.

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

Pre-existing; they block the result from being *seen*, not from being *correct*.

1. ~~**Image captions render empty.**~~ **Fixed** — verified 2026-09-09 at Stage 10.
   `src/_user/layouts/project.njk` now sets `projectTitle`, `projectYear`,
   `imageDescription` and `imageAuthor` at all four include sites, and rendered pages carry
   full captions (`The Gong Trophies / Berlin, March 2015 / Uri Moss`). What remains of that
   build noise is **69 × `ERROR: Missing project year`**, which is the project-years open item
   — most headers carry no year — and not a hand-off defect.
2. ~~**The four collection pages produce 0-byte files.**~~ **Fixed** — verified 2026-09-09 at
   Stage 10. `/collections/sculptures/` builds to 27.8 kB and lists all six of this stage's
   projects; the other three build likewise.

## Reproducing

```bash
python3 migrated-content/_tools/extract_projects.py 6            # DB  -> normalized/stage6.json
python3 migrated-content/_tools/convert_projects.py 6            # dry run
python3 migrated-content/_tools/convert_projects.py 6 --write    # -> src/posts/projects/
python3 migrated-content/_tools/verify_projects.py 6             # against raw/live/
```


The live pages `verify_projects.py` reads must be fetched first, one per project, through the
rate-limited fetcher — **never in parallel** (CLAUDE.md §7a):

```bash
bash migrated-content/_tools/fetch.sh \
  https://www.maja-explosiv.com/content/sculptures/collaborations/hand-of-man.html \
  migrated-content/projects/raw/live/hand-of-man.html
```

The path comes from `_census/url-to-uid.tsv` and is **not** derivable from the page tree — four
of Stage 10's eight live under `sculptural-work/`, not `collaborations/`. Check `*.headers` for
a 301 before concluding a page is gone.

The database must be running and must be the current dump — `SELECT LENGTH(bodytext) FROM
tt_content WHERE uid=1399;` must return **8441**. It is a system service and needs
`sudo systemctl start mysql`, which an agent shell cannot do; ask the owner.
