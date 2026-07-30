# Maja Explosiv — Redesign & Migration Plan

**Status document owner:** this file is the current source of truth for where the project stands and what's next. It supersedes `RESUME-WORK-HERE.md`, `MIGRATION-STATUS-REPORT.md`, and the various session-summary docs, which have been moved to `project_docs/_archive/` (see `_archive/MANIFEST.md`) rather than deleted.

**Last updated:** 2026-07-30

---

## Resume here (2026-07-30)

**Homepage tier 1 is done and, apart from two items that need the owner, fixed.** Findings
H1–H12 and the after-verification table are under Phase 2. The CTA is rebuilt to the current
design; the column, section headings, hero, category description, all nine gaps and the
footer are corrected and re-measured; `!important` is gone from both stylesheets.

**Still waiting on the owner** — in *Open items needing input*: the CTA label reads **Inter**
in Figma and was built in Geist; what the project card caption's 2nd and 3rd rows are for;
whether the two section headings are meant to be styled differently; and `#FFCC00` still has
no palette token even though it now renders.

**Sidebar visually checked (2026-07-30)** against
`figma-exports/sidebar-in-use-variant__46-1107.png` — the check that timed out last session
because the browser pane was closed. Wordmark, subtitle, both headings with their indented
sub-items, the footer brush and the credit band all land where the design puts them. No new
defects by eye; the numeric verification stands.

**Next step:** tier 1 on the single Project Page (`274:3273`), then the About components
(`46:901`) and the Contact overlay (`957:5992`). Breadth before depth (guide §9). Note that
About's Bio panel already had one homepage defect (H3) in it — worth expecting more of the
same class there.

**Two method notes worth keeping:**

- Measure the homepage at a **1295px viewport**. The frame is 1280 and the scrollbar is
  15px, so measuring at 1280 shifts every x by 15 and narrows the column — enough to invent
  findings.
- **Editing a layout or include under `src/_user/` needs the dev server restarted.**
  `.eleventy.js` copies them into `.cache/layouts/` and `.cache/includes/` at config time,
  so a running server keeps serving the old markup and it looks as though the change did
  nothing. CSS under `src/_user/assets/` is a watch target and does hot-reload.

---

## Resume here (2026-07-29, end of session)

**Read first:** `CLAUDE.md`, then this section, then `project_docs/figma-audit-guide.md`.

**What changed this session.** The project now has a repeatable way to find design
mismatches instead of looking for them by eye: a Figma REST API token plus
`scripts/figma_audit.py` and the guide. Applied to the sidebar it found six defects in a
component this file had marked "done", five of which are fixed and verified numerically.

**The method, in one line:** pull the node's real spec from the API, pull the same shape
from the rendered DOM, compare numbers — never pixels, never by eye. The guide's §8
"Traps" is the part that matters; two of those traps produce confidently wrong answers.

**State of play**

| Surface | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Sidebar | **done** — S1-S4, S6 fixed; S5 height open; checked by eye 2026-07-30 | not started | not started |
| Homepage | **done 2026-07-30** — H1-H10 fixed; H11, H12 with the owner | not started | not started |
| Single project | not started | | |
| About components | not started | | |
| Contact overlay | not started | | |
| Impressum | not started | | |

**Next step:** tier 1 on the homepage (`52:6427`). Breadth before depth — finish tier 1
everywhere before starting tier 2 anywhere (guide §9).

**Immediately actionable, no decisions needed**

- Scan Project Page (`274:3273`), Contact Overlay (`957:5992`) and Impressum
  (`612:6400`) for off-palette colours. Blocked only by Figma rate-limiting on the day;
  batch the ids into one request rather than looping.
- Visually check the sidebar. Every sidebar fix is verified numerically but was never
  seen — the preview pane was not displayed, so screenshots timed out.

**Waiting on the owner** — see *Open items needing input*: the off-palette greys, the
sidebar sub-item colour inconsistency, whether the wordmark becomes an SVG (S5's height
cannot be matched with live text), and what gives when the sidebar nav and footer collide
on short viewports.

**Two things that bit hard, so they do not bite again**

1. A text node's `style` in the API is only the *default*. Read naively it reports the
   sidebar subtitle and footer credit as Rethink Sans; both are actually Geist, overridden
   per character. That would have been two fabricated findings.
2. Compare text by **ink extents**, never block boxes. Comparing `.brand-title`'s block
   width against Figma's hug box overstated S5 by 6px.

---

---

## The two repos

- **`explosive`** (`Xpanda-org/explosive-11ty`) — the generic 11ty template. Owned by the same person as this site. Anything genuinely reusable by other sites belongs here.
- **`maja-explosiv`** (this repo, `Consistent1/maja-explosiv`) — Maja's site, forked from `explosive`. Uses the template's `src/_user/` override system so it can pull template updates without merge conflicts (`upstream` remote is configured and nearly caught up — one trivial commit behind).

**Working principle going forward:** when a change is generic (a bugfix, a new capability any site could use), it should be made in/ported to `explosive`. When a change is specific to Maja's content or Figma design, it belongs in this repo's `src/_user/` overrides — not in the base template directories. An audit of where this boundary has already been crossed is in progress (see Phase 0).

## Design source of truth

Figma file: [MajaExplosiv_Website Redesign](https://www.figma.com/design/18tst8uq38FlDlaZA5cPCz/MajaExplosiv_Website-Redesign) (owner's personal copy, free plan — exact values will be read via the Design-mode properties panel rather than Dev Mode).

> Corrected 2026-07-29: this file was previously recorded here (and in `ux-specification.md`) as "Maja Thommen_Website-Redesign" with a `Maja-Thommen_Website-Redesign` URL slug. The real name is **MajaExplosiv_Website Redesign** (slug `MajaExplosiv_Website-Redesign`); the old URL redirects, but the name was wrong.

**The PNG exports in `project_docs/_archive/design_screenshots/` are retired — do not use them.** They were captured 2025-11/2025-12, predate the 2026-07-24 wrong-frame correction, and carry no record of which frame they came from, so they may show stale drafts. Per the owner (2026-07-28): read Figma directly for anything design-related, taking fresh screenshots as needed, and accept the slowness if it buys any accuracy. Figma is the source of truth for design; the live site is the source of truth for content.

**Replaced 2026-07-29 by `project_docs/figma-exports/`.** A fresh set of 1x PNGs exported straight out of Figma (not screenshots — the owner pointed out Figma's own export is available and cleaner). Every file carries the node id it came from — enough on its own to re-open the source frame (`?node-id=<id>` on the file URL). The folder is gitignored at the owner's instruction, so the exports and their `MANIFEST.md` (which records each frame's exact in-file location and which variants were skipped as stale) are local-only; **re-export rather than assume they are present.** Covers: the whole homepage (`Main container`, 1280×6524), the Landing Section, the Projects Gallery Section, the single Project Page, the four current About Components variants, all six sidebar variants plus the `In Use` one cropped out, the Contact overlay, and the Impressum page. **These are for sanity-checking layout by eye** — exact values still come from Figma's properties panel, not from measuring pixels in a PNG.

## Agreed priorities

1. **Design/functionality first, content second.** Reasoning: several page templates (Timeline, Impressum) don't exist yet and others (Bio, Press, Links) are placeholders — migrating bulk content before those "slots" exist would mean redoing the work. Build the real templates against Figma first, then pour in content at scale.
2. **Migration correctness is the overall top priority** of the project; the template/site code-organization principle above is a secondary, ongoing discipline applied throughout, not a phase of its own.
3. GitHub Pages and the VPS/production host are both **deferred** — not blocking current work. Revisit GH Pages once there's something worth showing; VPS specifics (provider, deploy method) TBD later.

---

## Phase 0 — Housekeeping (in progress)

- Archive ~30 overlapping/superseded docs and duplicate JSON data files from `project_docs/` into `project_docs/_archive/` (move, never delete).
- Fix two latent config bugs: an orphaned dead file at `src/_user/_data/theme.js` (wrong folder name, never read by the build, holds stale non-Figma colors) and duplicate `site.js`/`site.json` + `collectionData.js`/`.json` pairs in `src/_user/data/` (both get processed by the data-override loop in `.eleventy.js`, which is undefined/fragile — should be exactly one file per data key).
- Fix `package.json` — `name` still says `"explosive"` (leftover from the fork).
- **Audit base-template-vs-override boundary violations.** `git diff upstream/main..main` shows direct edits to `src/_layouts/home.njk`, `theme/home.njk`, `theme/collection.njk`, `collection.njk`, a new `src/_includes/home/project-detail.njk`, `src/assets/css/main.css`, `src/assets/js/main.js`, and `.eleventy.js` — all outside the override system. Each needs classifying as Maja-specific (move into `src/_user/`) or generically useful (candidate to upstream into `explosive`). Findings to follow; execution happens after review since this touches live-rendering behavior.

## Phase 1 — Lock the design system

**Status: mostly done for colors and core typography (2026-07-24).** Confirmed by inspecting the Figma file directly (via a real, logged-in Chrome session — the file lives on the designer's account, view-only) and applied to `src/_user/data/theme.js` / `custom.css` / `base.njk`:

- **Colors** — real hex values from Figma's "Grey" variable collection: `#222222`/`#373737`/`#525252`/`#8E8E93`/`#B1B1B1`/`#B8B8B8`/`#EBEBEB`. Corrected a mistake made earlier in this same session: the sidebar's fill is actually bound to the `Background` variable (`#B8B8B8`), not the separate `Navigation Sidebar` variable (`#B1B1B1`) that exists in the file but isn't applied to the real component — confirmed by inspecting the component instance directly, not just the variable list.
- **Font family — real bug fixed**: the site was loading and using **Geist**, but Figma confirms every text layer checked uses **Outfit**. Geist doesn't appear anywhere in the design file. Swapped in `base.njk` (Google Fonts link) and `theme.js`.
- **Hero title** ("MAJA EXPLOSIV"): Outfit 700, **140.77px** (previous placeholder guess was 88.8976px — quite far off), 92% line-height, -3% letter-spacing (converted to `-0.03em` — Figma's `%` letter-spacing isn't valid CSS as a literal `%`, has to be em/px), uppercase, `#222222`.
- **Sidebar layout**: 252px width (was 250px), 17.69px padding, 2px `#222222` right border (was 1px `#444444`), `justify-content: space-between`.
- **Nav/logo text**: Outfit 700, 30px, 92%/-3%.
- **Lead paragraph text**: Outfit 500, 40px, 110%/-2.5%.
- **Body/tagline text**: Outfit 400, 32px, 110%/-2.5%.

**Update 2026-07-24, round 2**: got the remaining high-value tokens.
- **Button font**: confirmed **Geist** (600/SemiBold, 16px, 140% line-height, uppercase) - not Inter, which was never a confirmed value, just an old guess. Geist font loading restored in `base.njk` (scoped to buttons only - headings/body stay Outfit).
- **Section eyebrow label** ("WHO WE ARE" style): Outfit 700, 28.7px (rounded to 29px), 140% line-height, +2% tracking, uppercase, `#373737`. Added as a `section-title` token in `theme.js` but **not** wired into the existing `.section-title` CSS (that rule styles the big "Projects"/"About" headers and was deliberately changed to sentence-case/left-aligned per earlier explicit feedback - the Figma style found here looks like a different, currently-unbuilt eyebrow element, not a correction to that one; left as an available token rather than guessing).
- **Carousel**: confirmed a "Responsive Image Gallery" component exists in Figma - horizontal flow, 1058px fixed width, 24px gap. Structural spec noted; actually wiring the site's Datastar carousel to project galleries against this spec is still open.
- **"Cool CSS effect"**: grayscale-to-color image hover, confirmed directly in the Figma prototype (Present mode) on project photography. Turned out to already be implemented on `.featured-project-image` (top 4 hero thumbnails) - extended the same pattern to `.project-image img` (the main Sculptures/Installations/Performance/Paintings grid), which had it missing.

**Still unconfirmed / not pursued further**: h4–h6 sizes (kept as prior reasonable approximations - not worth more Figma hunting per the "close, not pixel-perfect" guidance), the spacing/gap scale beyond what was checked, other border colors, and whether `main.css`/`main.js` (the base-template copies, not the `_user` overrides) contain dead styling worth stripping - deferred from the Phase 0 audit pending a working visual-diff setup.

**Correction 2026-07-24, round 3 - the round 1/2 extraction was from the wrong Figma frame.** The file has multiple near-identical "Main container" instances scattered across draft/exploration regions (First Drafts, Exploration Working Process, Seperate Pages Solution, etc.) alongside the real one. Rounds 1-2 pulled values via text search, which landed on stale drafts without realizing it. The owner identified the actual canonical location precisely: big heading **"Onepager Solution"** → sub-heading **"Updated Components"** → the **"Main container"** frame beneath it (spatially positioned, not a literal parent in the layers panel - "Onepager Solution" and "Updated Components" are floating text labels, not containers). The equivalent for single-project pages is **"Project Page"** under **"(Updated Reusable) Components"**, to the right past a greyed-out page. For components specifically (sidebar, About tabs layout), the source is `Assets / Components` → far right → **"About Components"** - and where multiple variants of the same component exist there (e.g. 4 sidebar versions), only the one labeled **"In Use"** is current; the rest are stale.

Re-verified directly from that correct location and corrected in `theme.js`/`custom.css`/`base.njk`:
- **Font family is Geist everywhere** (headings, body, AND buttons) - not Outfit, which doesn't appear to be used anywhere in the correct frame. The round-1 "Outfit" conclusion was itself a wrong-frame artifact. Outfit's Google Fonts link removed entirely; Geist is now the sole family loaded.
- **Hero title ("MAJA")**: Geist 700, **85.94px** (not 140.77px), 74% line-height, -2% tracking.
- **Hero subtitle ("EXPLOSIV")**: Geist **500** (not 700 - a different weight from the title line, not identical as first assumed), **77.29px** (not 140.77px), same line-height/tracking as title.
- **Body/tagline text**: Geist 400, **22.45px** (not 32px), 110%/-2.5% unchanged.
- **Sidebar**: **224px width** (not 252px), padding **20px top/bottom, 24px left/right** (not a uniform 17.69px), border **1px** (not 2px) `#222222`. Cross-checked **three times independently** and all agree: the live instance inside the correct Main container, the component library's "In Use" instance selected by name, and again by explicitly counting to the rightmost of the 4 sidebar variants in Assets/Components per the owner's exact directions - all three read 224px.
- Confirmed the "Project Page" and "About Components" reference locations exist and contain real Bio/Timeline/Press/Links tab structure + the sidebar variants - out of scope for this round per the owner (single-project page explicitly deferred), and About Components implementation is planned for a dedicated follow-up session.

**Round 3 follow-up - gaps explicitly requested but not fully closed:**
- **Nav-title** ("MAJA EXPLOSIV" wordmark in the sidebar): turns out to be built as a `Mask group` (vector/graphic), not a plain text layer - there's no clean font-size property to read the way there is for the hero title. Left as the prior approximation (30px), font-family corrected to Geist for consistency. Needs a different extraction approach (e.g. asking the owner to export/inspect it directly in Figma) rather than more of the same navigation.
- **Lead paragraph & section-eyebrow** ("WHO WE ARE" style): not re-verified from the correct frame this round. Attempted twice - first click landed back on the already-confirmed hero body text (same node as `body-size`, not a distinct About-section style), second attempt drifted into an unrelated part of the layers tree while scrolling. Still carrying the wrong-frame round-1/2 values (Outfit-based) with only the font-family corrected to Geist. **Not confidently confirmed - treat these two specific tokens with more skepticism than the rest of this document until re-checked.**

**Fixed 2026-07-24, round 3 - sidebar footer color + missing decoration.** Owner feedback after reviewing the live build: the "ATELIER MAAS & THOMMEN" text at the bottom of the sidebar was the wrong color and missing a background graphic that an older version of the site had. Found `src/assets/images/corner.png` (439×72, the black brush-stroke graphic) already in the repo and already wired to the hero section and single-project pages (`background-position: right top`) - just never applied to the sidebar. Fixed in `custom.css`:
- `.sidebar-footer` now gets a full-bleed black background with `corner.png` positioned `right bottom` (its "tail end"), bled to the sidebar's true edges via negative offsets that cancel `.left-sidebar`'s own padding (clipped by its `overflow:hidden`).
- `.sidebar-footer p` color changed from `#666` to `var(--theme-colors-accent, #EBEBEB)` (the confirmed Off White token).

Verified via computed styles in-browser (background/text color/image all correct, no console errors) - not yet confirmed by eye against the actual Figma sidebar treatment (screenshot tooling unavailable this session), so worth a visual sanity check next session.
- Given how slow and error-prone Figma navigation is on this machine (each selection/search round-trips several seconds, and the panel repeatedly loses state), continuing to chase these two specific values hit clearly diminishing returns relative to the value already banked (font family, hero sizes, sidebar). Stopped here rather than burn further time for marginal gain - flagging honestly rather than guessing further.

**Corrected 2026-07-24, same day - the round 3 fix above was wrong.** Owner reviewed the live build again: the full-bleed black background + `filter: invert(1)` combination was backwards. `corner.png` is black ink on transparent, same asset used elsewhere with no inversion - it should render black there too, not be inverted to white. Fixed:
- `.sidebar-footer` background-color removed entirely (was `#000000`) - the sidebar's own background now shows through, same as everywhere else `corner.png` is used.
- `.sidebar-footer::before`'s `filter: invert(1)` removed - image renders in its natural black.
- Positioning/offsets (the `-20px/-24px` bleed, `right bottom` anchor, `rotate(180deg)`) intentionally left untouched this round - owner said they'll adjust positioning themselves. Still unconfirmed against Figma; don't treat as correct without a visual check.

**Working calibration (per owner, 2026-07-24)**: Figma is a forceful guideline, not a strict spec. Close adherence matters; pixel-exact values don't - e.g. 448.7845px may as well be 450px. Don't over-invest in chasing decimal precision on remaining tokens.

**Note on content vs. design system** (per owner, 2026-07-24): Figma governs structure, layout, spacing, and typography conventions per section — *not* literal copy. Project titles, descriptions, and most body text in the Figma file are placeholders the designer didn't keep in sync with the real site content (e.g. "The Sisyphos Gate" in Figma vs. whatever the actual migrated title is). Templates must pull all such text from front matter/content data, never hardcode strings copied from Figma. Fixed UI chrome (button labels, section eyebrows, footer nav) is treated as legitimate template text, not content — flag any case where that distinction gets ambiguous.

## Phase 2 — Finish templates & functionality to match Figma

Work through `design_screenshots/` page by page:

| Page | Current state |
|---|---|
| Homepage | Structurally close — sidebar, hero, featured grid, tabbed projects, about intro all present. Needs token-accurate styling pass once Phase 1 lands. **Projects tab bar brought in line with the About tab bar, 2026-07-29** — see below. |
| Single project | Close — `sisyphos-gate.md` is a working full example (images, layout) matching `project.png` reasonably well. |
| Bio | **Done.** Real content, transcribed verbatim from the live site (`maja-explosiv.com/info/bio.html`). |
| Press | **Content done** - full chronological press-mention list (1993-2018), transcribed from the live site. **Layout superseded 2026-07-29:** the earlier claim here that "no usable Figma layout existed" was wrong - it was an artifact of the `press.png` export being a mislabelled duplicate of `links.png`. Reading Figma directly shows a real Press design (description line + 3-column Responsive Image Gallery of the scanned clippings + text list). See the About Components spec below. Clipping images still need asset migration; placeholders in the interim. |
| Links | **Done.** Real content - full "Friends and Related Artists" directory (8 categories, 50 entries) with real outbound URLs, transcribed from the live site. Figma's text matched the live site verbatim, but had no real hrefs. |
| Timeline | **Done.** Real content - full career chronology (1993-2024, 85 entries) plus a Schooling section, transcribed from the live site's `/info/bio/bio-chronological.html`. The Figma mockup for this page was unreliable: mostly unfilled placeholder rows, plus at least two entries ("Urban Resilience", "Voices of the Forgotten") that don't exist on the real site and don't match Maja's practice - correctly flagged as suspect before the live-site check confirmed it. |
| Impressum | Page exists (`/impressum/`), footer link resolves. Content transcribed from the Figma mockup, which is itself marked "...to be continued" - needs real legal review before launch, not something to complete by guessing. Not yet cross-checked against the live site's `datenschutz` page. |
| Contact | Exists — verify against Figma's Contact frame. |
| Sidebar / nav | **Done (2026-07-29).** Rebuilt against the `Navigation6 Flip Yellow` variant — see the sidebar spec below. Fixed three latent bugs in the process, including a wrapper div with no styles that had silently disabled the sidebar's whole flex layout. |

**Key lesson from this pass**: Figma text content is unreliable and inconsistent in quality - sometimes verbatim-real (Links, Bio), sometimes a mix of real and fabricated-sounding entries (Timeline), sometimes just wrong (Press). The live site (`maja-explosiv.com`, a frameset-based TYPO3 site) is the actual source of truth for content per the site owner, and should be checked directly rather than trusting Figma's placeholder text - Figma governs structure/design only. All four About sub-pages plus Timeline are now sourced from the live site, not Figma.

**Architecture fix applied (2026-07-24)**: the homepage's About tabs (Bio/Timeline/Press/Links) were hardcoded as a duplicate HTML blob in `src/index.md`'s frontmatter, completely disconnected from `src/pages/about/*.md` (which had their *own*, different placeholder text). Rewired `src/_user/layouts/home.njk` to pull each tab from its real page via `collections.all | find("fileSlug", ...)` plus a new `excerpt` frontmatter field per page - same pattern the Projects tabs already used for collections. One source of truth per piece of content now; page bodies still need real content migrated in.

Also verify: the image carousel (Datastar-based, template feature) actually renders galleries per Figma spec; whether a "news feed" (mentioned in the original PRD/epics, and there's a `src/posts/news/` collection scaffold with one placeholder entry) is still in scope for this design or was dropped — not present in any current `design_screenshots`, needs a decision.

### Sidebar — extracted spec (2026-07-29)

Read from the Figma component `Assets / Components > SideBar Navigation`. It has six
variants; the current one is **`Navigation6 Flip Yellow`**, identified by the floating
`In Use` text label sitting directly above it. A file-wide search for "In Use" returns
7 hits: two `In Use` labels and five `Not In Use`. The other variants (`Tablet`,
`Mobile`, `Original Logo`, `Navigation5`, `Desktop`) are stale.

Shell (all already correct before this pass): 224px wide, 960px tall, padding 20px
top/bottom and 24px left/right, background `Grey/Semantic/Background` #B8B8B8, 1.13px
right border in #222222 (implemented as 1px).

| Element | Figma | Was |
|---|---|---|
| Wordmark | Mask group (vector), 188.32 x 27.69 footprint — no font size to read | text, 21.6px/700 |
| Subtitle | Geist 600, 14.01px, 162%, -3%, uppercase, #222222 | 12.8px, 400, +0.02em, #000 |
| Logo → nav gap | 80px | 40px |
| Gap between nav sections | 80px | 40px |
| Section heading | Geist **400**, 28px, 100%, -3%, uppercase, #222222 | 700, ~17px, +0.05em, #000 |
| Sub-item | Geist 400, 18px, 100%, -3%, uppercase, **#373737** | ~14.4px, +0.02em, #000 |
| Gap, heading → items and between items | 12px | ~3px |
| Footer credit | Geist 500, 18px, 119%, -3%, uppercase, **#B1B1B1** | 0.7rem, #EBEBEB |

The 12px gap checks out arithmetically: 28 + 4x18 + 4x12 = 148px, matching Figma's hug
for the Projects section; the nav block totals 405px and the implementation now measures
406px.

**Three latent bugs found while doing this:**

1. **`.sidebar-nav` had no styles anywhere in the codebase.** That wrapper div holds the
   header, nav and footer, so it was `.left-sidebar`'s only flex child — which made both
   `.left-sidebar { justify-content: space-between }` and `.nav-menu-container { flex: 1 }`
   completely inert. The footer stacked directly under the nav instead of sitting at the
   bottom of the sidebar. Fixed by making the wrapper the flex column.
2. **The footer graphic was the wrong asset** — see the asset note below.
3. **A global `li { padding-left: 8px }`** indented the sub-items further than the design.
   In Figma the sub-item and its section heading share a left edge; the ~4px that looks
   like an indent there is just glyph side bearing.

#### Sidebar footer brush — asset forensics

Worth recording because it was got wrong twice before and the reasoning is not obvious
from looking at the files.

- Figma's fill is named `upscale_image [Upscaled].png`. The repo already contained it,
  unreferenced, under a content-hash filename; renamed to `src/assets/images/sidebar-brush.png`
  (903x248).
- **That asset is mirror-symmetric about its horizontal centreline** — measured, its top
  half correlates **r = +0.996** with its flipped bottom half. It is the same fan doubled.
  Rotating the whole thing puts that mirror line down the middle of the sidebar, so the
  strokes splay both ways out of a black centre. That is wrong; the design uses a single
  fan with every stroke leaning the same way. Use **half** the asset.
- **`corner.png` (439x72) is precisely that half.** Correlated against the halves of the
  big asset: vs the top half rotated 180 degrees, r = +0.971 (x profile) / +0.993 (y);
  vs the bottom half flipped horizontally, r = +0.972 / +0.986. It is also strongly
  anti-symmetric itself (r = -0.798), confirming it is a single fan rather than a doubled
  one. So `sidebar-brush.png` is `corner.png`'s fan mirrored and upscaled.
- Implementation takes the half out of the upscaled asset rather than using `corner.png`
  directly: covering the sidebar needs a 3.1x upscale from corner.png's 72px edge versus
  1.8x from the big one. **Settled by measurement** (2026-07-29) in favour of the upscaled
  asset — see the resolved entry under "Open items needing input" for the numbers.
- **Final orientation: no rotation at all.** Several rotated variants were tried and all
  were wrong; the owner identified the correct one. The brush sits horizontally, exactly
  as the source image is drawn — strokes running left to right, dense end off to the left
  of the visible band. `transform: rotate(0deg)`, anchored `left: 0; top: 0`.
- **Superseded 2026-07-29 (evening): the crop is no longer guessed.** Everything above
  this point is the record of how it was reasoned out by measurement; the values below
  are read straight from Figma and replace the hand-tuned
  `background-size: 948px 260px / background-position: -185px -26px`.

#### Sidebar footer brush — derived from the Figma REST API (2026-07-29)

The crop had been tuned by eye across several sessions because Figma's properties panel
does not expose it. The REST API does. Node **`695:5735`** (RECTANGLE
`Frame 2147238582 3`) inside the In Use variant `695:5712` carries the visible fill:

```
scaleMode: "STRETCH"            <- what the Figma UI calls "Crop"
imageRef:  bd3f21a62c76e8ac3324d8e27543e5a566dccb83
imageTransform: [[0.26255646, 0, 0.22443195],
                 [0,        0.5, -5.04e-08]]
```

For a cropped fill that matrix is the visible window in normalised image space:
**x 22.44% → 48.70%, y 0% → 50%.** So the design uses the **top half** of the asset —
which confirms the earlier "use half of it" conclusion and, for the first time, states
which half and where the horizontal crop begins.

Box, relative to the 224 x 960 sidebar: **295.68 x 153.96 at x = -2.84, bottom flush**
with the sidebar's bottom edge. Converted to CSS (element W x H showing image fractions
fw, fh from fx, fy → `background-size` = W/fw x H/fh, `background-position` = -fx·bgW,
-fy·bgH):

```css
left: -3px; bottom: 0; width: 296px; height: 154px;
background-size: 1126px 308px;
background-position: -253px 0;
```

Three checks, none of them by eye:

1. **Asset identity settled by hash.** The `imageRef` downloads byte-identical
   (same SHA-256) to `src/assets/images/sidebar-brush.png`. The correlation forensics
   above are now corroboration rather than the only evidence.
2. **Self-consistent.** 1126/903 = 1.2470 and 308/248 = 1.2419 — a uniform 1.24x scale,
   0.45% apart, so no aspect distortion. The old warning still stands: any change to
   `background-size` must keep both axes on one scale factor.
3. **Silhouette matched against Figma's own rasteriser.** Rendered node `695:5712` at
   1x via `/v1/images` (a clean 224 x 960 PNG), reproduced what the CSS paints, and
   compared per-column top edges: **median 0px, p90 1px, r ≈ 0.94.** The handful of
   outliers move around as the darkness threshold changes — the signature of hairline
   stroke tips antialiasing differently between two renderers, not a geometric offset.

**`.sidebar-footer` must not clip.** It was `overflow: hidden`, which cuts the brush to
the 124px credit band. The brush is 154px tall and is meant to rise 30px above it: in
Figma the fill overflows its `Header` frame (`clipsContent: false`) and is cut by the
sidebar instead. Now `overflow: visible`, with `.left-sidebar`'s existing
`overflow: hidden` doing the clipping — same structure as the design.

- `corner.png` remains correct and untouched for its other uses (hero, project pages),
  where it is a thin sliver at the top.

### Sidebar audit — first run of the API method (2026-07-29)

First trial of `project_docs/figma-audit-guide.md`, comparing node `695:5712` against the
rendered sidebar at 224 x 960 (viewport 1440 x 960 so `height: 100vh` matches Figma's
960). **Six defects in a component this file had marked "done"** — all of it previously
signed off by eye. Nothing below is fixed yet.

**All six are now fixed or resolved — see the verification table at the end of this
section.** The findings are kept in full because the reasoning matters.

| # | Finding | Figma | Build (before) | Status |
|---|---|---|---|---|
| S1 | Sub-item colour | `#373737` (`VariableID:71:2973`) | `#525252` | fixed |
| S2 | Sub-item font weight | 400 | 500 | fixed |
| S3 | Sub-item left indent | text at x=34 (`paddingLeft: 10`) | x=24, flush | fixed |
| S4 | Nav block start | y=181 | y=150.27 (−30.7) | fixed |
| S5 | Wordmark footprint | 164 x 19.12 | text 169.09 wide | width fixed, **height still open** |
| S6 | Footer credit baseline | cap top y=906 | 900.9 (−5.1) | fixed |

- **S1 — fixed 2026-07-29.** `.nav-link` read `var(--theme-colors-text-secondary, #373737)`,
  but that token is `#525252` (Grey/600), so the fallback never fired and the rule rendered
  a colour its own comment contradicted. Note `#525252` *is* a real palette colour — this
  was the wrong token, not an off-palette value. Figma binds sub-items to Grey/700, which
  has no semantic alias; `theme.js` already carries it as `dark-gray`. Changed to
  `var(--theme-colors-dark-gray, #373737)`; verified rendering `rgb(55,55,55)`.
  Per the owner: **respect Figma and the palette, not the existing CSS.**
- **S2** — `_user`'s `.nav-link` never sets `font-weight`, so the base template's
  `main.css .nav-link { font-weight: var(--font-weight-5) }` (500) wins. A
  base-vs-override boundary leak of exactly the kind Phase 0 is auditing for.
- **S3 — this reverses an earlier conclusion in this file.** The sidebar spec above says
  "the sub-item and its section heading share a left edge; the ~4px that looks like an
  indent is just glyph side bearing", and `.nav-submenu li { padding-left: 0 }` was added
  on that basis, deliberately removing the base stylesheet's 8px. The API disagrees: each
  `Button sidebar` instance carries `paddingLeft: 10` and its text node sits at x=34
  against the heading's x=24. The indent is real and is 10px. The original 8px was closer
  to right than the "fix" that replaced it.
- **S4** — Figma's `Logo` frame is `layoutSizingVertical: FIXED` at 81px tall while its
  contents only fill 38.44px, so the 80px gap starts from y=101. The build's
  `.sidebar-header` hugs its content (ends at 70.26) before adding `margin-bottom: 80px`,
  landing the nav 30.7px high. This cascades: every nav row below is ~31px out.
- **S5 — smaller than first reported, and only half fixable.** The spec above records the
  footprint as 188.32 x 27.69 and the build was sized to land on it. That is
  `Rectangle 9`, the **mask source**, clipped by the mask and never rendered at that size;
  the wordmark renders at the `Mask group`'s 164 x 19.12. *My first measurement was also
  wrong*: I compared Figma's hug box against `.brand-title`'s **block** width (175), which
  is the container, not the text. The text was 169.09 — 5px over, not ~7%. Font size is
  now 21.4px, giving 164.41.
  **Still open:** the height cannot also match. 164 x 19.12 is far wider per unit height
  than Geist 800 sets, so matching the ink height would push the width past 200. Matching
  width was my judgement, not the design's instruction — closing the gap properly needs
  the exported SVG. See open items.
  *Method lesson:* for text, compare **ink extents** (via a `Range`), never block boxes.
  Same class of error as the `leadingTrim` trap.
- **S6 — confirmed against a 1x node render.** Figma's text box uses
  `leadingTrim: CAP_HEIGHT`, so y=906 is the cap top, not a line-box top. Rendering node
  `695:5712` at 1x and measuring the ink gives cap-tops at **y=906 and y=927**, cap-height
  13px both sides. The build's cap-tops (from `fontBoundingBoxAscent` + half-leading) were
  900.9 and 922.3 — **−5.1 and −4.7**, consistent across both lines, so a block offset
  rather than a leading error. Cause is exact: both sides bottom out at y=940, but Figma's
  trimmed box ends on the **baseline** while a CSS block ends on its **line box**; the
  difference is descent + half-leading = 4 + 0.71 = 4.71px. Fixed by taking
  `.sidebar-footer`'s bottom padding from 20px to 15px.

#### Verification after fixing (2026-07-29)

Measured at viewport 1440 x 960 so `height: 100vh` matches Figma's 960. Text positions
use ink extents and cap-tops from font metrics, not block boxes.

| Check | Figma | Build after |
|---|---|---|
| Sub-item weight / colour | 400 / `#373737` | 400 / `rgb(55,55,55)` |
| Heading ink x → item ink x | 24 → 34 (indent 10) | 24 → 34 (indent 10) |
| Logo block | y 20–101, h 81 | y 20–101, h 81 |
| Nav top / section 2 top | 181 / 409 | 181 / 409 |
| Wordmark ink width | 164 | 164.41 |
| Credit cap-tops | 906 / 927 | 905.9 / 927.3 |
| Shell | 224 x 960 | 224 x 960 |

Not confirmed by eye — the preview pane was not displayed, so screenshots timed out.
Worth a visual glance next session.

#### Tier 1 re-run with the relations method (2026-07-29, later)

Re-ran the sidebar as **tier 1** of the tiered plan in `figma-audit-guide.md` §9 —
coverage both directions, then *relationships* rather than absolute boxes. Two results
worth having:

**Coverage is clean.** Of 35 Figma nodes, exactly one has no build counterpart:
`Rectangle 9`, the wordmark's mask source, which never renders. Nothing in the design is
missing from the build.

**Two findings restated as broken relationships**, which is a better description than the
raw deltas the first pass produced:

- **S3 restated — the design has two content left edges, the build has one.** Figma puts
  22 nodes on x=24 and **9 nav sub-items on x=34**. The build puts all 34 visible elements
  on x=24. So this is not "a 10px padding is missing" on one item; it is that the
  heading/sub-item indent relationship does not exist in the build at all.
- **S4 restated — the gap is right, the block height is wrong.** Every declared gap
  matches (logo→nav 80, section→section 80, heading→item 12, item pitch 30). What differs
  is that Figma's `Logo` frame is `layoutSizingVertical: FIXED` at **81px** while its
  contents occupy only ~50, and the build's `.sidebar-header` hugs its content at
  **50.3px**. The 30.7px shift is a consequence, not the cause — fix the block height and
  everything below falls into place without touching any gap.

**Mechanism noted for the collision open item:** `.nav-menu-container` is `flex: 1` and
stretches to 685.7px, where Figma's equivalent hugs at 405px. That stretch is what lets
the nav run into the footer as the viewport shortens.

**Verified correct, no action:** 224 x 960 shell, 20/24 padding, 1px border, `#B8B8B8`
fill; section headings Geist 400/28px/-3%/`#222222`; the 12px gaps and 80px section gap;
section heights 148 and 177; footer band top at y=836; footer credit Geist 500/18px/119%/
-3%/`#B1B1B1`; subtitle Geist 600/14.01px/162%/-3%/`#222222`.

**Status:** the sidebar is no longer "done" — see S1-S6. The wordmark-as-vector question
also remains open.

### Homepage — tier 1 audit (2026-07-30)

Node **`52:6427`** (`Main container`, 1280x860, content overflows to 6524) against the build
at a **1295px viewport** — chosen so the layout width is exactly 1280 once the 15px
scrollbar is taken out. Getting that wrong shifts every x by 15px and silently narrows the
content column, so it is worth stating: **measure the homepage at 1295, not 1280.**

The design's structure, for the record:

```
52:6427  Main container          1280 x 860 (HORIZ)
  419:10288  SideBar Navigation   224 wide      <- an instance, scaled ~0.967; do NOT
  52:6430    Main content Contnr 1056 wide         re-derive sidebar values from it.
      padding L/R 24, bottom 138.8                 The canonical sidebar is 695:5712.
    120:7160  Landing Section    1008 @ x=248, padTop 178.47
    52:6457   Projects Gallery   1008 @ x=248, padTop 158.64
    120:6835  About Section      1008 @ x=248, padTop 174.00
    182:2812  Footer             1008 @ x=248, padBottom 38.67
  419:10287  Header (brush)       554.88 x 87.97 @ x=725  <- built, corner.png top right
```

Every section fills **1008 at x=248**. One spacing unit, **79.32 (≈80)**, generates nearly
every gap in the page: 79.32 between blocks, 39.66 = half, 59.49 = 0.75x, 158.64 = 2x,
96.67 and 174/178 as one-offs. **Coverage is otherwise clean** — no visible Figma node on
this frame lacks a build counterpart except the two noted under H2 and H12, and the build
invents nothing (`.hero-background` is a wrapper with no fill; `.home-content` is empty).

| # | Finding | Figma | Build | Bucket |
|---|---|---|---|---|
| H1 | **CTA is unreadable** — white text, no fill | (see H2) | `background-color: transparent !important` wins | fix |
| H2 | CTA structure and colours | 40.6px #1B1B1B disc + #FFCC00 chevron + dark label | black pill, white text, `↗` | owner |
| H3 | Hero paragraphs lose their token | 31.73/500 then 22.45/400 | both 17.6/400 | fix |
| H4 | Section headings | Geist 400, ~125px | 56px/700 | fix |
| H5 | Content column inset | 24px → column 1008 at x=248 | 32px → 992 at x=256 | fix |
| H6 | Category description | Geist 400, 25.78px | 16px | fix |
| H7 | Vertical rhythm | one 79.32 unit | ad-hoc 32/40/48/80 | fix |
| H8 | Hero block placement | anchored 178.47 below section top | centred in `100vh` | fix |
| H9 | Hero title line gap | 13.88 | 0 | fix |
| H10 | Footer typography and colour | see table below | ~half of it off | fix |
| H11 | Fourth font family in the file | CTA label is **Inter 500** | Geist | owner |
| H12 | Project card caption rows | 3 rows | 1 row | owner |

**H1 — the highest-value finding, and not a Figma one.** `main.css:131-138` sets
`background-color: transparent !important` on `.content-wrapper a, .main-content a, p a,
li a, h1..h6 a`. That `!important` beats `custom.css`'s `.cta-button { background-color:
#000000 }`, so the homepage's primary call to action renders **white text directly on
`#B8B8B8`** — about 2:1 contrast, effectively invisible. Confirmed by eye as well as by
computed style. Swept every anchor in `.main-content`: `.cta-button` is the only casualty,
so the blanket rule can be narrowed or dropped without collateral. This is exactly what
tier 2's "design-free invariants" check exists to catch, found early by accident.

**H2 — the design's CTA is not a pill at all.** The visible instance is
`388:5771 hover-interaction-3`: a 40.60px square/disc filled **#1B1B1B** containing a
white 2.03px line and a **#FFCC00** chevron, an 8.12px gap, then the label at
**Inter 500, 16.24px**, uppercase, **#1B1B1B**. The two sibling `Button` instances
(`843:11194`, `343:11918`) *are* dark pills with #EBEBEB Geist 600 text — and both are
`visible: false`, so they are drafts. This settles part of the off-palette open item:
#1B1B1B, #FFFFFF and #FFCC00 are all in the **rendered** CTA, not in hidden mock, so they
cannot be set aside as placeholder. Rebuilding the CTA needs those three decisions first.

**H3 — a token that never reaches the text.** `.hero-description` sets
`font-size: 22.45px` on the wrapper, but Open Props' normalize (`@import`ed by `main.css`)
sets a `font-size` on bare `p`. **A matching rule beats inheritance regardless of
specificity**, so both paragraphs render 17.6px. Same class as sidebar finding S2, and it
will recur anywhere a token sits on a wrapper around `<p>`. Figma wants two *different*
paragraphs: para 1 Geist **500 / 31.73px / lh 1.3 / −0.03em** in a 694px measure, para 2
Geist 400 / 22.45px / lh 1.1 / −0.025em across the full 1008. The gap between them is
39.66, the build has 20.

**H4 — headings are less than half the design size.** "Projects" is Geist 400,
**126.91px**, lh 1.2, −0.04em; "About" is Geist 400, **123.74px**, lh 0.74, −0.02em. Both
render as `.section-title` at 56px/700 with no tracking. Note the design's own two headings
disagree on line-height and tracking while agreeing on size to within 3px — flagged under
open items rather than normalised. The existing `padding-left: 48px` open item compounds
this: with H5 the heading ink starts **56px** right of the design's x=248.

**H5 — one systemic 8px offset, not four separate ones.** In Figma all four sections share
left edge 248 (`Main content Container` pads 24 inside 1056); in the build all four share
256 (32px padding). So the relationship is intact and the inset is simply wrong by 8, with
the column 16px narrow. **This bears on the `--about-shell-width: 1020px` decision of
2026-07-29**, which was read off the standalone component frames (`46:704` at 1220 wide,
`46:901` at 1299). Placed on the homepage those same components are 1008 (Projects) and
1018.25 (About tabs — which therefore overflows its own 1008 section, the artifact already
noted in the audit guide §8). 1008 vs 1020 is 1.2% and not worth chasing on its own; the
24-vs-32 inset is.

**H7 — the concrete gap mismatches**, all against the 79.32 unit:

| Gap | Figma | Build |
|---|---|---|
| Section heading → tab bar | 79.32 | 40 |
| Tab bar → category description | 59.49 | 80 |
| Category description → image grid | 59.49 | 32 |
| Image grid columns | 23.79 | 32 |
| Featured (landing) grid columns | 24.0 | 32 |
| About title → intro | 96.67 | 40 |
| About intro image → text | 79.32 | 48 |
| About intro → tab bar | 79.32 | 48 |
| Featured card image → caption | 14.0 | — |

Also: the About intro image is **345.03 x 260.04** in Figma against 308 x 229 built, and
its text column **524.16** wide against 621, with a 59.49 right pad the build lacks.

**H8/H9 — the hero.** `.hero-section { min-height: 100vh; align-items: center }` centres
the text block, so its position tracks viewport height; Figma anchors it with
`paddingTop: 178.47` and lets the section hug. At an 860px viewport the title lands at
271.4 against the design's 178.5, and the knock-on is that the featured grid starts ~156px
low. Within the title, `Title container` has a **13.88** gap between the "MAJA" and
"EXPLOSIV" line boxes; the build stacks them flush. Everything else about the two title
lines already matches exactly (85.94/700 and 77.29/500, lh 0.74, −0.02em, #222222) — that
part of the 2026-07-24 extraction holds up.

**H10 — footer.** The three-row structure, the two separators, the right-hand logo slot and
all six labels are correct. The values are not:

| Item | Figma | Build |
|---|---|---|
| Row-1 text | Geist 500, 16px, −3%, #222222 | 12px/400, #000, +0.6px on the location only |
| Brand line | "MAJA" Geist **800** + " EXPLOSIV" Geist **600**, 41.94px | 48px/500 with `<b>` at 900 |
| aka line | Geist 600, 24.46px, #222222 | 16px/400, #333 |
| Bottom nav | Geist 500, 16px, −3%, #222222 | 17.6px/400, #000 |
| Separator | 0.32px hairline #222222 | 2px #808080 |
| Row left edge | 248, flush with the column | 272 (48px inset) |
| Above / below | 0 above, 138.8 below | 80 above, 40 below |

The brand line's two-run structure is right and worth keeping: **MAJA at 800, EXPLOSIV at
600** — the same pairing as the sidebar wordmark, which is useful corroboration for the
open question about turning that wordmark into a vector.

**H12 — the card caption.** Figma's `Project Card` caption frame (59.53 tall, 14 below the
image) holds **three** rows: title+year, title+year, title+info. The build renders one
(title+year). The row *labels* are Figma placeholders so the content is not evidence, but
three rows versus one is structure. Card proportions are close: 492 x 327.52 (1.502) in
Figma, 480 x 324 (1.481) built.

**Verified correct, no action:** page background `#B8B8B8` on every section; hero title and
subtitle typography; the tab bars (Geist 400 / 32px / lh 1.2 / −0.04em, #222222 active,
#8E8E93 inactive) — the 2026-07-29 tab work holds, and the only remaining difference is the
column offset from H5; the top-right `corner.png` brush; the featured grid's staggered
second column; the footer's structure and labels; the 3-column category grid.

#### Fixed, and verified after (2026-07-30)

Everything except H11 and H12 is fixed; those two need the owner and are in *Open items*.
Measured at a 1295px viewport. Text is compared by **cap-top**, from Geist's own metrics,
wherever Figma trims a box to cap height — comparing those to CSS line boxes is the
`leadingTrim` trap from the audit guide §8 and would report ~10px errors that are not there.

| Check | Figma | Build after |
|---|---|---|
| Content column, all four sections | 1008 at x=248 | 1008 at x=248 |
| Hero title / subtitle box tops | 178.47 / 256.35 | 178.0 / 255.5 |
| Hero lead cap-top | 392.67 | 392.3 |
| Hero body cap-top | 537.32 | 536.3 |
| CTA box | 209.72 x 40.60 at y=592.45 | 209.3 x 40.6 at y=591.1 |
| CTA disc / label gap | 40.65 disc, 8.12 gap, label 161 wide | 40.6 / 8.2 / 160.6 |
| Featured grid top | 712.37 | 711.7 |
| Projects: section top → heading cap-top | 158.64 | 160.0 |
| Projects: heading → tab bar | 79.32 | 80.0 |
| Projects: description → image grid | 59.49 | 60.0 |
| About: section top → heading box top | 174.00 | 174.0 |
| About: heading → intro | 96.67 | 96.0 |
| About: intro image | 345.03 wide at x=248 | 345.0 at x=248 |
| About: intro text | 25.13px at x=672.35 | 25.13px at x=673.0 |
| About: intro → tab bar | 79.31 | 80.0 |
| Section → section gaps | 0 (each section's own top padding) | 0 |
| Footer rows | flush at x=248, Geist 500/16px/−3%/#222222 | as designed |
| Footer brand | MAJA 800 + EXPLOSIV 600 at 41.94px | as designed |

**One class of difference is left uncompensated on purpose.** Gaps that run from a
cap-trimmed Figma box to the next element are implemented at their nominal design value
rather than adjusted for the ~6px a CSS line box adds below the last baseline. The hero
chain *is* compensated — its errors were the largest and most visible — so its margins carry
odd numbers (70 / 25 / 35 instead of 80 / 40 / 40) with the arithmetic in the comments. The
worst residual elsewhere is the Projects category description at **+6.9px**; everything else
is under 2px. Compensating every gap would mean a dozen values that drift with font
metrics, for less than the owner's stated tolerance.

**Three things found while fixing, and fixed:**

1. **The About Bio panel had H3's defect too** — `.about-prose` set 26px on the wrapper, so
   Open Props' `:where(p,ul,ol,dl,h6){font-size:…}` won on the paragraphs and the Bio text
   rendered at 17.6px. Confirmed from the normalize source, not inferred. Fixed with
   `font: inherit` on `.about-prose p`. The other three About panels set type on the
   elements themselves and were already correct (17 / 19 / 17px as the spec records).
2. **`main.css` was styling Maja's hero.** `.hero-section`, `.hero-background` and
   `.hero-content` rules in the base stylesheet drew a bordered, rounded, padded box with
   its own `corner.png` and capped the text at `min(900px, 70vw)`. Most of what
   `custom.css`'s `.hero-background` declared existed only to cancel them. Both sides
   removed; the border became visible the moment the cancelling declarations went, which is
   how it surfaced.
3. **A pre-existing mobile overflow.** `.hero-title span:last-child` carries an explicit
   77.29px and the ≤768px rule only scaled `.hero-title`, so "EXPLOSIV" stayed at desktop
   size on a phone — 370px of unbreakable word, forcing 35px of horizontal overflow at
   375px wide. Now steps down at both breakpoints (4rem/3.6rem, 3rem/2.7rem — proportions
   kept, since mobile is not in Figma). At 375px `scrollWidth` now equals `clientWidth`.

**`!important` swept out of both stylesheets** (owner's instruction, 2026-07-30): 9 in
`custom.css` and 7 in `main.css`, leaving none in either. The justification is uniform and
checkable: **every rule in Open Props' normalize is wrapped in `:where()`, which has zero
specificity**, so any real selector already beats it — verified by reading the shipped
`normalize.min.css`, not assumed. That covers the `pre`/`code` background and the base
footer's `max-inline-size` overrides. The sidebar's four
`text-decoration/border-bottom: none !important` pairs were fighting `main.css`'s
`.nav-link`, which they outrank simply by loading later at equal specificity; verified inert
by a computed-style snapshot of all 11 nav links before and after — every value identical.
The one that was doing real damage is described under H1.

### About Components — extracted spec (2026-07-29)

Read directly from Figma, from the location the owner specified: **`Assets / Components` → the floating text label `About Components` → the frame beneath it, `Timeline_Press_Links_Content Container`** (node `46-901`, 1299 × 12686). A file-wide search for "About Components" returns exactly one hit — a Text layer (node `922-5934`), confirming it is a spatial label, not a container.

The container holds one component with a `Section` variant property. Variants, in vertical order by `Top`:

| Variant | Top | Height | Status |
|---|---|---|---|
| `Bio` | 288.7 | 643 | current |
| `Timeline` | 1260 | 1762 | current |
| `Old - Press Option 01` | 3216.2 | 2656.8 | **stale — ignore** |
| `Press Option 2` | 6072.8 | 3924.84 | current |
| `Links` | 10024.8 | 2561 | current |

Note the staleness convention here is an `Old - ` name prefix, *not* the `In Use` label used for the sidebar variants elsewhere in the file.

**Shell, identical across all four current variants:** vertical flow, fixed **1020px** wide, `Left: 100px`, **80px gap** between tab bar and content, 60px bottom padding.

**Tab bar** (`Title`): horizontal, fill 1020px, height 38px, `justify: space-between`. Labels are sentence case — Bio / Timeline / Press / Links. Geist 400, 32px, 120% line-height, −4% tracking. Active `#222222` (Semantic/Primary Text Color); inactive `#8E8E93` (Semantic/Inactive Element). No underline, no background, no box. Inactive labels carry an `On click → Change to <Section>` interaction — the design models the tabs as a variant swap.

**Bio:** body Geist 400, 26px, 120%, −4%, `#222222`, in an **840px** column inside the 1020px shell. The panel begins at *"Her experience in stage arts…"* — paragraph 1 of the bio is deliberately absent, because it lives in the About intro above the tab bar. Confirmed by the owner 2026-07-28.

**Timeline** — each row is horizontal, fixed 62px tall, with a 244px gap between the year and the text column:

| Column | Typography | Width |
|---|---|---|
| Year | Geist 400, 16.59px (→17), 120%, −2%, `#222222` | 37px |
| Title | Geist 400, 24px, 120%, −4%, `#222222` | 739px |
| Description | Geist 400, 17px, 100%, −4.5%, `#222222` | 739px |

37 + 244 + 739 = 1020 exactly. Section headings ("A partial chronology of experience", "Schooling"): Geist 400, 22.66px (→23), 100%, −3%, uppercased via CSS, at **60% opacity** on `#222222`.

**Press:** a real design does exist, contrary to the earlier note in this file — the retired `press.png` export was simply a mislabelled duplicate of `links.png`. Structure: tab bar → section description container (horizontal, fill 1020px, 60px gap) → **Responsive Image Gallery** (horizontal, fill 1020px, **24px gap**, 3 columns ≈ 324px each) of the actual scanned clippings → a text list of mentions. The description line reads "The links below open a larger, readable version of each press article in a new tab:".

**Links:** tab bar → an overall `Section title` ("Friends and related artists:", 60% opacity, same style as the Timeline section headings) → per-category headings → entry lines with inline underlined anchors. Matches the existing `linkCategories` data shape (`text` / `name` / `url` / `suffix`).

### Projects (category) tab bar — matched to the About tab bar (2026-07-29)

Figma draws the two bars identically. Confirmed against
`figma-exports/projects-gallery-section__46-704.png` (node 46:704) and
`figma-exports/about-01-bio__46-901.png`: in both, the bar runs x=100..1119 — a 1020px
span — with Geist 400 / 32px / 120% / −4%, sentence-case labels, active `#222222`,
inactive `#8E8E93`, no underline, border or background.

The Projects bar was 16px, `rgba(0,0,0,.4)` inactive / pure black active, no tracking, and
padded `0 3rem` inside a 1137px section, so its labels started 48px right of where the
About labels start.

Done in `custom.css` by **extending the existing About tab-bar selectors** to also match
`.projects-tabs .tab-buttons`, rather than restating the values — tab typography was
already declared in three places in that file and a fourth copy would have made the known
duplication problem worse. Both bars now measure identically in-browser (left 256, width
1020, 32px, −1.28px tracking, `rgb(34,34,34)` / `rgb(142,142,147)`), and were checked by
eye as well as by computed style.

The mobile (≤768px) rules now give the Projects tabs the same 1.5rem/wrap treatment as the
About tabs, replacing their old 0.875rem. Confirmed correct with the owner: there was never
a reason to think the two bars should diverge on mobile.

**Second pass, same day — the whole Projects section, plus a stale-code sweep.**

Measured off `figma-exports/projects-gallery-section__46-704.png` by scanning for the
leftmost/rightmost non-background pixel per band (the export has a transparent background,
so it has to be composited onto white first or everything reads as black):

| Band | Figma extent | Width |
|---|---|---|
| Tab bar | x=101…1118 | 1018 |
| Category description | x=101…924 | 824 |
| Image grid (sampled at three heights) | x=100…1119 | 1020 |

So the Projects section sits on the same 1020px column as About, with the description on the
same ~840px prose measure as the Bio panel. The build had `.projects-tabs` at 1057px, the
description capped at 800px with a 3rem inset, and `.posts-grid` with the same 3rem inset —
pushing both 48px right of the tab bar. Now: `.projects-tabs, .about-tabs` share
`max-width: var(--about-shell-width)`, and the description and grid lose their insets.
Measured after: tab bar 256/1020, description 256/840, grid 256/1020 — matching About's
256/1020 and 256/840 exactly.

**Stale CSS removed.** `.tab-button` appears in exactly two places in the whole site (the
two bars in `home.njk`; `main.js` only reads the class, never styles it), so once both bars
were styled from the shared rule the generic `.tab-buttons` / `.tab-button` / `:hover` /
`:focus` / `.active` blocks and their `@media (max-width: 768px)` counterparts were fully
shadowed. Deleted — about 60 lines.

Four declarations in them were **not** cosmetic and were folded into the shared rule first:
`margin: 0`, `flex: 0 0 auto`, `text-decoration: none`, `box-shadow: none`. Without them the
base template's `main.css` (`.tab-button` padding, and an active/focus `border-bottom` in
`--color-primary`) and Open Props' `:where(button)` box-shadow would have surfaced.

Verified the deletion is inert the same way the `custom.css` de-duplication was: a 33-property
computed-style snapshot plus box geometry for both bars and all eight buttons, taken before
and diffed after. The only differences were `max-width: 1020px → none` on the bars (the cap
moved to the parent, widths unchanged) and `gap: 0px → normal` (identical computed value for
a flex container). Every colour, font, border, shadow, outline and flex value unchanged.

One thing deliberately **not** changed, because it is not Projects-specific: `.section-title`
carries `padding-left: 48px`, so the "Projects" and "About" headings both sit 48px right of
their own tab bars. Figma has the heading flush with the column (x≈111 for "Projects" is
glyph side bearing off 100). Fixing it touches both sections equally — worth doing, but as
its own change rather than folded into this one. Logged under open items.

#### Timeline data format required by the migration

The Figma layout needs three fields per entry. The current `src/pages/about/timeline.md` has two (`date` + one prose blob with the title embedded), and uses month precision where Figma shows year only. **The extraction script should be changed to emit this shape** when the timeline content is migrated for real:

```yaml
timelineSections:
  - heading: "A partial chronology of experience"
    entries:
      - year: "2024"          # year only — Figma's left column shows no month
        title: "Die grosse Hafensszene"
        description: "The 4,5 x 2m metal drawing of the bigger harbor scene, for the dining room of Seminarhaus Kulturkosmos, Lärz, North Germany."
```

Until then the About work uses a small number of hand-converted entries as mock content, per the owner (2026-07-29): "if you need content in a different format, change some content and use it as mock content. We will change the migration script to meet the desired format in due time." The full 85-entry set stays in its current two-field shape and is **not** to be hand-migrated.

## Phase 3 — Content & image migration at scale

Current state (verified by running the build, not just reading old status docs):

- **26 of ~71** TYPO3 projects converted to Markdown: 7/28 sculptures, 6/26 installations, 6/9 performance, 7/8 paintings.
- Of those, only **paintings and one sculpture (Sisyphos Gate)** have images actually wired into front matter. Installations and performance have **zero** images linked even where the post exists.
- "Breath under Water" (the previously-missing painting): resolved — it's a whale sculpture miscategorized under paintings in TYPO3. Excluded from paintings; to be migrated later under sculptures/installations.
- Bio/Press/Links/Timeline text content is done (transcribed from the live site). What remains for this cluster is assets and the Timeline field split.
- **Press clipping scans located (2026-07-29): `old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja/presse/`** — 49 files, 47 JPG + 2 PDF (`2007_Alchemy_Bar_-_Wired_A4.pdf`, `2012_Wacken_Scull...pdf`; `2013_Destroy_HIV` exists as both). Filenames are already year-prefixed (`2004_casino1.jpg`, `1993_wohlgrott.jpg`), which maps cleanly onto the entries in `src/pages/about/press.md`. Note the spelling in the backup is `wohlgrott` vs. `Wohlgroth` in the page content. Six have been copied to `src/assets/images/shared/press/` as **placeholders only** — renamed to slug form, unoptimised (3.8 MB for six; the full set will need resizing before it ships). The remaining 43 are part of the bulk asset migration, not of the About work.

Once Phase 2 templates exist, resume the proven extraction scripts (`scripts/extract_typo3_projects.py` etc.) to migrate the remaining ~45 projects and wire up their images the same way paintings were done.

## Phase 4 — Verification & cutover

- Build/link/image integrity checks across all migrated content.
- Visual comparison against Figma and against the live site at maja-explosiv.com.
- GH Pages progress deploy (deferred — revisit when Phase 2/3 have something worth showing).
- VPS/production cutover (deferred — details TBD).

---

## Open items needing input

**This section is the single list for open questions of this kind.** When something needs the owner's judgement — a design inconsistency, an ambiguous spec, a content decision that can't be settled from Figma or the live site — record it here rather than in a new file or inline in a template comment. Resolved items get struck through with the resolution, not deleted, so the reasoning stays visible.

- [ ] **Links section uses a different font from everything else.** In the current `Links` variant of the About Components container, entry lines are **Rethink Sans** 400, 19.31px, 168% line-height, −2% tracking — while the tab bar, Bio and Timeline are all Geist, and Phase 1 round 3 concluded "Geist everywhere". Each category's entries are a single concatenated text node with link spans inside, which reads like pasted content that kept its own styling rather than a deliberate third font. **Resolved for now (owner, 2026-07-29): use Geist**, and note the inconsistency here in case the designer intended otherwise. Rethink Sans is not loaded by the site and should not be added without a decision.
  - **More instances found 2026-07-30 on the homepage frame**, which supports the "pasted content" reading rather than a deliberate second family: the **About-intro description** (`91:2988`, Rethink Sans 400 / 25.13px) and the footer's **Impressum** label (`I182:2812;52:6471`, 15.47px) — while its siblings Sitemap and search are Geist 500. Note also that the footer brand line's *default* style is Rethink Sans and is then 100% overridden to Geist per character, i.e. the same trap §8 of the audit guide warns about. Assumed covered by the same "use Geist" resolution; say so if not.
- [ ] **A fourth font family: the homepage CTA label is Inter.** `I388:5771;388:5734` in the visible CTA instance reads **Inter 500, 16.24px**, resolved through the override table so it is not the `style`-block trap. Inter appears nowhere else in the frames read so far, and Phase 1 explicitly retired it as "never a confirmed value, just an old guess". Presumed to be Geist 600 like the hidden pill variants, but that is a guess, not a reading. Blocks the CTA rebuild (H2).
- [ ] **The two homepage section headings are styled differently in Figma.** "Projects" (`I52:6457;46:707`) is Geist 400 / 126.91px / lh 120% / −4%; "About" (`91:2984`) is Geist 400 / 123.74px / lh 74% / −2%. Same family and weight, sizes 3px apart, but the line-height and tracking differ enough to change how each sits. One token or two? Rendered as Figma has them until decided (guide §7 bucket 2).
- [ ] **Figma's project card caption has three rows; the build renders one.** The `Project Card` component's caption frame is 59.53 tall and holds title+year, title+year, title+info. The row contents are placeholder, so what the second and third rows are *for* (medium? dimensions? photo credit?) cannot be read off the design — and the build's real data currently carries title, year, description and author. Needs a content decision before the card can be built to the design.
- [x] ~~**Sidebar footer brush: use `corner.png` or half of `sidebar-brush.png`?**~~ **Resolved 2026-07-29 by measurement: use half of `sidebar-brush.png`.** Per pixel at native size `corner.png` is sharper (mean |gradient| 27.5 vs 20.2), but that is just its edges packed into fewer pixels. At the size the sidebar actually renders (903x124) the ranking inverts: the brush half scores 20.2 against 16.9 for `corner.png` Lanczos-upscaled 2.1x, with slightly less halo (7.65% vs 7.87% of pixels neither opaque nor clear). So the upscale is not merely interpolated — it reconstructs edges better than resampling the small asset ourselves. A search of the TYPO3 backup for any third brush asset found nothing (20 hits, all webalizer stats graphs). **Fully closed 2026-07-29 (evening):** the `imageRef` on the Figma fill downloads byte-identical to `sidebar-brush.png`, so the asset choice is settled by hash rather than by inference, and the crop that was previously tuned by eye is now read off the fill's `imageTransform` — see the sidebar brush section above.
- [ ] **Sidebar wordmark is a vector in Figma, live text in the build.** Figma draws "MAJA EXPLOSIV" as a Mask group with a 188.32 x 27.69 footprint, so there is no font size to copy; it is currently set as Geist 800/22px to land on roughly that footprint. Decide whether it should stay as text (accessible, selectable, no extra asset) or become an exported SVG matching the design exactly.
- [x] ~~**`custom.css` has a large block of pre-existing duplicated rules.**~~ **Done 2026-07-29** (commits `8c09be3`, `88d5ca5`). The file had 217 top-level selectors with 34 declared more than once, the repeats concentrated in one region (~753-955) restating the hero / tab / custom-section / artwork rules from ~380-752. Cleared in three passes, each chosen to be provably cascade-neutral: 12 rules re-declared verbatim later, 41 declarations shadowed by a later rule with the same selector (skipping `!important`), then the 9 rules left empty plus two stubs. The four selectors that looked "divergent" in the initial survey turned out to be complementary fragments — different properties, not conflicting values — so they were folded into single definitions rather than needing a decision. 217 → 197 rules, 2182 → 2000 lines. Only `:root` is still declared twice, deliberately, with a comment at the first pointing to the second. Verified with a full computed-style snapshot (48 properties plus box geometry for every element) across 7 page/viewport combinations, diffed after each pass — all zero changes.
- [ ] **Off-palette greys in the design — all of these are the owner's calls, none are mine.** Corrected 2026-07-29: an earlier version of this entry stated a "rule" that off-palette values should be snapped to the nearest listed one, and used it to strike `#000000` off this list. **That rule does not exist.** The owner may choose to snap a value; the agent must not, and must never use snapping as grounds either to change something or to leave it unchanged. Until the owner decides, **the build should render what Figma renders** and the inconsistency stays flagged here. Scan of four canonical frames (Project Page, Contact Overlay and Impressum still to do — Figma rate-limited):
  - **`#000000`**, 20 uses, unbound to any variable. Includes the **sidebar ABOUT heading** — while its sibling PROJECTS heading is `#222222` bound to Grey/800 — plus the homepage About heading and Projects Gallery card titles. The build currently renders `#222222` for the sidebar heading, i.e. it does *not* match Figma. Not changed, because doing so would make two sibling headings different colours, which is precisely the open question below.
  - **`#1B1B1B`**, homepage "LETS GET IN TOUCH" button fill and label. Nearest `#222222` Grey/800.
  - **`#FFFFFF`**, homepage `Line 2` vector stroke. Nearest `#EBEBEB` Grey/0; pure white may be deliberate for a hairline.
  - **`#FFCC00`**, homepage `Vector` stroke. No yellow exists in the palette at all; the sidebar variant is named "Navigation6 Flip *Yellow*", so an accent may be intended but has no token.
  - **Sharpened 2026-07-30:** those three all belong to **one element** — the visible homepage CTA, `388:5771 hover-interaction-3` (disc fill #1B1B1B, chevron #FFCC00, cross-line #FFFFFF, label #1B1B1B). They are not scattered and they are not in hidden mock: the two dark-pill `Button` alternatives beside it are `visible: false`.
  - **Two of the three are now rendered, on the owner's instruction to update the CTA to the current design (2026-07-30).** `#1B1B1B` and `#FFCC00` are carried as `--theme-colors-cta-fill` and `--theme-colors-cta-chevron` in `theme.js`, commented as off-palette and unbound. They stay listed here because rendering them is not the same as deciding they belong in the palette — in particular `#FFCC00` is still the only yellow anywhere and has no token of its own. **`#FFFFFF` turned out not to be rendered at all:** it is `Line 2`, a zero-height vector sitting 5px outside the CTA's clip, and Figma's own rasteriser omits it from both the 30x30 and the 210x41 SVG export. It reads as part of a hover animation. Nothing to decide unless the hover state gets built.
  - Believed **out of scope rather than decided** — confirm if you disagree: `#193AF6` on "$5,200.00 2024" style labels is mock content (prices do not exist on this site), and `#060501` is the wordmark's mask source, which never renders.
- [ ] **Sidebar sub-item colours are inconsistent inside Figma itself.** Reading the fills off node `695:5712`: Sculptures `#373737`, Installations `#373737`, Performance `#222222`, Paintings `#222222`; then Bio `#222222`, Timeline `#222222`, Press `#373737`, Links `#373737`, Contact `#222222`. No pattern — not first/last, not alphabetical, not per section — and two of the nine are not bound to a colour variable at all, which reads like hand-editing rather than intent. This file records `#373737` as *the* sub-item colour. Is that right, or is a state (visited/current) being modelled? Blocks finding S1 in the sidebar audit above.
- [ ] **Sidebar nav and footer have no minimum gap, so they collide on short viewports.** Noticed 2026-07-29 at a 588px-tall viewport: the "TIMELINE" nav item runs into the top of the footer brush. `.left-sidebar` is `height: 100vh` with `justify-content: space-between`, and `.sidebar-nav` is `flex: 1` — so as the viewport shortens, the nav block and the 124px footer are pushed into each other with nothing to stop them. Figma only draws the sidebar at 960px tall, so the design says nothing about what should give first: the nav could scroll, the sections could tighten their 80px gaps, or the footer could shrink. Needs a decision, not a guess. Unrelated to the brush work — it predates it.
- [x] ~~**`.section-title` is indented 48px from its own section's content column.**~~ **Fixed 2026-07-30** as part of finding H4, which had to touch both headings anyway: the 48px `padding-left` is gone and both now sit flush at x=248 with the rest of their section. The asymmetry worry that deferred it does not apply when both change together.
- [ ] **How exact should gaps be where Figma's box is cap-height-trimmed?** Figma trims many text boxes to cap height (`leadingTrim: CAP_HEIGHT`), so its box ends on the baseline while a CSS line box ends ~6px lower, at the bottom of the descender plus half-leading. A gap implemented at its literal design value therefore renders ~6px larger than drawn, and the error accumulates down a column. **Current state (2026-07-30):** compensated in the homepage hero, where it was largest and most visible — its margins read 70 / 25 / 35 instead of 80 / 40 / 40, with the arithmetic in the CSS comments — and *not* compensated anywhere else, so those gaps carry the nominal design value. Worst residual is the Projects category description at **+6.9px**; every other gap on the homepage is within 2px. The trade-off: compensating everywhere buys exactness but replaces a handful of clean tokens with a dozen derived numbers that drift if the font's metrics change, all for less than the stated "34.95 may as well be 35" tolerance. Three ways to settle it — accept the residual as-is, compensate everywhere, or wait for `text-box-trim` to be safe to rely on (Baseline-newly-available; the audit guide currently rules it out) and let the browser do it exactly. Needs a preference, not a guess; it will come up on every surface still to be audited.
- [ ] **A share of what the audits keep finding belongs upstream in `explosive`, and is being fixed only here.** Several findings were base-template defects, not Maja ones, and were fixed in this repo's `src/assets/css/main.css` — which CLAUDE.md §6 explicitly permits, since our copy has already diverged from upstream (1048 lines there vs ~1250 here). But the fixes are generic and every site built on the template has the bugs:
  - the `!important` blanket on anchor backgrounds that made a link impossible to style as a button (finding H1);
  - `.hero-section` / `.hero-background` / `.hero-content` styling Maja's specific hero from inside the base stylesheet;
  - seven further `!important`s that only ever fought Open Props' zero-specificity `:where()` rules;
  - `.content-wrapper p, li { margin-inline: auto }`, which silently centres list items — recorded in this file since 2026-07-24 and still present;
  - the wider pattern: base rules that set type on bare `p` / `.nav-link` / `.tab-button` and quietly beat a `_user` token (findings S2, H3, and the About Bio panel).
  **Decision needed:** whether to port these to `Xpanda-org/explosive-11ty` now, or keep banking them here and reconcile in one pass later. Porting now means the two copies diverge less and other sites benefit; banking means not interrupting the audit. Either way it should be a deliberate choice — right now it is simply not happening. Related: Phase 0's base-vs-override boundary audit, which is the same problem from the other direction.
- [ ] Figma exact-value extraction — access pending.
- [ ] News feed: in or out of scope for this redesign?
- [ ] `docs/` folder (GH Pages build output) currently shows as deleted-but-uncommitted in `git status` — left untouched for now per "forget GH Pages for now."
- [ ] VPS/production host details — deferred.
- [ ] **Grayscale-on-hover image treatment — needs a real decision, not a guess.** `.featured-project-image` (top 4 homepage thumbnails) already had `filter: grayscale(100%)` → color-on-hover before this session; extended the same pattern to `.project-image img` (the main Sculptures/Installations/Performance/Paintings grid) after seeing grayscale project photos in Figma's Present/prototype mode. But checking further, Figma itself is inconsistent: the same Sisyphos Gate photo appears **in full color** near the top of the Sculptures grid and **in grayscale** in what looks like a duplicate/alternate card instance further down - same pattern as this file's other duplication issues (duplicate bio text, duplicate press.png/links.png exports). Owner note: "I may have added it to the thumbnails by mistake... if I added it there it was probably for a reason." Left both grayscale implementations in place rather than reverting on inconclusive evidence - resolve by checking with whoever has final say on the design (Maja/designer), not by more Figma spelunking.
