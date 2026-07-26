# Maja Explosiv — Redesign & Migration Plan

**Status document owner:** this file is the current source of truth for where the project stands and what's next. It supersedes `RESUME-WORK-HERE.md`, `MIGRATION-STATUS-REPORT.md`, and the various session-summary docs, which have been moved to `project_docs/_archive/` (see `_archive/MANIFEST.md`) rather than deleted.

**Last updated:** 2026-07-24

---

## The two repos

- **`explosive`** (`Xpanda-org/explosive-11ty`) — the generic 11ty template. Owned by the same person as this site. Anything genuinely reusable by other sites belongs here.
- **`maja-explosiv`** (this repo, `Consistent1/maja-explosiv`) — Maja's site, forked from `explosive`. Uses the template's `src/_user/` override system so it can pull template updates without merge conflicts (`upstream` remote is configured and nearly caught up — one trivial commit behind).

**Working principle going forward:** when a change is generic (a bugfix, a new capability any site could use), it should be made in/ported to `explosive`. When a change is specific to Maja's content or Figma design, it belongs in this repo's `src/_user/` overrides — not in the base template directories. An audit of where this boundary has already been crossed is in progress (see Phase 0).

## Design source of truth

Figma file: [Maja Thommen_Website-Redesign](https://www.figma.com/design/18tst8uq38FlDlaZA5cPCz/Maja-Thommen_Website-Redesign) (owner's personal copy, free plan — exact values will be read via the Design-mode properties panel rather than Dev Mode).

Full-page reference exports already captured in `project_docs/design_screenshots/`: homepage, project, bio, timeline, press, contact, links, impressum, sidebar, colors. Use these as the page-by-page checklist for Phase 2.

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
| Homepage | Structurally close — sidebar, hero, featured grid, tabbed projects, about intro all present. Needs token-accurate styling pass once Phase 1 lands. |
| Single project | Close — `sisyphos-gate.md` is a working full example (images, layout) matching `project.png` reasonably well. |
| Bio | **Done.** Real content, transcribed verbatim from the live site (`maja-explosiv.com/info/bio.html`). |
| Press | **Done.** Real content - full chronological press-mention list (1993-2018), transcribed from the live site. Note: Figma's `press.png` export turned out to be a duplicate of `links.png` (same image, wrong filename) - no usable Figma layout existed for this page, so it's styled to match Bio/Timeline/Links rather than a confirmed mockup. Press clipping images (opened via lightbox on the old site) still need asset migration, same as project images. |
| Links | **Done.** Real content - full "Friends and Related Artists" directory (8 categories, 50 entries) with real outbound URLs, transcribed from the live site. Figma's text matched the live site verbatim, but had no real hrefs. |
| Timeline | **Done.** Real content - full career chronology (1993-2024, 85 entries) plus a Schooling section, transcribed from the live site's `/info/bio/bio-chronological.html`. The Figma mockup for this page was unreliable: mostly unfilled placeholder rows, plus at least two entries ("Urban Resilience", "Voices of the Forgotten") that don't exist on the real site and don't match Maja's practice - correctly flagged as suspect before the live-site check confirmed it. |
| Impressum | Page exists (`/impressum/`), footer link resolves. Content transcribed from the Figma mockup, which is itself marked "...to be continued" - needs real legal review before launch, not something to complete by guessing. Not yet cross-checked against the live site's `datenschutz` page. |

**Key lesson from this pass**: Figma text content is unreliable and inconsistent in quality - sometimes verbatim-real (Links, Bio), sometimes a mix of real and fabricated-sounding entries (Timeline), sometimes just wrong (Press). The live site (`maja-explosiv.com`, a frameset-based TYPO3 site) is the actual source of truth for content per the site owner, and should be checked directly rather than trusting Figma's placeholder text - Figma governs structure/design only. All four About sub-pages plus Timeline are now sourced from the live site, not Figma.
| Contact | Exists — verify against `contact.png`. |
| Sidebar / nav | Implemented, verify exact colors/spacing against `sidebar.png` + `colors.png` once tokens are locked. |

**Architecture fix applied (2026-07-24)**: the homepage's About tabs (Bio/Timeline/Press/Links) were hardcoded as a duplicate HTML blob in `src/index.md`'s frontmatter, completely disconnected from `src/pages/about/*.md` (which had their *own*, different placeholder text). Rewired `src/_user/layouts/home.njk` to pull each tab from its real page via `collections.all | find("fileSlug", ...)` plus a new `excerpt` frontmatter field per page - same pattern the Projects tabs already used for collections. One source of truth per piece of content now; page bodies still need real content migrated in.

Also verify: the image carousel (Datastar-based, template feature) actually renders galleries per Figma spec; whether a "news feed" (mentioned in the original PRD/epics, and there's a `src/posts/news/` collection scaffold with one placeholder entry) is still in scope for this design or was dropped — not present in any current `design_screenshots`, needs a decision.

## Phase 3 — Content & image migration at scale

Current state (verified by running the build, not just reading old status docs):

- **26 of ~71** TYPO3 projects converted to Markdown: 7/28 sculptures, 6/26 installations, 6/9 performance, 7/8 paintings.
- Of those, only **paintings and one sculpture (Sisyphos Gate)** have images actually wired into front matter. Installations and performance have **zero** images linked even where the post exists.
- "Breath under Water" (the previously-missing painting): resolved — it's a whale sculpture miscategorized under paintings in TYPO3. Excluded from paintings; to be migrated later under sculptures/installations.
- Bio/Press/Links/Timeline need real content sourced from the TYPO3 backup (`old/`, gitignored, 1.6GB) or the live site.

Once Phase 2 templates exist, resume the proven extraction scripts (`scripts/extract_typo3_projects.py` etc.) to migrate the remaining ~45 projects and wire up their images the same way paintings were done.

## Phase 4 — Verification & cutover

- Build/link/image integrity checks across all migrated content.
- Visual comparison against Figma and against the live site at maja-explosiv.com.
- GH Pages progress deploy (deferred — revisit when Phase 2/3 have something worth showing).
- VPS/production cutover (deferred — details TBD).

---

## Open items needing input

- [ ] Figma exact-value extraction — access pending.
- [ ] News feed: in or out of scope for this redesign?
- [ ] `docs/` folder (GH Pages build output) currently shows as deleted-but-uncommitted in `git status` — left untouched for now per "forget GH Pages for now."
- [ ] VPS/production host details — deferred.
- [ ] **Grayscale-on-hover image treatment — needs a real decision, not a guess.** `.featured-project-image` (top 4 homepage thumbnails) already had `filter: grayscale(100%)` → color-on-hover before this session; extended the same pattern to `.project-image img` (the main Sculptures/Installations/Performance/Paintings grid) after seeing grayscale project photos in Figma's Present/prototype mode. But checking further, Figma itself is inconsistent: the same Sisyphos Gate photo appears **in full color** near the top of the Sculptures grid and **in grayscale** in what looks like a duplicate/alternate card instance further down - same pattern as this file's other duplication issues (duplicate bio text, duplicate press.png/links.png exports). Owner note: "I may have added it to the thumbnails by mistake... if I added it there it was probably for a reason." Left both grayscale implementations in place rather than reverting on inconclusive evidence - resolve by checking with whoever has final say on the design (Maja/designer), not by more Figma spelunking.
