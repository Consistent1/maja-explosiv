Phase B — UI Implementation (master/detail, tabs, tokens)
===============================================

Summary
-------
- Branch: `ui/fix-start` (work in progress)
- Goal: match Figma Onepager main page — implement accessible tabs, two-column master/detail on home, right-column project preview, and apply design tokens.

What I changed (Phase B)
-------------------------
- JavaScript (`src/assets/js/main.js`):
  - Enhanced `initTabs()` and `activateTab()` to support both ARIA-based tablists (`role="tablist"`) and the simple `.tab-buttons` markup used in `src/index.md`.
  - Added `initProjectPreview()` which wires clicks on `.post-card` / `.project-card` elements to populate the right-column `#project-detail` aside with title, image, excerpt, and link. This is progressive enhancement — it reads DOM content and updates the detail panel without server calls.
  - `initProjectPreview()` is called on `DOMContentLoaded` alongside other initializers.

- CSS (`src/assets/css/main.css`):
  - Added support for `.tab-button` and `.tab-pane` to style the simple tab markup used in `src/index.md`.
  - Added styling for `.project-detail` (right-column) to show project image, title, meta, and controls in a compact card.
  - Minor typography mapping is already in place via theme variables injected by `base.njk`.

- Theme tokens (`src/_user/data/theme.js`):
  - Expanded theme color tokens to match the Figma Main Page (grays and structural tokens) and adjusted font stacks for body/heading.

Why this approach
-----------------
- Progressive enhancement: server-side HTML is untouched; JS only enhances behavior where available.
- Two-tab implementations supported so we can iteratively update `src/index.md` markup later to the accessible pattern without breaking the current content.

How to continue later (resume instructions)
-----------------------------------------
1. Checkout the branch where work is saved:

```bash
git checkout ui/fix-start
```

2. Start the Eleventy dev server (if not already running) for live reload and visual QA:

```bash
npm run serve
```

3. Work to continue (priority order):
  - Completed: Converted the simple `.tab-buttons` markup in `src/index.md` to ARIA-based markup (`role="tablist"`, each tab `role="tab"` with `aria-controls`, and panels with `role="tabpanel"` + `id`). This improves accessibility and integrates with `initTabs`.
  - Completed: Updated templates that render project/post cards (`src/_layouts/theme/home.njk`, `src/_layouts/home.njk`, and collection templates) to include useful `data-*` attributes (`data-year`, `data-medium`, `data-excerpt`) and added `data-src` on images for lazy-loading / preview wiring.
   - Flesh out the project detail partial `src/_includes/home/project-detail.njk` with additional fields or an initial server-rendered selection (for first project) if desired.
   - Fine-tune CSS tokens (fonts, sizes, spacing) using Figma values. `src/_user/data/theme.js` contains tokens — adjust them and refresh the dev server.

4. Testing & QA checklist:
   - Open the homepage and verify tabs switch content correctly (both desktop and mobile widths).
   - Click a project card/post to see the right detail update; verify image, title, excerpt, and link are populated.
   - Check keyboard navigation on tabs (Left/Right arrows) and ensure focus ring is visible.
   - Verify color/background tokens applied correctly. If colors look off, edit `src/_user/data/theme.js` and restart Eleventy (changes are injected into the `:root` by `base.njk`).

Notes & Implementation Details
------------------------------
- Theme injection: `src/_layouts/theme/base.njk` renders theme JS data into `:root` as CSS variables `--theme-<group>-<key>`, so updating `src/_user/data/theme.js` is the canonical way to change colors and fonts.
- Accessibility: tabs support both patterns; when converting markup to ARIA tabs, ensure `aria-controls` and `aria-selected` states are present. `initTabs()` will add behavior but not mutate markup ownership beyond selection.

Files touched in this phase
-------------------------
- `src/assets/js/main.js` — updated tab logic + added project preview wiring
- `src/assets/css/main.css` — added tab-button/tab-pane support and `.project-detail` styles
- `src/_user/data/theme.js` — added tokenized palette and font stacks
- `src/_user/data/theme.js` — added tokenized palette and font stacks
- Note: `--theme-colors-background` was updated from `#222222` to a light tone and the site body background was set to `#B8B8B8` via `src/assets/css/main.css` for Figma parity.
- `project_docs/ui-phase-b.md` — this document
 
Recent delta (typography & colors)
---------------------------------
- `src/_user/data/theme.js`: corrected background to a light page background and added a `typography` group with `base-size`, `line-height`, and `h1..h6` sizes.
- `src/assets/css/main.css`: mapped the injected `--theme-typography-*` variables to local `--ui-*` variables and applied them to body and headings so changes in `src/_user/data/theme.js` immediately affect typography.
 
Applied Figma tokens (this update)
---------------------------------
- `src/_user/data/theme.js`: updated colors to match the Figma Main Page CSS — set `background: #222222` (page chrome), `container: #B8B8B8`, `surface: #EBEBEB`, `border: #EBEBEB`, and `text`/`muted` tokens.
- `src/_user/data/theme.js`: added hero/display typography tokens from the Figma CSS (`hero-title`, `hero-subtitle`, `display-1`, `lead`) and adjusted `h1..h6` sizes.
- `src/assets/css/main.css`: added `.hero-title`, `.hero-subtitle`, and `.lead` rules that read the injected `--theme-typography-*` variables so the hero and lead text sizes match Figma.


If you want me to continue now, I can:
- Convert the existing `src/index.md` tab HTML to ARIA tablist markup and test the keyboard and hash deep-linking behavior.
- Improve templates that render project cards to include `data-*` attributes so previews show richer metadata.
- Tweak typography and colors to match Figma precisely (if you provide the exact hexes or allow me to scrape the Figma file).

-- End of Phase B notes
