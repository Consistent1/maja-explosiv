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
| 6 | Projects — murals | **done** — 3 projects, 40 images, verified 3/3 against live: heading, description, every caption, **and gallery order** |
| 7 | Projects — paper work | **done** — 4 projects, 52 images, verified 5/5 against live. 1 page skipped: 982 is a shortcut to 924, whose content belongs to container 1049 |
| 8 | Projects — event organisation | **done** — 3 projects, 78 images, verified 3/3 against live. Category changed TBD → `installations` (owner). First stage with multi-block text |
| 9 | Projects — performance | **PARTIAL, 4 of 6** — 89 images, verified 6/6 against live. `casino-gitano` and `elxt-90` HELD pending the video decision |
| 10 | Projects — collaborations | **PARTIAL, 5 of 8** — 46 images, verified 8/8 against live. `wheel-of-power` and `destroy-hiv` HELD on video; `metal-group-xix` HELD on a 12-thumbnail RTE index table that `body_md` corrupted — see SOURCE.md § *Stage 10*, and the three guards added because of it |
| 11 | Projects — sculptural work | **40 of 44** — 491 images, verified 44/44 against live. Three sub-stages (`11a` 1039→sculptures, `11b` 1040→installations, `11c` 1068 Portraits→sculptures). Held: 1064 The Helixes (video), 1050 The Birds + 1068 Portraits (RTE payload). Skipped by design: 949, which renders page 937's content via `content_from_pid` |
| 12 | News | **STRUCK 2026-09-09** — confirmed moot. `tt_news` *is* the timeline; Stage 3 owns all of it. The only other store, pid 1045, is a hidden copy of the Bio sysfolder with nothing unique in it |
| 13–14 | Misc, reconciliation | not started. 13 includes container **1049**, which no stage owns |

## Layout

```
_tools/verify_rendered.py
              Whole-site check: every value the migration writes into front matter must
              appear in the BUILT page, or be listed in its NOT_RENDERED table with a
              reason. Run after a build. Added 2026-09-09, after project captions rendered
              the project title under every image for three weeks while every other check
              passed -- the data was right, the page was not.

_census/      Stage 0. page-tree.json, url-to-uid.tsv, content-inventory.tsv,
              coverage-map.tsv, pages-without-content.tsv, image-census-db.tsv,
              out-of-scope-roots.tsv, quarantine.tsv
_tools/       Extraction and verification scripts. db.sh is the only DB entry point.
links/        Stage 1. SOURCE.md, manifest.json, raw/ → normalized/ → converted/, verification/
projects/     Stages 6-11. SOURCE.md, raw/db + raw/live, normalized/stage<N>.json,
              converted/<category>/<slug>.md. One shared pipeline; a stage is a row
              in _tools/extract_projects.py -> STAGES. Stage keys are STRINGS: stage 11
              is three rows (11a/11b/11c) because container 877 splits into two
              sub-containers with different categories, one of which nests a third.
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
