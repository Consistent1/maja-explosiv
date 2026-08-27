# Onboarding — next session

**Written:** 2026-08-05. **Substantially revised 2026-08-25** — the plan is now approved and
several of the cautions below were resolved by measurement.
**Read after `CLAUDE.md`, before anything else.**

---

## 1. Where things stand, in three sentences

The content-migration plan at **`project_docs/content-migration-plan.md`** was **approved by the
owner on 2026-08-25** and governs all migration work; `PLAN.md` Phase 3 now redirects to it.
Nothing has been migrated yet — no migration code exists and `migrated-content/` does not exist.
The next actions are Stage 0 (census), Stage 0b (quarantine), then Stage 1 (Links), and then a
full stop to report.

## 1a. What changed on 2026-08-25, and what it retires

Four things were settled, each of which retires a caution that earlier drafts treated as live:

- **The plan is approved.** The instruction "do not start implementing, the plan is under review"
  no longer applies to the migration. `CLAUDE.md` §5's standing rule still does — approval of the
  plan is not a standing licence, and each stage still stops and reports.
- **The database is loaded and verified.** Local MySQL 8, database `usr_p51487_2`, user `maja`,
  107 tables. Queried with `/usr/bin/mysql`, which was already installed. **The service is
  `start`ed, not `enable`d, so it does not survive a reboot** — expect to ask the owner to
  restart it rather than assuming the data is gone.
- **Content drift is one row.** Comparing the fresh dump (`old/usr_p51487_2_2026-08--1.sql`)
  against the January 2025 one — decoding MySQL escapes first, or every row looks different —
  **exactly one content value changed in nineteen months: `tt_content.uid=1399.bodytext`, the
  Links page.** Everything else is identical. An earlier claim of *zero* drift was generalised
  from three sampled rows and was wrong; see plan §2.0a. Image drift remains unmeasured.
- **Make sure the database is loaded from the CURRENT dump.**
  `SELECT LENGTH(bodytext) FROM tt_content WHERE uid=1399;` → **8441** is current, 10340 is the
  January dump. Stage 1 first ran against the stale one and passed all eleven local checks while
  being wrong, because local checks verify the pipeline, not the source.
- **Encoding is solved and is not a content transformation.** Connect with charset `latin1` and
  read the bytes as UTF-8; the text is already correct. Do **not** apply
  `encode('latin1').decode('utf-8')` against the loaded database — it corrupts correctly-read
  text. §2.3 of the plan has the evidence.

## 2. What you must not do

Read `CLAUDE.md` §5 first — its working agreements are still in force. On top of them, three
rules established or reinforced this session:

1. ~~**Do not start implementing — the plan is under review.**~~ **Approved 2026-08-25.**
   `CLAUDE.md` §5 still stands: approval is not a standing licence, each stage stops and reports,
   and anything outside the plan's scope still needs a fresh go-ahead.
2. **Install nothing. Ask for tools and access.** The owner's words: *"NEVER assume that you
   can or cannot do anything and seek alternatives. ALWAYS ask me for assistance/guidance when
   it comes to tool-use, access, and the like."* This session broke that rule — a 332 MB
   MariaDB image was pulled and a container run, unprompted, to test whether the dump would
   load. The owner halted the session twice. The image has been removed. The right move was one
   question; the owner had *already offered* to provide a database.
3. **Never commit.** New, 2026-08-05: *"all commits are my department."* Leave work in the
   working tree and report it. This extends the existing no-branches rule.

## 3. The one thing most likely to be got wrong

**Content is extracted from local sources. The live site is only ever used to verify.**

| | |
|---|---|
| **Extract from** | The SQL database (owner provides a server, loaded from `old/usr_p51487_2.sql`) and the filesystem backup `old/TYPO3BU/_/` |
| **Verify against** | `maja-explosiv.com`, read-only |
| **Never** | Take content from the live site. Not a paragraph, not a caption, not a URL |

The owner was emphatic: *"NO CONTENT SHOULD COME FROM THE OLD SITE DIRECTLY!"* If the backup is
missing something the live site has, **the owner refreshes the dump** — you do not crawl for it.

**Still fully in force**, and note that the 2026-08-25 drift measurement does not weaken it:
knowing the database matches a fresh dump says nothing about whether the *live site* matches
either, which is exactly what verification is for.

This is not arbitrary. The two sources must stay independent or verification is circular: if
extraction and verification both came from the live site, the checks would only test the
conversion step, and an extraction that silently dropped items would produce a census missing
those same items and pass every check. One backfill from the live site makes that item
permanently unverifiable. §6a of the plan is the handling procedure.

**Also: ignore all previously migrated content in `src/`.** Not a source, not a reference, not a
cross-check — it will be overwritten. The only thing read from `src/` is *format*, and that
comes from the layouts in `src/_user/layouts/`, not from content files.

## 4. What was actually decided this session

Settled, and recorded in the plan's decisions block:

- Extraction sources: local DB + filesystem backup. Verification: live site only.
- The owner provides SQL server access.
- Ignore previously migrated content; the check that would have diffed against the four
  hand-transcribed About pages (V10) is **dropped**.
- Projects are extracted by the **old site's six categories** (sculptural work, collaborations,
  performance, event organisation, murals, paper work), then mapped to the new four via a table
  **the owner reviews**. Not by keyword heuristic — that heuristic is how "Breath under Water",
  a whale sculpture, got filed under paintings.
- Dead outbound links migrate exactly as they are. Reachability is reported as information;
  no URL is ever "fixed" without the owner asking.

Still open: **D6** (is news / guestbook / calendar / address / datenschutz in scope — needed at
Stage 5) and **D7** (UIDs 918–923 and 982 have no `tt_content` rows; needed at Stage 6). The
fresh-dump option in D7 is now **closed** — a fresh dump exists and those pages still have no
`tt_content`, so the remaining choices are locating the content elsewhere or reconsidering
`cache_pages`.

Two open items were added to `PLAN.md` on 2026-08-25: **which images move with the quarantine**
(needed before Stage 2) and **what happens to the four upstream template demo posts**.

## 5. Findings worth not rediscovering

- **`cache_pages` exists.** The dump contains a table with **fully-rendered page HTML for 116
  `page_id`s** — no prior session recorded it. **It is not used** (the owner said to ignore the
  old cache), but it retires a claim that would otherwise misdirect Stage 6:
  `typo3-technical-findings.md` asserts that "82% of painting pages use STATIC HTML CONTENT
  instead of database-stored content" and recommends web-scraping. UIDs 918–923 and 982 all have
  rendered output in `cache_pages`, so that inference is not established — **and acting on the
  web-scraping recommendation would now violate the no-live-content rule.** Do not build on it.

- **`src/posts/projects/installations/hinwil.md` is corrupt** — it opens with three paragraphs
  about the Affenbande monkey sculptures before its actual Hinwil text. Two projects
  concatenated by an earlier run. Cited in the plan as evidence that existing migrated content
  is not a baseline worth preserving.

- ~~**The dump has real double-encoded UTF-8, and the fix must be tested per field.**~~
  **Superseded 2026-08-25.** It is double-encoded *in the file*, uniformly across every content
  table (measured: `tt_content` 829/0, `tx_dam` 336/0, `pages` 3/0, double vs single). But loading
  the dump **undoes** it — the server transcodes utf8→latin1 on import and collapses
  `c3 83 c2 a4` back to `c3 a4`. **Connect with charset `latin1`, read the bytes as UTF-8, apply
  no transformation.** Applying the old fix to a correctly-read string corrupts it. Positive test
  strings remain useful: `Käthe`, `Zürich`, `Luginbühl`, `Lärz`, `Köln`, `Hervé`, `Pfäffikon`,
  `Fer à Coudre`.

- **Links content is confirmed present in `tt_content`** — the `bimbotown.de` href appears at
  line 76523 of the dump inside a `tt_content` INSERT. Stage 1 does not need to hunt for it.

- **`tx_realurl_pathcache` / `tx_realurl_urlencodecache`** map live URLs ↔ page UIDs. This is
  what joins the live-site census to database records without guessing by title.

- **The old site is frameset-based**, so a naive crawler will miss routes. Frame `src`
  attributes have to be followed as links when building the live-site census.

## 6. What to do first

**Stages 1–5 are complete.** Stages **6–14** remain, and the full brief for all of them —
project context, the two-repo boundary, reading list, per-stage detail, pitfalls and tips — is
the **`HANDOFF — the rest of the migration`** section at the end of
`project_docs/content-migration-plan.md`. **Read that after this file; it supersedes the step
list below.**

The steps below are the original Stage 0/1 sequence, kept for reference:

1. Read `CLAUDE.md`, then this file, then `project_docs/content-migration-plan.md` in full.
2. **Check the database is up** — `mysql -u maja -pmaja usr_p51487_2 -e "SELECT COUNT(*) FROM
   tt_content;"` should return 546. A socket error just means the service is stopped; **ask the
   owner to start it**, do not start services yourself.
3. **Stage 0 — census.** Both censuses and the diff, per §8 of the plan. Live-site fetching is
   via the in-app browser, sequential, ~1 request / 2 seconds, never parallel.
4. **Stage 0b — quarantine.** Move all 38 Markdown files under `src/pages/` and `src/posts/` to
   `pre-migration-content/`, mirroring their paths. Moved, never copied, never deleted (§5.1).
   The site goes substantially empty at this point; the owner has accepted that.
5. **Stage 1 — Links**, then **stop and report.** The owner asked for Links only, explicitly,
   with nothing else migrated after it.

## 7. Repo state

At the end of the 2026-08-25 session — **nothing committed, everything in the working tree.**

Modified: `project_docs/content-migration-plan.md` (approved; drift, encoding, quarantine,
verification scope), `project_docs/PLAN.md` (Phase 3 redirected, two open items added), and this
file. Added: `old/usr_p51487_2_2026-08--1.sql`, the fresh dump.

`migrated-content/` and `pre-migration-content/` **do not exist yet** — Stage 0 and Stage 0b
create them. No migration code has been written.
