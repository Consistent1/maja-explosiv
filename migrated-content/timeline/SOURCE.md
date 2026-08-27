# Timeline — source record

**Content type:** Timeline · **Stage:** 3 · **Migrated:** 2026-08-27

## Where it came from — not what the plan assumed

The plan expected prose to reshape. **The timeline is not text content at all.** It is
**`tt_news` records**, rendered by two `list_type = 9` (tt_news) plugin elements:

| | |
|---|---|
| Page | `pages.uid = 1016`, `info/bio/bio-chronological` |
| Plugin 1 | `tt_content.uid = 1198` — heading *"A partial chronology of expierience:"*, categories 17, 20–25, 39 → **79 entries** |
| Plugin 2 | `tt_content.uid = 1406` — heading *"Schooling:"*, category 26 → **6 entries** |
| Records | `tt_news`, storage page **864**, ordered `datetime desc` |
| Old render template | `fileadmin/s-maj/tpl/NewsBio.tmpl` |

**This also resolves Stage 12.** The plan lists "News — only if it renders live" as a separate
stage on the assumption that `tt_news` is a news feed. It is the chronology. Stage 12 should be
re-scoped or struck.

Two further elements on the page (`1405`, `1495`) contain **only images**, embedded in bodytext
as `uploads/RTEmagicC_*` — the third reference mechanism logged as unaudited in `PLAN.md`. They
are not migrated.

## The reshaping, and why

The old page renders **two** columns; `NewsBio.tmpl` emits only `###NEWS_SUBHEADER###` and
`###NEWS_CONTENT###`. **The `title` field is never displayed on the old site**, though every
record has one.

The new design (`about-content.njk` + `custom.css`) is **three-part**: a `<dt>` year in a
**37px** column, then an optional title at 1.5rem and a description at 1.0625rem.

Owner's instruction, 2026-08-27: **use the year only for display, titles as-is, bodytext as-is,
and import all remaining detail as metadata** so the presentation can be re-derived later without
returning to the database. Duplication between title and body text is accepted.

| rendered field | from | note |
|---|---|---|
| `year` | first 4-digit year in the source's own `short` label, else `datetime` — **except `since`, see below** | 37px fits a year; Figma shows a year |
| `title` | `tt_news.title` | verbatim; **newly visible** — the old site never showed it |
| `description` | `tt_news.bodytext` | verbatim, tags stripped, `<br>` → space |

**Preserved on every entry but not rendered:** `source_uid`, `source_date_label` (the original
label verbatim), `source_datetime` (full ISO timestamp), `source_categories`,
`source_category_names`, `source_bodytext_html` (the untouched RTE markup). Section level keeps
`source_plugin_uid` and `source_categories`.

**30 of 85 labels were reduced to a bare year** for display — 16 with month (`"05- 2024:"`) and
14 ranges (`"1997–2001:"`). **Every one is recoverable from `source_date_label`.**

**The two `since` labels are the exception** and keep their word: `"since 2020:"` renders as
**`Since 2020`**, `"since 2007:"` as `Since 2007` (owner, 2026-08-27). Reducing them to a bare
year is actively misleading — see the next section.

## Verification

| | |
|---|---|
| entries | source 85 = converted 85 = rendered 85 = **live 85** |
| sections | 2 = 2 |
| order | **matches the live site position for position** |
| description text | **85 of 85** live descriptions fully contained in ours |
| encoding | `Zürich`, `Käthe`, `Pfäffikon` correct |

Ours renders *more* than the old site — the title line — by design.

## Excluded: 4 records

Four live `tt_news` records on page 864 are in **category 27**, which neither plugin selects, so
they are invisible on the live site and are not migrated. All four titled **Elxt 90**,
2000–2003. Preserved with every field at `excluded/excluded-records.json` and copied to
`image-archive/live/about/timeline-excluded/`. **Open question for Maja** in `PLAN.md`.

## The `since` entries, and why they keep their word

Entries sort by `datetime desc`, matching the live site exactly. But the *displayed* year now
comes from the label rather than the timestamp, and the two diverge for `since` entries:

| entry | label | timestamp | sorts at | would display |
|---|---|---|---|---|
| Die Affenbande | `since 2020:` | **2022**-09-19 | 3rd, between 2023 and 2022 | `2020` |

Reduced to a bare year it reads as a sorting fault — "2020" wedged between 2023 and 2022. On the
old site the label said `since 2020:` and explained itself in place.

**Rendered as `Since 2020`, the entry explains its own position again.** The other `since` entry
(uid 191, `since 2007:`, timestamp 2007) is unaffected by ordering but is treated the same way
for consistency.

**Cost:** the year column is **37px** and `Since 2020` will not fit — it wraps to two lines, so
those two rows are taller than the rest. Accepted, and flagged for Maja: the alternatives are to
widen the column, sort by displayed year instead of timestamp, or accept the wrap.
