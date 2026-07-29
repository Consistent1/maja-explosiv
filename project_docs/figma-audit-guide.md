# Auditing the build against Figma, methodically

How to find real differences between this site and the design without spending hours
in the Figma UI, and without the guesswork that has cost this project time before.

Companion tool: `scripts/figma_audit.py`.

---

## 1. Why not just look at it

Two tempting approaches both fail here, for reasons worth stating once:

**Overlaying a Figma export on a screenshot.** Figma's text is placeholder, its photos
are different photos, most projects have no images migrated yet, and real copy wraps
differently from mock copy. The diff lights up almost entirely for reasons nobody cares
about, and real defects are buried in the noise.

**Eyeballing side by side.** This project has a documented case of it failing: a base
rule (`.content-wrapper p, li { margin-inline: auto }`) silently centred list items, and
it survived review because CSS metrics were checked but element *positions* were not. It
looked fine. It wasn't.

So: **compare numbers to numbers.** Screenshots are the sanity check at the end, never
the detection mechanism.

## 2. The token

A Figma personal access token with the `file_content:read` scope, at
`~/.config/figma/token`, mode 600, outside the repo.

```bash
mkdir -p ~/.config/figma && (umask 077; read -rsp 'Figma token: ' t && printf '%s' "$t" > ~/.config/figma/token) && echo
curl -s -o /dev/null -w '%{http_code}\n' -H "X-Figma-Token: $(cat ~/.config/figma/token)" https://api.figma.com/v1/me
```

`200` means it works. Never print the file, never paste the token into a chat or a commit.

## 3. Getting the design side as data

```bash
scripts/figma_audit.py spec 695:5712                  # flattened, human-readable
scripts/figma_audit.py spec 695:5712 --json spec.json # machine-readable
scripts/figma_audit.py raw  695:5712 --json raw.json  # untouched API response
scripts/figma_audit.py render 695:5712 --out ref.png  # 1x PNG straight from Figma
scripts/figma_audit.py image bd3f21a6 --out fill.png  # the source asset behind a fill
```

Responses are cached under `scripts/.figma-cache/` (gitignored); pass `--refresh` after
the design changes.

`spec` gives, per node: id, name, type, box **relative to the node you asked for**,
auto-layout mode / gap / padding, rotation, clipping, effective text style, fills and
strokes with their bound variable ids.

The three commands that matter beyond `spec`:

- **`render`** produces a pixel-accurate reference from Figma's own rasteriser. Far
  better than an export you cropped by hand, and the basis for any silhouette check.
- **`image`** downloads the actual asset behind an image fill. Hash it against the repo
  copy — that settles "is this the same file?" by identity rather than by inference.
- **`raw`** for when something looks wrong and you need to see what the API really said.

## 4. Finding the right node

This file is full of near-identical stale drafts, and picking the wrong one has burned
hours more than once. **Never search by text.** Start from the locations recorded in
`CLAUDE.md` §4, get a node id once, and then work from ids.

Useful ids so far:

| Node | What |
|---|---|
| `695:5712` | Sidebar, `Navigation6 Flip Yellow` — the `In Use` variant |
| `46:1107` | Sidebar component set (all six variants) |
| `52:6427` | Homepage `Main container` |
| `46:901` | About components container |
| `46:704` | Projects Gallery Section |
| `274:3273` | Single project page |
| `957:5992` | Contact overlay |

A component **set** returns all variants; index into the one you want by name
(`Navigation=Navigation6 Flip Yellow`), never by position.

## 5. Getting the built side as data

With the dev server running, in the browser console:

```js
(() => {
  const props = ['display','position','width','height','maxWidth','padding','margin',
    'gap','rowGap','justifyContent','alignItems','flexDirection','overflow',
    'fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','textTransform',
    'color','backgroundColor','borderLeftWidth','borderRightWidth','borderTopWidth',
    'borderBottomWidth','borderColor','backgroundImage','backgroundSize',
    'backgroundPosition','opacity'];
  const root = document.querySelector(ROOT_SELECTOR).getBoundingClientRect();
  const out = {};
  for (const [key, sel] of Object.entries(MAP)) {
    const el = document.querySelector(sel);
    if (!el) { out[key] = null; continue; }              // absent is a finding
    const r = el.getBoundingClientRect(), c = getComputedStyle(el);
    const o = { _box: [ +(r.left-root.left).toFixed(2), +(r.top-root.top).toFixed(2),
                        +r.width.toFixed(2), +r.height.toFixed(2) ] };
    props.forEach(p => o[p] = c[p]);
    out[key] = o;
  }
  return JSON.stringify(out);
})()
```

Boxes are relative to the same root as the Figma side, so the two are directly
comparable. **A `null` is a finding, not an error** — it means the design has something
the build doesn't.

## 6. The mapping

The audit needs an explicit Figma-node → CSS-selector map, written by hand, one per
surface. It is the part that takes judgement, and it is worth more than the diff: it is a
durable record of which frame is canonical for which piece of the site — exactly the
knowledge this project keeps having to rediscover.

Keep it next to the audit it belongs to. Record deliberate non-correspondences too
("Figma's X has no counterpart because …") so they are not rediscovered as bugs.

## 7. Comparing

Do **not** pick a tolerance up front. Record every delta with its magnitude, then look at
the distribution before deciding what counts — a ±2px cut-off chosen in advance either
buries real 3px errors or floods the report with rounding noise.

- **Geometry**: report in bands (≥8px / 4–8 / 2–4 / <2). The owner's calibration is
  "34.95 may as well be 35", so sub-pixel differences are never findings.
- **Colours, font families, font weights**: exact. No tolerance.
- **Font sizes**: ±0.5px.
- **Ignore entirely**: text content, image assets, anything inside a section known to be
  unbuilt. Figma's copy is placeholder and is *not* a source of truth (`CLAUDE.md` §3).

Sort by magnitude, then triage every finding into one of three buckets:

1. **The build is wrong** → fix.
2. **Figma is ambiguous or self-inconsistent** → `PLAN.md` § *Open items needing input*.
3. **Deliberate deviation** → also `PLAN.md`, with the reasoning, so it is not
   re-litigated next session.

Bucket 2 is real and common — the design contradicts itself in several places (see §8).

## 8. Traps

Every one of these was hit for real. They are the reason this document exists.

### `style` on a text node is only the DEFAULT

The rendered style may be entirely different. `characterStyleOverrides` (one id per
character) indexes into `styleOverrideTable`, and a node can be **100% overridden** — its
`style` block then describes a font that is never drawn.

Reading `style` alone reported the sidebar subtitle and footer credit as *Rethink Sans*.
Both are actually Geist (600/14.01px and 500/18px). That would have been two invented
"inconsistencies", and one of them would have "justified" changing correct code.

`figma_audit.py` resolves this. If you query the API by hand, resolve it yourself, and
flag mixed runs rather than picking one.

> Open question this raises: PLAN.md records the About **Links** entries as Rethink Sans,
> read from the properties panel. Worth re-checking against the API before treating it as
> real.

### `letterSpacing` is absolute px, tied to the size it was authored at

It is *not* the percentage the UI shows. To get em, divide by the font size **from the
same style dict**. If an override changes `fontSize` but not `letterSpacing`, carrying
the px value gives nonsense — the sidebar subtitle read as −0.0514em where Figma shows
−3%. Carry the *ratio* across the override instead.

### `leadingTrim: CAP_HEIGHT` makes the box cap-height-tight

Figma's box then hugs the capitals rather than the line box, so it will never match a CSS
line box. The sidebar subtitle is a 10px-tall box containing 14px text. CSS has no stable
equivalent (`text-box-trim` is too new to rely on). **Compare text by baseline/left edge
and by font metrics — not by box height** whenever this is set.

### `scaleMode: "STRETCH"` is what the UI calls "Crop"

And `imageTransform` is the visible window in normalised image space:

```
[[a, _, tx],       visible x: tx .. tx+a      (fractions of image width)
 [_, d, ty]]       visible y: ty .. ty+d      (fractions of image height)
```

To CSS, for an element W×H showing fractions (fw, fh) from (fx, fy):

```
background-size     = W/fw  ×  H/fh
background-position = -fx·bgW , -fy·bgH
```

**Always check the implied scale is uniform** (`bgW/imgW ≈ bgH/imgH`). If it isn't,
either the design stretches the image or the decode is wrong — and a wrong decode will
not land on uniform by chance, so this doubles as a correctness check. It caught a 2×
vertical stretch in the sidebar brush.

### `rotation` is relative to the parent

A node at −90° inside a parent at +90° is unrotated on screen. Don't propagate one
without the other. `absoluteBoundingBox` is already axis-aligned in absolute space, so
for geometry you can usually ignore rotation entirely — but not when converting to a CSS
`transform`.

### `absoluteBoundingBox` vs `absoluteRenderBounds`

`absoluteBoundingBox` is the node's own box. `absoluteRenderBounds` is what is actually
inked, **after clipping**. When they differ, something is being clipped — which is itself
information. In the sidebar the brush's box is 295.68 wide but its render bounds are
224: the sidebar clips it. Use render bounds to reason about what is visible; use the
bounding box to reason about the geometry to implement.

### Clipping lives on the frame, not the fill

Check `clipsContent`. The sidebar brush overflows its `Header` frame
(`clipsContent: false`) and is cut by the sidebar instead. Reproducing that structure —
rather than clipping at the nearest ancestor — is what let the strokes rise above the
credit band.

### Exported PNGs have a transparent background

`Image.convert('RGB')` turns transparent into **black**, so every edge-detection scan
returns the full frame width. Composite onto white first:

```python
src = Image.open(p).convert('RGBA')
flat = Image.alpha_composite(Image.new('RGBA', src.size, (255,)*4), src)
```

### Variable names are not readable on this plan

Fills carry `boundVariables.color.id` (e.g. `VariableID:75:2984`), but resolving ids to
names needs `/v1/files/:key/variables/local`, which is Enterprise-only. Treat the id as a
stable identity: *same id ⇒ same token*, which is enough to spot two things that should
share a token but don't.

### The design contradicts itself

Not everything that differs is a build defect. Known cases: the same photo appears in
colour and in greyscale in different homepage cards; the four sidebar nav items use two
different greys with no apparent pattern; the homepage tab bars overflow their own frame.
When Figma disagrees with itself, that is bucket 2 — a question, not a fix.

## 9. Running it in tiers

Do **not** run every class of check on one surface and then move on. Run **tier 1 across
every surface first**, then tier 2 across every surface, and so on. Breadth before depth:
tier 1 finds the things that are visibly wrong, and finding them everywhere is worth more
than finding subtle problems in one place while the rest is unexamined.

### Tier 1 — does it match the design

1. **Coverage, both directions.** Every visible Figma node with no mapping (design
   elements the build may be missing), and every visible DOM box inside the audited
   region with no Figma counterpart (things we invented). A diff cannot see absence.
2. **Relationships, not just boxes.** Shared left edges, shared baselines, equal gaps
   within a run, equal widths, centring. Report the broken *relationship*, not a raw
   delta — "sub-items no longer share their heading's indent" beats "x is 10px out", and
   relationships survive the fact that Figma's placeholder copy wraps differently from
   real content.
3. **Typography.** Family, size, weight, line-height, tracking, case — per §8's traps.
4. **Colour.** Value, palette membership, and *which token* it should be. A colour can be
   on the palette and still be the wrong one (see the sidebar's S1: `#525252` is a real
   palette colour, just not the one Figma binds).

### Tier 2 — is it built correctly

5. **Cascade ownership.** For each mapped element, which stylesheet and rule won each
   design-relevant property. Anything the design specifies but `_user` does not declare is
   silently supplied by the base template — that is finding S2's whole class, and it
   doubles as the Phase 0 boundary audit.
6. **Token provenance.** Every design-relevant literal in `custom.css` should be a
   `var()`; every `var()` should resolve to a value in the Figma palette; two things bound
   to the same Figma variable should use the same CSS token. A hardcoded value that
   happens to match renders identically and passes every other check.
7. **Design-free invariants.** No overlapping text boxes, no horizontal overflow, nothing
   clipped, contrast above threshold. These need no mapping and no design, run cheaply at
   many widths, and catch what Figma is silent about — which is most of the responsive
   range. The sidebar nav/footer collision was found by accident; this would find it by
   rule.
8. **States.** Hover, focus-visible, current/active. Everything else here measures the
   default state only.

### Tier 3 — does it survive reality

9. **Real content extremes.** Longest actual title, emptiest collection, project with no
   image. Figma shows four nav items and short titles; the build generates from ~71
   projects. Design files never show these states, so nothing ever compares them, and they
   are where layouts actually break.
10. **Regression baseline.** Commit the extracted spec + comparison output so a later
    change that silently re-breaks a fixed finding shows up as a diff.

### How much Figma API does this actually need?

Very little, and it does **not** grow with the number of checks.

- One request per surface, cached to disk under `scripts/.figma-cache/`. The design is
  static between edits, so this is a handful of requests total, once.
- Batch ids in a single call — `?ids=a,b,c` — rather than looping. Fetching seven large
  subtrees back to back triggers HTTP 429, and Figma's limit resets over minutes, so
  serial retries with short backoff do not help.
- **Tiers 2 and 3 need no API calls at all.** Cascade ownership, token provenance,
  invariants, content robustness and regression are DOM- and CSS-side, or reuse the
  cached spec.
- `render` is the only per-check extra, and only for graphical comparisons.

So the API cost is front-loaded and small. The expensive part is judgement, not requests.

## 10. Verifying a fix

Same discipline as detection.

- **Numerically, before/after.** Snapshot computed styles + boxes, change, re-snapshot,
  diff. Anything that changed and shouldn't have is a regression. This is how the tab-CSS
  deletion was shown to be inert.
- **Against Figma's rasteriser** for anything graphical: `render` the node at 1× and
  compare per-column profiles (top edge, ink coverage). Report median and p90, not the
  max — a single hairline stroke antialiasing differently will blow up the max while the
  geometry is exact.
- **Then** look at it. Visual confirmation last, never first.
