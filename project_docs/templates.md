# Eleventy Template System Documentation
**Maja Explosiv Website**

**Last Updated:** December 23, 2025  
**Template Engine:** Nunjucks (.njk)

---

## Overview

The Maja Explosiv website uses a hierarchical template system built on Eleventy with Nunjucks. Templates are organized using an **override system** that allows site-specific customizations without modifying base template files, preventing merge conflicts when pulling upstream updates.

---

## Template Hierarchy

### Core Layout Chain

```
base.njk
  └── sidebar-layout.njk
        ├── home.njk
        ├── page.njk
        ├── post.njk (with project detection)
        ├── project.njk
        ├── collection.njk
        └── collections-overview.njk

contact.njk (extends base.njk directly, bypasses sidebar)
```

---

## Template Override System

### How It Works

1. **Base Templates:** `src/_layouts/` (upstream template, tracked in git)
2. **Theme Templates:** `src/_layouts/theme/` (copies for extending, tracked in git)
3. **User Overrides:** `src/_user/layouts/` (site customizations, tracked in git)
4. **Build-Time Merging:** `.cache/layouts/` (generated, git-ignored)

At build time:
- Base layouts copied to `.cache/layouts/`
- User overrides copied to `.cache/layouts/` (overwriting base)
- Eleventy uses `.cache/layouts/` as the layouts directory
- No source files modified - clean separation!

### Current Site Customizations

All layouts in `src/_user/layouts/` are customized to extend `sidebar-layout.njk` instead of `base.njk` to ensure the fixed left sidebar appears consistently across all page types.

---

## Template Descriptions

### 1. base.njk
**Purpose:** Foundation HTML structure for all pages  
**Location:** `src/_user/layouts/base.njk`  
**Extends:** None (root template)

**Features:**
- HTML document structure (`<html>`, `<head>`, `<body>`)
- Meta tags (SEO, Open Graph, Twitter Cards)
- Google Fonts loading (Inter, Rethink Sans, Geist)
- CSS theme variables injection
- Main stylesheet includes (`main.css`, `custom.css`)
- JavaScript includes

**Blocks:**
- `{% block head %}` - Additional head content
- `{% block header %}` - Header section
- `{% block content %}` - Main content area
- `{% block footer %}` - Footer section
- `{% block scripts %}` - Additional scripts

**Usage:** Extended by `sidebar-layout.njk` and `contact.njk`

---

### 2. sidebar-layout.njk
**Purpose:** Provides fixed left sidebar navigation wrapper  
**Location:** `src/_user/layouts/sidebar-layout.njk`  
**Extends:** `base.njk`

**Site-Specific Feature:** Fixed left sidebar (250px width, 100vh height)

**Structure:**
```html
<div class="main-container">
    <aside class="left-sidebar">
        <!-- Brand header: MAJA EXPLOSIV / AKA MAJA THOMMEN -->
        <nav class="nav-menu-container">
            <!-- PROJECTS section -->
            <!-- ABOUT section -->
        </nav>
        <!-- Footer: ATELIER MAAS & THOMMEN -->
    </aside>
    <main class="main-content">
        <!-- Child template content -->
    </main>
</div>
```

**Navigation Sections:**
- **PROJECTS:** Sculptures, Installations, Performance, Paintings
- **ABOUT:** Bio, Timeline, Press, Links, Contact

**Features:**
- Fixed positioning (no scrollbars)
- Compact spacing to fit all navigation
- Tab integration with `data-tab-link` attributes
- Breadcrumb suppression for homepage
- Conditional page title display (`showPageTitle`)

**Used By:** home.njk, page.njk, post.njk, project.njk, collection.njk, collections-overview.njk

---

### 3. home.njk
**Purpose:** Homepage template with hero, carousel, and tabbed sections  
**Location:** `src/_user/layouts/home.njk`  
**Extends:** `sidebar-layout.njk`

**Design:** "One-page" experience with tabbed navigation

**Features:**
- **Hero Section:**
  - Optional background image
  - Title and subtitle display
  - Description content
  - CTA button with arrow icon
  
- **Carousel Support:**
  - Multiple slides configuration
  - Image display with captions
  - Automatic slideshow or manual controls

- **Custom Sections with Tabs:**
  - Projects section (tabbed: sculptures, installations, performance, paintings)
  - About section (tabbed: bio, timeline, press, links)
  - Tab switching via URL hash
  - Dynamic content loading

**Front Matter Example:**
```yaml
layout: home.njk
title: "Maja Explosiv"
hero:
  title: "MAJA EXPLOSIV"
  subtitle: "Artist & Sculptor"
  description: "Contemporary art..."
customSections:
  - id: "projects"
    title: "PROJECTS"
    hasTabs: true
    tabs: [...]
```

**Used For:** `src/index.md`

---

### 4. page.njk
**Purpose:** Static page template  
**Location:** `src/_user/layouts/page.njk`  
**Extends:** `sidebar-layout.njk`

**Features:**
- Optional featured image with caption
- Main content area
- Last modified date (if `showLastModified: true`)
- Related pages section (if `relatedPages` defined)
- Table of contents placeholder (if `showTableOfContents: true`)

**Structure:**
```html
<article class="page-content">
    <div class="page-featured-image">...</div>
    <div class="page-body">{{ content | safe }}</div>
    <div class="page-meta">...</div>
    <aside class="related-pages">...</aside>
</article>
```

**Used For:** About pages, general static content

---

### 5. post.njk
**Purpose:** Generic post template with **automatic project detection**  
**Location:** `src/_user/layouts/post.njk`  
**Extends:** `sidebar-layout.njk`

**Key Feature:** Detects if post is a project and applies different markup

**Project Detection Logic:**
```javascript
{% set isProject = (category in ['sculptures', 'installations', 'performance', 'paintings']) 
                   or ('sculptures' in tags) 
                   or ('installations' in tags) 
                   or ('performance' in tags) 
                   or ('paintings' in tags) %}
```

**If Project (`isProject = true`):**
- Uses project-specific markup (same as `project.njk`)
- Large prominent title
- Full-width hero image
- Compact metadata section
- Project description area
- **Image gallery from `images` front matter** ✨ (Added Dec 23, 2025)
- Legacy `mediaGallery` support

**If Regular Post (`isProject = false`):**
- Standard blog post layout
- Post header with featured image
- Post meta (collections, date, author, reading time)
- Post content
- Post footer (tags, social sharing)

**Image Gallery Support (Projects):**
```yaml
images:
  - src: /assets/images/projects/sculptures/example/example-01.jpg
    alt: "Image description"
    caption: "Optional caption"
  - src: /assets/images/projects/sculptures/example/example-02.jpg
    alt: "Second image"
```

Renders as:
```html
<div class="project-gallery">
    <div class="gallery-item">
        <img src="..." alt="..." loading="lazy">
        <p class="gallery-caption">...</p>
    </div>
</div>
```

**Used For:** All posts including projects (default layout for `src/posts/`)

---

### 6. project.njk
**Purpose:** Dedicated project/artwork display template  
**Location:** `src/_user/layouts/project.njk`  
**Extends:** `sidebar-layout.njk`

**Design Reference:** `project_docs/design_screenshots/project.png`

**Features:**
- Large, prominent project title
- Full-width hero image (`featuredImage`) as focal point
- Compact metadata section:
  - Title label
  - Description label  
  - Author label (if present)
  - Year display (right-aligned)
- Project description content area
- Media gallery for additional images (`mediaGallery`)

**Structure:**
```html
<article class="project-page">
    <header class="project-header">
        <h1 class="project-title">{{ title }}</h1>
    </header>
    <div class="project-hero-image">...</div>
    <div class="project-metadata">...</div>
    <div class="project-content">{{ content | safe }}</div>
    <div class="project-gallery">...</div>
</article>
```

**Current Usage:** Available but not actively used (projects use `post.njk` instead)

**Note:** The markup is identical to the project section in `post.njk`, but requires explicit `layout: project.njk` in front matter.

---

### 7. collection.njk
**Purpose:** Collection listing/overview page template  
**Location:** `src/_user/layouts/collection.njk`  
**Extends:** `sidebar-layout.njk`

**Displays:** Grid of posts within a single collection

**Features:**
- **Collection Header:**
  - Hero image background (if `collectionData.featuredImage` defined)
  - Collection title and description
  - Post count
  - Parent collection link (for nested collections)

- **Posts Grid:**
  - Card-based layout
  - Featured image per post
  - Post title (linked)
  - Excerpt/description
  - Date

**Structure:**
```html
<div class="collection-page">
    <header class="collection-header">
        <div class="collection-hero">...</div>
        <div class="collection-meta">X posts</div>
    </header>
    <div class="collection-content">
        <div class="posts-grid">
            <article class="post-card">...</article>
        </div>
    </div>
</div>
```

**Used For:** `/collections/{collection-name}/` pages (blog, tutorials, web-development)

**Note:** Currently configured collections are blog-related. Project categories (sculptures, installations, etc.) are not yet configured as Eleventy collections.

---

### 8. collections-overview.njk
**Purpose:** Overview page showing all collections  
**Location:** `src/_user/layouts/collections-overview.njk`  
**Extends:** `sidebar-layout.njk`

**Displays:** Grid of all available collections

**Features:**
- Overview header with title and description
- Collections grid with cards:
  - Featured image
  - Collection title with color accent
  - Collection description
  - Post count
  - Nested collections indicator
  - "View Collection" link

**Structure:**
```html
<div class="collections-overview">
    <header class="overview-header">...</header>
    <div class="overview-content">{{ content | safe }}</div>
    <section class="collections-section">
        <div class="collections-grid">
            <article class="collection-overview-card">...</article>
        </div>
    </section>
</div>
```

**Used For:** `/collections/` page

---

### 9. contact.njk
**Purpose:** Full-screen modal contact page  
**Location:** `src/_user/layouts/contact.njk`  
**Extends:** `base.njk` (bypasses sidebar)

**Design Reference:** `project_docs/design_screenshots/contact.png`

**Special Feature:** Modal overlay presentation (no sidebar)

**Structure:**
```html
<div class="contact-modal-overlay">
    <div class="contact-modal-content">
        <div class="contact-modal-header">
            <!-- ATELIER MAAS & THOMMEN -->
            <!-- 10997 BERLIN -->
        </div>
        <div class="contact-modal-body">
            {{ content | safe }}
        </div>
        <div class="contact-modal-footer">
            (Click outside to close)
        </div>
        <!-- Decorative plant images -->
    </div>
</div>
```

**Interactive Features:**
- Click outside modal to close (navigates back)
- ESC key closes modal
- Decorative images positioned bottom-center and right-faded

**Used For:** `/contact/` page

---

## Template Selection Guide

### When to Use Each Template

| Content Type | Layout | Why |
|-------------|--------|-----|
| Homepage | `home.njk` | Hero, carousel, tabbed sections |
| Static page (About, Bio) | `page.njk` | Simple content, optional features |
| Blog post | `post.njk` | Standard blog formatting |
| **Project/Artwork** | **`post.njk`** | **Auto-detects projects, shows gallery** |
| Collection listing | `collection.njk` | Grid of posts in collection |
| All collections | `collections-overview.njk` | Overview of all collections |
| Contact page | `contact.njk` | Modal overlay design |
| Dedicated project (optional) | `project.njk` | Explicit project layout (not used) |

---

## Current Project Configuration

### Project Categories (Not Eleventy Collections)

Currently, projects are organized by:
- **Folder structure:** `src/posts/projects/{category}/`
- **Front matter:** `category: sculptures` or tags
- **Categories:** sculptures, installations, performance, paintings

**These are NOT configured as Eleventy collections** - they are organizational categories/tags only.

### Converting to Collections (Future)

To make sculptures/installations/etc. true Eleventy collections, would need to:
1. Define collections in `.eleventy.js`
2. Create collection overview pages: `/collections/sculptures/`, etc.
3. Update navigation to link to collection pages

---

## Front Matter Examples

### Project Post (using post.njk)
```yaml
---
title: "Sisyphos Gate"
date: 2013-08-01
category: sculptures
tags:
  - sculptures
  - sculptural work
  - gate
layout: post.njk
images:
  - src: /assets/images/projects/sculptures/sisyphos-gate/gate-01.jpg
    alt: "Front view"
    caption: "Main entrance"
  - src: /assets/images/projects/sculptures/sisyphos-gate/gate-02.jpg
    alt: "Detail view"
---

Project description content here...
```

### Static Page (using page.njk)
```yaml
---
title: "About"
description: "About the artist"
layout: page.njk
featuredImage: /assets/images/about-hero.jpg
showLastModified: true
relatedPages:
  - url: /about/bio/
    title: "Biography"
---

Page content here...
```

### Collection Page (using collection.njk)
```yaml
---
layout: collection.njk
collectionName: blog
title: "Blog"
description: "Latest articles and updates"
---
```

---

## Key Customizations from Upstream

### Changes Made to Templates

All documented in [changes.md](../changes.md):

1. **Sidebar Integration:**
   - All main layouts extend `sidebar-layout.njk` instead of `base.njk`
   - Ensures fixed left sidebar on all pages except contact

2. **Project Detection in post.njk:**
   - Auto-detects project posts by category/tags
   - Applies project-specific markup automatically
   - No need to manually choose `project.njk`

3. **Image Gallery Support:**
   - Added `images` front matter support to `post.njk`
   - Renders gallery for project posts
   - Supports `src`, `alt`, and `caption` per image

4. **One-Page Homepage:**
   - Tabbed sections for Projects and About
   - Carousel component
   - URL hash navigation

5. **Contact Modal:**
   - Full-screen overlay design
   - Click-outside-to-close behavior
   - Decorative plant images

---

## CSS Styling

Templates rely on CSS defined in:
- `src/assets/css/main.css` - Base template styles
- `src/_user/assets/css/custom.css` - Site-specific overrides

**Key Custom Styles:**
- `.left-sidebar` - Fixed sidebar positioning (250px, no overflow)
- `.main-content` - Content offset (`margin-left: 250px`)
- `.project-page` - Project layout styles
- `.project-gallery` - Image gallery grid
- Tab styling with transitions and active states

See [changes.md](../changes.md) for complete CSS customization details.

---

## Template Blocks and Filters

### Common Nunjucks Blocks
- `{% block head %}` - Additional head content
- `{% block header %}` - Header section
- `{% block content %}` - Main content
- `{% block footer %}` - Footer section
- `{% block scripts %}` - Additional scripts

### Common Filters
- `| safe` - Renders HTML without escaping
- `| url` - Converts to URL
- `| slug` - Creates URL-friendly slug
- `| date('YYYY-MM-DD')` - Formats date
- `| dateDisplay` - Custom date display
- `| title` - Title case conversion
- `| find('property', 'value')` - Finds item in array
- `| getPostsByCollection(name)` - Filters posts by collection
- `| getUniqueCollections` - Gets unique collection names

---

## Build Process

### Template Merging

During build (defined in `.eleventy.js`):

1. Create `.cache/layouts/` directory
2. Copy all files from `src/_layouts/` to `.cache/layouts/`
3. Create `.cache/layouts/theme/` subdirectory with base template copies
4. Copy all files from `src/_user/layouts/` to `.cache/layouts/` (overwrites base)
5. Eleventy uses `.cache/layouts/` as the layouts directory

**Result:** User customizations always win, no source file modifications.

### Watch Targets

Eleventy watches for changes in:
- `src/_layouts/`
- `src/_user/layouts/`
- `src/_includes/`
- `src/_user/includes/`
- `src/_user/assets/css/`

Changes trigger automatic rebuild in development mode (`npm run serve`).

---

## References

- **Template System Details:** [README.md](../README.md) - Sections on "Template Override System"
- **Site Customizations:** [changes.md](../changes.md) - All template modifications documented
- **Design Screenshots:** `project_docs/design_screenshots/` - Visual references for layouts
- **Eleventy Config:** `.eleventy.js` - Build configuration and override system

---

**Document End**
