# Links — verification report

**Stage 1 · run 2026-08-25 · status: PASSED (19/19), V8 outstanding**

## Result

**11 local checks and 8 live checks pass. The V0c source gap is empty.**

### Local — pipeline fidelity

| Check | Result | Detail |
|---|---|---|
| V1a count parity | PASS | source = normalized = converted = rendered = **50** |
| V1a category parity | PASS | 8 = 8 |
| V2 bijection on url | PASS | 0 source-only, 0 rendered-only |
| V3 field fidelity | PASS | 0 differences |
| V4 order fidelity | PASS | category and within-category order |
| V6 urls byte-identical to database | PASS | all 50 verbatim in the raw bodytext |
| V6 no silent http→https | PASS | source schemes preserved |
| V7 no mojibake | PASS | none of `Ã Â â€ ï»¿` |
| V7 non-ASCII strings intact | PASS | 7 derived cases incl. `Hervé Thiot`, `Fer à Coudre`, `Lärz`, `Köln`, and two U+00A0 |
| V11 installed = migrated artefact | PASS | byte-identical |
| V11 src/ only migration output | PASS | exactly 1 file |

### Live — against `https://www.maja-explosiv.com/info/links.html`

Fetched with `curl` (owner-authorised), sequential, 2s apart. Raw bytes, headers and fetch
timestamp in `raw/live/`; census re-derivable, sha256 `c0a2d45cc0445f8f`, fetched
2026-08-25T10:01:57Z.

| Check | Result |
|---|---|
| V0b truth census built | PASS — 8 categories, 50 entries |
| V0c source gap | **PASS — empty**, no `missing-from-source` rows |
| V1 count parity incl. live | PASS — live 50 = rendered 50 |
| V2 bijection against live | PASS — both directions |
| V4 order fidelity against live | PASS |
| V4 heading order and text | PASS |
| V3/V5 rendered output vs live page | **PASS — 0 differences** |

V5 is the check that matters most: our built HTML was re-parsed and compared field-by-field to
the live page. Every url, anchor text, prefix and suffix matches.

## The route to this result, recorded because the detour was instructive

The first run of this stage **passed all 11 local checks and was wrong.** It produced 66 entries
where the live page publishes 50, and the report concluded the live site must be served by an
unknown database.

The cause was mundane: **the local MySQL had been loaded from the January 2025 dump.** The fresh
2026-08-25 dump arrived later and was never loaded. Every local check compared the pipeline
against its source, and the source was stale — so all eleven passed.

Comparing the two dumps properly (decoding MySQL string escapes first, since phpMyAdmin and
mysqldump escape quotes differently and write blobs in different notation) shows **exactly one
content value changed across the entire site in nineteen months: `tt_content.uid=1399.bodytext`,
this page.** 10,345 → 8,441 bytes. Everything else is identical.

Two lessons worth keeping:

1. **A pipeline can be perfectly faithful to the wrong input.** Local checks verify the pipeline;
   only the live comparison verifies the *source*. This is the entire argument for the
   extraction/verification split in §"Why this split is the right one", and it earned its keep
   here on the first stage.
2. **An earlier claim of "zero drift" was generalised from three sampled rows** without saying it
   was a sample. Stated as a whole-table result, it was wrong. See plan §2.0a.

## Content notes

- **`tt_content.uid = 1400`** (`ON MY OWN BEHALF:`, Casino Gitano on MySpace) is `hidden = 1`,
  unpublished, and **absent from the live page too** — so excluding it is confirmed correct, not
  just defensible. Raw bytes kept; ledger status `not-migrated`.
- **Two entries are split across consecutive `<link>` tags sharing one href** — an RTE artefact:
  `Paka the U` + `ncredible`, and `Hervé` + ` Thiot`. They are rejoined by concatenating the raw
  anchor contents and cleaning once, so inner spacing survives. Cleaning each fragment first
  yields `HervéThiot`.
- **The source's eight category headings are preserved verbatim**, trailing colons included, per
  owner decision 10.

## Outstanding

**V8 — visual comparison** needs a browser for screenshots of the two pages side by side. `curl`
covers every structural check; it cannot render. This is the only part of Stage 1 not done.
