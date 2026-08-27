# Maja Explosiv — Redesign & Migration Plan

**Status document owner:** this file is the current source of truth for where the project stands and what's next. It supersedes `RESUME-WORK-HERE.md`, `MIGRATION-STATUS-REPORT.md`, and the various session-summary docs, which have been moved to `project_docs/_archive/` (see `_archive/MANIFEST.md`) rather than deleted.

**Last updated:** 2026-08-27

---

## Resume here (2026-08-27)

**Everything that needs your judgement is in one place: § _Open items needing input_, at the
bottom of this file. 41 open items.** Nothing is filed anywhere else. Where the detail is
too long to sit in that list, the item names the document that holds it — every such document
is linked from here or from `project_docs/DOCS.md`, which indexes all of them.

**Content migration — Stage 6 (murals) is done.** 3 projects, 40 images, verified 3/3 against
the live site on heading, description, every caption, **and gallery order**. Stages 7–14 not
started. Per-stage detail: `migrated-content/README.md`; method and decisions:
`migrated-content/projects/SOURCE.md`; the remaining brief: the HANDOFF section at the end of
`project_docs/content-migration-plan.md`.

**Two bugs found and fixed this session, both of which passed every existing check:**

- **Galleries were in the wrong order.** They order by `tx_dam_mm_ref.sorting_foreign`, not
  `tx_dam.sorting`. Right images, right captions, right count — only the sequence wrong, which
  does not look broken. `verify_projects.py` now compares the *order* against the live page for
  every stage. All 1006 site images were renumbered and re-verified pixel-identical to the
  archive.
- **GitHub Actions could never have deployed.** `cache: npm` hard-fails without a committed
  lockfile, at a step before the fallback could run. Fixed upstream; the lockfile is now
  committed here.

**The two defects that blocked project pages from *looking* right are fixed** (2026-08-27) —
empty image captions and 0-byte collection pages. Both were pre-existing, not caused by the
migration, and invisible until there was content to reveal them. Every changed value is
recorded with its previous value in Phase 2 § *Project Page & collection pages — build
corrections*. Fixing the second caught a third problem: the layout would have published the
template's placeholder copy ("Two-dimensional painted works") over Maja's own prose.

**The Project Page Figma spec is extracted and the frame verified** — Phase 2 § *Project Page —
extracted spec (2026-08-27)*. Geometry, type, the caption contract, what happens past the ninth
image, and the traps hit reading it.

---

## Resume here (2026-07-30)

**Homepage tier 1 is done and, apart from two items that need the owner, fixed.** Findings
H1–H12 and the after-verification table are under Phase 2. The CTA is rebuilt to the current
design; the column, section headings, hero, category description, all nine gaps and the
footer are corrected and re-measured; `!important` is gone from both stylesheets.

**Published.** Commits `923afff` (fixes) and `2b38c82` (docs rebuild) are on `main` and live
at <https://consistent1.github.io/maja-explosiv/> — Pages build `built`, verified by fetching
the live HTML and CSS. Working tree clean, `_site` rebuilt without the path prefix so the
local server is usable again.

**Still waiting on the owner** — in *Open items needing input*, six live questions: the CTA
label reads **Inter** in Figma and was built in Geist; what the project card caption's 2nd and
3rd rows are for; whether the two section headings are meant to be styled differently;
`#FFCC00` still has no palette token even though it now renders; **how exact to be about gaps
that start from a cap-height-trimmed Figma box**; and **whether to port the generic
`main.css` fixes upstream to `explosive`** rather than only fixing them here. The last two
were added 2026-07-30 and both affect how the remaining surfaces get audited, so they are
worth settling before the next tier-1 pass.

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
3. ~~GitHub Pages and the VPS/production host are both **deferred**~~ — **GitHub Pages is live as of 2026-07-30**: <https://consistent1.github.io/maja-explosiv/>, served from `main` at path `/docs`, so committing a rebuilt `docs/` and pushing *is* the publish. The VPS/production host is still deferred (provider, deploy method TBD). How the deploy interacts with the local dev server is documented in `README.md` § *Serving, building and deploying* — it is not obvious and it has caused confusion twice.

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

#### 5. Hero image was repeated as the first gallery image — fixed

`project.njk` set the hero from `featuredImage` (which the converter fills from `images[0]`)
and then began the gallery again at `images[0]`. Every project showed image 1 twice in a row,
and once captions were wired, its caption twice.

Introduced `galleryImages` — `images` with the hero removed — and pointed all three gallery
sections at it instead of `images`. The slice is **guarded on `images[0].src` matching the
hero**, so an unrecognised `featuredImage` falls back to showing every gallery image rather
than silently dropping one. The hero's own caption lookup now uses the null-safe `find`
filter rather than a loop-scoped `{% set %}`, which Nunjucks does not reliably propagate.

The intro section's threshold also changed from `images.length > 1` to
`galleryImages.length > 0`: under the old test a project with exactly one gallery image
rendered **no gallery at all** and that image was never shown.

Verified by building five fixtures covering every shape, since the failure modes here are
silent:

| case | result |
|---|---|
| no `images`, no `featuredImage` | no hero, no gallery, description full width |
| one image | hero only, gallery empty |
| two images | hero + 1 gallery image beside the text |
| `featuredImage` **not** in `images[]` | hero is extra, all gallery images still shown |
| `images` but no `featuredImage` | hero = image 1, gallery starts at image 2 |

All five render sensibly, none error, none drop an image. Real pages: wohlgroth 10,
felix-und-regula 18, murals-europe 12 — **no duplicates**. Fixtures were removed after the run.

**A trap worth remembering:** the first measurement after this change still showed the
duplicate, because `.eleventy.js` copies `src/_user/layouts/` into `.cache/` at config time,
so the first build after a layout edit can render the previous copy (`CLAUDE.md` §7b). Build
twice, or restart, before believing a layout change did nothing.

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

### Project Page — extracted spec (2026-08-27)

Read from Figma node **`274:3273`**, and the frame was **verified from the canvas**, not
taken on trust from an export manifest. Two floating labels sit inside the
`Project Page Desktop` section, each directly above the frame it names:

| label | at x | frame beneath it |
|---|---|---|
| `126:7719` **`Old Version Backup`** | 50528 | `120:7255` "About Page", **`opacity: 0.1`** — stale |
| `609:6209` **`(Updated Reusable) Components`** | 52366 | `274:3273` **`Project Page`**, full opacity — **this one** |

The section sits at x=50184, immediately right of `Main Page - Onepager Version` (the
homepage, x=46592, w=3339) which carries its own `Onepager Solution` label. This matches
`CLAUDE.md` §4 and the owner's recollection that the project page lies to the right of the
homepage design.

#### Geometry

Content column **x=248** — the 224px sidebar plus a 24px gutter — inside a 1056px
`Main Content Container`. Every image is a `Project Card` instance: image on top, caption
beneath, stacked vertically **12.31px** apart.

| y | element | width |
|---|---|---|
| 185 | Title | 1008 |
| 375 | hero card, full width | 1001 |
| 1286 | text column (two paragraphs, 480px) + card to its right | 488 |
| 1934 | the same pattern again | 488 |
| 2582 | full-width card | 1001 |
| 3351 | two cards side by side, 25px gap | 488 |
| 3999 | three cards, ~20.5px gap | 320 |

Cards are inset 24px from the container's left edge but 31px from its right. Rendered as
Figma has it; the asymmetry is listed in *Open items*.

#### Type

| element | font | size | line-height | tracking | colour |
|---|---|---|---|---|---|
| Project title | Geist 400 | 118.97px | 0.74 | −0.02em | `#222222` |
| Caption **Title** (left) | Geist 400 | 20.51px | 1.0 | −0.045em | `#222222` |
| Caption **Year** (right) | Geist 400 | 14.36px | 1.2 | −0.02em | `#525252` |
| Caption **Description** | Geist 400 | 16.41px | 1.0 | −0.045em | `#525252` |
| Caption **Author** | Geist 400 | 16.41px | 1.0 | −0.045em | `#525252` |

Caption rows are **10.26px** apart. Every caption node sets `leadingTrim: CAP_HEIGHT`, so
Figma's box heights (15px, 12px) hug the capitals and have **no stable CSS equivalent** —
compare by baseline and font metrics, never by box height (audit guide §8).

Per the include's own contract, confirmed by the design: **Title and Year are the
project's; Description and Author are the image's.**

#### Beyond the ninth image

Figma draws nine cards. Real projects have more — Stage 6 alone has 10, 12 and 18.
**Owner's decision (2026-08-27): "if a project has more images, do more of the same."**
The tail pattern therefore repeats rather than terminating: continue cycling the row
shapes, so image 10 onward keeps producing the same kinds of rows the design ends on.

#### Traps hit while reading this frame

Recorded because each cost time and two of them produced wrong statements to the owner:

- **`figma_audit.py spec` does not flag invisible nodes.** It prints nodes with
  `visible: false` and `opacity: 0` as if they render. This frame has 6 hidden nodes and
  18 at zero opacity — including an `Info` text on caption rows 2 and 3 that was briefly
  reported as part of the caption. **Cross-check anything read from `spec` against `raw`.**
- **Node names lie; read `characters`.** The four body-text blocks are *named* with the
  component's default lorem ("For more than three decades, our dedicated team…"). They are
  visible instances whose actual text is the real copy.
- **Do not measure the PNG export.** Audit guide §8: Figma exports have a transparent
  background and `Image.convert('RGB')` turns that black, corrupting edge detection. A
  content-column measurement taken that way read 252/997 where the API says 248/1001.
- **Reading the export by eye invented a carousel.** A chevron "seen" at the foot of the
  three-column row corresponds to no node anywhere in the frame.
- Trap #1 of the guide — `style` being only the default — was **checked and is clear
  here**: `characterStyleOverrides` and `styleOverrideTable` are empty on all caption and
  title nodes, so these values are what actually renders.

#### Can the database supply this?

Measured across all 1,071 images in live galleries, and all 79 project text elements:

| caption field | source | coverage |
|---|---|---|
| image Title | `tx_dam.title` | **1071/1071** |
| image Description | `tx_dam.description` | **1028/1071** |
| image Author | `tx_dam.creator` | **561/1071** — absent for roughly half |
| project Title | `tt_content.header` | present, but see below |
| project **Year** | `tt_content.header` | **only 24 of 79** carry one |

So the captions are buildable, with the Author line simply absent where there is no
`creator`. **The project Year is the real gap** — most sculpture headers are a bare title
(`The Throne`, `The Wolf`). It cannot be recovered from `tx_dam.date_cr`: that is the
photograph's date, not the project's, and it disagrees — Wohlgroth's images date to 1994
while its header says 1993. Listed in *Open items* as a question for Maja.

Two further findings for the later stages, from the same query: **8 project headers are
empty**, and several pages carry **more than one `text` element** (page 926 has three,
1054 and 1064 two) — including video link-lists (`Bagger Videos / Music:`,
`Elxt 90 Videos:`) which no stage currently handles.
`extract_projects.py` records these in `anomalies[]` rather than silently taking the first.

### Project Page & collection pages — build corrections (2026-08-27)

Applied against the spec above. **Every previous value is recorded here**, so any change can
be reversed or audited without git archaeology. No content was edited: Maja's prose, the
migration output and the database values are all untouched — only templates and CSS changed.

#### 1. Image captions rendered empty — fixed

`src/_user/layouts/project.njk` included `project-image-caption.njk` at three sites and
passed it **nothing**. The include reads `projectTitle`, `projectYear`, `imageDescription`,
`imageAuthor`; Nunjucks `{% include %}` inherits the parent context, and none of those names
existed in it. Result: `ERROR: Missing project title for image caption` ×40 and
`... year ...` ×40, and an empty `<div class="project-image-caption">` under every image.

- All **four** call sites now set the four variables (plus `projectSlug`, `context`,
  `imageIndex`, which the include uses only for error messages).
- **The hero image gained a caption**, which Figma has and the template omitted. It captions
  the `images[]` entry whose `src` matches what is displayed, so a project whose
  `featuredImage` is not in `images[]` gets no caption rather than a wrong one.
- `project-image-caption.njk`: the guard `{% if (projectTitle or projectYear) and not
  imageDescription %}` **removed**. It suppressed the title/year row whenever an image had a
  description — i.e. on essentially every real image. Figma shows all three rows always.

Result: **80 build errors → 0**, 11 captions on `wohlgroth` (hero + 10), 0 empty caption divs.

#### 2. Caption CSS — every value differed from Figma

`src/_user/assets/css/custom.css`. Figma values from node `274:3273`:

| property | was | now (Figma) |
|---|---|---|
| `.project-image-caption` `gap` | `0.25rem` (4px) | `0.641rem` (10.26px) |
| `.project-image-caption` `margin-top` | `0.5rem` (8px) | `0.769rem` (12.31px) |
| `.caption-title` size / weight | `0.95rem` / `500` | `1.282rem` (20.51px) / `400` |
| `.caption-title` colour | `#000000` | `#222222` |
| `.caption-year` size / weight | `0.95rem` / `500` | `0.897rem` (14.36px) / `400` |
| `.caption-year` colour | `#000000` | `#525252` |
| `.caption-description` size | `0.875rem` | `1.026rem` (16.41px) |
| `.caption-description` colour | `#000000` | `#525252` |
| `.caption-author` size | `0.875rem` | `1.026rem` (16.41px) |
| `.caption-author` style | **italic** | not italic |
| `.caption-author` colour | `#666666` | `#525252` |
| tracking (all four) | none | `-0.045em`, except `.caption-year` `-0.02em` |

The title and year were previously the same size and weight, which inverted the hierarchy —
Figma's title is 20.51px against a 14.36px year.

**One deliberate deviation, flagged not hidden:** Figma sets `line-height: 1.0` on
description and author. Those are single-line in the design but wrap in reality, and 1.0
clips descenders on a wrapped line, so **1.25** is used. Figma's `leadingTrim: CAP_HEIGHT`
means its boxes have no CSS equivalent anyway (audit guide §8).

#### 3. Collection pages emitted 0-byte files — fixed

`src/collections/{sculptures,installations,performance,paintings}.md` carried only `title`
and `description`. With no `layout`, Eleventy wrote an empty file, so `/collections/paintings/`
was blank no matter how much content existed. Added three keys per file — `layout:
collection.njk`, `collectionName: <name>`, `permalink: /collections/<name>/` — matching the
template's own `src/collections/blog.md`. **The existing `title` and `description` lines were
not touched.**

#### 4. …and the fix would have published placeholder copy

`collection.njk` read its heading and blurb from `collectionData.js`, which holds the
**template's generic strings**. The real prose is in the page files:

| collection | `collectionData.js` (template placeholder) | `src/collections/<name>.md` (Maja's prose) |
|---|---|---|
| sculptures | "Three-dimensional sculptural works" | "For Maja, the transformation of materials, primarily through sculpting…" |
| installations | "Installation art pieces" | "The numerous collaborations with other artists…" |
| performance | "Performance art documentation" | "Maja Thommen became interested in stage work…" |
| paintings | "Two-dimensional painted works" | "As long as I can remember, a pen and paintbrush have accompanied my life" |

`src/_user/layouts/collection.njk` now prefers the **page's own** `title`/`description` and
falls back to `collectionData`. **Neither source was edited** — both still hold exactly what
they held. `collectionData.js` continues to supply navigation, submenus and colour; it is
configuration, not copy.

Result: `/collections/paintings/` is **20,424 bytes** listing all three Stage 6 projects,
under Maja's own blurb. The other three render correctly and are empty pending Stages 7–11.

#### Verification

Full build, 18 files: **only the 4 known `featuredProjects.json` errors remain**. All routes
200. Stage 6 still verifies 3/3 against live (heading, description, every caption, order).

## Phase 3 — Content & image migration at scale

Current state (verified by running the build, not just reading old status docs):

- **26 of ~71** TYPO3 projects converted to Markdown: 7/28 sculptures, 6/26 installations, 6/9 performance, 7/8 paintings.
- Of those, only **paintings and one sculpture (Sisyphos Gate)** have images actually wired into front matter. Installations and performance have **zero** images linked even where the post exists.
- "Breath under Water" (the previously-missing painting): resolved — it's a whale sculpture miscategorized under paintings in TYPO3. Excluded from paintings; to be migrated later under sculptures/installations.
- Bio/Press/Links/Timeline text content is done (transcribed from the live site). What remains for this cluster is assets and the Timeline field split.
- **Press clipping scans located (2026-07-29): `old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja/presse/`** — 49 files, 47 JPG + 2 PDF (`2007_Alchemy_Bar_-_Wired_A4.pdf`, `2012_Wacken_Scull...pdf`; `2013_Destroy_HIV` exists as both). Filenames are already year-prefixed (`2004_casino1.jpg`, `1993_wohlgrott.jpg`), which maps cleanly onto the entries in `src/pages/about/press.md`. Note the spelling in the backup is `wohlgrott` vs. `Wohlgroth` in the page content. Six have been copied to `src/assets/images/shared/press/` as **placeholders only** — renamed to slug form, unoptimised (3.8 MB for six; the full set will need resizing before it ships). The remaining 43 are part of the bulk asset migration, not of the About work.

### Superseded by the migration plan — approved 2026-08-25

**This phase is now governed by `project_docs/content-migration-plan.md`**, approved by the owner
on 2026-08-25. Read that document, not this section, before doing any migration work. The
substance of what changes:

- **The old extraction scripts are not resumed.** This section previously said to "resume the
  proven extraction scripts (`scripts/extract_typo3_projects.py` etc.)". They wrote straight into
  `src/` with no census, no denominator and no separation between extraction and verification,
  which is the specific failure the migration plan exists to fix.
- **Everything above describing existing content is now placeholder inventory, not progress.**
  The 26 converted projects, the wired paintings images, and the Bio/Press/Links/Timeline text
  are **not** a partial migration to be continued — the plan replaces all of it. Note the line
  above: that text content was *"transcribed from the live site"*, which is precisely what the
  plan's decision 1 forbids, and why its V10 check was dropped and existing `src/` content is
  never consulted as a source.
- **Existing content is quarantined before Stage 1, not kept in place** (owner, 2026-08-25).
  All 38 Markdown files under `src/pages/` and `src/posts/` are **moved** — never deleted — to
  `pre-migration-content/` at the repo root, mirroring their original paths. That directory sits
  outside Eleventy's input dir, so nothing in it builds. The resulting invariant is that
  `src/pages/` and `src/posts/` contain **only** migration output, checkable from a directory
  listing. **The site goes substantially empty until the stages fill it, and the owner has
  accepted that** in exchange for the separation. See §5.1 of the plan.
- **The "26 of ~71 projects" figure above is wrong — it is 23.** The count included three
  `placeholder-*.md` category stubs.
- **Content drift is measured, not feared.** A fresh dump taken 2026-08-25 was compared
  field-by-field against the January 2025 one: **zero content change across nineteen months**
  (§2.0). Image drift remains unmeasured.

Facts in this section that remain useful — the press-clipping location and filename convention,
the "Breath under Water" miscategorisation, the image-wiring state — are kept above as
reconnaissance. Their *conclusions about what to do next* are superseded.

## Phase 4 — Verification & cutover

- Build/link/image integrity checks across all migrated content.
- Visual comparison against Figma and against the live site at maja-explosiv.com.
- GH Pages progress deploy — **done, and now the routine**: `npm run deploy:github`, commit
  `docs/`, push. First published 2026-07-30 with the homepage fixes. Stop the dev server
  first and rebuild locally afterwards; `README.md` explains why.
- VPS/production cutover (deferred — details TBD).

---

## Open items needing input

**This section is the single list for open questions of this kind.** Every problem,
question and design inconsistency across the redesign *and* the content migration is
recorded here — including ones whose detail lives in another document, which the item
names. `project_docs/DOCS.md` indexes every document in the repo and marks which are
current; `migrated-content/_tools/RUNBOOK-images.md` is the procedure for the image
pipeline. Nothing needing the owner's judgement is filed anywhere else. When something needs the owner's judgement — a design inconsistency, an ambiguous spec, a content decision that can't be settled from Figma or the live site — record it here rather than in a new file or inline in a template comment. Resolved items get struck through with the resolution, not deleted, so the reasoning stays visible.

- [x] ~~**The hero image is a duplicate of the first gallery image, and now carries a
  duplicate caption.**~~ **FIXED 2026-08-27**, see Phase 2 § *build corrections* §5. Originally: (raised 2026-08-27, visible only since the captions were wired.)
  `project.njk` sets the hero to `featuredImage`, which the converter fills from `images[0]`,
  and then the intro section starts again at `images[0]`. So every project shows image 1
  twice in a row, and since 2026-08-27 with the same caption twice. Figma does not do this:
  its hero is the first card and the next card is the *second* image. **Fixing it means
  changing which images each section draws, which is the grid work (Figma spec, Phase 2)
  rather than the caption work** — so it is left as found. Deciding whether to do the full
  grid pass is the owner's call.

- [ ] **The project page grid does not match Figma.** (raised 2026-08-27; the captions are
  now correct, this is the remaining fidelity gap.) Figma (`274:3273`, Phase 2 spec) pairs
  **one** image with each text block, then a full-width card, then a **two-column** row, then
  a **three-column** row. `project.njk` stacks **two** images beside the text and puts
  everything after image 3 into one generic row container. Whether to do the full grid pass
  is the owner's call; the spec and geometry are extracted and ready.

- [ ] **`collectionData.js` still holds the template's placeholder descriptions.** (raised
  2026-08-27.) "Three-dimensional sculptural works", "Installation art pieces", "Performance
  art documentation", "Two-dimensional painted works". They no longer render — `collection.njk`
  now prefers the page's own front matter, where Maja's real prose lives — but the stale
  strings remain in the config and will resurface for any collection page lacking a
  `description`. Delete them, or replace them with the real copy?

- [ ] **A layout edit can silently render the previous version.** (raised 2026-08-27; it cost
  a wrong measurement this session.) `.eleventy.js` copies `src/_user/layouts/` and
  `src/_user/includes/` into `.cache/` **at config time**, so the first build *after* editing
  one of those files can still emit the old markup — the change looks like it did nothing.
  `CLAUDE.md` §7b records this for the dev server; it applies to one-off builds too. Build
  twice, or restart, before concluding a layout change had no effect. **The real fix is
  upstream** in `explosive` — this is generic template infrastructure, not Maja-specific.

- [ ] **The caption's Year line is styled inconsistently with the other three.** (raised
  2026-08-27, Figma node `274:3273`, cosmetic but it is a real inconsistency in the design.)
  Caption Title, Description and Author are all `line-height 1.0` / `letter-spacing
  −0.045em`. The **Year** alone is `line-height 1.2` / `−0.02em`. Nothing about the layout
  explains the difference and it does not follow the size change — the project title, at
  118.97px, also uses −0.02em, so the Year may have inherited from a different text style.
  **Rendered as Figma has it**, per `CLAUDE.md` §3; not normalised to match its neighbours.
  Question for the owner: is this intentional, or should the Year match the other three?

- [ ] **Most projects have no year, and the caption design has a slot for one.** (raised
  2026-08-27, Stage 6; blocks a complete caption from Stage 7 onward.) The Figma caption's
  top row is `Title` left, `Year` right. The year comes from `tt_content.header`, which is
  written `"Title, Year"` — but **only 24 of 79 project text elements carry one**. Most
  sculpture headers are a bare title: `The Throne`, `The Wolf`, `Bill Parooka`. Eight
  headers are empty entirely. It cannot be derived from `tx_dam.date_cr`: that is the
  photograph's date, not the project's, and the two disagree — Wohlgroth's images date to
  1994 while its header says 1993. **This is information the database does not contain.**
  Either Maja supplies the years, or the Year slot stays empty for ~70% of projects.

- [ ] **Project cards are inset asymmetrically.** (raised 2026-08-27, minor.) Within the
  1056px `Main Content Container` the 1001px cards sit 24px from the left edge and 31px
  from the right. Rendered as Figma has it. Likely imprecision rather than intent, but
  that is the owner's call, not a thing to snap to 24/24.

- [x] ~~**Project image captions render empty — the layout never passes the data.**~~ **FIXED 2026-08-27** — see Phase 2 § *Project Page & collection pages — build corrections*. 80 build errors → 0. Original raised
  2026-08-27, Stage 6, blocks every project page from Stage 6 on.)
  `src/_user/layouts/project.njk` includes `project-image-caption.njk` three times without
  setting `projectTitle`, `projectYear`, `imageDescription` or `imageAuthor`. Nunjucks
  `{% include %}` inherits the parent context, and those names do not exist in it — `title`
  and `year` do. So the include logs `ERROR: Missing project title for image caption` and
  emits `<div class="project-image-caption">` containing nothing but whitespace. **80 such
  errors for Stage 6's 40 images.** The data is all present in the front matter
  (`images[].title`, `.description`, `.author`, plus the project's `title` and `year`); only
  the hand-off is missing. This is the build noise `CLAUDE.md` §7b recorded as "gone" — it was
  gone only because the content was quarantined, and it returns with every migrated project.
  **The Figma spec is now extracted** — see *Project Page — extracted spec (2026-08-27)* in
  Phase 2. It settles what the caption shows: `Title` (project) left with `Year` (project)
  right, then `Description` (image), then `Author` (image). `project-image-caption.njk` and
  its CSS already implement exactly that structure, so the remaining work is (a) passing the
  four variables at `project.njk`'s three call sites, (b) giving the hero image a caption,
  which Figma has and the template omits, and (c) removing the include's
  `and not imageDescription` guard, which suppresses the title/year row whenever a
  description exists — Figma shows all three rows together, always.
  **Every caption value in `custom.css` also differs from Figma** (title 15.2px/500 vs
  20.51px/400; year the same size as the title instead of smaller and grey; author italic
  where Figma is not). The type table in the Phase 2 spec has the exact values.

- [x] ~~**The four collection pages produce 0-byte files.**~~ **FIXED 2026-08-27** — see Phase 2 § *Project Page & collection pages — build corrections*. The fix also caught that the layout would have published template placeholder copy over Maja's prose. Original raised 2026-08-27, Stage 6.)
  `src/collections/{paintings,sculptures,installations,performance}.md` carry only `title` and
  `description` — no `layout`, no `collectionName`, no `permalink` — unlike the template's own
  `src/collections/blog.md`, which has all three. Eleventy writes an empty file. So
  `/collections/paintings/` is empty no matter how many projects exist, and Stage 6's three
  projects are reachable only at their own URLs. Pre-existing since December 2025 and missed
  because there was no content to reveal it. The fix is four front-matter blocks, but the
  **permalink and page copy are design decisions** — the existing descriptions are real prose
  someone wrote, and where they belong on the page is a Figma question.

- [ ] **`featuredProjects.json` dangles after the quarantine.** (raised 2026-08-25, needed before
  the site is presentable again.) `src/_user/data/featuredProjects.json` names four projects by
  slug — `sculptures/sisyphos-gate`, `installations/blumenwolke`, `sculptures/the-wolf`,
  `paintings/akwa`. Stage 0b moved those files out, so the build now logs four
  `ERROR: Featured project ... not found` lines. **The build still completes and writes the
  site**, so this is not blocking, but it is a real consequence the migration plan did not
  anticipate: quarantining content breaks *configuration that references content by slug*. It
  resolves naturally once Stages 6–11 migrate the projects — but the new slugs come from the old
  site's six categories mapped to the new four, so the four entries will need repointing rather
  than just reappearing. Whether the homepage should feature these same four is the owner's call.

- [ ] **A hidden Links entry: migrate it or not?** (raised 2026-08-25.) The Links page has a
  second content element, `tt_content.uid = 1400`, header `ON MY OWN BEHALF:`, containing one
  entry — Casino Gitano on MySpace. It is `hidden = 1` in TYPO3, so it is unpublished and does
  not appear on the live site; Stage 1 excluded it on that objective ground and recorded it as
  `not-migrated`. Its raw bytes are kept at
  `migrated-content/links/raw/db/tt_content-1400.bodytext.html`. **If it should appear on the new
  site, say so** — reinstating it is a one-line change. Not urgent.

- [x] ~~**Which database backs `www.maja-explosiv.com` today?**~~ **Resolved 2026-08-25, same
  day it was raised — it was my error, not a real question.** `db1010.mydbserver.com/usr_p51487_2`
  is the live database. Stage 1 appeared to find the live site publishing content the database
  had never seen; in fact the local MySQL was loaded from the **January 2025** dump, and the fresh
  2026-08-25 dump — which does contain that content — was never loaded. Comparing the two dumps
  properly (decoding MySQL escapes first) shows **exactly one content value changed across the
  whole site in nineteen months: `tt_content.uid=1399.bodytext`, the Links page.** Everything else
  is identical. Detail in the migration plan §2.0a.

- [ ] **The site has no favicon.** (raised 2026-08-26.) `src/_user/layouts/base.njk` referenced
  `/assets/images/favicon.ico`, which has never existed in this repo — a 404 on every page,
  live today. The reference is now removed rather than pointed at a stand-in: the only logo
  asset present (`shared/site/logo.svg`) is itself marked *"Placeholder logo SVG. Replace with
  your branded logo"* — a grey box with text — so generating an icon from it would ship
  placeholder design, which §3 says is the owner's call, not mine. **Supply a real icon and
  restore the line in `base.njk`** (the removed markup is left there as a comment).
  Same applies to `logo.svg` itself, which `site.js` still points at.

- [ ] **Two nav links have never existed: `/sitemap/` and `/search/`.** (raised 2026-08-26.)
  Broken in the deployed `docs/` too, so they are 404s on the live site right now and predate
  the migration. Either build the pages or drop the links — not a migration question.

- [ ] **The deleted `sennhof` page looks like a staging page — check it before Stages 6–11.**
  (raised 2026-08-26.) `pages.uid = 1079`, deleted and hidden, preserved at
  `migrated-deleted-content/maja/deleted-pages/1079-sennhof/`. Two signals point the same way:
  its text sits under a heading *"workshop views"* but describes the **Affenbande monkeys**
  (five sculptures, 2020–2022, Zürich, Galerie Neurotitan) — and its images overlap heavily
  with other projects: **19 files shared with `hinwil`**, 17 more with `affenbande`,
  `hafenszene` and `hinwil` together (see `image-archive/DUPLICATES.md`).
  That combination reads like a working page Maja used to gather material across several
  projects rather than a project of its own. **Worth her eye before those projects are
  migrated** — some of its text may be the only surviving description of the Affenbande work,
  and some of its images may be miscredited if treated as a project in their own right.

- [x] ~~**D5 — the six→four category mapping.**~~ **Substantially resolved 2026-08-26** by the
  owner's rule: anything that does not fall neatly into a new category goes to a `TBD/` category
  folder rather than being guessed at. **60 of 75 visible projects map from the source itself** —
  notably the 46 in `sculptural-work`, which the old site had already split into *Sculptures*
  (29) and *Installations* (17). **13 go to `TBD/`**: `collaborations` (8, a mode not a medium),
  `event-organisation` (3, events not artworks), `possibilities` (2, incl. Breath Under Water).
  `recent-work`'s two entries were checked and excluded — zero content, zero children, zero
  images, so they are navigation shells rather than projects. Full table in the migration plan, decision 13.
  Emptying `TBD/` remains an open task, but no longer blocks the project stages.

- [x] ~~**ASK MAJA: should `collaborations` survive as a body of work?**~~ **Withdrawn
  2026-08-27 — the question was based on a wrong premise of mine.** `collaborations` does not
  exist on the new site at all; it is not a category and was never going to be. The only
  question was ever **which new category each project goes to**, and the owner has answered it:
  the eight collaborations projects go to `sculptures`. Nothing curatorial was at stake.

- [ ] **ASK MAJA: misspellings in the press entries — correct them or keep them verbatim?**
  The old site's press list contains **"Destoy HIV"** (Destroy), **"Anouncment"**
  (Announcement) and **"Wacken Scull"** (Skull). Migrated **verbatim**, per the rule that
  content is transcribed not edited. There is also a name inconsistency: the clipping files say
  `wohlgrott` while the page text says **Wohlgroth**. Her call whether these are fixed on the
  new site.

- [x] ~~**Press: 3 PDF clippings render without a link.**~~ **Fixed 2026-08-27** in
  `src/_user/includes/about-content.njk`: the list loop now uses `entry.image or entry.file`,
  so PDFs link as they do on the old site. The gallery still keys on `image` alone, correctly —
  a PDF is not an `<img>`. Linked entries 45 → 48.

- [ ] **ASK MAJA: the timeline now shows titles the old site never displayed.** The old page
  rendered only a date label and a paragraph — its template (`NewsBio.tmpl`) never output the
  `title` field, although every record has one. The new design has a dedicated title slot, so
  all 85 entries now show a title above their text. For 32 entries the paragraph also opens with
  a bold name, and **in 16 of those the two differ** — title *Bimbo Town* above text starting
  *Jim Whiting*; title *Wheel of Power* above *Derevo*. Both facts are true (the work and the
  collaborator) but they now read as two lines. Owner accepted the duplication pending her view.
  **Detail: `migrated-content/timeline/SOURCE.md`.**

- [ ] **ASK MAJA: should 4 excluded timeline records appear on the new site?** Four live
  `tt_news` records on page 864 sit in **category 27**, which neither timeline plugin selects —
  so they are invisible on the live site and were not migrated. All four are titled **Elxt 90**,
  covering 2000, 2001, 2002 and 2003. Authored and then left uncategorised, which may have been
  deliberate or an oversight. Every field preserved at
  `migrated-content/timeline/excluded/excluded-records.json`, copied to
  **`image-archive/live/about/timeline-excluded/`** with a README.

- [x] ~~**The site's configured email address is a placeholder and is wrong.**~~ **Corrected
  2026-08-27.** `src/_user/data/site.js` now carries `m-e@maja-explosiv.com` and
  `0049 (0)30 505 970 27`, from `tt_content 1311` and confirmed against the live site. It
  previously had `info@maja-explosiv.com` (commented as a placeholder) and an empty phone. The
  build no longer references the placeholder anywhere.

- [ ] **ASK MAJA: three hidden elements on the old contact page — do any belong on the new one?**
  All three are recorded in full in `migrated-content/legal/SOURCE.md`:
  - **An abandoned contact form** (`tt_content 1279`, "Anfrage"). Its content is the mail-form
    extension's **own shipped example text**, never configured. The new site has no contact form
    — should it?
  - **A hidden image**, `kartePariskl.jpg` (707×785) — reads as *Karte Paris klein*. Archived at
    `image-archive/hidden/about/contact/kartePariskl.jpg`.
  - **An empty text element** (`tt_content 1477`) — created, never filled. Nothing to migrate.

- [ ] **ASK MAJA: is the studio address on the contact page current?**
  `ATELIER / MAAS & THOMMEN / 10997 BERLIN` comes from the Figma design and is hardcoded in
  `contact.njk`. It appears **nowhere in the migrated source**, so the migration has no way to
  verify it — it is the one piece of contact information that cannot be checked against the old
  site. Everything else on the page (phone, email) migrated verbatim and matches.

**Recorded difference, no action needed:** the *"Webdesign and Realisation: Werner Trunk,
Oppelnerstr. 9, 10997 Berlin, Ust Id DE 190483520, wtweb.com"* credit appears on the old contact
page and is **deliberately not carried to the new site** (owner, 2026-08-27). Documented verbatim
in `migrated-content/legal/SOURCE.md`, raw bytes kept. It was the only postal address in the
entire migrated source — and it is the web designer's, not Maja's.

**Recorded difference, no action needed:** the old contact page showed a photograph,
`webthanksxy.jpg` (1876×1916, `tt_content 1478`). The new design uses its own imagery instead
and **the old photo is deliberately not carried over**. It is preserved at
`image-archive/live/about/contact/webthanksxy.jpg`. Noted in
`migrated-content/legal/SOURCE.md`.


- [ ] **ASK MAJA: is the Datenschutzerklärung current, and should the Impressum stay inside the
  contact page?** The privacy policy migrated **verbatim** — 24,834 characters of German GDPR
  text, 31 sections — because legal text is transcribed and not edited. **Its provenance and date
  are unknown and nobody has reviewed it.** Separately, Maja has **no separate Impressum page**:
  the obligation is discharged by two blocks on the contact page headed `Impressum:` (her contact
  details, and a web-design credit for Werner Trunk with a Ust-Id). Both are legal-compliance
  questions rather than migration ones. Detail: `migrated-content/legal/SOURCE.md`.

- [ ] **ASK MAJA: is the Bio text right, and is the phrasing what she wants?** The bio migrated
  **verbatim from the database and is character-identical to the live site** (1,084 chars), so
  nothing was introduced — but it has not been revisited in years and several things stand out:

  - *"oeuvre includes, sculpture (metal, stone and wood) robotics, kinetic art, illustration and
    painting"* — stray comma after "includes", missing one after "wood".
  - *"Elxt90"* — written `Elxt 90` everywhere else on the site.
  - Third person throughout, shifting between "Maja Explosiv", "Maja", "Maja Thommen" and
    "M. Thommen".
  - *"where she has resided since 2004"* — still accurate?
  - The first paragraph becomes the **`excerpt`** shown beside the portrait on the About intro,
    so it now carries more weight than it did on the old site. Worth her reading it as a
    standalone opening rather than as paragraph one of four.

  **Also: the old page embeds a portrait** (`uploads/RTEmagicC_ichsw.jpg.jpg`) that is *not* the
  photograph the new design uses (`shared/profile/maja.webp`). Which should it be?

  Full detail, including the paragraph split and how line breaks were handled:
  **`migrated-content/bio/SOURCE.md`**.

- [ ] **ASK MAJA: two timeline entries show `Since 2020` / `Since 2007` instead of a bare year,
  and they wrap.** Entries sort by timestamp, matching the live site, but the displayed year now
  comes from the source label. **`since 2020:` carries a 2022 timestamp**, so a bare "2020" would
  sit between 2023 and 2022 and read as a sorting fault. Rendering `Since 2020` makes the
  position explain itself — but **the year column is 37px, so it wraps to two lines** and those
  rows are taller than the rest. Alternatives: widen the column, sort by displayed year rather
  than timestamp, or accept the wrap. Detail in `migrated-content/timeline/SOURCE.md`.

- [ ] **ASK MAJA: what order should the press gallery use?** The new site's gallery holds the
  same 48 images as the old one but **21 of 48 sit in a different position**. Nothing is missing,
  extra or duplicated. The old page built its gallery and its link list as two independent
  elements ordered differently; the new page builds both from one list, so the gallery inherits
  the list's order. Options: reproduce the old gallery's sequence, order by date, or keep the
  current list order. Worth knowing the old order may be nothing more than upload sequence.
  **Full detail and a position-by-position comparison: `migrated-content/press/GALLERY-ORDER.md`.**

- [ ] **ASK MAJA: should the third 2018 press PDF appear on the site?**
  `20180525ZürcherOberländer_1.pdf` (610 KB) exists in the media library and is preserved in the
  archive, but **no press entry links it and the gallery does not show it** — so it is invisible
  on the old site too, and the migration keeps it that way. There are three 2018 *Zürcher
  Oberländer* PDFs and only two are used. She may know whether this one was superseded, a
  duplicate, or simply forgotten. Context: `migrated-content/press/GALLERY-COMPANIONS.md`.

- [ ] **ASK MAJA: is the press gallery change OK?** Three entries link a **PDF**, which cannot be
  an `<img>`, so they would have shown in the list but not the gallery. Each was given a JPG
  companion so the gallery matches the live site at **48 images**. Nothing is invented — every
  companion comes from a local source.

  | entry links | gallery shows | where the image comes from |
  |---|---|---|
  | `20180525ZürcherOberländer2.pdf` | `2018-zuercheroberlaender2.jpg` | the clipping JPG beside the PDF |
  | `20180519ZürcherOberländer.pdf` | `2018-zuercheroberlaender.jpg` | the clipping JPG beside the PDF |
  | **`2013_Destroy_HIV.pdf`** | **`2013-destroy-hiv-clipping.jpg`** | **`typo3temp/pics/89d9b1aeec.jpg`** — TYPO3's own render of the PDF, 257×345, taken from the backup |

  **The Destroy HIV pairing was wrong twice before this.** It was first matched to
  `2013_Destroy_HIV.jpg` on the shared filename — that file is a **728×140 banner**, a different
  asset that appears nowhere on the live press page. It was then removed altogether. The correct
  image is TYPO3's rendered thumbnail, which was in the backup all along.

  Worth Maja's eye: **is the Destroy HIV clipping the right picture**, and are the two 2018
  pairings right — those were verified against the live gallery's own DAM titles and positions,
  but a person who knows the material would confirm faster than a filename match.

  Detail: `migrated-content/press/GALLERY-COMPANIONS.md`. All 53 press source files are archived
  at `image-archive/live/about/press/` with `PROVENANCE.json`.

- [ ] **Ask Maja to confirm the 8 collaborations projects belong under `sculptures`** — she may overrule.

- [ ] **Run a "live page, hidden gallery" census before Stages 6–11** — how many published pages have their gallery switched off, as Metal Group XIX does. The archive's hidden bucket is 145 MB, so this is not a one-off.

- [ ] **Pages that are published while their image gallery is hidden.** (raised 2026-08-27,
  needed before Stages 6–11.) **Metal Group XIX** (`pages.uid = 1078`) is the known case: the
  page is live with two text blocks, but its gallery element (`uid 1655`, CType `list`) is
  `hidden = 1`, so its **50 images do not display on the live site.** Confirmed by fetching
  `content/sculptures/collaborations/metal-group-xix.html` — text renders, gallery does not.

  The images are safe in `image-archive/hidden/collaborations/metal-group-xix/`. The migration
  currently follows the live site and gives such a page no gallery, which is faithful. **But 50
  archived photographs of a project that shows none may simply be a switch Maja forgot was off**
  — worth asking rather than silently inheriting.

  **This is almost certainly not the only such page** — the hidden bucket of the archive holds
  145 MB. A census of "live page, hidden gallery" should run before the project stages.

- [ ] **Two `pyrofessor` files were left behind in the 2026-08-27 recovery.**
  `fileadmin/s-pf/images/Show/domäne_mandelbrenner.jpg` and `domäne_trompete_big.jpg` — the only
  non-ASCII-path files in the database that are **not Maja's**. They belong to the other site
  sharing this TYPO3 install (D8), so they were deliberately not retrieved and not archived.
  36 of 38 such files were recovered; these are the 2. **No action needed unless `pyrofessor`
  content ever comes into scope** — recorded so the 36/38 gap is explained rather than looking
  like an oversight.

- [ ] **A third image-reference mechanism was missed by the census: images embedded in
  `bodytext` HTML.** (raised 2026-08-27.) The image census covered `tx_dam_mm_ref` (galleries)
  and `tt_content.image`, but **not `<img>` tags written directly into rich-text content**.
  Measured: **70 content elements contain `<img>`, 38 of them live, referencing 163 distinct
  files — 148 present in the backup.** Many are TYPO3 `uploads/RTEmagicC_*` thumbnails used to
  build in-page navigation grids (Metal Group XIX has 13 such 160x160 links to other projects),
  and some belong to `pyrofessor` (`fileadmin/s-pf/`), not Maja.

  Mostly navigation furniture rather than artwork, so probably low value — **but it is unaudited
  and the archive does not contain them.** Needs a pass before the image census can be called
  complete.

- [ ] **Three real projects sit outside the old site's six categories.** (raised 2026-08-26,
  needed before Stage 6.) The migration plan's stage table assumes every project lives under
  one of the six containers. It does not: **`Breath Under Water` (77 images), `Alchemy Bar`
  (36) and `Sculptures` (32)** hang off `recent work` (uid 867) and `- possibilities -`
  (uid 1049). The image archive now files them under `recent-work/` and `possibilities/`, but
  the **stage table needs 145 images and 3 projects added to it**, and the six→four mapping
  (D5) has to cover them.

- [ ] **155 image references point at content rows that no longer exist.** (raised 2026-08-26.)
  `tx_dam_mm_ref` rows whose `uid_foreign` matches no `tt_content` record — dangling references
  left by deletions that did not clean up the link table. They are skipped by the archive
  builder and counted as `ref-to-missing-content`. Harmless, but worth knowing before anyone
  treats the link table's row count as an image census.

- [ ] **Which images move with the quarantine?** (raised 2026-08-25, needed before **Stage 2 —
  Press**.) §5.1 of the migration plan moves all content Markdown out of `src/` before Stage 1,
  but `src/assets/images/` is left alone. That directory mixes two things: site chrome the
  templates require, and placeholder content assets — including the six press clippings recorded
  in Phase 3 as copied in "as placeholders only", unoptimised at 3.8 MB for six. Separating them
  needs a file-by-file call. Not urgent: Stage 1 (Links) writes no images. **Needed before Stage
  2**, which is the first stage that does.

- [ ] **What happens to the four upstream template demo posts?** (raised 2026-08-25.)
  `welcome-to-explosive-website.md`, `getting-started-with-11ty.md`, `css-grid-layout-guide.md`
  and `image-carousel-demo.md` come from the `explosive` template, not from TYPO3. No migration
  stage produces or replaces them, so this is a template decision rather than a migration one:
  quarantine them, delete them as scaffolding, or keep them. They are quarantined with everything
  else in the meantime, because the §5.1 invariant admits no exceptions and a move is reversible.

- [ ] **Links section uses a different font from everything else.** In the current `Links` variant of the About Components container, entry lines are **Rethink Sans** 400, 19.31px, 168% line-height, −2% tracking — while the tab bar, Bio and Timeline are all Geist, and Phase 1 round 3 concluded "Geist everywhere". Each category's entries are a single concatenated text node with link spans inside, which reads like pasted content that kept its own styling rather than a deliberate third font. **Resolved for now (owner, 2026-07-29): use Geist**, and note the inconsistency here in case the designer intended otherwise. Rethink Sans is not loaded by the site and should not be added without a decision.
  - **More instances found 2026-07-30 on the homepage frame**, which supports the "pasted content" reading rather than a deliberate second family: the **About-intro description** (`91:2988`, Rethink Sans 400 / 25.13px) and the footer's **Impressum** label (`I182:2812;52:6471`, 15.47px) — while its siblings Sitemap and search are Geist 500. Note also that the footer brand line's *default* style is Rethink Sans and is then 100% overridden to Geist per character, i.e. the same trap §8 of the audit guide warns about. Assumed covered by the same "use Geist" resolution; say so if not.
- [ ] **A fourth font family: the homepage CTA label is Inter.** `I388:5771;388:5734` in the visible CTA instance reads **Inter 500, 16.24px**, resolved through the override table so it is not the `style`-block trap. Inter appears nowhere else in the frames read so far, and Phase 1 explicitly retired it as "never a confirmed value, just an old guess". Presumed to be Geist 600 like the hidden pill variants, but that is a guess, not a reading. Blocks the CTA rebuild (H2).
- [ ] **The two homepage section headings are styled differently in Figma.** "Projects" (`I52:6457;46:707`) is Geist 400 / 126.91px / lh 120% / −4%; "About" (`91:2984`) is Geist 400 / 123.74px / lh 74% / −2%. Same family and weight, sizes 3px apart, but the line-height and tracking differ enough to change how each sits. One token or two? Rendered as Figma has them until decided (guide §7 bucket 2).
- [x] ~~**Figma's project card caption has three rows; the build renders one.** The `Project Card` component's caption frame is 59.53 tall and holds title+year, title+year, title+info. The row contents are placeholder, so what the second and third rows are *for* (medium? dimensions? photo credit?) cannot be read off the design — and the build's real data currently carries title, year, description and author. Needs a content decision before the card can be built to the design.~~
  **RESOLVED 2026-08-27. No content decision is needed — the rows are Description and Author,
  and the reading that produced this question was of node *names*, not node *content*.** The
  three rows' actual `characters` are `Title`/`2025`, `Description`/`Info`, `Author`/`Info`;
  every node is *named* "Title", "Year" or "Info" regardless of what it renders, which is why
  they read as "title+year, title+year, title+info". The right-hand cells on rows 2 and 3
  carry **`opacity: 0`** — deliberately invisible, and absent from Figma's own PNG export. So
  the caption is: **Title left + Year right, then Description, then Author**, left-aligned,
  which is exactly what the build's data already carries and what
  `project-image-caption.njk` was written for. Full spec, including type and geometry, in
  Phase 2 § *Project Page — extracted spec (2026-08-27)*.
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
- [x] ~~`docs/` folder (GH Pages build output) currently shows as deleted-but-uncommitted in `git status`~~ — **resolved 2026-07-30.** `docs/` is committed build output (Pages needs it in the repo) and is regenerated by `npm run deploy:github`, never hand-edited. It still contains stray `_includes/` and `_layouts/` copies from a passthrough rule; harmless, and on the cleanup list in `pending-changes.md`.
- [ ] VPS/production host details — deferred.
- [ ] **Grayscale-on-hover image treatment — needs a real decision, not a guess.** `.featured-project-image` (top 4 homepage thumbnails) already had `filter: grayscale(100%)` → color-on-hover before this session; extended the same pattern to `.project-image img` (the main Sculptures/Installations/Performance/Paintings grid) after seeing grayscale project photos in Figma's Present/prototype mode. But checking further, Figma itself is inconsistent: the same Sisyphos Gate photo appears **in full color** near the top of the Sculptures grid and **in grayscale** in what looks like a duplicate/alternate card instance further down - same pattern as this file's other duplication issues (duplicate bio text, duplicate press.png/links.png exports). Owner note: "I may have added it to the thumbnails by mistake... if I added it there it was probably for a reason." Left both grayscale implementations in place rather than reverting on inconclusive evidence - resolve by checking with whoever has final say on the design (Maja/designer), not by more Figma spelunking.
