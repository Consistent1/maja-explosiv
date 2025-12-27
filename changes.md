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
- **File Modified:** `src/_user/layouts/post.njk`
- **Changes:** Dedicated layout for individual project pages featuring:
  - **Title:** Large, prominent project title at the top
  - **Featured/Hero Image:** Full-width primary project image
  - **Two-Column Intro Section:**
    - Left column: Project description and content (text)
    - Right column: First two gallery images stacked vertically
  - **Third Image:** Full-width display (if available)
  - **Remaining Images:** Grid layout in rows of 2-3 images, top-aligned
  - **Responsive:** Stacks into single column on mobile devices
- **Purpose:** Showcase individual artworks following the design specified in `project_docs/design_screenshots/project.png`
- **Impact:** Creates a focused, gallery-style presentation that emphasizes both the artwork and its description, with a clear visual hierarchy from hero image through supporting images

#### Layout Overrides for Sidebar Consistency
- **Files Created:** 
  - `src/_user/layouts/page.njk`
  - `src/_user/layouts/post.njk`
  - `src/_user/layouts/collection.njk`
  - `src/_user/layouts/collections-overview.njk`
- **Changes:** All layout overrides extend `sidebar-layout.njk` instead of `base.njk`
- **Purpose:** Ensure the fixed left sidebar appears consistently across all page types (static pages, blog posts, collection pages, etc.)
- **Impact:** Creates a unified navigation experience throughout the entire site

### 2. CSS/Styling Customizations

#### Main CSS File
- **File:** `src/_user/assets/css/custom.css`
- **Major Changes:**
  - **Box Model Reset:** Added `box-sizing: border-box` globally to fix layout issues
  - **Fixed Sidebar Styling:**
    - Position: fixed, 250px width, 100vh height
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
  - **Featured Projects Section:**
    - Responsive grid layout (auto-fit, minmax 280px)
    - Grayscale-to-color hover effect using CSS filters
    - Square aspect ratio (1:1) with `aspect-ratio` property
    - Overlay with gradient background for project titles
    - Box shadow and transform effects on hover
    - Error display styling for build-time validation messages
  - **Project Image Captions:**
    - Standardized caption component for all project images
    - Three-line layout: Title/Year (top), Description (middle, optional), Author (bottom, optional)
    - Title left-aligned, year right-aligned on same line
    - Responsive font sizing for mobile devices
    - Applied consistently across homepage, collection pages, and single project pages
  - **Project Page Layout Styling:**
    - Two-column intro section: Description (left) + First 2 images (right, stacked)
    - CSS Grid layout with equal columns (1fr 1fr) and 3rem gap
    - Full-width third image section with consistent padding
    - Gallery rows for remaining images: `repeat(auto-fit, minmax(280px, 1fr))`
    - Top-aligned images in gallery rows using `align-items: start`
    - Responsive mobile layout: Stacks all columns vertically below 768px
  - **About Section Intro:**
    - Grid layout (`display: grid`) with image on left and text on right
    - Image uses natural dimensions with no additional styling, margins, or padding
    - Text container uses flexbox to center content both horizontally and vertically
    - Grid columns: `auto` (image) and `1fr` (text area)
    - Responsive: Stacks vertically on mobile (below 768px)
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
  - Featured projects section showcasing selected works
  - Custom sections for Projects and About with tabbed interfaces
  - Tab content defined inline in front matter
- **Collections Used:**
  - `sculptures`
  - `installations`
  - `performance`
  - `paintings`

#### Featured Projects Section
- **File Created:** `src/_user/includes/featured-projects.njk`
- **Data File:** `src/_user/data/featuredProjects.json`
- **Purpose:** Display curated selection of featured projects on homepage
- **Features:**
  - Data-driven: Projects listed in `featuredProjects.json` control display order
  - Automatic image resolution: Uses featured image, first image from project, or specified override
  - Build-time validation: Displays specific error messages if projects or images not found
  - Two-column masonry layout: Projects distributed into left and right columns (odd/even split)
  - CSS-based grayscale effect: Images displayed in grayscale (`filter: grayscale(100%)`), transition to color on hover
  - Project info displayed below images: Title, description, and author shown beneath each project image
  - Maintains template compatibility: Works with both regular builds and GitHub Pages deployment
- **CSS Styling:**
  - Flexbox layout with two columns (`display: flex`, `gap: 2rem`)
  - Right column offset: `margin-top: 8rem` for staggered masonry effect
  - Images preserve original aspect ratios (no forced cropping)
  - Minimal top padding (0.5rem) to position closer to CTA
  - Smooth grayscale transitions (0.4s) for hover effects
  - Responsive breakpoints: adapts column layout for mobile screens
- **Error Handling:**
  - Validates project exists in collections
  - Checks for available images (featuredImage, images array, or override)
  - Displays red error boxes with specific details during development
  - Logs errors to console for debugging

### 6. Project Image Caption System

#### Overview
A standardized caption system displays metadata beneath all project images across the site. The system uses reusable Nunjucks templates with consistent styling to show title, year, description, and author information.

#### Implementation Files
- **Templates:**
  - `src/_user/includes/project-image-caption.njk` - For homepage and collection pages
  - `src/_user/includes/single-project-image-caption.njk` - For individual project pages
- **Styling:** `src/_user/assets/css/custom.css` (Project Image Captions section)
- **Integration:** Applied in:
  - `src/_user/includes/featured-projects.njk` - Featured projects on homepage
  - `src/_user/layouts/home.njk` - Projects tab section
  - `src/_user/layouts/collection.njk` - Collection listing pages
  - `src/_user/layouts/post.njk` - Individual project gallery images

#### Caption Structure
Each caption displays up to three lines of information:
1. **Top line:** Title (left-aligned) and Year (right-aligned) - both required
2. **Middle line:** Description (left-aligned) - optional
3. **Bottom line:** Author (left-aligned, italicized) - optional

#### Data Source Logic

**Homepage and Collection Pages:**
- **Title:** From project's `title` field
- **Year:** Extracted from project's `date` field (YYYY format)
- **Description:** From image's `description` field (if available in images array)
- **Author:** From image's `author` field (if available in images array)

**Single Project Pages:**
- **Title:** From individual image's `title` field
- **Year:** From image's `date` or `year` field
- **Description:** From image's `description` field
- **Author:** From image's `author` field

#### Image Metadata Schema
Each image in a project's `images` array should include:
```yaml
images:
  - src: /path/to/image.jpg
    title: "Image Title"        # Required
    date: 2023-08-01            # Required (or use year: 2023)
    year: 2023                  # Alternative to date
    description: "Description"  # Optional
    author: "Author Name"       # Optional
    alt: "Alt text"             # Optional (defaults to title)
```

#### Alt Text Fallback Logic
If `alt` is not provided for an image:
- On homepage/collections: Falls back to project title
- On single project pages: Falls back to image title

#### Error Handling
- **Missing required fields (title/year):** Logged to build console with context (project slug, image index, location)
- **Build behavior:** Continues without failing; omits missing information from display
- **Error message format:** `"ERROR: Missing [field] for [context] in project '[slug]' (image #[index])"`

#### CSS Styling Details
- **Font sizes:** 0.95rem for title/year, 0.875rem for description/author
- **Layout:** Flexbox with `justify-content: space-between` for title/year alignment
- **Spacing:** 0.25rem gap between caption lines, 0.5-0.75rem margin above caption
- **Colors:** 
  - Title/year: Primary text color (#000000)
  - Description: Primary text color
  - Author: Lighter text color (#666666), italicized
- **Responsive:** Font sizes reduce slightly on mobile (<768px)

#### Grayscale Effect Compatibility
The caption system preserves the grayscale-to-color hover effect on featured project images:
- Images use `filter: grayscale(100%)` by default
- On hover: `filter: grayscale(0%)`
- Captions remain outside the hover effect scope

### 7. About Section Intro

#### Overview
The About section on the homepage features an introductory section with an image and biographical text positioned above the tabbed content (Bio, Timeline, Press, Links).

#### Implementation
- **Template Modified:** `src/_user/layouts/home.njk`
  - Added special handling for the About section (`section.id == 'about'`)
  - Inserted `.about-intro` container before the tabs
- **CSS Added:** `src/_user/assets/css/custom.css`
  - New `.about-intro` styles for grid layout and alignment

#### Structure
The intro section contains:
1. **Image:** `src/assets/images/maja.webp` - A portrait photo of Maja Explosiv
2. **Text:** Biographical information about the artist

#### Layout Details
- **Grid Layout:**
  - `display: grid`
  - `grid-template-columns: auto 1fr` - Image column auto-sizes to content, text takes remaining space
  - `gap: var(--size-fluid-4)` - Fluid spacing between image and text (48px on desktop)
  - `align-items: center` - Vertically centers image and text
- **Image Styling:**
  - No additional styling applied - displays at natural dimensions (308px × 229px)
  - `margin: 0` and `padding: 0` - No spacing around the image
  - Left edge aligns with content area
- **Text Container:**
  - `display: flex` with `align-items: center` and `justify-content: center`
  - Centers text both horizontally and vertically in available space
  - `text-align: center`
  - Font size: `var(--font-size-fluid-1)` with `var(--font-lineheight-3)` line height

#### Content
The biographical text reads:
> "Maja Explosiv, born Maja Thommen in Pfäffikon, Switzerland in 1973, is a multidisciplinary artist whose extensive physical artwork oeuvre includes sculpture (metal, stone and wood), robotics, kinetic art, illustration and painting."

#### Responsive Behavior
On mobile devices (below 768px):
- Grid switches to single column (`grid-template-columns: 1fr`)
- Gap reduces to `var(--size-fluid-2)`
- Image is horizontally centered using `margin-inline: auto`

### 8. Featured Image Fallback System

#### Overview
Project pages automatically display a featured image at the top of the page. If no explicit `featuredImage` is defined in the project's front matter, the system automatically uses the first image from the `images` array as the featured image.

#### Implementation
- **Files Modified:**
  - `src/_user/layouts/post.njk` - For project posts (primary)
  - `src/_user/layouts/project.njk` - For dedicated project template
  - `src/_user/layouts/collection.njk` - For project cards in collection listings
  - `src/_user/layouts/home.njk` - Already had this logic implemented

#### Fallback Logic
```nunjucks
{% set displayImage = featuredImage %}
{% if not displayImage and images and images.length > 0 %}
    {% set displayImage = images[0].src %}
{% endif %}
```

#### Duplicate Prevention
To prevent the featured image from appearing twice (once as hero and again in the gallery), the gallery loop skips any image that matches the `displayImage`:

```nunjucks
{% for image in images %}
    {% if image.src != displayImage %}
        {# Display image in gallery #}
    {% endif %}
{% endfor %}
```

#### Behavior
1. **Explicit featuredImage:** If `featuredImage` is defined in front matter, it's used as the hero image and excluded from the gallery
2. **Implicit fallback:** If no `featuredImage` is defined, the first image from the `images` array becomes the featured image and is excluded from the gallery
3. **No duplication:** The featured image (whether explicit or implicit) appears only at the top of the page, never in the gallery below

#### Example Usage

**With explicit featuredImage:**
```yaml
---
title: "Project Name"
featuredImage: /assets/images/projects/hero.jpg
featuredImageAlt: "Hero image alt text"
images:
  - src: /assets/images/projects/detail1.jpg
    alt: "Detail 1"
  - src: /assets/images/projects/detail2.jpg
    alt: "Detail 2"
---
```
Result: `hero.jpg` displays as featured image; gallery shows only `detail1.jpg` and `detail2.jpg`

**Without explicit featuredImage:**
```yaml
---
title: "Project Name"
images:
  - src: /assets/images/projects/image1.jpg
    alt: "Main view"
  - src: /assets/images/projects/image2.jpg
    alt: "Detail view"
---
```
Result: `image1.jpg` automatically becomes the featured image; gallery shows only `image2.jpg`

### 9. Tab Navigation System

#### Tab Bar Structure
The homepage features two tabbed sections (Projects and About) with interactive tab bars (tablists):

**Projects Section:**
- **Source:** Dynamically generated in `src/_user/layouts/home.njk`
- **Tabs:** Sculptures, Installations, Performance, Paintings
- **Content:** Pulls from Eleventy collections to display project images with captions
- **Design (Updated Dec 2025):**
  - **Category Description:** Each tab displays a description text aligned to the left, above the images grid
  - **Description Source:** Pulled dynamically from collection markdown files (`src/collections/sculptures.md`, etc.) using frontmatter `description` field
  - **Layout:** Simple images in 3-column grid (no card styling)
  - **Column Offset:** Second column starts lower (4rem margin-top) than first and third columns
  - **Image Display:** Clean images without card backgrounds, shadows, or borders; images maintain their original aspect ratios (not cropped)
  - **Metadata:** Title and year displayed below each image using project-image-caption template
  - **Removed:** Card backgrounds, titles beneath captions, and description text (kept only image captions)
- **HTML Structure:**
  ```html
  <div class="tab-buttons" role="tablist">
    <button role="tab" aria-selected="true" class="tab-button" data-tab="sculptures">Sculptures</button>
    <!-- More tabs... -->
  </div>
  <div class="tab-content">
    <div id="sculptures" role="tabpanel" class="tab-pane active">
      <div class="category-description">
        <p>{{ description from sculptures.md }}</p>
      </div>
      <div class="posts-grid">
        <!-- Project images with captions -->
      </div>
    </div>
  </div>
  ```
- **CSS Styling:**
  - `.category-description`: Left-aligned text (max-width 800px, padding 0 3rem 2rem)
  - `.posts-grid`: 3-column grid with 2rem gap, padding 0 3rem
  - `.post-card:nth-child(3n+2)`: 4rem top margin for second column offset
  - `.post-card`: Transparent background, no shadows or borders (simple image display)
  - `.post-card-image img`: `object-fit: contain` to preserve aspect ratios (no cropping)
  - `.post-card-content`, `.post-card-title`, `.post-card-description`: Hidden (display: none)

**About Section:**
- **Source:** Static HTML in `src/index.md` front matter (`customSections.content`)
- **Tabs:** Bio, Timeline, Press, Links
- **Content:** Static HTML paragraphs
- **Structure:** Identical to Projects (same HTML pattern)

#### How Tab Switching Works
- **JavaScript:** `src/assets/js/main.js` contains `initTabs()` and `activateTab()` functions
- **ARIA Compliance:** Uses `role="tab"`, `role="tablist"`, and `role="tabpanel"` for accessibility
- **Visual State:** Managed via both `aria-selected` attribute and `.active` CSS class
- **Key Fix (Dec 2025):** Updated `activateTab()` to handle elements with both `role="tab"` AND `class="tab-button"`
  - Changed from `if...else if` to separate `if` statements
  - Ensures `.active` class is properly added/removed (controls underline styling)
  - Initializes `.active` class on page load based on `aria-selected="true"`
- **Keyboard Navigation:** Arrow keys switch between tabs
- **URL Hash Support:** Tabs can be activated via URL hash (e.g., `#sculptures`)

#### Integration with Sidebar
- **Left sidebar links** have `data-tab-link` attributes
- Clicking sidebar "SCULPTURES" link activates the sculptures tab on the homepage
- JavaScript handles scrolling to the tab section and activating the correct tab

## Files Added/Modified

### Files Created
- `src/_user/layouts/home.njk`
- `src/_user/layouts/project.njk`
- `src/_user/layouts/page.njk`
- `src/_user/layouts/post.njk`
- `src/_user/layouts/collection.njk`
- `src/_user/layouts/collections-overview.njk`
- `src/_user/includes/featured-projects.njk`
- `src/_user/data/featuredProjects.json`
- `changes.md` (this file)

### Files Modified
- `src/_user/assets/css/custom.css` (extensive modifications)
- `src/_user/includes/left-nav.njk` (customized navigation)
- `.eleventy.js` (passthrough copy fix)
- `src/index.md` (home page content and structure)
- `src/assets/js/main.js` (tab switching fix - Dec 2025)

### Files Reviewed (No Changes)
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
- ✅ Featured projects section with grayscale hover effects

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

**Summary:** Implemented comprehensive font family system using Geist, Rethink Sans, and Inter fonts. Updated section title styling to large, bold, left-aligned headings matching homepage.png design.

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

### 2. Section Title Styling (Updated: December 20, 2025)

**Design Update:**
After detailed analysis of the homepage.png design file, section titles were updated from decorative bars to large, bold, left-aligned headings.

**Previous Implementation (Removed):**
- Centered section titles with decorative horizontal bars on both sides
- Small text (1rem) with wide letter spacing
- Uppercase text transformation

**Current Implementation:**
- **Visual Style:**
  - Large, prominent headings (~56px / 3.5rem on desktop)
  - Bold font weight (700) for strong visual hierarchy
  - Left-aligned with consistent padding
  - Sentence case ("Projects", "About") for modern, sophisticated look
  - Full opacity (no transparency)
  - No decorative bars or lines
  
- **CSS Implementation** (`src/_user/assets/css/custom.css`):
  - Font size: `3.5rem` (desktop), `2.5rem` (mobile)
  - Font weight: `700` (bold)
  - Text alignment: `left` with `3rem` left padding (`1.5rem` on mobile)
  - Text transform: `none` (allows sentence case from content)
  - Letter spacing: `normal` (removed wide spacing)
  - Opacity: `1` (full visibility)
  - Margins: `3rem` top, `2.5rem` bottom (adjusted for mobile)
  - **Removed**: `::before` and `::after` pseudo-elements (decorative bars)
  - **Removed**: Flexbox layout properties (no longer needed)

- **Responsive Design:**
  - Mobile: Reduced font size (2.5rem), reduced padding (1.5rem)
  - Adjusted margins for better mobile spacing
  - Maintains visual hierarchy across breakpoints

**Visual Result:**
- ✅ Section titles match homepage.png design exactly
- ✅ Strong visual hierarchy through size and weight
- ✅ Clean, modern appearance without decorative elements
- ✅ Properly left-aligned with consistent spacing
- ✅ Sentence case for sophistication
- ✅ Responsive scaling for mobile devices

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

---

## Footer Implementation (December 21, 2025)

**Summary:** Implemented the global site footer matching the "Bottom.png" design, featuring a 3-tier structure with brand identity, contact info, and utility links.

**Design Details:**
- **Structure:**
  1. **Top Tier:** Location (Berlin), Email Contact, Warning Icon (SVG).
  2. **Middle Tier:** Centered Brand Identity ("MAJA EXPLOSIV", "AKA MAJA THOMMEN") flanked by horizontal separator lines.
  3. **Bottom Tier:** Utility Navigation (Sitemap, Search, Impressum).
- **Styling:**
  - White background (`#FFFFFF`) to match the About section.
  - Symmetrical vertical spacing (2rem margins) around horizontal separators.
  - Large brand typography (5rem) for strong visual impact.
  - Clean, uppercase typography for information key-values.

**Files Modified:**
- `src/_user/includes/footer.njk` - Rewritten structure using semantic HTML.
- `src/_user/assets/css/custom.css` - Defined footer grid, typography, and spacing properties.

**Template Compatibility:**
- Uses the `theme.paths.footer` override mechanism.
- Fully compatible with `sidebar-layout.njk` used on both Home and Project pages.
