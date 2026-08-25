# Links — source record

**Content type:** Links · **Stage:** 1 · **Extracted:** 2026-08-25

## Where this came from

| | |
|---|---|
| **Source** | Local MySQL database `usr_p51487_2`, table `tt_content` |
| **Page** | `pages.uid = 974`, title `links`, realurl path `info/links` |
| **Elements** | `tt_content.uid = 1399` (published) and `1400` (hidden) |
| **Connection** | charset `latin1`, bytes read as UTF-8 — see plan §2.3. No transformation applied |
| **Live site** | **Not touched.** Extraction is database-only (decision 1) |

Raw bytes in `raw/db/`, with SHA-256 per element in `manifest.json`.

## What was migrated

`tt_content.uid = 1399`, header `FRIENDS AND RELATED ARTISTS:`, 10,340 bytes of TYPO3 RTE
markup — **8 categories, 66 entries**. The header renders (`header_layout` is default), so it
is content and becomes `linksHeading`.

Every entry is `[prefix] <link href …>anchor</link> [suffix]` on one line, under a
`<b>CATEGORY:</b>` heading. Parsed to `(heading, prefix, anchor, href, suffix)`; hrefs carried
through byte-identically, 64 `http` and 2 `https`, none rewritten.

## What was NOT migrated, and why

**`tt_content.uid = 1400`** — header `ON MY OWN BEHALF:`, one entry (Casino Gitano on MySpace).
**`hidden = 1` in TYPO3, so it is unpublished and does not appear on the live site.** Excluded on
that objective ground, not on judgement. Its raw bytes are extracted and kept in `raw/db/`, and
it is recorded in the ledger as `not-migrated`.

**This is flagged for the owner**: if it should appear on the new site, that is a content
decision, and reinstating it is a one-line change.

## Template configuration (not content)

`title`, `layout`, `permalink` are the layout's requirements, taken from
`src/_user/layouts/about-page.njk` and `src/_user/includes/about-content.njk`. **Nothing was
carried over from the file being replaced**, which is quarantined at
`pre-migration-content/pages/about/links.md` and was not read.

## Notes for whoever runs this next

- **Two entry shapes exist and the difference is load-bearing.** 61 suffixes start with `,` and
  5 start with a space (`</link> /GB`). The template appends `suffix` directly after `</a>`, so
  stripping that leading space renders `Giles Walker/GB`. An early version of the normaliser did
  exactly that; `clean_suffix()` exists to prevent it.
- **Trailing colons in headings are source content**, kept verbatim. An early version stripped
  them — that is tidying, not migrating.
- **URL rot is not a migration criterion.** Reachability was not tested and no URL was "fixed".
