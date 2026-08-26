# Content Migration Plan — TYPO3 → Eleventy

**Status: APPROVED by the owner, 2026-08-25.** Migration may proceed under the stage order in §8.
**Written:** 2026-08-05. Revised 2026-08-13 (database, encoding, verification scope) and
2026-08-25 (drift measured; placeholder separation).
**Scope:** migrating all content from `maja-explosiv.com` (TYPO3 4.2.14) into this Eleventy site,
content type by content type, with each type verified before the next one starts.

### Owner decisions, 2026-08-05 — these override anything below that disagrees

1. **Content is extracted from local sources only** — the SQL database and the filesystem
   backup. **No content ever comes from the live site.** Not a paragraph, not a caption, not a
   URL. If something needed is absent locally, the remedy is a **fresh backup or dump from the
   owner** — never a fetch from the live site. If I ever think an exception is warranted, I ask
   first and do not proceed without an answer.
2. **The live site is the verification source, and only that.** `maja-explosiv.com` is read to
   check that what we migrated matches what is published. It is never an extraction source.
3. **Ignore all previously migrated content.** The existing project Markdown and the four
   hand-transcribed About pages are not sources, not references, not cross-checks. V10 is
   **dropped**. Nothing in `src/` is consulted for content.
4. **SQL server access provided by the owner.** No local parser, no container, no service
   started here.
5. **Extract projects by the old site's six categories**, map to the new four via an
   owner-reviewed table.
6. **Never assume a capability, in either direction.** Where a task needs a tool, an access
   route, or a permission, **ask** — do not conclude it is impossible and route around it, and
   do not conclude it is permitted and proceed.

### Owner decisions, 2026-08-13 — these override anything below that disagrees

7. **Database access: a local MySQL 8 service on this machine.** Supersedes D1's "owner
   provides an SQL server." Database `usr_p51487_2`, user `maja`, loaded by the owner from
   `old/usr_p51487_2.sql` on 2026-08-13. Verified: 107 tables, matching the dump's 107
   `CREATE TABLE` statements. Queried with `/usr/bin/mysql` (8.0.46, already installed).
8. **Live-site verification is fetched with the in-app browser**, sequentially, at
   **~1 request / 2 seconds, never in parallel.** Settles the §12 question. At that rate the
   ~94-page census is roughly three minutes. The rate exists because the live site is TYPO3 4.2
   on shared hosting: a burst could degrade it for real visitors, or trip host flood protection
   and return errors that would read as missing content and corrupt the census.
9. **Encoding is a connection setting, not a content transformation** (§2.3, rewritten).

### Owner decision, 2026-08-25 — source metadata is preserved

10. **Keep all the original information from the old site, including its categories, in the
    migrated output.** The new site may present a category differently, or group content under
    its own four categories instead of the old six — **that is a presentation choice and it does
    not licence discarding the source's own structure.** Every migrated artefact carries the
    source's categorisation and identifiers alongside whatever the new site needs to render it.

    Concretely: `source_uid` and `source_page` (already in §7) are joined by
    **`source_category`** — the old site's category verbatim — on every project, and by whatever
    equivalent grouping the source carries for other content types. For Links, the source's eight
    `<b>` category headings are content and are preserved verbatim, including trailing colons.

    **Why it matters beyond tidiness:** the source metadata is what makes re-verification
    possible after the fact. Once the old site is gone, a migrated file that dropped its origin
    can never be checked against anything again.

### Owner decision, 2026-08-25 — hidden content is migrated, not dropped

11. **Content the old site marked `hidden` is migrated like any other content, and stored in
    `migrated-hidden-content/` rather than in `src/`.** A README there records each item's origin.

    **Why it is not a front-matter flag.** The obvious alternative — a `published: false` key —
    does not work cleanly in this codebase. Eleventy's two native mechanisms each do half the
    job (`permalink: false` withholds the URL but leaves the page in `collections.all`;
    `eleventyExcludeFromCollections` does the reverse), the three collections in `.eleventy.js`
    are built with raw globs that bypass the latter entirely, and `home.njk` pulls About panels
    with `collections.all | find(...)` — so a page with `permalink: false` would still render
    inside the homepage tab. A directory outside `dir.input` needs none of that machinery and is
    checkable by looking.

    **Scale:** 109 `tt_content` elements are hidden-and-not-deleted, across many pages
    (`Casino Gitano` 9, `Skulpturen` 7, `Destroy HIV` 6, `The Helixes` 6 …). This is not an
    edge case and every stage from 2 onward will produce some.

    Ledger status for these items is **`migrated-hidden`**.

### Owner decision, 2026-08-25 — deleted content is migrated too, in full

12. **Content the old site marked `deleted` is also migrated, into `migrated-deleted-content/`,
    preserving all the information.** This reverses the exclusion argued for one decision
    earlier: TYPO3's delete flag is a recycle bin rather than an archive, so migrating it was
    initially declined as resurrecting discarded work. **The owner's call is to keep it** — and
    the deciding fact is that when the old site is switched off this material vanishes with no
    other copy.

    **"All the information" is taken literally: every column of every record.** 103 `tt_content`
    rows × 89 columns and 99 `pages` rows × 71 columns, verified complete. This is not
    over-engineering — **39 of the 103 deleted elements have no `bodytext`**; `image`, `menu`,
    `list` and `table` elements keep their content in image references, `pi_flexform` XML and
    record pointers. A bodytext-only extraction would have produced empty files and reported
    success. Binary columns are kept base64 with byte count and SHA-256, never lossily decoded.

    **Only 9 of the 202 deleted records are Maja's.** The other 193 belong to unrelated sites
    that shared this database — `karin` (45), `mhk` (43), `wtweb design` (35), `blog` (22),
    `universe1` (23), `pyrofessor` (9) and others. The output is bucketed `maja/` vs
    `other-sites/` so the distinction is visible and the remainder can be dropped without loss.
    This is the same pattern as D8.

    **Deleted content cannot be verified against the live site** — it is by definition
    unpublished, so V0b/V0c/V5 have nothing to compare against. It rests on the database's
    authority alone, which is why the complete record is preserved rather than a rendering.

    Ledger status **`migrated-deleted`**. Two findings already: `Die Weglampen 2015` (uid 1060)
    is a superseded draft of the live `Die Weglampen` (1063), while `sennhof` (uid 1079) holds
    Affenbande text that **appears nowhere on the live site** — genuinely unpublished content
    that the earlier exclusion would have lost.

### Why this split is the right one, not just a constraint

Extracting from the database and verifying against the live site are **independent
derivations**. That independence is the entire value of the verification standard in §6.

Had extraction and verification both come from the live site — which is what the previous
revision of this document proposed, wrongly — then V1–V9 would only ever have tested the
conversion step. An extraction that silently dropped items would have produced a census
missing those same items, and every check would have passed against a denominator that was
already wrong. **A check cannot catch an error in the thing that defined what "correct" means.**

With the split, the live site is an outside witness that never saw the database. If the
extractor drops an entry, the live page still has it, and V2 reports it. That is a real test.

**The corollary is the rule in decision 1, and it matters more than it looks:** the moment a
missing item gets backfilled from the live site, that item becomes unverifiable — it would be
checked against the source it came from. So gaps are escalated and the *source* is repaired.
See §6a.

---

## 1. What this plan is for

Prior migration work in this repo produced **23** projects (not the "~26" every earlier draft
repeated — the count included three `placeholder-*.md` stubs), most without images, plus four
hand-transcribed About pages. It stalled, and the record of *why* is scattered across
a dozen archived docs. The recurring failure was not effort — it was that **extraction was
never separated from verification**. Content was pulled, written straight into `src/`, and
declared done; when something was wrong there was no way to tell whether the extraction, the
conversion, or the template was at fault, and no denominator to say what "done" meant.

This plan fixes that with three rules:

1. **Nothing is migrated in bulk without a census first.** You cannot verify that everything
   arrived if you never established what "everything" was.
2. **Extracted content is isolated and immutable.** It lands in `migrated-content/`, is never
   edited in place, and is *copied* into the site. The site can be rebuilt from it at any time.
3. **One content type at a time, verified to a fixed standard before the next starts.**

---

## 2. Sources, and which one wins

Two roles, strictly separated. Nothing crosses between them.

**Extraction sources — where content comes from:**

| # | Source | What it is |
|---|---|---|
| **E1** | **SQL server** (owner-provided, from `old/usr_p51487_2.sql` — MySQL 5.0 dump, **2025-01-02**) | All text content, page tree, ordering, gallery/DAM wiring, URL↔UID mapping |
| **E2** | **`old/TYPO3BU/_/`** | Filesystem backup — image bytes. `fileadmin/s-maj/` (~1,440), `uploads/` (~253) |

**Verification source — what we check against:**

| # | Source | What it is |
|---|---|---|
| **V1** | **`maja-explosiv.com`** | The live TYPO3 site. Read-only, for comparison. **Never extracted from.** |

The backup is nineteen months older than the live site (generated 2 January 2025). Its currency
cannot be established from inside itself — which is what the live site is for. What the live site
must never do is *supply* the difference; see §6a.

### 2.0 Drift, measured — the central risk is empirically zero *(2026-08-25)*

Every earlier revision called the stale database "the central risk" and sized the whole of §6a
around it. **It has now been measured rather than estimated, and there is no drift.**

The owner produced a fresh dump on 2026-08-25 (`old/usr_p51487_2_2026-08--1.sql`, mysqldump
5.7.44 against the same 5.0.96 server, `SET NAMES utf8`, clean `-- Dump completed` footer). It
was compared against the January 2025 dump field-by-field, not merely by counts:

| table | 2025-01 | 2026-08 | uid sets |
|---|---|---|---|
| `pages` | 278 | 278 | identical |
| `tt_content` | 546 | 546 | identical |
| `tx_dam` | 2727 | 2727 | identical |
| `tt_news` | 164 | 164 | identical |
| `tx_dam_mm_ref` | 1822 | 1822 | identical |
| `tx_realurl_pathcache` | 1218 | 1218 | identical |

**After normalising the two exporters' formatting, the only differences anywhere are:**

- `pi_flexform` and `l18n_diffsource` — phpMyAdmin serialises blobs as `0x613a31…` hex,
  mysqldump as `_binary '…'`, and the two escape `"` differently. Same bytes, different
  serialisation.
- `pages.SYS_LASTCHANGED` on **2 rows of 278** (uid 926 "Elxt 90", uid 974 "links"). That is
  TYPO3's cache-render timestamp, not an edit timestamp: `tstamp` on both rows still reads 2012
  and 2009 respectively, unchanged.

Everything else that moved is cache and log — `cache_hash` +426, `sys_log` +47, the
`tx_realurl_*` caches, `sys_refindex` −14, `sys_history` −10. **No content table moved at all.**

The 38 MB vs 49 MB file-size difference is entirely format: mysqldump omits the per-statement
column list phpMyAdmin repeats across all ~87,000 rows, and the cache tables are smaller. Size
was never evidence of loss, and is not a usable proxy for row count between two exporters.

**Consequences, and they are load-bearing:**

1. **The January 2025 dump was never stale.** Nineteen months of wall-clock produced zero content
   change. The site has not been edited since well before the backup.
2. **V0c, §6a and the source-gap machinery stay in place but should be expected to sit inert.**
   They are guards against a condition now measured to be absent, not a schedule-shaping risk.
   §10's prediction that Links was "the content type most likely to have drifted" is specifically
   falsified: uid 974 *is* the links page, and its content is untouched.
3. **Either dump is authoritative; they are equivalent.** The loaded database derives from the
   January dump and does not need reloading. The August dump is retained as the current-dated
   source of record. Neither is overwritten.

### 2.0a Corrected twice on 2026-08-25 — the real answer

**Both earlier versions of this section were wrong, in opposite directions. This is the
measured result.**

**Attempt 1 said "zero content drift."** That came from comparing the two dumps tuple-by-tuple
and finding differences only in `pi_flexform` and `l18n_diffsource`. **The method was sound; the
sampling was not.** Three rows were inspected and the result generalised to all 546. What the
three rows showed was real — those two columns differ only in serialisation notation
(phpMyAdmin writes blobs as `0x613a…` hex, mysqldump as `_binary '…'`, and they escape `"`
differently) — but three rows do not license a claim about 546.

**Attempt 2 said the live site must be served by a different database**, because the live Links
page showed 52 entries where the loaded database held 66. That inference was also wrong, and for
a duller reason: **the loaded database was built from the January 2025 dump.** The fresh dump
arrived on 2026-08-25 and was never loaded. The comparison was against stale data throughout.

**The correct result**, from comparing both dumps field-by-field with MySQL string escapes
decoded first:

| table | rows | uid sets | genuinely changed |
|---|---|---|---|
| `tt_content` | 546 | identical | **1 row** — uid **1399**, `bodytext`, 10,345 → 8,454 bytes |
| `pages` | 278 | identical | 0 (2 rows differ only in `SYS_LASTCHANGED`, a cache timestamp) |
| `tx_dam` | 2,727 | identical | 0 (`l18n_diffsource` notation only) |
| `tt_news` | 164 | identical | 0 (`l18n_diffsource` notation only) |
| `tx_dam_mm_ref` | — | identical | 0 |

**Exactly one content value changed on the whole site in nineteen months, and it is the Links
page.** That is why press and bio match their January-2025 cached renderings exactly while Links
does not.

`db1010.mydbserver.com/usr_p51487_2` **is** the live database. There is no second database and no
mystery — D9 is withdrawn.

**What this costs and what it teaches:**

- The stale-source risk is genuinely low, but "low" was established by measurement only on the
  second attempt. **The first attempt's error was generalising from a sample without saying it
  was a sample** — the claim was stated as if the whole table had been compared.
- **Comparing two dumps from different exporters requires decoding escapes before comparing.**
  Raw literal comparison reports every row as different and invites exactly the hand-waving that
  produced attempt 1. `l18n_diffsource` in hex notation still defeats a naive unescaper.
- The live-site check did its job. It caught a stale extraction that every one of the eleven
  local checks passed, because the local checks compare the pipeline against its source and the
  source itself was out of date. **A pipeline can be perfectly faithful to the wrong input.**

**Two limits on the original claim, stated so they are not overread:**

- It proves the *database* is unchanged. It says nothing about the D7 pages (918–923, 982) whose
  content is not in `tt_content` at all — if their content lives outside the database, this
  comparison could not see it in either direction.
- **It covers no images.** `old/TYPO3BU/_/` remains the January 2025 filesystem backup and has
  been compared to nothing. Image drift is unmeasured and stays an open risk into Stage 6.

### 2.1 `cache_pages` — present locally, not used for content

The dump contains a table no previous session recorded: `cache_pages`, holding **fully-rendered
page HTML** for 116 distinct `page_id`s. It is a *local* source, so decision 1 does not exclude
it on those grounds — but the owner has said to ignore the old cache, so **it is not used**.

Recorded here because it retires a claim that would otherwise misdirect a later stage:
`typo3-technical-findings.md` concludes that "82% of painting pages use STATIC HTML CONTENT
instead of database-stored content" — inferred from those pages having no `tt_content` rows —
and proposes web-scraping as the remedy. But UIDs **918, 919, 920, 921, 922, 923 and 982** all
have rendered output in `cache_pages`. "The content is not in the database" is therefore not
established, and that doc's web-scraping recommendation should not be acted on — it would also
violate decision 1.

**This becomes a live question at Stages 6–7**, where those exact pages are migrated. If their
content genuinely is not in `tt_content` or any other source table, the options are: find where
it actually lives, get a fresh dump, or reconsider the cache. **That is a decision for the
owner, and I will ask rather than pick.** Flagged as D7.

### 2.2 Other tables worth naming

- `tx_realurl_pathcache` (**1,218 rows**) / `tx_realurl_urlencodecache` — map live URLs ↔ page
  UIDs. This is what lets a live-site census be joined to database records rather than guessed
  at by title.
- `tx_dam` (**2,727 rows**) + `tx_dam_mm_ref` — how galleries actually resolve to image sets.
  **Corrected 2026-08-26:** this entry previously said `startingpointdam` in the FlexForm XML was
  the key. It is not, and it is not used at all — see §2.4.
- `tt_news` (**164 rows**), `tt_address`, `tx_cal_event`, `tx_veguestbook_entries` — small
  tables that may or may not render on the live site. Stage 0 decides; none are assumed dead.

**Counts corrected 2026-08-13, and the correction matters more than the numbers.** Every figure
in earlier drafts was derived by counting patterns in the 49 MB dump *text*. Against the loaded
database they are wrong, some badly: `pages` is **278 rows, not 179**; `tx_dam` 2,727 not 2,688;
`tt_news` 164 rows, not the "4 INSERTs" that was really a count of INSERT *statements*, each
carrying many rows. **No number inherited from a pre-database session is trustworthy** —
including "~71 projects" and "~94 active pages", which Stage 0 now establishes by query rather
than by grep. `cache_pages` at 116 is the one figure that survived.

### 2.3 Character encoding — settled 2026-08-13

**In the dump file**, the text is double-encoded UTF-8: real UTF-8 bytes were read as Latin-1
and re-encoded, so `ä` appears as `c3 83 c2 a4` rather than `c3 a4`, and `Käthe` reads as
`KÃ¤the`. Diagnosed and fixed in an earlier session; see
`_archive/investigations/encoding-fix-summary.md` (2025-10-29).

**Two findings from 2026-08-13 replace that fix rather than confirming it.**

**1. It is uniform across every table we migrate.** A per-table byte scan of the dump, counting
double- against single-encoded sequences for `ä ü ö ß é`:

| table | double | single |
|---|---|---|
| `tt_content` | 829 | **0** |
| `cache_pages` | 972 | **0** |
| `tx_dam` | 336 | **0** |
| `tt_news` | 110 | **0** |
| `pages` | 3 | **0** |
| `sys_log` | 1177 | 253 |
| `static_countries` | 66 | 11 |
| `static_template` | 0 | 18 |

Every content table is uniformly double-encoded, without exception. The single-encoded text is
confined to `sys_log`, `static_countries` (CJK country names) and TYPO3's stock
`static_template` — none of it migrated content. The earlier draft's "treat encoding as a
per-field question, the dump could be mixed" was correct caution while unverified; it is now
measured, and the answer is that it is not mixed.

**2. Loading the dump undoes the double-encoding, so there is nothing left to fix.** The dump
carries its own `SET NAMES utf8` while the tables are `latin1`, so on import the server
transcoded utf8→latin1 and collapsed `c3 83 c2 a4` back to `c3 a4`. Reading `pages.title` for
Käthe out of the loaded database:

```
--default-character-set=latin1   → 4b c3 a4 74 68 65       = "Käthe"   correct UTF-8
--default-character-set=utf8mb4  → 4b c3 83 c2 a4 74 68 65 = "KÃ¤the"  mojibake
```

**The rule, therefore: connect with charset `latin1` and interpret the returned bytes as UTF-8.**
The text is then already correct and no transformation is applied at any point.
`text.encode('latin1').decode('utf-8')` is **not** used against this database — it exists solely
to undo damage a utf8 connection introduces, and applying it to a correctly-read string corrupts
it. Anyone browsing this database by hand (SQLTools included) must set the same charset or they
will see mojibake and misread it as a data problem.

This is a strictly better position than the earlier one: the silent-fallback failure mode that
§6/N2 was written to guard against cannot occur, because there is no fallback and no
transformation. V7 stays as a tripwire — if a mojibake signature ever appears in output, the
connection is misconfigured, and that must fail loudly rather than degrade.

### 2.4 How galleries resolve to image files — settled 2026-08-26

**Use the DAM link table. Do not match by folder, and do not use `startingpointdam`.**

```
tx_dam_mm_ref.uid_foreign -> tt_content.uid   (the gallery element)
tx_dam_mm_ref.uid_local   -> tx_dam.uid       (the image)
tx_dam.file_path + file_name                  (the file in old/TYPO3BU/_/)
tt_content.pid -> pages.uid                   (the project page)
ident = 'rgsmoothgallery'
```

Note the direction: **`uid_local` is the image and `uid_foreign` is the content element**, which
is the opposite of what the column names suggest. Joining it backwards returns plausible-looking
nonsense (1,165 "content elements" and 118 "images") rather than an error.

**~~`startingpointdam` — resolved, and it is vestigial.~~** Earlier notes treated it as the key to
gallery resolution (§2.2 said "path-based, not hierarchical; `startingpointdam` in the FlexForm
XML is the key"). **That is wrong.** Its 32 distinct values are small integers that do not
correspond to `tx_dam_cat` at all — that table has 27 rows and the values run to 50. More
decisively: of 96 live gallery elements, **94 carry both a `startingpointdam` value and explicit
DAM file references**, and the 2 without references have values of `''` and `'0'` — empty
galleries, not galleries depending on the field. **No gallery anywhere resolves through it.** It
is a leftover backend browse-root setting for the file picker.

**Ordering comes from `tx_dam.sorting`.** `tx_dam_mm_ref.sorting` is **zero on every row** and
carries no information. `tx_dam.sorting` has 1,165 distinct values. V4 depends on getting this
right.

**Scale, measured 2026-08-26:**

| | |
|---|---|
| image files in `old/TYPO3BU/_/` | **18,336** |
| referenced by a live gallery | **1,165** (1,132 present on disk) |
| known to `tx_dam` at all | 2,178 |
| on disk but never referenced | **16,299** |
| bytes of the referenced set | **391 MB** |

**89% of the backup is noise** — thumbnails, TYPO3-processed derivatives, and the images of the
other sites that shared this database (§D8). Copying by folder would drag most of it along; the
join yields exactly what the old site displayed.

**Two secondary reference paths, noted so they are not forgotten:**

- **`tt_content.image` → `uploads/pics/`.** Ten live elements use it (9 `image`, 1 `textpic`)
  rather than DAM. Small, but a DAM-only extractor silently drops them — and silence is
  indistinguishable from "this element had no pictures".
- **`tx_dam_mm_ref` also carries other `ident` values** — `tx_damttcontent_files` (63),
  `cfa_mooflow` (8), `and_shadowbox` (6). Only `rgsmoothgallery` has been analysed. Check these
  before declaring the image census complete.

**Basename collisions: 7.** Across 1,165 referenced images there are 1,158 distinct basenames, so
seven names are reused in different folders (`DSC02542.JPG`, `lx-i1.jpg`, `lx-i1-2.jpg`,
`lx-i3.jpg`, `1webHome-2.jpg` …). Too few to constrain the naming scheme, but enough that a flat
target directory keyed on basename would silently overwrite files. Per-project folders make it
moot.

**Image reuse across pages — measured, because it determines the directory structure:**

| images used on | count |
|---|---|
| exactly 1 page | **1,028 (95%)** |
| exactly 2 pages | **54 (5%)** |
| 3 or more pages | **0** |

The 5% is not scattered. It is three recognisable patterns: duplicate/variant pages of one work
(`Breath Under Water` / `Whale`), **event pages reusing photographs of works that have their own
project pages** (`Eurokon` → `Nailed Tanks`, `Torso`, `Eagle`; `Eurokot` → `Iron Channel`), and
test pages. **Per-project folders are therefore the right structure**, with the shared 5%
referenced from two Markdown files rather than duplicated on disk.

**Source gap in the image set:** 30 of 1,522 live gallery links resolve to files absent from the
January 2025 backup — **`Käthe` (16 of 16) and `Bernhard` (12 of 12) have no images at all**,
plus 2 press clippings. Not an encoding problem: the `Käthe_Kollwitz` directory is simply not in
the backup, only its sibling `Alberto_Giacometti`. Per §6a the remedy is a fresh filesystem
backup, never a fetch from the live site. This is the image drift §2.0a flagged as unmeasured.

---

## 3. Ground rules

- **`migrated-content/` is append-only and never hand-edited.** If output is wrong, the
  extractor is fixed and the stage re-run. Hand-patching extracted content destroys the audit
  trail and is the single easiest way to make this whole exercise worthless.
- **Content enters `src/` only by copy.** The migrated artefact stays intact and authoritative.
- **Every stage produces a reconciliation ledger** — one row per source item, carrying its
  source identity, its target identity, and its status. This is what converts "all the content
  migrated" from an assertion into a checkable claim.
- **No hand-migration at scale** (`CLAUDE.md` §3). If a script cannot do it, that is a finding,
  not an invitation to type it out.
- **Figma is irrelevant here.** This is a content migration. Figma governs design; its text is
  placeholder and is never a content source.
- **Differences are reported, not resolved.** Anything needing judgement goes to
  `PLAN.md` § *Open items needing input*, per `CLAUDE.md` §5.
- **Existing content in `src/` is ignored entirely.** Not a source, not a reference, not a
  cross-check. The migrated output is derived from the live site and is expected to *replace*
  what is there. Where an existing file happens to differ, that is not a finding to
  investigate — it is prior work being superseded.
  **Existing content is never consulted as a source, and is physically removed from the content
  directories before Stage 1** — moved, not deleted, to `pre-migration-content/` (§5.1). After
  that point a file's location is its provenance, and the question of confusing the two cannot
  arise.
  The one thing still read from `src/` is **format**: which front-matter keys the templates
  consume. That is a property of the templates, not of the content, and it is confirmed by
  reading the layouts in `src/_user/layouts/`, not by trusting any existing content file.
- **Never assume a capability in either direction.** If a step needs a tool, a network route,
  a credential or a service, **ask.** Do not conclude something is impossible and quietly
  substitute a worse approach; do not conclude something is permitted and proceed. This rule
  exists because this plan's own reconnaissance broke it — a container image was pulled and
  run without asking, when the right move was a one-line question.
- **Never commit. Commits are the owner's, without exception** (owner, 2026-08-05). Work is
  left in the working tree and reported; `git add` and `git commit` are not run. This extends
  the existing no-branches rule in `CLAUDE.md` §5.

---

## 4. Layout of `migrated-content/`

New directory at the repo root. Per content type:

```
migrated-content/
  README.md                    index: every type, its source, its stage status
  _census/                     Stage 0 — the denominator for the whole migration
    live-site-urls.tsv
    page-tree.json
    url-to-uid.tsv
    coverage-map.tsv           every live URL → content type → target artefact
    unassigned.tsv             live URLs not claimed by any type  ← must reach zero
    quarantine.tsv             every file moved at Step 0b → its original src/ path
  _tools/                      extraction + verification scripts (not site code)
  links/
    SOURCE.md                  what this content is, where it came from, how it was pulled
    manifest.json              machine-readable provenance, counts, checksums, timestamps
    raw/                       untouched bytes, one file per source. NEVER edited.
      live/...                 fetched HTML + fetch timestamp + HTTP headers
      db/...                   tt_content rows, cache_pages HTML
    normalized/                encoding-fixed, structured, still source-shaped
    converted/                 exactly the file(s) the new site expects
    verification/
      report.md
      reconciliation.tsv
      diffs/
  press/  timeline/  bio/  impressum/  contact/  news/  misc/
  projects/
    sculptural-work/  collaborations/  performance/
    event-organisation/  murals/  paper-work/
```

`raw/` → `normalized/` → `converted/` is the discipline that makes verification meaningful.
`raw/` proves what the source said. `converted/` is what the site gets. Any dispute is settled
by re-running the middle step, never by editing either end.

**`misc/`** catches content that appears on the live site but belongs to no type — each item in
its own subfolder with a `SOURCE.md` naming the live URL it came from and what it is. Reaching
`unassigned.tsv` = 0 rows is a release condition of the whole migration.

**Project categories are the six the old site actually has**, not the four the new site uses.
Extracting by source category keeps the migration auditable against the source; mapping to the
new four is a conversion step with its own recorded rules (see §9, decision D5).

---

## 5. The per-stage pipeline

Five steps, same for every content type.

**E — Extract.** Query the database; copy image bytes from the filesystem backup. Output into
`raw/db/` and `raw/files/`, with the queries used, row counts, and checksums. **No live-site
access in this step at all.** No interpretation.

**N — Normalize.** Encoding fix, HTML-in-`bodytext` → structured data, whitespace
normalization. Output is still *source*-shaped, not target-shaped.

**C — Convert.** Transform to the exact shape the new site expects (§7). Output into
`converted/`.

**I — Install.** Copy `converted/` into `src/`. Never move; never edit afterwards.

### 5.1 Quarantining the pre-migration content *(owner requirement, revised 2026-08-25)*

**The owner's instruction, verbatim in substance:** it is fine to destroy the current site, but
the existing files must not be deleted — they are **moved out of the content directories** so
migrated and pre-migration content can never be mixed.

This supersedes two earlier attempts at this section. The first deleted everything the migration
did not produce, which would have destroyed work the owner still wanted. The second kept
everything in place and distinguished it with a `provenance:` front-matter key, which preserved
a working site at the cost of leaving both kinds of file side by side in the same directories.
**Physical separation is stronger than either**, and it is what was asked for: the invariant it
creates is checkable by looking at a directory listing, not by trusting a key that any file can
declare.

#### The invariant

> **After Step 0b, `src/pages/` and `src/posts/` contain only content the migration produced.**

Nothing to reconcile, nothing to mistake, no flag to maintain. A file's location *is* its
provenance. **The site will be substantially empty between Step 0b and Stage 14, and the owner
has explicitly accepted that** — the working placeholder site is deliberately given up in
exchange for an unambiguous separation.

#### Where it goes

A new directory at the repo root, **outside Eleventy's input directory** (`.eleventy.js` sets
`dir.input = "src"`), so nothing in it is built, collected or routed:

```
pre-migration-content/
  README.md                          what this is, when it was moved, why, and how to read it
  pages/about/bio.md                 (was src/pages/about/bio.md)
  posts/projects/sculptures/kathe.md (was src/posts/projects/sculptures/kathe.md)
  ...
```

**Paths mirror their origin exactly.** The original location is the only record of where a file
came from, and mirroring it means that record cannot be lost or mis-transcribed. Files are
**moved, never copied** — a copy would recreate the mixing this exists to prevent.

**A second safety net, for free:** everything under `src/pages/` and `src/posts/` is tracked in
git, so the move shows up as deletions plus untracked additions and the original content stays
recoverable from history whatever happens to the new directory. Note that `/old` *is* gitignored,
so neither SQL dump is tracked — the quarantine has a recovery path the dumps do not. Whether
`pre-migration-content/` and `migrated-content/` get tracked is the owner's call at commit time
(D3).

#### Three classes of file, handled differently

The 38 Markdown files under `src/pages/` and `src/posts/` are not one population:

| Class | Count | What it is | Disposition |
|---|---|---|---|
| **Maja content** | 30 | The earlier hand-migration: 23 real projects, bio, links, press, timeline, about, contact, impressum | **Quarantined.** This is what the migration replaces |
| **Category placeholder stubs** | 4 | `placeholder-{news,installation,performance,sculpture}.md` — stubs keeping empty categories from breaking | **Quarantined**, and expected not to return: the migration populates those categories for real |
| **Upstream template demo posts** | 4 | `welcome-to-explosive-website.md`, `getting-started-with-11ty.md`, `css-grid-layout-guide.md`, `image-carousel-demo.md` | **Owner's decision, flagged not assumed** — see below |

**The four demo posts are not a migration question.** They come from the `explosive` template, not
from TYPO3, and no stage of this plan produces or replaces them. They can be quarantined with
everything else, deleted as template scaffolding, or kept. That is a template decision, and the
plan does not make it unasked. Until it is made they are quarantined with the rest, because the
invariant above admits no exceptions and a reversible move is the safe default.

**A correction that falls out of this inventory:** `PLAN.md` and §1 of this plan both say "26 of
~71 projects" were converted. The real figure is **23** — the count included three
`placeholder-*.md` stubs. One more inherited number that does not survive being checked (§2.2).

#### What replaces the deletion step

Install no longer deletes anything, because there is nothing left in `src/` to delete. Each stage
simply writes its output into directories the quarantine emptied. Files that were quarantined are
recorded once, in `pre-migration-content/README.md` and in `_census/quarantine.tsv`, with their
original path — not per-stage in each ledger, since the move happens once at Step 0b rather than
progressively.

The ledger status `superseded` accordingly means **"a quarantined file this stage's output
replaces"**, recorded for traceability. It no longer implies a deletion.

#### Release condition

The migration is complete when `unassigned.tsv` contains zero rows (§4) **and** every row in
`quarantine.tsv` is accounted for — either superseded by migrated output, or recorded as an
owner decision not to migrate it. A quarantined file that is neither is an unanswered question,
not a finished migration.

#### Images

`src/assets/images/` is **not** covered by the move as specified, and this is a real loose end.
Some of it is site chrome the templates need; some is placeholder content assets — for instance
the six press clippings `PLAN.md` records as copied in "as placeholders only", unoptimised. The
two cannot be separated without going file by file. **Flagged as an open item**, to be settled
before Stage 2 (Press), which is the first stage that writes images. Content Markdown is
quarantined at Step 0b regardless; images are a separable question and not a reason to delay it.

**V — Verify.** §6, in full. A stage is not done until its report says so.

---

## 6. The verification standard

Every stage passes all of these, or it does not pass. Results go in
`migrated-content/<type>/verification/report.md`.

### How much of this each stage actually runs *(added 2026-08-13)*

The full apparatus — ten checks plus `SOURCE.md`, `manifest.json`, checksums, a reconciliation
ledger, a diffs directory and screenshots — run fourteen times costs more than the migration it
is protecting. Stage 5 is a handful of legal pages; it does not need the machinery that 46
sculpture entries need. Scaling it down is not a weakening of the standard, it is putting the
standard where the risk is.

**Full suite** — Stage 1 (Links), because it is the pipeline's proof; Stage 6 (murals), the
first stage with galleries, images and DAM; Stage 11 (sculptural work), the largest by far.

**Reduced suite** everywhere else: V0, V1a, V2, V5, V7, V9, V11. Dropped there are V3 field-by-field
percentages, V4 order fidelity where order carries no meaning, V6 asset integrity where a stage
has no assets, and V8 screenshots. **V5, V9 and V11 are never dropped** at any stage — rendered-output
verification, the ledger, and provenance integrity are what make the claim "everything arrived"
checkable at all.

Any stage running reduced says so in its report, and names what it skipped. A reduction is a
recorded decision, never a silent omission.

**Every check below compares against the live site.** Not the dump, not the filesystem backup,
not `cache_pages`, not existing content in `src/`. The database is the *subject* of the test,
never the standard it is tested against.

### V0 — Two censuses, and the gap between them

**V0a — Source census.** Every item the extraction found in the database. The extraction
denominator. Recorded in `manifest.json` with counts and the queries that produced them.

**V0b — Truth census.** Every item on the corresponding **live page**. The verification
denominator, recorded with fetch timestamp and a checksum over the fetched HTML, so it can be
re-derived later and shown to be the same census.

**V0c — The gap.** `V0b − V0a` is a first-class output, written to
`verification/source-gap.tsv`. It is the answer to "is the January 2025 backup still an
adequate source for this content type?" — and it is the check that no previous attempt in this
project had at all. A non-empty gap **halts the stage** and goes to the owner (§6a).

### V1 — Count parity *(revised 2026-08-13)*

Two claims, not one, because they fail for different reasons and only one of them is a bug.

**V1a — pipeline identity, and it is strict.**
`source items == normalized items == converted items == rendered items`. Four numbers, one
value. The pipeline is required to be lossless; any mismatch is a defect in our own code and
**fails the stage**.

**V1b — source-vs-truth delta, reported not enforced.**
`truth census − source census` is computed and recorded, and it *is* V0c. It is a measurement of
how far the dump has drifted from the live site, handled under §6a.

**Why this was split.** The earlier version demanded all five numbers be a single value, the
truth census among them. But V0c exists precisely to surface the gap between database and live
site, and §10 predicts a non-empty one for Links — so V1 as written failed by construction on
the very first stage, and the plan predicted its own halt. A check that a known, expected,
separately-reported condition must not occur is not a check. V1a tests the thing we control;
V1b measures the thing we do not.

### V2 — Item-level bijection
Set difference computed **in both directions** on a stable per-item key. Zero source items
missing from the target; zero target items absent from the source. Count parity alone does not
catch a dropped item paired with an invented one — this does.

### V3 — Field fidelity
Per item, per field, normalized-text comparison against the source. Reported as an exact-match
percentage with every non-match itemised. Normalization is limited to whitespace collapse and
Unicode NFC; anything more aggressive would hide real differences.

### V4 — Order fidelity
The site's sequence matches the source's sequence. Both project galleries (featured image =
first by `tx_dam.sorting`) and the timeline depend on order being right, and order is invisible
to counts and to field comparison.

### V5 — Rendered-output verification
**Build the site, parse the generated HTML, re-extract the same structure, and compare against
the live-site census again.** V1–V4 test the Markdown; V5 tests what a visitor sees. A field
present in front matter but never rendered by the template passes V1–V4 and fails here — and
that class of bug is invisible to every check that stops at the file. This is the check that
closes the loop *live page → migrated page*, and it is the one that most directly answers
"did everything on the old site make it to the new one".

### V6 — Link and asset integrity
Every `href` well-formed and byte-identical to the source (no silent `http`→`https`, no
trailing-slash normalization). Every referenced image exists on disk at the referenced path,
is non-zero, and decodes as an image. Internal links resolve to real routes.

### V7 — Encoding
Zero occurrences of mojibake signatures (`Ã`, `Â`, `â€`, `Ã¤`, `ï»¿`) in converted output or
rendered HTML. Positive test too: known-good strings — `Käthe`, `Zürich`, `Luginbühl`, `Lärz`,
`Köln`, `Hervé`, `Pfäffikon` — appear correctly.

### V8 — Live-site visual comparison
Render both the migrated page and the live page, compare by eye, screenshots into
`verification/`. `CLAUDE.md` §7 records a real bug that passed every computed-style check and
was only visible on screen. Machine checks do not replace looking.

### V9 — Reconciliation ledger
`verification/reconciliation.tsv`, one row per source item:

```
source_id  source_url  source_excerpt  target_file  target_key  status  note
```

`status` ∈ `migrated` / `omitted-by-decision` / `missing` / `differs` / `missing-from-source` /
`superseded` (a placeholder file replaced by this stage and deleted — see §5.1).
**`missing` or `missing-from-source` in any row fails the stage.** `omitted-by-decision`
requires a recorded owner decision — it is not a category an agent may assign on its own
judgement. `missing-from-source` means the live site has it and the backup does not: a source
problem, not a migration problem, and handled by §6a.

### V11 — Provenance integrity *(added 2026-08-25, revised same day)*

Enforces the §5.1 invariant: **`src/pages/` and `src/posts/` contain only content the migration
produced.** Run over `src/` after Install:

1. **Every content file in `src/` has a matching artefact in
   `migrated-content/<type>/converted/`.** A file with none did not come from the migration, and
   is either a quarantine step that was missed or something written by hand. Either way it fails
   the stage.
2. **The move was a move, not a copy** — nothing sits in `pre-migration-content/` and in `src/`
   at the same path.

This is the only check in §6 that looks at files **the migration did not write**, which is
precisely the blind spot §5.1 exists to close. A directory listing settles it; there is no
front-matter key to trust. Never dropped, at any stage.

It fails only on content that is *extra*. An empty category is not a failure — emptiness is the
expected state between Step 0b and the stage that fills it.
---

## 6a. When the backup is missing something the live site has

**Revised 2026-08-25: this was written expecting it to happen routinely. It should not.** §2.0
measured the database against a fresh dump and found zero content drift across nineteen months,
so this section is now a guard against an absent condition rather than a routine path. It is kept
in full — the measurement covers the database, not images (Stage 6 onward) and not the D7 pages —
but a `missing-from-source` result should now be treated as *surprising* and investigated as a
possible extraction bug before it is accepted as genuine drift. The rule:

1. **Do not backfill from the live site.** Ever. An item copied from the live site can never be
   verified — it would be checked against the source it came from, which is not a check.
   Doing this once would silently convert a real gap into a passing stage, and the gap would
   never be found again.
2. **Record it** in `verification/source-gap.tsv` and as `missing-from-source` in the ledger,
   with the live URL and enough excerpt to identify it.
3. **Report to the owner, and do not proceed past the affected items.** *(Revised 2026-08-13:
   this said "halt the stage".)* With a fresh dump in hand a gap should be rare and a halt is the
   right response. Against a stale source, drift is the expected condition rather than the
   exceptional one, and halting on it stops the migration permanently instead of surfacing a
   decision. So: the gap is recorded, the items carrying it are held, **the rest of the stage
   may complete**, and the stage is reported as *passed with a recorded gap* — never as clean.
   What must not happen is a gap being absorbed silently, which is what §6a exists to prevent.
4. **The owner refreshes the backup or dump**, then the stage re-runs from the start.

If a gap turns out to be small and the owner decides it is not worth a fresh dump, they may
mark those items `omitted-by-decision` — **that is their call and it must be recorded as
theirs.** It is not a status an agent may assign to make a stage pass.

### V10 — *(dropped)*
The earlier draft proposed diffing migrated output against the four hand-transcribed About
pages as a free error signal. **Removed on the owner's instruction to ignore previously
migrated content** — and it is the better call regardless: a transcription of unverified
accuracy can anchor you to its own mistakes, and the live site settles every question it
could have raised.

---

## 7. Target formats

**These are the *shapes the templates consume*, not content.** Each is confirmed by reading the
layout that renders it (`src/_user/layouts/about-page.njk`, `post.njk`, and the includes they
pull in) — the template is the authority on format. Existing content files are not consulted,
and every one of them is expected to be overwritten.

**Links** — `src/pages/about/links.md`, front matter `linkCategories: [{heading, entries: [{text?, name, url, suffix?}]}]`.
`name` is the anchor text, `url` its href, `text` an optional prefix before the link, `suffix`
optional trailing prose. Layout `about-page.njk`, permalink `/about/links/`.

**Press** — `pressEntries: [{title, image?}]` plus `pressNote`. Images under
`/assets/images/shared/press/`.

**Timeline** — `timelineSections: [{heading, entries: [{year, title, description}]}]`.
Three fields per entry, **year only, no month** — Figma's left column shows no month. The live
site's prose has the title embedded and uses month precision, so this is a genuine reshaping
step, not a copy. Specified in `PLAN.md` § *Timeline data format required by the migration*.

**Bio** — paragraph 1 in `excerpt` (rendered as the About intro beside the portrait),
remaining paragraphs in the Markdown body. Deliberate, confirmed by the owner 2026-07-28.

**Projects** — `src/posts/projects/<new-category>/<slug>.md`:

```yaml
title, date, year, category, tags[], layout: post.njk
featuredImage, featuredImageAlt
images: [{src, alt, title?, year?}]
source_uid, source_page          # provenance — keep, it is what makes re-verification possible
```

Images to `/assets/images/projects/<category>/<slug>/` per `asset-organization-strategy.md`.

**Why wholesale replacement is the right call**, in one example:
`src/posts/projects/installations/hinwil.md` opens with three paragraphs about the Affenbande
monkey sculptures before its actual Hinwil text — two projects concatenated into one file by an
earlier run, sitting in the repo undetected. Existing content is not a baseline worth
preserving, and V2/V3 exist precisely to catch this class of error.

---

## 8. Stage order

Stage 0 is mandatory and blocks everything. Then, by increasing complexity:

| Stage | Type | Items (est.) | Introduces |
|---|---|---|---|
| **0** | **Census** | — | The denominator. No migration. |
| **0b** | **Quarantine pre-migration content** | 38 files | Move `src/pages/` + `src/posts/` Markdown to `pre-migration-content/`, mirroring paths. Nothing deleted. Site goes substantially empty — accepted by the owner (§5.1) |
| **1** | **Links** ← *runs first, per instruction* | ~50 in 8 categories | The whole pipeline, on text-only structured data |
| 2 | Press | ~60 entries, 49 clipping files | Assets, at small scale |
| 3 | Timeline | ~85 entries | Reshaping prose into 3 fields |
| 4 | Bio + About intro | 4 paragraphs | Body-vs-excerpt split |
| 5 | Impressum / Datenschutz / Contact | few | Legal text — verbatim, no cleanup |
| 6 | Projects — murals | 3 | First project category. Galleries, DAM |
| 7 | Projects — paper work | 5 | Includes UID 982 |
| 8 | Projects — event organisation | 3 | |
| 9 | Projects — performance | 6 | |
| 10 | Projects — collaborations | 8 | |
| 11 | Projects — sculptural work | ~46 | Largest; deliberately last |
| 12 | News | TBD Stage 0 | Only if it renders live |
| 13 | Misc | TBD Stage 0 | Whatever Stage 0 could not classify |
| 14 | Global reconciliation | — | `unassigned.tsv` = 0; all ledgers pass |

Projects run smallest-first so the gallery/DAM machinery is proven on 3 items before it is
trusted with 46.

### Stage 0 — Census (detail)

Stage 0 builds **both** censuses and diffs them, at whole-site level, before any content type
is migrated. Its real purpose is to answer one question up front: **how much has the site
changed since January 2025?** That number determines whether this migration can run on the
existing backup at all, and it is far better known now than discovered at Stage 11.

**Source census (database):**

1. Extract the page tree from `pages` (179 rows, ~94 active). Output `page-tree.json`.
2. Resolve each page's public URL via the `tx_realurl` tables. Output `url-to-uid.tsv`.
3. Inventory content per page: `tt_content` rows, plus `tt_news`, `tt_address`, `tx_cal_event`,
   `tx_veguestbook_entries`. Flag pages with **no** content rows — the Stage 6/7 question (D7).
4. Build the image census from `tx_dam` + FlexForm `startingpointdam`, reconciled against the
   filesystem backup. Three-way: configured / on disk / referenced.

**Truth census (live site):**

5. **Enumerate every reachable page on the live site.** Nav tree plus a crawl. The site is
   frameset-based, so a naive crawler misses routes — frame `src` attributes are followed as
   links. Output `live-site-urls.tsv`.

**The diff, which is the actual output:**

6. `coverage-map.tsv` — every live URL → its UID → content type → planned target artefact.
7. `unassigned.tsv` — live URLs claimed by no content type. **Must reach zero** before the
   migration is called complete.
8. `source-gap.tsv` — **live pages with no counterpart in the backup.** The headline number.
9. `removed-since-backup.tsv` — active UIDs with no live URL. Not an error: content deleted
   since January 2025, which we should *not* migrate. Owner confirms before anything is dropped.

Stage 0 is reviewed with the owner before Stage 1 converts anything, and will likely change the
stage table above — that is its job. **If step 8 comes back large, the right move is a fresh
dump before migrating anything**, not migrating around the holes.

---

## 9. Decisions

**Settled 2026-08-05:**

- ~~**D1 — database access.**~~ **Resolved 2026-08-13: a local MySQL 8 service**, database
  `usr_p51487_2`, user `maja`, loaded by the owner from the dump. Verified at 107 tables.
  Queried with the already-installed `/usr/bin/mysql`; nothing was installed and no container
  was used. Connections must set charset `latin1` (§2.3).
- ~~**D2 — live site.**~~ **Up, and it is the sole verification source.**
- ~~**D4 — existing hand-transcribed content.**~~ **Ignored entirely and replaced.** V10 dropped.
- ~~**D5 — project categories.**~~ **Extract by the old six, map to the new four via an
  owner-reviewed table.** Confirmed. The mapping table is produced before Stage 6 writes any
  project file.

- ~~**D3 — commit `migrated-content/`?**~~ **Moot — I never commit** (owner, 2026-08-05).
  Whether it is tracked or gitignored is the owner's call at commit time. I will propose a
  `.gitignore` line for `raw/` image bytes and leave the decision alone.

**Still open:**

**D6 — scope.** In or out: news feed, guestbook, calendar events, address records,
`datenschutz`. Stage 0 reports what exists in the database and what renders live; you decide
what ships. Not needed until Stage 5.

~~**D7 — pages with no `tt_content`.**~~ **RESOLVED 2026-08-25 by direct query, and its premise
was false.** UIDs 918–923 each have **2 live `tt_content` rows**; their content was in the
database all along. UID 982 has none because it is a **shortcut page pointing at uid 924**
("Breath Under Water"), which itself has 4 live rows. Nothing is missing, nothing needs locating,
no fresh dump was required, and `cache_pages` is not needed.

This also definitively retires `typo3-technical-findings.md`'s claim that "82% of painting pages
use STATIC HTML CONTENT instead of database-stored content" and its web-scraping recommendation.
§2.1 could only say the claim was *not established*; it is now **disproved**.

**A different set of pages does have no content**, found by Stage 0: 27 active `doktype=1` pages,
of which 20 are grid-layout scaffolding (`2-4`, `3-1`, `4-2` … under "1 struktur - menues") and
the rest are section containers (`info`, `content`, `Archiv`, `Installations`, `Sculptures`).
None is a content page. Listed in `_census/pages-without-content.tsv`.

~~**D9 — which database backs the live site today?**~~ **WITHDRAWN 2026-08-25, same day.**
Raised on the belief that the live site was served by an unknown database. It is not:
`db1010.mydbserver.com/usr_p51487_2` is the live database, and the fresh dump contains the live
Links content. The apparent divergence was mine — Stage 1 queried a database loaded from the
**January 2025** dump, because the fresh dump was never loaded after it arrived. See §2.0a.

**D8 — the database contains a second, unrelated website.** *(New, 2026-08-25.)* Root `uid=733`
**"pyrofessor"** carries 50 active pages — a fire-show business, with its own Start, Kontakt,
Impressum, Datenschutz, Sitemap and galleries. Maja's site is the separate `uid=860` subtree.
Stage 0 scopes everything to uid 860 and records the others in
`_census/out-of-scope-roots.tsv` (`pyrofessor` 50, `Media` 1, `templates ext` 1). **Confirm this
scoping is right** — migrating the whole database would pull in an unrelated site. Needed before
Stage 2.

**Two things I will ask for when Stage 1 starts**, flagged now rather than assumed (§3):

- **How to reach the SQL server** — host/port/credentials, or whatever route you prefer.
- **How to fetch the live site for verification.** I have an in-app browser and can also fetch
  over plain HTTP, but I am not picking one and starting to hit your site. Tell me which, and
  any rate you want me to stay under. Stage 1 is a handful of requests; the project stages are
  ~70 pages.

---

## 10. Stage 1 — Links, in full

What runs first, on your go-ahead.

What runs first, on your go-ahead. **Text only, zero assets, ~50 items** — the cheapest place
to prove the whole pipeline before it is trusted with 46 projects and 1,400 images.

**Extraction source: the database.** The links content is in `tt_content` — confirmed during
reconnaissance: the `bimbotown.de` href appears at line 76523 of the dump inside a `tt_content`
INSERT. One or more content elements on the Links page; Stage 0 identifies the UID.

**Verification source: the live Links page**, expected at `maja-explosiv.com/info/links.html`,
confirmed by Stage 0 rather than assumed.

**E** — Query `tt_content` for the Links page's content element(s). Store the raw `bodytext`,
the query, and row checksums in `links/raw/db/`. **No live fetch in this step.**

**N** — Fix encoding, verified positively against `Hervé Thiot`, `Köln`, `Lärz`, `Fer à Coudre`.
Parse the `bodytext` HTML into an ordered list of
`(category_heading, prefix_text, anchor_text, href, suffix_text)`. Output `normalized/links.json`.

**C** — Emit `converted/links.md`: the `linkCategories` shape of §7. The non-content front
matter (`title`, `layout`, `permalink`, `description`, `excerpt`, `linksHeading`) is template
configuration, taken from the layout's requirements — reported as *not* migrated content, so
nothing is silently carried over from the file being replaced.

**I** — Copy to `src/pages/about/links.md`, overwriting.

**V** — V0–V9:
- **V0a** source census from the database; **V0b** truth census by fetching the live page;
  **V0c** the gap. A non-empty gap halts the stage and comes to you (§6a).
- V1: five counts agree — source, normalized, converted, rendered, live.
- V2: bijection against the live page keyed on normalized `href`, both directions.
- V3: `anchor_text`, `prefix`, `suffix` compared per entry against the live page.
- V4: category order, and entry order within each category, match the live page.
- **V5: build, parse rendered `/about/links/`, re-extract every `(heading, text, href)`, compare
  to the truth census.**
- V6: every href byte-identical to the database value, and matching the live page. No rewriting
  of any kind. Format-validate each URL.
- V7: mojibake scan; the four accented strings above render correctly.
- V8: migrated page and live page side by side, screenshots kept.
- V9: ledger, ~50 rows, zero `missing`, zero `missing-from-source`.

**Then I stop**, per your instruction, and report before anything else is touched.

**Expected friction, so it is not a surprise:** the Links page is the content type most likely
to have drifted since January 2025 — outbound link lists get edited. If the live page has
entries the database does not, that is V0c doing its job, and the answer is a fresh dump, not
a copy-paste from the live page.

**Note on URL rot:** several links date to the 1990s–2000s and some hosts are certainly dead.
**Reachability is explicitly not a migration criterion** — a dead link that is on the live site
gets migrated exactly as it is. I will report which are unreachable as information only, and
will not "fix" a single URL without you asking.

---

## 11. Risks

| Risk | Handling |
|---|---|
| ~~**Database is stale — the central risk**~~ | **Closed 2026-08-25 by measurement** (§2.0). A fresh dump was compared field-by-field against the January 2025 one: zero content drift, nineteen months apart. V0c and §6a remain as guards, expected inert. **Not closed for images** — see the row below |
| **Image drift is unmeasured** | `old/TYPO3BU/_/` is still the January 2025 filesystem backup and has been compared to nothing. The database measurement says nothing about it. Live from Stage 6, where galleries first matter |
| **Temptation to backfill a gap from the live site** | Forbidden (§6a). It would make the item unverifiable and turn a real gap into a silent pass. `missing-from-source` fails the stage; only the owner can downgrade it |
| Live site goes down mid-migration | It is the only verification source, so a stage cannot be verified without it. Migration **pauses** and I say so — no declaring a stage verified against the backup |
| Live site changes during the migration | Every truth census records fetch timestamp + checksum, so it is re-derivable and datable |
| Frameset hides routes from the crawler | Stage 0 follows frame `src` as links. `unassigned.tsv` = 0 is a release condition, so an unreached page surfaces as a gap rather than passing silently |
| ~~Encoding edge cases~~ | **Closed 2026-08-13** (§2.3). Uniform double-encoding across all content tables, undone by the import; connect as `latin1` and apply no transformation. V7 remains as a tripwire for a misconfigured connection, and fails loudly |
| Content genuinely absent from `tt_content` (pages 918–923, 982) | D7 — the owner decides between locating it elsewhere, a fresh dump, or the cache. Not an agent's call |
| Category misassignment | Owner-reviewed mapping table, not a keyword heuristic (the heuristic is how a whale sculpture was filed under paintings) |
| Images migrated that the old site never displayed | DAM/FlexForm decides what was configured to display; the live page confirms it |
| Scope creep into design work | This plan touches content only. Template defects get logged to `PLAN.md`, not fixed here |
| Assuming a capability instead of asking | §3 ground rule. It has already happened once in this project |

---

## 12. Status of what was needed from the owner

1. ~~**Approve or amend this revision.**~~ **Approved 2026-08-25.**
2. ~~**SQL server access.**~~ Provided 2026-08-13; see decision 7.
3. ~~**How you want the live site fetched for verification.**~~ Settled 2026-08-13: in-app
   browser, sequential, ~1 request / 2 seconds; see decision 8.
4. ~~**A fresh dump.**~~ Provided 2026-08-25 and compared: zero content drift (§2.0).

Nothing outstanding. D6 waits until Stage 5, D7 until Stage 6.

**Next: Stage 0 (census), Stage 0b (quarantine), then Stage 1 (Links) — then stop and
report**, per the owner's instruction that Links runs alone with nothing migrated after it. I
commit nothing; everything is left in the working tree.
