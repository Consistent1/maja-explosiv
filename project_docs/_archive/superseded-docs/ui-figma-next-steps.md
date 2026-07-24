**UI Figma Next Steps**

- **Purpose:** Capture the actionable edits and verification steps needed to make the site match the Figma "Main Page" screenshot (sidebar + top hero + muted/light container background).
- **Branch:** `ui/fix-start` (current working branch for these UI changes)

Files to update (primary):
- `src/_user/data/theme.js` — source of truth for color tokens, typography sizes, and font family names. Add or replace Figma tokens here (background, container, surface, border, text, muted, hero sizes, display sizes, fonts). This will make theme-wide changes easy and reversible.
- `src/assets/css/main.css` — wire theme tokens into components, replace hard-coded fallbacks, and add precise layout values (sidebar width, hero paddings, grid column sizes). Keep fallback values for safety but prefer `var(--theme-*)` lookups.
- `src/_user/includes/left-nav.njk` — ensure semantic structure for header/footer areas inside the sidebar (already present, may add wrapper classes if needed for spacing).
- `src/_layouts/theme/home.njk` or `src/_layouts/home.njk` — confirm hero markup includes the container and `hero-background` wrapper used by CSS; include image assets if necessary.

Assets:
- Put Figma-exported decorative assets in `src/assets/images/figma/` or `src/_user/assets/images/` and reference them via the public path used by the site generator (prefer `src/assets/images/...` for 11ty default pipelines).
- The corner graphic referenced in the Figma screenshot exists at `src/_user/assets/images/corner.png` — confirm served path (I used fallbacks in CSS that may need adjusting to `/assets/images/...`).
 - The corner graphic referenced in the Figma screenshot existed at `src/_user/assets/images/corner.png` and has been moved to `src/assets/images/corner.png` for reliable serving. `main.css` now references `/assets/images/corner.png`.

High-level UI changes to apply (desktop-first):
1. Sidebar
   - Make the left sidebar fixed at the left edge with exact width `252px` (Figma). Use `position: fixed` and ensure main content margin-left matches.
   - Background: `#B8B8B8` (Figma) — wire as `--theme-colors-container` or `--theme-colors-sidebar` in `theme.js`.
   - Right border: `1px solid #222222` (Figma) — wire as `--theme-colors-border`.
   - Layout: `display:flex; flex-direction:column; justify-content:space-between; padding:17.6875px` (Figma). Do not hard-code large gaps; rely on `space-between` for header/footer placement.

2. Global background and container
   - The site is currently using a dark page background (`--theme-colors-background: #222222`). Figma uses a light page background and a light container where main content sits. Replace page `background` token with the Figma page bg (light gray) and use `--theme-colors-container` for the inner panel color.
   - Update `body { background-color: var(--theme-colors-background) }` to reflect the new token.

3. Hero / top section
   - Wrap hero content in `.hero-background` and use `--theme-colors-container` for its background and `--theme-colors-border` for the subtle border.
   - Place the corner image into the hero container's top-right (use background-image or absolutely-positioned `<img>` inside the container). Confirm served image path.
   - Use exact hero font sizes and line-height from Figma (replace `--theme-typography-hero-title`, `--theme-typography-hero-subtitle`).

4. Image grid and posts
   - Use a CSS Grid tuned to the Figma thumbnail sizes (min column size and gap). Use an `aspect-ratio` consistent with the design (square or 4:3 as required).

5. Typography
   - Confirm the two families used in Figma (heading and body). Update `theme.js` `fonts.heading` and `fonts.body` and ensure `main.css` uses `var(--theme-fonts-*)` for headings/body.

6. Responsive behavior
   - Desktop: fixed left sidebar. Mobile: collapse the sidebar into a top navigation or hide behind the existing `.mobile-menu-toggle`. Add media queries to remove `position: fixed` and reset `margin-left` for small screens.

Verification steps after changes
1. Build and serve locally: `npm run serve` (or `npm run build` + `npx http-server _site -p 8081`) and open `http://localhost:8081/`.
2. Verify `:root` CSS variables are injected correctly (look for `--theme-colors-background`, `--theme-colors-container`, `--theme-typography-hero-title`).
3. Verify hero corner image appears in the top-right of the hero container.
4. Confirm the left sidebar is fixed and main content is offset by 252px on desktop.
5. Test mobile breakpoints and ensure the sidebar collapses correctly.

Approximate values currently present in the codebase (to replace with exact Figma tokens):
- Sidebar width: `252px` (present — exact)
- Sidebar padding: `17.6875px` (present — exact)
- Sidebar background: `#B8B8B8` (present — exact)
- Sidebar border-right: `1px solid #222222` (present — exact)
- Page background: currently `#222222` (dark) — must be replaced with Figma page background (light gray)
- Container background: present fallback `#B8B8B8` — verify exact Figma shade

Recent applied changes (quick fixes):
- Moved corner image to `src/assets/images/corner.png` and updated `src/assets/css/main.css` to reference `/assets/images/corner.png`.
- Set the page body background to `#B8B8B8` and the footer background to `#B8B8B8` in `src/assets/css/main.css` to match the Figma container color.
- Hero paddings: `var(--size-6)` used (approx — confirm exact spacing)
- Hero max-inline-size: `min(900px, 70vw)` (approx)
- Hero title font-size: `--theme-typography-hero-title: 88.8976px` (from earlier Figma CSS — confirm)
- Hero subtitle font-size: `--theme-typography-hero-subtitle: 79.9508px` (from earlier Figma CSS — confirm)
- Posts grid min column: `minmax(220px, 1fr)` (approx)
- Image aspect-ratio: `4/3` (approx — Figma may use squares)

Notes on asset paths
- Template references commonly expect `/assets/...` in the generated site. If an asset is in `src/_user/assets/...`, adjust the served path or move the file under `src/assets/images/`.

If you'd like, I can apply these token updates and the final CSS mapping after you provide the exact Figma tokens (colors, fonts, pixel sizes). For now, this file documents the plan and the approximate values to be replaced.

-- End of file
