# Migrated hidden content

**This is migrated content that the old site did not publish. It is not built and has no URL.**

The directory sits outside Eleventy's input directory (`.eleventy.js` sets `dir.input = "src"`),
so nothing here is collected, routed or rendered — the same mechanism that keeps
`pre-migration-content/` inert. No front-matter flag is involved and none is needed.

## What this is, and why it exists separately

TYPO3 marks a record `hidden = 1` when it exists in the backend but is not shown on the site.
Maja used this: **109 content elements across the site are hidden but not deleted.** They are
real, authored content — often earlier versions, seasonal material, or entries retired when a
link died — that she chose to take down rather than delete.

Earlier, the migration simply dropped them. On the owner's instruction (2026-08-25) they are
**migrated like any other content and stored here**, so nothing authored is lost, and so the
decision to publish or not stays the owner's rather than being made silently by an extractor.

## Hidden is not the same as deleted

| TYPO3 state | rows | what it means | what the migration does |
|---|---|---|---|
| `hidden = 1`, `deleted = 0` | 109 | Authored, taken down, still in the backend | **Migrated, stored here** |
| `deleted = 1` | 103 | Sent to TYPO3's recycle bin | **Not migrated** — see below |
| live | 334 | Published | Migrated into `src/` |

**Deleted content is deliberately excluded**, and that has not been asked for. TYPO3's `deleted`
flag is a recycle bin, not an archive; treating it as content would resurrect things that were
thrown away. If it should be migrated too, that is a separate decision.

## Layout

Paths mirror where the content would live in `src/` if it were published:

```
migrated-hidden-content/
  README.md
  pages/about/links.md      would be src/pages/about/links.md
```

Every file carries its origin in front matter, so no file depends on this README to be
identifiable:

```yaml
source_uid:   "1400"        tt_content.uid in the old database
source_page:  "974"         pages.uid it belonged to
source_path:  "info/links"  its realurl path on the old site
source_state: "hidden"      TYPO3 tt_content.hidden = 1
```

## What is here now

| File | Origin on the old site | Content | Why it was hidden |
|---|---|---|---|
| `pages/about/links.md` | `tt_content.uid = 1400` on `pages.uid = 974`, live path `https://www.maja-explosiv.com/info/links.html` | Heading **"ON MY OWN BEHALF:"** with one entry — *Casino Gitano*, `http://www.myspace.com/casinogitano`, suffix "on myspace" | Not recorded in the database. **Almost certainly because the URL died** — MySpace destroyed most pre-2016 content. The element sorts *above* the published one (`sorting` 128 vs 256), so it was once the first block on the Links page |

Verified absent from the live page: neither `casinogitano` nor `ON MY OWN BEHALF` appears in the
fetched HTML, so hiding it did take it off the site.

Note *Casino Gitano* is also one of Maja's own projects (`pages.uid = 933`,
`content/show/performance/casino-gitano`), migrating at Stage 9 — so the subject survives
regardless. Only this outbound link to it is unpublished.

## Publishing something from here

Move the file to the mirrored path under `src/` and rebuild. The front matter is already in the
shape the layouts consume — these are complete, valid files, not fragments.

Two cautions before publishing anything:

- **Check the URL still resolves.** Most of this content was hidden because something rotted.
- **Merge rather than overwrite** where a published file already exists at the mirrored path.
  `pages/about/links.md` here holds *only* the hidden category; the published `src/` file holds
  the other eight. Copying over it would delete 50 entries.

## Provenance

Raw source bytes for everything here are kept under `migrated-content/<type>/raw/db/`, and each
item has a ledger row in that type's `verification/reconciliation.tsv` with status
`migrated-hidden`. This directory is derived output, not a source: it can be regenerated.
