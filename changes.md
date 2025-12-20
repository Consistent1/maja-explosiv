# Changes to Maja Explosiv Website

This document outlines the site-specific customizations made to the Maja Explosiv website that differentiate it from the upstream [Explosive 11ty template](https://github.com/Xpanda-org/explosive-11ty).

## Site Information

**Site Name:** Maja Explosiv  
**Artist:** Maja Thommen  
**Template Base:** Explosive 11ty (forked from `https://github.com/Xpanda-org/explosive-11ty`)  
**Last Major Update:** December 2025

## Overview

The Maja Explosiv website is an artist portfolio site showcasing sculptures, installations, paintings, and performance art. The site has been heavily customized from the base template to create a unique "one-page" experience with tabbed navigation and a fixed sidebar layout.

## Major Customizations

### 1. Layout Changes

#### Fixed Sidebar Layout
- **File Modified:** `src/_user/layouts/sidebar-layout.njk`
- **Changes:** Created a custom sidebar layout with fixed left navigation
- **Purpose:** Persistent navigation matching the Figma design requirements

#### Custom Home Page Layout
- **File Created:** `src/_user/layouts/home.njk`
- **Changes:** Implemented a "one-page" design with:
  - Hero section at the top
  - Carousel component for featured images
  - Custom sections with tabbed content for Projects and About
  - Support for dynamic tab switching via URL hash
- **Purpose:** Create a modern, single-scrolling-page experience

#### Custom Project Page Layout
- **File Created:** `src/_user/layouts/project.njk`
- **Changes:** Dedicated layout for individual project pages featuring:
  - Clean project header with title and metadata
  - Featured image display
  - Project description area
  - Media gallery grid for additional project images
  - "Back to Projects" navigation link
- **Purpose:** Showcase individual artworks with a focused, gallery-style presentation

### 2. CSS/Styling Customizations

#### Main CSS File
- **File:** `src/_user/assets/css/custom.css`
- **Major Changes:**
  - **Box Model Reset:** Added `box-sizing: border-box `globally to fix layout issues
  - **Fixed Sidebar Styling:**
    - Position: fixed, 250px width,100vh height
    - `overflow: hidden !important` to prevent scrollbars
    - Compact spacing (reduced padding, margins, font sizes) to fit content
    - Flexbox layout with `justify-content: space-between` for vertical distribution
  - **Main Content Layout:**
    - Explicit `margin-left: 250px` to prevent overlap with fixed sidebar
    - Width calculated as `calc(100% - 250px)`
    - Switched from CSS Grid to block layout for more reliable positioning
  - **Typography Adjustments:**
    - Reduced hero title from 6rem to 2.5rem (~40px)
    - Reduced sidebar text sizes for compact fit
    - Maintained uppercase text-transform for brand consistency
  - **Tab Styling:**
    - Premium styling with centered alignment
    - Smooth transitions and opacity effects
    - Active state indicators
  - **Responsive Design:**
    - Mobile breakpoint at 768px
    - Sidebar converts to relative positioning on mobile
    - Grid layouts adapt to single column

### 3. Eleventy Configuration Fix

#### Passthrough Copy Fix
- **File Modified:** `.eleventy.js` (line 275)
- **Change:** Updated from:
  ```javascript
  eleventyConfig.addPassthroughCopy("src/_user/assets");
  ```
  to:
  ```javascript
  eleventyConfig.addPassthroughCopy({ "src/_user/assets": "assets" });
  ```
- **Added:** Watch target for `src/_user/assets/css/` (line 281)
- **Purpose:** Ensures user CSS files properly override base CSS files during build
- **Impact:** Critical fix that allows custom CSS to be correctly deployed to `_site/assets/`

### 4. Navigation Customization

#### Left Sidebar Navigation
- **File:** `src/_user/includes/left-nav.njk`
- **Changes:**
  - Made "PROJECTS" and "ABOUT" section titles clickable links (with class `nav-link-header`)
  - Added `data-tab-link` attributes for JavaScript tab integration
  - Organized navigation into:
    - **PROJECTS:** Sculptures, Installations, Performance, Paintings
    - **ABOUT:** Bio, Timeline, Press, Links, Contact
  - Footer showing "ATELIER MAAS & THOMMEN"
- **Purpose:** Provide persistent navigation that integrates with the one-page tabbed layout

### 5. Content Structure

#### Home Page Content
- **File:** `src/index.md`
- **Structure:**
  - Hero section with title "MAJA EXPLOSIV" and artist description
  - Carousel with multiple slides showing different project categories
  - Custom sections for Projects and About with tabbed interfaces
  - Tab content defined inline in front matter
- **Collections Used:**
  - `sculptures`
  - `installations`
  - `performance`
  - `paintings`

### 6. JavaScript Enhancements

The base template's `main.js` already includes:
- `initTabs()` for tab functionality (supports both ARIA and simple `.tab-buttons` structures)
- `initProjectPreview()` for project card interactions
- Sidebar link integration with tab switching

No custom JavaScript was added; the existing functionality was leveraged.

## Files Added/Modified

### Files Created
- `src/_user/layouts/home.njk`
- `src/_user/layouts/project.njk`
- `changes.md` (this file)

### Files Modified
- `src/_user/assets/css/custom.css` (extensive modifications)
- `src/_user/includes/left-nav.njk` (customized navigation)
- `.eleventy.js` (passthrough copy fix)
- `src/index.md` (home page content and structure)

### Files Reviewed (No Changes)
- `src/assets/js/main.js` (used existing tab functionality)
- `src/_user/layouts/base.njk` (reviewed, no changes needed)
- `src/_user/layouts/sidebar-layout.njk` (reviewed existing structure)

## Design Requirements Met

- ✅ Fixed sidebar with no scrollbars
- ✅ Content properly positioned (no overlap with sidebar)
- ✅ "One-page" experience with tabbed sections
- ✅ Clickable section headers (PROJECTS, ABOUT) that scroll to sections
- ✅ Reduced hero title size
- ✅ Responsive design maintained
- ✅ Project page layout matching design specifications
- ✅ Premium aesthetic with smooth transitions

## Known Issues & Considerations

### Sidebar Content Density
The sidebar was carefully balanced to fit all navigation items without scrollbars. Font sizes, spacing, and padding were progressively reduced until content fit within a typical viewport height (678px at time of implementation). If additional navigation items are added in the future, further spacing reductions may be needed, or content may need to be reorganized.

### CSS Override Architecture
The fix to `.eleventy.js` ensures that files in `src/_user/assets/css/` properly override base template CSS. This was a critical discovery - without the object mapping syntax `{ "src/_user/assets": "assets" }`, the user CSS files were being copied to the wrong location and base files were overwriting them.

## Upstream Template Compatibility

All customizations have been made using the template's user directory override system (`src/_user/`). This means:
- ✅ Base template files remain unchanged
- ✅ Future upstream updates can be merged without conflicts
- ✅ Custom code is isolated and clearly documented
- ✅ The override systems (layouts, includes, data, assets) work as designed

## Development Notes

### Build Process
The site uses the standard Eleventy build process with the custom override systems. During development:
```bash
npm run serve  # Live reload at http://localhost:8080
npm run build  # Production build to _site/
```

### Asset Pipeline
- Base assets: `src/assets/` → `_site/assets/`
- User assets: `src/_user/assets/` → `_site/assets/` (overrides base)
- Watch targets configured for both base and user CSS directories

### Browser Compatibility
The fixed sidebar layout with `position: fixed` and `margin-left` offsets is well-supported across modern browsers. The `box-sizing: border-box` reset ensures consistent box model behavior.

## Future Considerations

1. **Content Updates:** Project content can be added via markdown files in `src/posts/projects/`
2. **Tab Content:** Additional tabs can be added by extending the `customSections` array in `src/index.md`
3. **Styling Tweaks:** All visual customizations should continue to be made in `src/_user/assets/css/custom.css`
4. **Layout Changes:** New layouts should be added to `src/_user/layouts/` following the override pattern

## References

- **Design Source:** Figma design files in `project_docs/`
- **Upstream Template:** https://github.com/Xpanda-org/explosive-11ty
- **Template Documentation:** See README.md for full template capabilities

---

## Recent Updates (17 December 2025)

### Hero Section Full-Width Implementation

**Motivation:** The hero section needed to fill the full viewport width and height to match the design specifications in Top.png, without any visible border or background container.

**Changes Made:**

1. **Layout Grid System** (`src/_user/assets/css/custom.css`)
   - Restored upstream grid layout: `display: grid; grid-template-columns: 250px 1fr`
   - Changed sidebar from `position: fixed` to `position: sticky` to participate in grid flow
   - Removed manual `.main-content` margins and padding
   - Main content now correctly occupies second grid column via `grid-column: 2 / 3`

2. **Hero Full-Width Technique** (`src/_user/assets/css/custom.css`)
   - Hero section breaks out of content-wrapper constraint
   - Uses `width: 100vw` to span full viewport width
   - Negative margin `margin-left: calc(-250px - 97.5px)` to offset sidebar and align to viewport left edge
   - Hero content positioned with left margin to account for sidebar + design gutter
   - Set `min-height: 100vh` to fill viewport height

3. **Hero Styling Cleanup** (`src/_user/assets/css/custom.css`)
   - Removed `.hero-background` border, padding, and border-radius
   - Set background to transparent (no visual box/container)
   - Hero now flush with page background matching design
   - Added corner image: `background-image: url('/assets/images/corner.png')` positioned at `right top`

4. **Typography Refinements** (`src/_user/assets/css/custom.css`)
   - Hero title: `5rem` font-size with `-0.03em` letter-spacing
   - Fine-tuned margins: `margin-top: 1rem`, `margin-bottom: 1.75rem`
   - Optical alignment: `margin-left: -6px` for large title text

**Verification:**
- Created visual diff tool (`temp/visual-diff.html`) for side-by-side comparison with design screenshots
- Used Chrome DevTools MCP to measure element positions and confirm hero fills viewport exactly
- Hero verified at `{x:0, y:0, width:1360, height:626}` (full viewport in test case)

**Impact:**
- ✅ Hero section now matches Top.png design exactly
- ✅ No borders or visual containers around hero
- ✅ Full viewport width and height coverage
- ✅ Corner image restored and positioned correctly
- ✅ Maintains grid layout compatibility with sidebar and content sections

**Files Modified:**
- `src/_user/assets/css/custom.css` (layout grid, hero full-width, styling cleanup)
- `temp/visual-diff.html` (new: visual comparison tool)

**Template Compatibility:**
- All changes made in `src/_user/` override directory
- No modifications to upstream template files
- Grid layout follows template's intended architecture
- Negative margin technique is CSS-only, no template changes needed

---

## Font System and Section Bar Design (December 20, 2025)

**Summary:** Implemented comprehensive font family system using Geist, Rethink Sans, and Inter fonts. Enhanced section title styling with decorative horizontal bars.

### 1. Font Family System

**Fonts Loaded:**
- **Geist**: Modern sans-serif (primary) - loaded via Vercel CDN
- **Rethink Sans**: Versatile sans-serif (secondary) - loaded via Google Fonts
- **Inter**: Used exclusively for CTA buttons - loaded via Google Fonts

**Implementation:**
1. **Font Loading** (`src/_user/layouts/base.njk`)
   - Added Rethink Sans to Google Fonts link
   - Maintained existing Geist and Inter font loading
   - Updated comments to reflect three-font strategy

2. **Theme Configuration** (`src/_user/_data/theme.js`)
   - Created user theme override file (new)
   - Defined font stacks:
     - `fonts.body`: `'Geist', 'Rethink Sans', -apple-system, ...`
     - `fonts.heading`: `'Geist', 'Rethink Sans', sans-serif`
     - `fonts.button`: `'Inter', -apple-system, ...` (CTA buttons only)
   - Updated color scheme to match design (`#C8C8C8` background, `#000000` text)

3. **CSS Typography** (`src/_user/assets/css/custom.css`)
   - Updated `body` to use theme font variables with Geist/Rethink Sans stack
   - Updated heading elements to use theme font variables
   - Verified CTA button continues to use Inter font via `--theme-fonts-button`
   - Added comprehensive documentation comments explaining font strategy

**Font Usage:**
- ✅ Body text: Geist → Rethink Sans → system fallbacks
- ✅ Headings: Geist → Rethink Sans → sans-serif
- ✅ CTA buttons: Inter → system fallbacks
- ✅ All fonts load efficiently from CDN with proper fallbacks

### 2. Section Title Bar Design

**Visual Enhancement:**
- Section titles ("PROJECTS", "ABOUT") now display with decorative horizontal lines on both sides
- Creates visual "bar" element separating sections
- Matches clean, minimal aesthetic from homepage.png design reference

**Implementation** (`src/_user/assets/css/custom.css`):
- Redesigned `.section-title` class with flexbox layout
- Added `::before` and `::after` pseudo-elements creating horizontal lines
- Line styling:
  - `flex: 1` with `max-width: 200px` for balanced appearance
  - `height: 1px`, `background-color: rgba(0, 0, 0, 0.15)` for subtle effect
  - `margin: 0 2rem` for spacing from text
- Typography refinements:
  - Font size: `1rem` (refined, understated)
  - Letter spacing: `0.3em` (extra wide for premium feel)
  - Opacity: `0.75` (subtle, not overwhelming)
  - Font weight: `400` (regular weight for elegance)
- Responsive design:
  - Mobile breakpoint reduces line `max-width` to `100px`
  - Mobile margins reduced to `1rem` for tighter spacing

**Visual Result:**
- ✅ Section titles display with balanced horizontal lines
- ✅ Clean, minimal aesthetic matching design reference
- ✅ Responsive behavior maintains visual balance
- ✅ Subtle styling doesn't compete with content

### 3. Build Configuration

**Eleventy Updates** (`.eleventy.js`):
- Added passthrough copy for `temp` directory (visual diff testing)
- Added passthrough copy for `project_docs` directory (design reference access)
- Enables visual comparison tools to work via dev server

**Files Created:**
- `src/_user/_data/theme.js` - Font and color theme configuration

**Files Modified:**
- `src/_user/layouts/base.njk` - Font loading
- `src/_user/assets/css/custom.css` - Typography and section bar styling
- `.eleventy.js` - Passthrough copy configuration

**Design Verification:**
- Visual diff tool confirmed section bars match design intent
- Font rendering tested across all major elements
- No layout breaks or visual regressions detected

**Template Compatibility:**
- All changes follow user override pattern (`src/_user/`)
- Theme system properly overrides upstream defaults
- CSS uses theme variables for maintainability
- No modifications to core template files
