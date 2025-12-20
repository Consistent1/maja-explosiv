# Homepage Design Implementation Plan

**Project:** Maja Explosiv Website Homepage Redesign  
**Date Created:** 17 December 2025  
**Designer:** Based on Figma design files in `/project_docs/Design Screenshots/`  
**Template:** Explosive 11ty (upstream)

---

## Overview

This plan outlines the implementation of the homepage design for the Maja Explosiv website to match the designer's specifications. The implementation will use the template's customization and theming mechanisms wherever possible to avoid modifying core template files.

To understand how the template is organised, used, and deployed read the README.md file.
To understand how the site diverges from the template read the changes.md file.

### Template Structure and Content Organization

**Important:** Different sections and subsections should have their own templates for better content management:

- **Project Categories:** Each category (Sculptures, Installations, Performance, Paintings) should have its own collection template
- **About Subsections:** Each subsection (Bio, Timeline, Press, Links) should have its own template with appropriate content
- **Templates should contain actual content**, not just placeholder text
- This modular approach allows easy content updates without modifying the main homepage template

### Navigation Behavior

**Bidirectional Navigation:** The sidebar and tab systems work together:

1. **Sidebar → Sections:** Clicking "PROJECTS" or "ABOUT" in the sidebar navigates to that section on the homepage
2. **Sidebar → Tabs:** Clicking a subsection link (e.g., "SCULPTURES", "BIO") navigates to the section AND activates the corresponding tab
3. **Tabs → Sidebar:** When a user clicks a tab, the sidebar should reflect the active state (highlight the corresponding link)
4. **URL Hash Updates:** Navigation updates the URL hash (#projects, #sculptures, #bio, etc.)
5. **Direct Links:** Users can share or bookmark specific tabs via URL hash

---

## Design Analysis Summary

Based on the design files reviewed:
- **Screenshots:** `homepage.png`, `project.png`, `impressum.png`, `contact.png`

The homepage follows a **one-page layout** with these main sections:
1. Fixed left sidebar navigation
2. Hero section with title and description
3. Featured images section (static images with grayscale-to-color hover effect)
4. Projects section (grid-based project cards with static images)
5. About section (text content)
6. Footer section

**Note on Images:** The images at the top of the page and in the projects section are NOT a carousel. They are static images determined by parsing a data file at build time. The featured images section has a special animation effect: images display in grayscale and smoothly transition to color on hover.

---

## Typography and Font System

**Implementation Status:** ✅ Completed (December 20, 2025)

The site uses a three-font system as specified in the design:

### Font Families

1. **Geist** (Primary)
   - Source: Vercel CDN (`@vercel/style-guide`)
   - Usage: Primary font for headings and body text
   - Style: Modern, clean sans-serif
   - Loaded in: `src/_user/layouts/base.njk`

2. **Rethink Sans** (Secondary)
   - Source: Google Fonts
   - Usage: Secondary/fallback font for body text and all text elements
   - Style: Versatile sans-serif with excellent readability
   - Loaded in: `src/_user/layouts/base.njk`

3. **Inter** (Buttons Only)
   - Source: Google Fonts
   - Usage: **Reserved exclusively for CTA buttons** (e.g., "LETS GET IN TOUCH")
   - Style: Neutral, highly readable interface font
   - Loaded in: `src/_user/layouts/base.njk`

### Font Stack Configuration

Configured in `src/_user/_data/theme.js`:

```javascript
"fonts": {
  "body": "'Geist', 'Rethink Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
  "heading": "'Geist', 'Rethink Sans', sans-serif",
  "button": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
}
```

### CSS Implementation

- Body text: Uses `var(--theme-fonts-body)` → Geist, Rethink Sans
- Headings (h1-h6): Uses `var(--theme-fonts-heading)` → Geist, Rethink Sans
- CTA Buttons: Uses `var(--theme-fonts-button)` → Inter

**Files:**
- Font loading: `src/_user/layouts/base.njk`
- Theme config: `src/_user/_data/theme.js`
- CSS application: `src/_user/assets/css/custom.css`

---

## Part 1: Fixed Left Sidebar

### Current State
- Sidebar exists with navigation
- Fixed positioning at 250px width
- Contains: MAJA EXPLOSIV header, PROJECTS nav, ABOUT nav, ATELIER footer

### Design Requirements

#### 1.1 Sidebar Header
**Styling:**
- Background: Light gray (`#C8C8C8` or similar)
- Title: "MAJA EXPLOSIV" - Bold, uppercase, black text (~18-20px)
- Subtitle: "AKA MAJA THOMMEN" - Regular weight, uppercase, smaller (~11-12px)
- Spacing: Tight vertical spacing between title and subtitle

**Behavior:**
- Non-interactive header (no links)
- Fixed at top of sidebar

**Files to Modify:**
- `src/_user/includes/left-nav.njk`
- `src/_user/assets/css/custom.css`

---

#### 1.2 Navigation Sections
**Styling:**
- Section headers: "PROJECTS", "ABOUT" - Bold, uppercase (~14px)
- Nav links: Uppercase, regular weight (~12-13px)
- Color: Dark gray/black text on light gray background
- Hover state: Subtle underline or color change
- Active state: Should be clearly indicated
- Spacing: Minimal padding between items

**Navigation Structure:**
- **PROJECTS** (clickable header linking to #projects)
  - SCULPTURES
  - INSTALLATIONS
  - PERFORMANCE
  - PAINTINGS
- **ABOUT** (clickable header linking to #about)
  - BIO
  - TIMELINE
  - PRESS
  - LINKS
  - CONTACT

**Behavior:**
- **Section headers (PROJECTS, ABOUT):** Clickable links that scroll to corresponding section on homepage
  - Link to `/#projects` and `/#about` respectively
- **Sub-items:** Clickable links that scroll to section AND activate corresponding tab
  - Examples: `/#sculptures`, `/#bio`, `/#press`
- **Active state synchronization:** When user clicks a tab on the page, corresponding sidebar link should highlight
- **Smooth scroll behavior:** Scroll animation to section
- **URL hash updates:** Navigation updates browser URL with hash
- **Bidirectional:** Sidebar → Tabs AND Tabs → Sidebar state updates

**JavaScript requirements:**
- Listen for tab changes and update sidebar active states
- Listen for sidebar clicks and activate corresponding tabs
- Handle URL hash on page load to activate correct tab and highlight sidebar

**Files to Modify:**
- `src/_user/includes/left-nav.njk`
- `src/_user/assets/css/custom.css`
- May need: `src/_user/assets/js/custom.js` for bidirectional navigation logic
- Verify: `src/assets/js/main.js` supports this or needs extension

---

#### 1.3 Sidebar Footer
**Styling:**
- Text: "ATELIER" on first line, "MAAS & THOMMEN" on second line
- Font: Uppercase, smaller size (~11px)
- Color: Medium gray
- Alignment: Left-aligned
- Position: Fixed at bottom of sidebar

**Behavior:**
- Static text, no interaction
- Always visible at bottom of sidebar viewport

**Files to Modify:**
- `src/_user/includes/left-nav.njk`
- `src/_user/assets/css/custom.css`

---

#### 1.4 Sidebar Overall Layout
**Styling:**
- Width: 250px (current - keep as is)
- Height: 100vh
- Position: Fixed left
- Background: `#C8C8C8` or similar light gray
- Border: Thin right border, darker gray/black
- **CRITICAL:** No scrollbars - all content must fit within viewport
- Padding: Controlled spacing to fit all elements

**Behavior:**
- Fixed position (does not scroll with page)
- Content should fit without overflow
- Responsive: Convert to mobile menu on small screens

**Files to Modify:**
- `src/_user/assets/css/custom.css`

---

## Part 2: Hero Section

### Current State
- Hero section exists with "MAJA EXPLOSIV" title
- Has description text and CTA button
- Title is 2.5rem (~40px)

### Design Requirements

#### 2.1 Hero Title
**Styling:**
- Text: "MAJA EXPLOSIV" split across two lines
- Font: Bold, uppercase, very large (~60-80px for desktop)
- Color: Black `#000000` or very dark gray
- Line height: Tight (0.9-1.0)
- Letter spacing: Normal or slightly tight
- Alignment: Left-aligned
- Margin: Generous top margin (~60-80px from top of content area)

**Behavior:**
- Static, no animation on load
- Responsive: Scale down proportionally on smaller screens

**Files to Modify:**
- `src/index.md` (hero title content)
- `src/_user/layouts/home.njk` (hero markup)
- `src/_user/assets/css/custom.css`

---

#### 2.2 Hero Description
**Styling:**
- Text: "multidisciplinary artist whose extensive oeuvre includes metal work, illustration, painting, theatre development and project management."
- Font: Regular weight, sentence case (~18-20px)
- Color: Dark gray `#333` or similar
- Line height: 1.4-1.6 for readability
- Max width: ~600-700px
- Spacing: Moderate margin below title (~30-40px)

**Second paragraph:**
- Text: "For commissions, collaborations or bookings reach out to us."
- Same styling as first paragraph
- Spacing: Small gap between paragraphs (~20px)

**Behavior:**
- Static text
- Should be readable and well-spaced

**Files to Modify:**
- `src/index.md` (hero description)
- `src/_user/assets/css/custom.css`

---

#### 2.3 Call-to-Action Button
**Styling:**
- Text: "↗ LETS GET IN TOUCH" (arrow icon + text)
- Background: Dark/black `#222` or `#000`
- Text color: White
- Shape: Rounded pill button (border-radius: ~25-30px)
- Padding: ~12px 30px
- Font: Uppercase, medium weight (~14px)
- Arrow icon: Top-right arrow before text
- Hover state: Darker background or subtle scale effect

**Behavior:**
- Links to `/contact/` page
- Smooth hover transition
- Cursor changes to pointer

**Files to Modify:**
- `src/index.md` (CTA button config)
- `src/_user/assets/css/custom.css`

---

#### 2.4 Hero Overall Layout
**Styling:**
- Background: Light gray matching overall page `#C8C8C8`
- Padding: Generous padding around content (~60px top, 40px sides)
- Max-width: Content should not extend too wide
- Alignment: Left-aligned within content area

**Behavior:**
- First visible section after page load
- Should anchor the page visually
- Responsive: Adjust padding and font sizes

**Files to Modify:**
- `src/_user/layouts/home.njk`
- `src/_user/assets/css/custom.css`

---

## Part 3: Featured Images Section

### Current State
- Current implementation has a carousel component
- Shows three slides with images, titles, and captions
- Has navigation arrows and dots
- **NEEDS TO BE REPLACED** with static image grid

### Design Requirements

**Note:** This is NOT a carousel. These are static images displayed in a grid that show a grayscale-to-color hover effect.

#### 3.1 Featured Images Container
**Styling:**
- Width: Full width of content area (not full viewport - respects sidebar)
- Layout: Horizontal grid/flexbox layout (likely 2-3 images side by side)
- Background: Transparent or matches page background
- Margin: Generous spacing from hero section (~60-80px)
- Gap: Spacing between images (~20-30px)

**Behavior:**
- Static display (no autoplay, no rotation)
- Images are loaded from data file at build time
- No navigation controls needed (not a carousel)

**Files to Modify:**
- `src/_user/assets/css/custom.css`
- `src/index.md` (remove carousel, add featured images data)
- `src/_user/layouts/home.njk` (replace carousel markup with static image grid)
- May need: Data file for featured images

---

#### 3.2 Featured Images - Grayscale to Color Effect
**Styling:**
- **Default state:** Images displayed in grayscale using CSS filter
  - `filter: grayscale(100%);`
- **Hover state:** Images transition to full color
  - `filter: grayscale(0%);`
- **Transition:** Smooth transition (not immediate)
  - `transition: filter 0.4s ease;` or similar
- Aspect ratio: Maintain original aspect ratios
- Object-fit: Cover (fills space while maintaining aspect)
- Alt text: Descriptive for accessibility
- Loading: Lazy load for performance
- Border-radius: Slight rounded corners (~8-12px) optional
- Box-shadow: Subtle shadow optional

**Behavior:**
- Images start in grayscale
- On hover, smoothly transition to color over ~0.4 seconds
- On mouse leave, smoothly transition back to grayscale
- Clickable - may link to respective collection pages or projects
- No automatic transitions or animations

**Data structure:**
- Images loaded from data file (e.g., `src/_data/featuredImages.json`)
- Structure:
  ```json
  [
    {
      "src": "/path/to/image.jpg",
      "alt": "Description",
      "link": "/collections/category/" (optional)
    }
  ]
  ```

**Files to Modify:**
- `src/_user/assets/css/custom.css` (grayscale effect styling)
- `src/index.md` or data file (featured images data)
- `src/_user/layouts/home.njk` (markup for image grid)

---

#### 3.3 Featured Images - Optional Overlay/Caption
**Styling:**
- **If captions/titles are needed:**
  - Position: Bottom of image with gradient overlay or below image
  - Gradient (if overlay): Dark semi-transparent gradient from bottom
  - Title: Bold text (~16-18px)
  - Alignment: Left-aligned or centered
  - Color: White if overlay, black if below image
- **If no captions:**
  - Images stand alone without text overlay

**Behavior:**
- Static (no fade effects)
- Grayscale hover effect applies to entire image including overlay area

**Design Decision Needed:**
- Verify from design whether captions/titles are shown on featured images
- May be minimal or no text on these images

**Files to Modify:**
- `src/_user/assets/css/custom.css`
- `src/_user/layouts/home.njk`

---

#### 3.4 Featured Images - Layout Grid
**Styling:**
- **Grid Layout:**
  - Display: CSS Grid or Flexbox
  - Columns: 2-3 images horizontally (based on design)
  - Gap: ~20-30px between images
  - Width: Each image takes equal space
  - Alignment: Centered within content area
  
- **Image sizing:**
  - Height: Consistent height across images (~400-500px) OR
  - Aspect ratio: Maintain original ratios
  - Width: Flex to fill available space equally

**Behavior:**
- Static grid (no dynamic reordering)
- Number of images determined by data file
- All images visible simultaneously (no hiding/showing)

**No navigation controls needed** - this is not a carousel

**Files to Modify:**
- `src/_user/assets/css/custom.css`
- `src/_user/layouts/home.njk`

---

## Part 4: Projects Section

### Current State
- Projects section exists with tabs
- Tabs: Sculptures, Installations, Performance, Paintings
- Content: Just placeholder text currently

### Design Requirements

#### 4.1 Projects Section Container
**Styling:**
- Background: Same light gray as page `#C8C8C8`
- Padding: Large vertical padding (~80-100px top/bottom)
- Max-width: Content should breathe within page width
- Margin: Spacing from carousel section

**Behavior:**
- Scroll-to anchor: ID `#projects`
- Should be visually distinct section
- Responsive: Adjust padding on mobile

**Files to Modify:**
- `src/index.md` (section config)
- `src/_user/assets/css/custom.css`

---

#### 4.2 Projects Section Title

**Implementation Status:** ✅ Completed (December 20, 2025)

**Styling:**
- Text: "PROJECTS" (uppercase)
- Font: Geist with Rethink Sans fallback
- Size: 1rem (16px) - refined, understated
- Weight: 400 (regular weight for elegance)
- Color: Black with 0.75 opacity
- Letter spacing: 0.3em (extra wide for premium feel)
- Alignment: Center with decorative horizontal bars

**Bar Design:**
- Horizontal lines flanking the title text on both sides
- Lines: 1px height, rgba(0, 0, 0, 0.15) color
- Line length: Flex-grows with max-width 200px (desktop), 100px (mobile)
- Spacing: 2rem margin between line and text (desktop), 1rem (mobile)
- Implementation: CSS flexbox with `::before` and `::after` pseudo-elements

**Behavior:**
- Static heading with decorative visual bars
- Acts as visual anchor and separator for section
- Responsive: Line length and spacing adjust on mobile

**Files Modified:**
- `src/_user/assets/css/custom.css` - Section title bar styling
- `src/index.md` - Section title text (already in place)

---

#### 4.3 Project Category Tabs
**Styling:**
- **Tab Container:**
  - Alignment: Center
  - Spacing: Even distribution
  - Border-bottom: Thin line under all tabs
  
- **Individual Tabs:**
  - Text: Uppercase (~13-14px)
  - Color: Medium gray when inactive
  - Active color: Black
  - Active indicator: Bottom border (2-3px solid black)
  - Padding: ~12px 20px
  - Background: Transparent
  - Hover: Text darkens, cursor pointer
  - Transition: Smooth color and border transitions

- **Tab labels:**
  - SCULPTURES
  - INSTALLATIONS  
  - PERFORMANCE
  - PAINTINGS

**Behavior:**
- Click to switch between project categories
- Only one tab active at a time
- Active tab shows corresponding project grid
- URL hash updates: `#sculptures`, `#installations`, etc.
- Smooth content transition (fade or slide)

**Files to Modify:**
- `src/index.md` (tab structure)
- `src/_user/assets/css/custom.css`
- Verify: `src/assets/js/main.js` (tab switching logic)

---

#### 4.4 Project Grid Layout
**Styling:**
- **Grid Container:**
  - Display: CSS Grid
  - Columns: 3 columns on desktop (may adjust based on content)
  - Gap: ~20-30px between items
  - Margin-top: ~40px from tabs
  - Responsive: 2 columns on tablet, 1 column on mobile

**Design shows masonry-like layout with varying image sizes:**
- Some images are portrait orientation
- Some are landscape
- Some are larger/smaller
- **Consider:** CSS Grid with auto-flow dense, or manual sizing

**Behavior:**
- Grid adjusts to viewport size
- Items maintain aspect ratios
- Smooth layout shifts

**Files to Modify:**
- `src/index.md` (will need to add actual project data)
- `src/_user/layouts/home.njk` (project grid markup)
- `src/_user/assets/css/custom.css`
- May need: New include file for project cards

---

#### 4.5 Individual Project Cards
**Styling:**
- **Card Container:**
  - Background: White or very light color
  - Border-radius: ~8px
  - Box-shadow: Subtle shadow
  - Overflow: Hidden (for image)
  - Aspect ratio: Varies by image
  
- **Card Image:**
  - Width: 100%
  - Height: Auto or fixed based on design
  - Object-fit: Cover
  - Display: Block
  - Hover: Slight scale effect (1.05) with smooth transition
  
- **Card Metadata (overlay or below image):**
  - Title: Bold, black (~16-18px)
  - Description: Regular, gray (~13-14px)
  - Author: Small, light gray (~11-12px)
  - Year: Light gray, aligned right (~11-12px)
  - Padding: ~15-20px if below image
  - Background: If overlay - semi-transparent gradient

**Based on design screenshots:**
- Design shows: Project thumbnail, Title, Year (e.g., "Wacken 2025")
- Metadata appears to be overlaid or below image
- Some cards show just image, some have text overlay

**Behavior:**
- Entire card is clickable
- Links to individual project page
- Hover: Image scales slightly, shadow deepens
- Cursor: Pointer
- Transition: Smooth 0.3s ease

**Files to Modify:**
- Will need to create project data structure
- `src/_user/layouts/home.njk` or new include
- `src/_user/assets/css/custom.css`
- May need: `src/_data/projects.json` or similar

---

#### 4.6 Projects Tab Content
**Current:** Just placeholder paragraph text  
**Design shows:** Grid of actual project cards with images

**Template Structure:**
Each project category should have its own template/include file:
- `src/_user/includes/projects/sculptures.njk` - Sculptures tab content
- `src/_user/includes/projects/installations.njk` - Installations tab content
- `src/_user/includes/projects/performance.njk` - Performance tab content
- `src/_user/includes/projects/paintings.njk` - Paintings tab content

**Content needed for each category:**
- **Sculptures:** Project cards for sculpture works with actual content
- **Installations:** Project cards for installation works with actual content
- **Performance:** Project cards for performance works with actual content
- **Paintings:** Project cards for painting works with actual content

**Each template should include:**
- Grid layout of project cards
- Real project data (titles, images, years, descriptions)
- Proper markup for accessibility

**Data structure needed:**
```yaml
projects:
  sculptures:
    - title: "Project Name"
      image: "/path/to/image.jpg"
      year: "2025"
      description: "Short description"
      author: "Maja Explosiv"
      link: "/projects/project-slug/"
```

**Behavior:**
- Load project data from collections or data file
- Filter by active tab category
- Display as grid of cards
- Support pagination if many projects

**Files to Modify:**
- `src/index.md` (replace placeholder with grid markup)
- `src/_user/layouts/home.njk`
- May need: Data file for projects
- `src/_user/assets/css/custom.css`

---

## Part 5: About Section

### Current State
- About section exists with tabs
- Tabs: Bio, Timeline, Press, Links
- Content: Placeholder text in Bio tab

### Design Requirements

#### 5.1 About Section Container
**Styling:**
- Background: White `#FFFFFF` - **DIFFERENT FROM PROJECTS** (key visual separation)
- Padding: Large vertical padding (~80-100px top/bottom, ~60px sides)
- Max-width: Narrower than projects section (~800-900px centered)
- Margin: No margin on sides (extends full width)
- Border-top: Thin line to separate from projects section (optional)

**Behavior:**
- Scroll-to anchor: ID `#about`
- Visually distinct from gray project section above
- Responsive: Adjust padding on mobile

**Files to Modify:**
- `src/index.md` (section config)
- `src/_user/layouts/home.njk`
- `src/_user/assets/css/custom.css`

---

#### 5.2 About Section Title

**Implementation Status:** ✅ Completed (December 20, 2025)

**Styling:**
- Same styling as Projects section title (consistency)
- Text: "ABOUT" (uppercase)
- Font: Geist with Rethink Sans fallback
- Size: 1rem (16px)
- Weight: 400 (regular)
- Color: Black with 0.75 opacity
- Letter spacing: 0.3em
- Alignment: Center with decorative horizontal bars

**Bar Design:**
- Identical to Projects section for visual consistency
- Horizontal lines flanking the title on both sides
- Lines: 1px height, rgba(0, 0, 0, 0.15) color
- Responsive behavior matches Projects section

**Behavior:**
- Static heading with decorative visual bars
- Acts as visual anchor for section

**Files Modified:**
- `src/_user/assets/css/custom.css` - Shared `.section-title` class
- `src/index.md` - Section title text (already in place)

---

#### 5.3 About Category Tabs
**Styling:**
- Same styling as Projects tabs (consistency)
- **Tab labels:**
  - BIO
  - TIMELINE
  - PRESS
  - LINKS

**Behavior:**
- Same as Projects tabs
- Click to switch content
- URL hash updates: `#bio`, `#timeline`, etc.

**Files to Modify:**
- `src/index.md` (tab structure)
- `src/_user/assets/css/custom.css`

---

#### 5.4 About Content Areas
**Template Structure:**
Each About subsection should have its own template/include file:
- `src/_user/includes/about/bio.njk` - Bio tab content
- `src/_user/includes/about/timeline.njk` - Timeline tab content
- `src/_user/includes/about/press.njk` - Press tab content
- `src/_user/includes/about/links.njk` - Links tab content

**Content for each tab based on design:**

**BIO Tab:**
- **Template:** `src/_user/includes/about/bio.njk`
- **Content:** Biography text in paragraphs with actual content
- **Design shows:** Multiple paragraphs of text, well-spaced
- **Sample text visible:**
  - "...Divo, Grex Portmann and Mike Tucker to name a few."
  - "At present Maja Thommen spends her time focused on her sculptural and illustrative work in her current hometown of Berlin, Germany, where she has resided since 2004."

**Styling (applies to all About tabs):**
- Font: Regular weight (~16-18px)
- Color: Dark gray `#333`
- Line height: 1.6-1.8 for readability
- Paragraph spacing: ~20-25px
- Max width: ~700px centered
- Text alignment: Left

**TIMELINE Tab:**
- **Template:** `src/_user/includes/about/timeline.njk`
- **Content:** Chronological list of exhibitions, awards, milestones
- **Suggested format:** Year-based list or visual timeline
- **Should include real timeline data**

**PRESS Tab:**
- **Template:** `src/_user/includes/about/press.njk`
- **Content:** Press mentions, articles, media coverage
- **Suggested format:** List of press items with dates and sources
- **Should include real press data**

**LINKS Tab:**
- **Template:** `src/_user/includes/about/links.njk`
- **Content:** External links, resources, social media
- **Suggested format:** List of links with descriptions
- **Should include real links**

**Behavior:**
- Only active tab content is visible
- Smooth transitions between tabs
- Content should be scannable and readable
- Links should be styled distinctly

**Files to Modify:**
- `src/index.md` (update tab content from placeholders to real content)
- `src/_user/assets/css/custom.css`

---

## Part 6: Footer Section

### Current State
- No dedicated footer visible in current design
- Sidebar footer shows "ATELIER MAAS & THOMMEN"

### Design Requirements

#### 6.1 Footer Container
**Styling:**
- Background: White (matches About section) or light gray
- Border-top: Thin line `#DDDDDD` or similar
- Padding: ~40-60px vertical, ~60px horizontal
- Width: Full width of content area (respects sidebar)
- Position: Bottom of page

**Behavior:**
- Static footer at bottom of page
- Not fixed (scrolls with content)

**Files to Modify:**
- `src/_user/layouts/home.njk` or base layout
- `src/_user/includes/footer.njk` (may override)
- `src/_user/assets/css/custom.css`

---

#### 6.2 Footer Content
**Based on design screenshot (Bottom.png):**

**Left side:**
- Text: "BERLIN, GERMANY"
- Smaller, uppercase, light gray

**Center:**
- **Brand info:**
  - "MAJA EXPLOSIV" - Bold, large
  - "AKA MAJA THOMMEN" - Regular, smaller
  - Horizontal line separator above and below

**Right side:**
- Email: "M-E@MAJA-EXPLOSIV.COM"
- Logo/icon: Triangle warning-style logo

**Bottom row:**
- Left: "SITEMAP"
- Center: "SEARCH"
- Right: "DATENSCHUTZ" (Privacy/Data Protection)

**Styling:**
- Layout: CSS Grid (3 columns for top row, 3 for bottom)
- Font: Uppercase for most text
- Color: Black/dark gray on white/light background
- Spacing: Generous between sections
- Alignment: Top row items align to their columns, bottom row spread across

**Behavior:**
- Links should be functional
- Email should be clickable (mailto:)
- Sitemap links to sitemap page
- Search might trigger search modal/page
- Datenschutz links to privacy policy

**Files to Modify:**
- `src/_user/includes/footer.njk`
- `src/_user/assets/css/custom.css`
- May need: `src/_user/data/site.json` for footer data

---

## Part 7: Responsive Design

### ⚠️ DEFERRED IMPLEMENTATION NOTICE

Responsive design should **only be implemented if the changes are trivial** (e.g., basic CSS adjustments that take minimal effort). If any responsive design requirement is not trivial to implement, it should be added to the "Deferred Changes" list at the end of this document.

**Full responsive design will be implemented at a future date.**

### Design Requirements (For Reference)

#### 7.1 Mobile Layout (<768px) - DEFER IF NOT TRIVIAL
**Sidebar:**
- Convert to hamburger menu or top navigation
- Full-width layout on mobile
- Collapsible navigation

**Hero:**
- Title scales down (~40-50px)
- Description scales down (~16px)
- Padding reduces

**Featured Images:**
- Single column layout OR
- Horizontal scroll
- Grayscale effect may remain or be disabled

**Projects Grid:**
- Single column layout
- Full-width cards
- Maintains card styling

**About:**
- Single column
- Tabs may scroll horizontally or stack

**Footer:**
- Stacks into single column
- Elements center-aligned

**Files to Modify (if implemented):**
- `src/_user/assets/css/custom.css` (media queries)

---

#### 7.2 Tablet Layout (768px - 1024px) - DEFER IF NOT TRIVIAL
**Sidebar:**
- May remain visible or convert to menu
- Possibly narrower

**Projects Grid:**
- 2 columns

**Other sections:**
- Scale proportionally between mobile and desktop

**Files to Modify (if implemented):**
- `src/_user/assets/css/custom.css` (media queries)

---

## Part 8: Interactions and Behaviors

### 8.1 Smooth Scrolling
**Requirement:**
- Clicking sidebar nav links should smooth scroll to sections
- URL hash should update
- Scroll offset should account for any fixed headers

**Implementation:**
- CSS: `scroll-behavior: smooth;` on html element
- Or JavaScript smooth scroll implementation
- Verify with existing template JS

**Files to Modify:**
- `src/_user/assets/css/custom.css`
- May verify: `src/assets/js/main.js`

---

### 8.2 Tab Switching
**Requirement:**
- Clicking tabs switches visible content
- Only one tab active at a time
- Smooth fade transition
- URL hash updates
- Browser back/forward works with tabs
- Direct links to tabs work (e.g., `#sculptures`)

**Current state:**
- Template already has `initTabs()` function in `main.js`
- Verify it supports all requirements

**Files to Verify:**
- `src/assets/js/main.js`
- May need custom JS in `src/_user/assets/js/custom.js`

---

### 8.3 Hover Effects
**Requirements:**
- **Links:** Underline or color change
- **Buttons:** Background darkens or subtle scale
- **Project cards:** Image scales, shadow deepens
- **Carousel controls:** Opacity increases
- All transitions: 0.2-0.3s ease

**Files to Modify:**
- `src/_user/assets/css/custom.css`

---

### 8.4 Featured Images Grayscale Effect
**Requirements:**
- Images display in grayscale by default
- Smooth transition to color on hover (~0.4s ease)
- Smooth transition back to grayscale on mouse leave
- Effect should work consistently across browsers
- No JavaScript required (pure CSS)

**Implementation:**
- CSS filter property: `filter: grayscale(100%);` for default
- Hover state: `filter: grayscale(0%);`
- Transition: `transition: filter 0.4s ease;`

**Browser compatibility:**
- Modern browsers support CSS filters
- Consider fallback for older browsers (graceful degradation)

**Files to Modify:**
- `src/_user/assets/css/custom.css`

---

### 8.5 Accessibility
**Requirements:**
- All interactive elements keyboard accessible
- ARIA labels on tabs, carousel controls
- Focus states clearly visible
- Screen reader friendly
- Skip links functional
- Alt text on all images

**Current state:**
- Template already has good accessibility
- Verify all custom components maintain this

**Files to Verify:**
- All modified layouts and includes
- Custom CSS for focus states

---

## Implementation Workflow

### Implementation Instructions

**This section outlines HOW the plan should be executed:**

1. **Implement parts sequentially in order:**
   - Part 1: Fixed Left Sidebar
   - Part 2: Hero Section
   - Part 3: Featured Images Section (static with grayscale effect)
   - Part 4: Projects Section
   - Part 5: About Section
   - Part 6: Footer Section
   - Part 7: Responsive Design (ONLY if trivial - otherwise defer)
   - Part 8: Interactions and Behaviors

2. **For each part:**
   - Implement all subcomponents for that part
   - Test styling and behavior for each subcomponent
   - Use browser tools to verify visual match with design
   - Cross-reference with design screenshots

3. **After each part is complete:**
   - **Verify visual match:** Use browser inspection tools (DevTools, screenshots) to compare against design files
   - **Test behavior:** Verify all interactions work as specified
   - **Update documentation:**
     - Update `changes.md` If template files were modified or if new features were added, add an entry with date and details
     - Update `homepage-changes.md` with implementation details

4. **Verification checklist for each part:**
   - [ ] Styling matches design (colors, fonts, spacing, sizes)
   - [ ] Layout matches design (positioning, alignment, grid)
   - [ ] Behavior matches specification (clicks, hovers, transitions)
   - [ ] Responsive behavior works correctly
   - [ ] Accessibility maintained (keyboard nav, ARIA, focus states)
   - [ ] No console errors
   - [ ] Documentation updated

5. **Tools for verification:**
   - **Browser DevTools:** Inspect elements, check computed styles, test responsive views
   - **Playwright or similar:** Take screenshots, compare with design
   - **Manual testing:** Click through all interactions, test keyboard navigation
   - **Side-by-side comparison:** Open design screenshots alongside running site

6. **Live server usage:**
   - Server runs at `http://localhost:8080/`
   - Server auto-watches for changes (no manual rebuild needed)
   - Refresh browser to see CSS/template changes
   - Some changes may require hard refresh (Ctrl+Shift+R)

7. **Documentation updates:**
   - **`changes.md`**: Document any modifications to base template files
     - Format: Date, files changed, reason, description
     - Document template files modification (not _user files)
     - Document new customization capabilities  
   
   - **`homepage-changes.md`**: Track all implementation work
     - Format: Date, Part implemented, files changed, notes
     - Updated after each part is completed
     - Include before/after notes, challenges encountered
   
8. **File organization:**
   - All customizations in `src/_user/` directory when possible
   - Override template files using user directory pattern
   - Keep base template files unchanged when possible
   - Use data override system for theme/configuration changes

---

## Files That Will Be Modified/Created

### Definitely Modified
- `src/index.md` - Update hero, carousel, sections content
- `src/_user/assets/css/custom.css` - All styling changes
- `src/_user/includes/left-nav.njk` - Sidebar navigation
- `src/_user/layouts/home.njk` - Homepage layout structure

### Possibly Modified
- `src/_user/includes/footer.njk` - Footer design implementation
- `src/_user/data/theme.js` - Theme color/font overrides
- `src/_user/data/site.json` - Site metadata if needed

### Possibly Created
- `src/_user/includes/project-card.njk` - Reusable project card component
- `src/_user/assets/js/custom.js` - Custom JavaScript if needed
- `src/_data/projects.json` - Project data structure
- `src/_user/includes/carousel-custom.njk` - If carousel needs heavy customization

### Documentation Files
- `/project_docs/homepage-changes.md` - **CREATE NEW** - Track implementation progress
- `/project_docs/homepage-changes-plan.md` - **THIS FILE** - The plan document
- `changes.md` - **UPDATE** - If template files modified

### Verification Files
- May create temporary screenshots in `.playwright-mcp/` for comparison

---

## Key Design Decisions & Notes

1. **Color Palette:**
   - Background: `#C8C8C8` (light gray)
   - Sidebar: Same light gray
   - Text: `#000000` or `#222222` (black/very dark gray)
   - About section: `#FFFFFF` (white) - key visual separator
   - Accents: Black buttons, black active states

2. **Typography:**
   - Font families: font-family: Geist, Rethink, and Inter (for a button)
   - Headings: Bold, uppercase, large
   - Body: Regular weight, good readability
   - Navigation: Uppercase, compact
   - Consistent hierarchy throughout

3. **Spacing:**
   - Generous padding around sections (80-100px vertical)
   - Moderate gaps in grids (20-30px)
   - Tight spacing in sidebar to avoid scrollbars
   - White space used effectively for breathing room

4. **Layout Strategy:**
   - Fixed sidebar (250px) with content offset
   - One-page scroll experience
   - Tab-based content within sections
   - Grid-based project display
   - Responsive stacking on mobile

5. **Interaction Patterns:**
   - Smooth scrolling to anchors
   - Tab switching with URL hash updates
   - Hover states for feedback
   - Carousel autoplay with pause-on-hover
   - Keyboard accessibility maintained

6. **Content Priority:**
   - Hero introduces artist immediately
   - Carousel showcases visual work
   - Projects section is main content (needs real project data)
   - About provides context
   - Footer has contact/legal info

---

## Success Criteria

Implementation will be considered successful when:

1. ✅ Visual design matches Figma designs in all major aspects
2. ✅ All sections are fully implemented with real or realistic content
3. ✅ Navigation and tabs work smoothly
4. ✅ Carousel functions correctly with autoplay and pause
5. ✅ Project cards display in grid with proper styling
6. ✅ Responsive design works on mobile, tablet, desktop
7. ✅ All interactions have appropriate hover/active states
8. ✅ Accessibility standards maintained (keyboard nav, ARIA, alt text)
9. ✅ No console errors or broken functionality
10. ✅ Documentation is complete and up-to-date
11. ✅ Customizations use template override system (no template core modifications if possible)

---

## IMPORTANT

1. Proceed through each part systematically
2. Verify each part before moving to the next
3. Update documentation as you go

---

## Notes and Considerations

- **Design shows masonry grid:** May need custom CSS Grid with varying row/column spans, or consider CSS library
- **Project data needed:** Current design has placeholder - will need real project data structure
- **Images needed:** High-quality images for carousel and project cards
- **Content completion:** About section tabs need full content (timeline, press, links)
- **Mobile menu:** Sidebar conversion to mobile menu needs design specification (hamburger menu pattern recommended)
- **Performance:** Consider lazy loading for images, especially in project grid
- **Browser testing:** Test in Chrome, Firefox, Safari, Edge
- **Template updates:** Plan should work with future upstream template updates due to override system usage

---

---

## Deferred Changes

The following items are deferred to future implementation:

### Responsive Design (Deferred)
- Full mobile layout implementation (Part 7.1)
- Tablet layout optimizations (Part 7.2)
- Mobile navigation menu conversion
- Touch-optimized interactions

**Reason for Deferral:** Responsive design will be implemented in a dedicated phase to ensure proper testing across devices and to avoid complicating the initial desktop implementation.

**Items to be added during implementation:**
- Any responsive design changes that prove non-trivial will be documented here
- Additional deferred items discovered during implementation

---

**End of Plan**
