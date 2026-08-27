# migrated-content/

Isolated, reproducible output of the TYPO3 → Eleventy content migration
(`project_docs/content-migration-plan.md`, approved 2026-08-25).

**Never hand-edited.** If output is wrong the extractor is fixed and the stage re-run. Content
enters `src/` only by copy; the artefact here stays authoritative.

## Start here

Stages 1–5 are done. For everything that remains, read **`HANDOFF — the rest of the migration`**
at the end of `project_docs/content-migration-plan.md` — reading list, per-stage brief, pitfalls.

## Status

| Stage | Type | Status |
|---|---|---|
| 0 | Census | **done** — source side. Whole-site live census still to run |
| 0b | Quarantine | **done** — 38 files moved to `pre-migration-content/` |
| 1 | Links | **PASSED 19/19** (11 local + 8 live). V8 visual comparison outstanding |
| 2 | Press | **passed with a recorded gap** — 50 entries, 48 assets; 2 files missing from backup (umlaut paths) |
| 3 | Timeline | **done** — 85 entries, 2 sections, order and text match live; 4 records excluded (unreferenced) |
| 4 | Bio | **done** — 4 paragraphs, character-identical to live |
| 5 | Contact + Datenschutz | **done** — 133 of 133 live paragraphs present. No separate Impressum exists; it is on the contact page |
| 6–14 | Projects, News, Misc | not started. **Stage 12 (News) is likely moot** — `tt_news` turned out to be the timeline, not a news feed |

## Layout

```
_census/      Stage 0. page-tree.json, url-to-uid.tsv, content-inventory.tsv,
              coverage-map.tsv, pages-without-content.tsv, image-census-db.tsv,
              out-of-scope-roots.tsv, quarantine.tsv
_tools/       Extraction and verification scripts. db.sh is the only DB entry point.
links/        Stage 1. SOURCE.md, manifest.json, raw/ → normalized/ → converted/, verification/
```

## The one thing to know before running anything

`_tools/db.sh` connects with **charset `latin1`** and that is not optional. The dump's
double-encoding was undone when it was imported, so the stored bytes are already correct UTF-8.
Connecting as utf8 re-introduces mojibake; applying the old
`encode('latin1').decode('utf-8')` fix to a correctly-read string corrupts it. Plan §2.3.

**The database must be loaded from the *current* dump.** It is currently loaded from
`old/usr_p51487_2_2026-08--1.sql` (2026-08-25). Stage 1 initially ran against the January 2025
dump and produced content that passed every local check while being 16 entries out of date. If
you are unsure which is loaded: `SELECT LENGTH(bodytext) FROM tt_content WHERE uid=1399;` returns
**8441** for the current dump, 10340 for the January one.

`db.sh` also fails loudly on SQL errors — it filters only the password warning from stderr. An
earlier version suppressed all of stderr and silently returned nothing for a broken query.
