# Bio — source record

**Content type:** Bio · **Stage:** 4 · **Migrated:** 2026-08-27

## Where it came from

| | |
|---|---|
| Page | `pages.uid = 865`, `info/bio` |
| Element | `tt_content.uid = 1404`, 1,263 bytes, header "Bio" — the page's only content |
| Verified against | `https://www.maja-explosiv.com/info/bio.html` |

## What was done

The source is **one** RTE block. The live site renders it as a single `<p class="bodytext">`
with `<br />` line breaks — not as separate paragraphs.

Two kinds of break, distinguished:

- **`<br /><br />`** — a blank line between blocks. Treated as a **paragraph** break. Four blocks.
- **single `<br />`** — the author's manual line wrap mid-sentence. Converted to a **space**.
  Preserving these as line breaks would hard-wrap the text at the author's 2000s-era column
  width and break reflow at every viewport.

Split per plan §7, settled 2026-07-28: **paragraph 1 → `excerpt`** (rendered beside the portrait
in the About intro), **paragraphs 2–4 → the Markdown body**.

Preserved in front matter but not rendered: `source_uid`, `source_page`, `source_path`,
`source_portrait`, `source_paragraph_count`.

## Verification

| | |
|---|---|
| paragraphs | 4 (1 excerpt + 3 body) |
| text vs live | **1,084 characters both sides, identical after whitespace normalisation** |
| containment | live ⊆ ours **and** ours ⊆ live |
| encoding | `Pfäffikon` and the typographic apostrophe in `Thommen’s` correct |

Nothing added, nothing dropped.

## The portrait is not migrated

The source block opens with `<img src="uploads/RTEmagicC_ichsw.jpg.jpg">` — a portrait of Maja
embedded directly in the body text, via the third reference mechanism logged as unaudited in
`PLAN.md`. It is **recorded in `source_portrait` but not inlined**, because the new design has
its own portrait slot in the About intro (`about-image`, currently
`/assets/images/shared/profile/maja.webp`).

**The original is now archived** at `image-archive/live/about/portraits/ichsw.jpg` — **1000×729**,
where the old site only ever displayed a 214×156 derivative. Five further portraits from the same
folder were archived with it; see that directory's `README.md`. None of the six is in `tx_dam`, so
the gallery-based archive builder had never seen them.

**Whether the old portrait should replace the current one is open** — the two are different
photographs.

## Open question

The exact phrasing of the bio is unresolved and is a question for Maja. See `PLAN.md`.
The text here is the database's, verbatim, including:

- **"oeuvre includes, sculpture (metal, stone and wood) robotics, kinetic art"** — a comma after
  "includes" and none after "wood".
- **"Elxt90"** — elsewhere on the site written `Elxt 90`.
- Third-person throughout, shifting between "Maja Explosiv", "Maja", "Maja Thommen" and
  "M. Thommen".
- **"where she has resided since 2004"** — dated; unchanged since it was written.
