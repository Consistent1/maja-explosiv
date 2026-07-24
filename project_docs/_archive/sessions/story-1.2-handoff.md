# Story 1.2: Implement Site-Specific Content Structure - Handoff Document

**Story:** 1.2
**Epic:** 1 - Project Foundation & Content Migration
**Agent Handoff:** Winston (Architect) → Amelia (Developer)
**Date:** 2025-10-29

---

## Story Overview

**As a:** Developer
**I want:** To configure this project's content files and data models according to the design, using the conventions provided by the (now validated) upstream template
**So that:** The project is correctly organized and ready for the incoming migrated content.

---

## Acceptance Criteria

1. ✅ Eleventy collections for "projects" and "news" are defined in the project's local configuration.
2. ✅ The content directory (`src/posts`, `src/pages`) is populated with placeholder Markdown files that match the site's information architecture.
3. ✅ Global data files (e.g., `src/_data/site.js`) are configured with site-specific information like the site title and navigation structure.
4. ✅ The local development server correctly builds and serves the placeholder structure without errors.

---

## Architecture Context (from Story 1.1)

### Template Capabilities Validated ✅

The upstream `explosive-11ty` template provides:

- **Collections System:** Dynamic collections via `postCollections` front matter
- **Content Structure:** `src/posts/` for content, `src/pages/` for static pages
- **Data Files:** `src/_data/` for global configuration
- **Override System:** `src/_user/` for site-specific customizations
- **Carousel Component:** Already implemented for image galleries
- **Build Pipeline:** `npm run serve`, `npm run build`, `npm run build:github`

### No Template Changes Required

Story 1.1 confirmed that no upstream template enhancements are needed. All required functionality exists.

---

## Content Structure Requirements

Based on the PRD and UX Specification:

### Collections Needed

1. **Projects Collection** (Portfolio Items)
   - Categories: Sculptures, Installations, Performance, Paintings
   - Each project has multiple images (carousel)
   - Metadata: title, date, description, category

2. **News Collection** (News Feed)
   - Chronological listing
   - Metadata: title, date, content

### Static Pages Needed

1. **Homepage** (`/`)
   - Featured content section
   - Projects section with tabs
   - About section with tabs
   - Contact section

2. **About Pages**
   - Bio
   - Press
   - Links

3. **Contact Page**
   - Placeholder (form not implemented in MVP)

---

## Implementation Guidance

### Step 1: Configure Collections

**File:** `.eleventy.js` (already has collections system)

The template already defines collections in `.eleventy.js` (lines 282-308):
- `allPosts` - All posts
- `pages` - Static pages
- `postCollections` - Dynamic collections based on front matter

**Action:** Verify existing collections work for our needs. May need to add custom collections for "projects" and "news" if not already covered.

### Step 2: Create Placeholder Content Structure

**Content Directory Structure:**

```
src/
├── posts/
│   ├── projects/
│   │   ├── sculptures/
│   │   │   └── placeholder-sculpture.md
│   │   ├── installations/
│   │   │   └── placeholder-installation.md
│   │   ├── performance/
│   │   │   └── placeholder-performance.md
│   │   └── paintings/
│   │       └── placeholder-painting.md
│   └── news/
│       └── placeholder-news.md
└── pages/
    ├── about/
    │   ├── bio.md
    │   ├── press.md
    │   └── links.md
    └── contact.md
```

**Asset Directory Structure:**

```
src/assets/images/
├── projects/
│   ├── sculptures/
│   │   └── placeholder-sculpture/
│   │       └── placeholder.jpg
│   ├── installations/
│   │   └── placeholder-installation/
│   │       └── placeholder.jpg
│   ├── performance/
│   │   └── placeholder-performance/
│   │       └── placeholder.jpg
│   └── paintings/
│       └── placeholder-painting/
│           └── placeholder.jpg
├── news/
│   └── 2024/
│       └── placeholder-news/
│           └── placeholder.jpg
└── shared/
    ├── profile/
    ├── press/
    └── general/
```

**Asset Organization Strategy:**

- **By Category + Series:** Images organized by category (sculptures, installations, etc.) and then by series/project name
- **No Giant Directories:** Each series has its own subdirectory (typically 5-20 images)
- **Flexible Reuse:** Any image can be referenced from any post using absolute paths
- **Naming Convention:** Use slugified series names for directories, descriptive or sequential names for files
  - Example: `/assets/images/projects/sculptures/urban-fragments/urban-fragments-01.jpg`
- **Shared Directory:** For images used across multiple contexts (profile photos, press kit, logos)

**Why This Structure:**
- Avoids single directory with hundreds of images
- Mirrors how artists think about their work (by series/project)
- Doesn't duplicate posts structure but complements it
- Easy to find and manage related images
- Scalable for future growth
- Migration-friendly for TYPO3 content

**Placeholder Front Matter Template:**

```yaml
---
title: "Placeholder Sculpture"
date: 2025-10-29
description: "Placeholder description for a sculpture project"
postCollections: ["projects", "sculptures"]
series: "placeholder-sculpture"
featured: false
images:
  - src: "/assets/images/projects/sculptures/placeholder-sculpture/placeholder.jpg"
    alt: "Placeholder sculpture image"
    caption: "Placeholder caption"
---

Placeholder content goes here. This will be replaced with migrated content from TYPO3.
```

**Example for Different Categories:**

```yaml
# Installations
postCollections: ["projects", "installations"]
series: "placeholder-installation"
images:
  - src: "/assets/images/projects/installations/placeholder-installation/placeholder.jpg"

# Performance
postCollections: ["projects", "performance"]
series: "placeholder-performance"
images:
  - src: "/assets/images/projects/performance/placeholder-performance/placeholder.jpg"

# Paintings
postCollections: ["projects", "paintings"]
series: "placeholder-painting"
images:
  - src: "/assets/images/projects/paintings/placeholder-painting/placeholder.jpg"

# News
postCollections: ["news"]
images:
  - src: "/assets/images/news/2024/placeholder-news/placeholder.jpg"
```

### Step 3: Configure Global Data Files

**File:** `src/_data/site.js`

Update with site-specific information:

```javascript
module.exports = {
  name: "Maja Explosiv",
  title: "Maja Thommen - Artist Portfolio",
  description: "Portfolio website for artist Maja Thommen",
  url: "https://consistent1.github.io/maja-explosiv/",
  author: "Maja Thommen",
  language: "en",
  locale: "en_US"
};
```

**File:** `src/_data/navigation.js` (may need to create)

Define navigation structure:

```javascript
module.exports = [
  {
    label: "Projects",
    url: "/#projects",
    children: [
      { label: "Sculptures", url: "/#sculptures" },
      { label: "Installations", url: "/#installations" },
      { label: "Performance", url: "/#performance" },
      { label: "Paintings", url: "/#paintings" }
    ]
  },
  {
    label: "About",
    url: "/#about",
    children: [
      { label: "Bio", url: "/about/bio/" },
      { label: "Press", url: "/about/press/" },
      { label: "Links", url: "/about/links/" }
    ]
  },
  {
    label: "Contact",
    url: "/contact/"
  }
];
```

### Step 4: Verify Build

**Commands to run:**

```bash
# Start development server
npm run serve

# Verify build succeeds
npm run build

# Check for errors in terminal output
```

**Expected Outcome:**
- Server starts without errors
- All placeholder pages are accessible
- Collections are populated
- No build warnings or errors

---

## Asset Organization Details

### Naming Conventions

**Directory Names:**
- Use slugified series/project names: `urban-fragments`, `light-and-space`
- Lowercase, hyphen-separated
- Descriptive and meaningful

**File Names:**
- **For portfolio images:** `[series-slug]-[number].jpg`
  - Example: `urban-fragments-01.jpg`, `urban-fragments-02.jpg`
  - Self-documenting, can identify series from filename
- **For shared/news images:** `[descriptive-name].jpg`
  - Example: `maja-portrait.jpg`, `exhibition-berlin-opening.jpg`
  - More semantic, easier to identify specific images

### Migration Preparation

This structure is designed to support the upcoming migration (Stories 1.4-1.5):

**Story 1.4 (Migrate Static Assets):**
- Extract images from TYPO3 backup
- Organize into category/series subdirectories
- Rename files using naming conventions
- Create mapping file (old path → new path)

**Story 1.5 (Link Migrated Content and Assets):**
- Use mapping file to update image references in Markdown
- Update front matter with new image paths
- Verify all images are correctly referenced

### Placeholder Images

For Story 1.2, you can use:
- Simple colored rectangles (create with any image editor)
- Free placeholder images from https://placehold.co/
- Example: `https://placehold.co/800x600/png?text=Placeholder+Sculpture`
- Download and save to appropriate directories

---

## Files to Review/Modify

1. **`.eleventy.js`** - Verify collections configuration (lines 282-308)
2. **`src/_data/site.js`** - Update site metadata
3. **`src/_data/navigation.js`** - Create navigation structure (may not exist yet)
4. **`src/posts/`** - Create placeholder content
5. **`src/pages/`** - Create static pages
6. **`src/assets/images/`** - Create asset directory structure with placeholders
7. **`package.json`** - Verify scripts are correct (already validated)

---

## Success Criteria Checklist

### Content Structure

- [ ] Collections for "projects" and "news" are defined
- [ ] Placeholder content exists in `src/posts/projects/` (4 categories: sculptures, installations, performance, paintings)
- [ ] Placeholder content exists in `src/posts/news/`
- [ ] Static pages exist in `src/pages/about/` (bio, press, links)
- [ ] Contact page exists at `src/pages/contact.md`

### Asset Structure

- [ ] Asset directory structure created in `src/assets/images/`
- [ ] Subdirectories for projects (sculptures, installations, performance, paintings)
- [ ] Subdirectories for news (organized by year)
- [ ] Shared directory created (profile, press, general)
- [ ] Placeholder images placed in appropriate directories
- [ ] Image paths in placeholder Markdown files follow naming conventions

### Configuration

- [ ] `src/_data/site.js` has correct site information
- [ ] Navigation structure is defined (in `src/_data/navigation.js` or similar)

### Build Verification

- [ ] `npm run serve` starts without errors
- [ ] `npm run build` completes successfully
- [ ] All placeholder pages are accessible in browser
- [ ] Placeholder images display correctly on pages

---

## Notes for Developer (@dev)

- **Don't worry about design/styling** - This is just structure for migration
- **Keep it simple** - Minimal placeholder content is fine
- **Use existing template patterns** - Follow the conventions in the template
- **Test the build** - Make sure everything compiles before marking complete

---

## Next Story

**Story 1.3:** Script and Execute Content Migration
- Extract content from TYPO3 SQL database
- Convert to Markdown files
- Populate the structure created in Story 1.2

---

**Ready for @dev to implement!**

