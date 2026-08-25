# Migrated deleted content

**Records the old TYPO3 site had marked deleted. Migrated in full, not built, no URLs.**

Outside Eleventy's input directory (`.eleventy.js` sets `dir.input = "src"`), so nothing here is
collected, routed or rendered — the same mechanism as `pre-migration-content/` and
`migrated-hidden-content/`.

## What "deleted" means here

TYPO3 does not erase records. `deleted = 1` moves them to what is effectively a recycle bin:
invisible in the backend and on the site, but still in the database. When the old site is
switched off, this is the material that would vanish without trace.

Earlier revisions of the migration plan excluded it deliberately, on the argument that a recycle
bin is not an archive. **The owner instructed otherwise on 2026-08-25: migrate it, keep it in its
own folder, preserve all the information.** That is what this is.

## Read this before using anything here

**Only 9 of the 202 records are from Maja's site.** The other 193 belong to *other websites* that
shared this database over the years.

| Origin | Deleted pages | Deleted elements |
|---|---|---|
| **`maja` (root uid 860)** | **2** | **7** |
| `karin` (735) | 31 | 14 |
| `mhk` (765) | 26 | 17 |
| `blog` (954) | 13 | 9 |
| `universe1` (764) | 8 | 15 |
| `wtweb design` (833) | 7 | 28 |
| `wtweb.net` (929) | 3 | — |
| `pyrofessor` (733) | — | 9 |
| `t3`, `think`, `schau`, `alt`, template storages | 9 | 2 |

This is the same pattern as the live `pyrofessor` site found during Stage 0 — the database has
hosted several unrelated projects. **The `other-sites/` material is preserved because the
instruction was to preserve everything, not because the migration has any use for it.** It is
other people's work; deleting the folder loses nothing of Maja's.

## Layout

```
migrated-deleted-content/
  README.md
  index.tsv          every record: uid, table, parent, title, CType, bucket, file
  manifest.json      extraction timestamp and counts
  maja/              <- root uid 860. The 9 records that matter
    deleted-pages/<pid>-<slug>/
      page.json          the complete `pages` row, all 71 columns
      content-<uid>.json the complete `tt_content` row, all 89 columns
      content-<uid>.md   readable rendering, where the element has text
    on-surviving-pages/  deleted elements whose page still exists
  other-sites/<site>/  same structure, everything else
```

## What "preserve all the information" means concretely

**Every column of every record**, not just the renderable ones — verified: 103 `tt_content` files
each carry all **89** columns, 99 `pages` files each carry all **71**.

This matters because **39 of the 103 deleted elements have no `bodytext` at all.** `image`,
`menu`, `list` and `table` elements keep their content in other columns — image references,
`pi_flexform` XML, record pointers. A bodytext-only extraction would have written empty files for
them and called it done. Their `.md` file says so explicitly and points at the `.json`.

Binary columns are preserved base64-encoded with their byte count and SHA-256 rather than being
dropped or lossily decoded. Text is read at connection charset `latin1` and is already correct
UTF-8 (plan §2.3); a mojibake scan across all 202 files returns zero.

The `.md` files are a convenience rendering — TYPO3 `<link>` tags become Markdown links, `<b>`
becomes bold. **The `.json` is authoritative.**

## Maja's deleted content, in detail

### `deleted-pages/1060-die-weglampen-2015/` — "Die Weglampen 2015"

Two elements: *The Path Illumination* (`list`, a gallery) and *Die Kalandraka Weglampen* (`text`).
Custom path illumination for the Kalandraka climbing refuge in Rodellar, Spain — 16 lamps from
industrial raw piping, XIX metal group, concept by Grex Portmann and Maja Thommen, built with
Uri Moss in Sennhof, Switzerland, October 2015.

**This is a superseded draft, not lost work.** The live site publishes the same project at
`pages.uid = 1063` ("Die Weglampen"), with slightly fuller text — the live version adds *"The
lamps are made to withstand the weather as well as vandalism."* Kept for the record; the live
version is the one to migrate.

### `deleted-pages/1079-sennhof/` — "sennhof"

Four elements. **This one is not superseded — its text appears nowhere on the live site.** The
element headed *workshop views* describes the Affenbande monkey sculptures: five monkeys built
from 2020, the first three installed in Zürich in June 2021, four and five in September 2022,
formed from 4mm and 6mm round steel, welded and ground; the first two shown in July 2020 in
*Lauschen statt Rauschen* at Galerie Neurotitan, for the 25th anniversary of Haus Schwarzenberg
in Berlin Mitte.

Note the mismatch: the page is titled *sennhof* and the element *workshop views*, but the text is
about the monkeys. **Worth the owner's eye** — this may be text that was moved elsewhere and the
original deleted, or a genuinely unpublished description of the Affenbande project.

### `on-surviving-pages/1068-portraits/`

One deleted element on the still-live *Portraits* page (`pages.uid = 1068`). The page itself is
published; only this element was removed.

## Relationship to the rest of the migration

Nothing here is a source for the site build. Every record has a row in `index.tsv`, and Maja's
records carry ledger status **`migrated-deleted`** in the owning stage's
`verification/reconciliation.tsv`.

**Deleted content is not verifiable against the live site** — by definition it is not published,
so V0b/V0c/V5 have nothing to compare it to. It is preserved on the database's authority alone,
which is why the complete record is kept rather than a rendering.

## Regenerating

`python3 migrated-content/_tools/extract_deleted.py` rebuilds this directory from the database.
It is derived output; edits here would be overwritten.
