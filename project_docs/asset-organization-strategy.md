# Asset Organization Strategy - Maja Explosiv Website

**Author:** Winston (Architect)
**Date:** 2025-10-29
**Status:** Approved

---

## Overview

This document defines the asset organization strategy for the Maja Explosiv portfolio website. The strategy balances maintainability, flexibility, and scalability while avoiding the pitfalls of storing hundreds of images in a single directory.

---

## Design Principles

1. **No Giant Directories** - Avoid single directories with hundreds of files
2. **Conceptual Organization** - Mirror how artists think about their work (by series/project)
3. **Flexible Reuse** - Any image can be referenced from any post
4. **Migration-Friendly** - Support mapping from TYPO3 file structure
5. **Long-Term Maintainability** - Easy to find, add, and manage images
6. **Scalable** - Structure grows naturally with content

---

## Directory Structure

```
src/assets/images/
├── projects/
│   ├── sculptures/
│   │   ├── [series-slug-1]/
│   │   │   ├── [series-slug-1]-01.jpg
│   │   │   ├── [series-slug-1]-02.jpg
│   │   │   └── [series-slug-1]-03.jpg
│   │   ├── [series-slug-2]/
│   │   └── [series-slug-3]/
│   ├── installations/
│   │   ├── [series-slug-1]/
│   │   └── [series-slug-2]/
│   ├── performance/
│   │   ├── [series-slug-1]/
│   │   └── [series-slug-2]/
│   └── paintings/
│       ├── [series-slug-1]/
│       └── [series-slug-2]/
├── news/
│   ├── 2024/
│   │   ├── [event-slug-1]/
│   │   └── [event-slug-2]/
│   ├── 2023/
│   └── 2022/
└── shared/
    ├── profile/
    │   └── maja-portrait.jpg
    ├── press/
    │   └── press-kit-images/
    └── general/
        └── logos/
```

---

## Naming Conventions

### Directory Names

**Format:** `[descriptive-slug]`

**Rules:**
- Lowercase only
- Hyphen-separated (kebab-case)
- Descriptive and meaningful
- No spaces, underscores, or special characters

**Examples:**
- ✅ `urban-fragments`
- ✅ `light-and-space`
- ✅ `body-in-motion`
- ❌ `Urban_Fragments`
- ❌ `project 1`
- ❌ `série-française` (avoid non-ASCII)

### File Names

#### Portfolio Images (Projects)

**Format:** `[series-slug]-[number].jpg`

**Rules:**
- Match the parent directory slug
- Use zero-padded numbers (01, 02, 03, etc.)
- Consistent file extension (.jpg, .png, etc.)

**Examples:**
- `urban-fragments-01.jpg`
- `urban-fragments-02.jpg`
- `light-and-space-01.jpg`

**Benefits:**
- Self-documenting (can identify series from filename)
- Easy to sort and sequence
- Clear relationship to parent directory

#### News and Shared Images

**Format:** `[descriptive-name].jpg`

**Rules:**
- Descriptive and semantic
- Lowercase, hyphen-separated
- Avoid generic names like "image1.jpg"

**Examples:**
- `maja-portrait-2024.jpg`
- `exhibition-berlin-opening.jpg`
- `award-ceremony-group-photo.jpg`
- `logo-maja-explosiv.svg`

**Benefits:**
- More semantic and self-explanatory
- Easier to identify specific images
- Better for one-off or unique images

---

## Organization by Category

### Projects (Portfolio Work)

**Path:** `src/assets/images/projects/[category]/[series-slug]/`

**Categories:**
- `sculptures/` - Three-dimensional sculptural works
- `installations/` - Installation art pieces
- `performance/` - Performance art documentation
- `paintings/` - Two-dimensional painted works

**Typical Structure:**
```
projects/sculptures/urban-fragments/
├── urban-fragments-01.jpg
├── urban-fragments-02.jpg
├── urban-fragments-03.jpg
├── urban-fragments-04.jpg
└── urban-fragments-05.jpg
```

**Typical Directory Size:** 5-20 images per series

### News

**Path:** `src/assets/images/news/[year]/[event-slug]/`

**Organization:** By year, then by event/article

**Example:**
```
news/2024/
├── exhibition-berlin/
│   ├── opening-night.jpg
│   └── installation-view.jpg
└── award-ceremony/
    └── award-photo.jpg
```

### Shared Assets

**Path:** `src/assets/images/shared/[category]/`

**Categories:**
- `profile/` - Artist portraits and headshots
- `press/` - Press kit images, logos for media
- `general/` - Logos, icons, other shared assets

**Use Case:** Images used across multiple contexts (homepage, about page, press page, etc.)

---

## Referencing Images in Content

### In Markdown Front Matter

**Absolute Paths from Site Root:**

```yaml
---
title: "Urban Fragments"
date: 2024-03-15
description: "A series exploring urban decay and renewal"
postCollections: ["projects", "sculptures"]
series: "urban-fragments"
images:
  - src: "/assets/images/projects/sculptures/urban-fragments/urban-fragments-01.jpg"
    alt: "Urban Fragments - Piece 1"
    caption: "Rusted metal and concrete, 2024"
  - src: "/assets/images/projects/sculptures/urban-fragments/urban-fragments-02.jpg"
    alt: "Urban Fragments - Piece 2"
    caption: "Detail view showing texture"
---
```

### Reusing Images Across Posts

**Same image referenced in multiple places:**

```yaml
# Homepage featured content
featuredImage: "/assets/images/projects/sculptures/urban-fragments/urban-fragments-01.jpg"

# Press page
pressImages:
  - "/assets/images/projects/sculptures/urban-fragments/urban-fragments-01.jpg"
  - "/assets/images/shared/press/exhibition-photo.jpg"

# About page
authorPhoto: "/assets/images/shared/profile/maja-portrait-2024.jpg"
```

**Benefits:**
- Single source of truth for each image
- No duplication of files
- Easy to update (change file, all references update)

---

## Migration Strategy

### Story 1.4: Migrate Static Assets

**Process:**

1. **Extract images from TYPO3 backup**
   - Locate image files in TYPO3 fileadmin directory
   - Identify associated metadata from database

2. **Analyze and categorize**
   - Determine category (sculptures, installations, etc.)
   - Identify series/project grouping
   - Determine original sequence/order

3. **Create directory structure**
   - Create category directories
   - Create series subdirectories
   - Use slugified names from TYPO3 metadata

4. **Copy and rename files**
   - Copy images to appropriate directories
   - Rename using naming conventions
   - Preserve original quality (no compression yet)

5. **Create mapping file**
   - Document old path → new path
   - Include metadata (category, series, sequence)
   - Use for reference updates in Story 1.5

**Mapping File Format (JSON):**

```json
{
  "migrations": [
    {
      "typo3_id": "123",
      "old_path": "fileadmin/user_upload/sculptures/img_0456.jpg",
      "new_path": "/assets/images/projects/sculptures/urban-fragments/urban-fragments-01.jpg",
      "category": "sculptures",
      "series": "urban-fragments",
      "sequence": 1,
      "alt_text": "Urban Fragments - Piece 1",
      "caption": "Rusted metal and concrete, 2024"
    }
  ]
}
```

### Story 1.5: Link Migrated Content and Assets

**Process:**

1. **Load mapping file**
2. **Update Markdown front matter** with new image paths
3. **Verify all images** are correctly referenced
4. **Test build** to ensure no broken image links

---

## Future Optimization (Phase 2)

Once content is migrated and the site is live, consider:

1. **Eleventy Image Plugin**
   - Generate responsive image sizes
   - Create WebP/AVIF versions
   - Automatic optimization

2. **Thumbnail Generation**
   - Create thumbnails for gallery views
   - Reduce page load for collection pages

3. **Lazy Loading**
   - Implement lazy loading for below-fold images
   - Improve initial page load performance

4. **CDN Integration**
   - Consider image CDN for faster delivery
   - Automatic format negotiation

**Note:** For MVP (Epic 1), keep it simple - organize originals, reference correctly, optimize later.

---

## Maintenance Guidelines

### Adding New Series

1. Create new subdirectory: `src/assets/images/projects/[category]/[new-series-slug]/`
2. Add images using naming convention: `[new-series-slug]-01.jpg`, etc.
3. Create corresponding Markdown file in `src/posts/projects/[category]/`
4. Reference images in front matter

### Adding Images to Existing Series

1. Determine next sequence number
2. Add image with correct naming: `[series-slug]-[next-number].jpg`
3. Update Markdown front matter to include new image

### Reorganizing Series

1. Move/rename directory
2. Update image filenames if series slug changes
3. Update all Markdown files that reference the series
4. Test build to verify no broken links

---

## Benefits of This Strategy

✅ **Manageable Directory Sizes** - No single directory with hundreds of images
✅ **Logical Organization** - Mirrors how artists think about their work
✅ **Flexible Reuse** - Any image can be referenced from anywhere
✅ **Migration-Friendly** - Clear mapping from TYPO3 structure
✅ **Scalable** - Easy to add new series and categories
✅ **Maintainable** - Easy to find and manage images
✅ **Git-Friendly** - Clear structure for version control
✅ **Future-Proof** - Supports optimization and enhancement

---

## Questions and Answers

**Q: What if an image belongs to multiple categories?**
**A:** Store it in the primary category and reference it from other posts. Use the `shared/` directory if it truly doesn't belong to any specific category.

**Q: What if I don't know the series name during migration?**
**A:** Use a temporary slug like `untitled-series-1` and rename later. Update references in Markdown files after renaming.

**Q: Should I compress images before adding them?**
**A:** For MVP, no. Store originals and add optimization in Phase 2 with Eleventy Image plugin.

**Q: What about videos or other media?**
**A:** Follow the same organizational pattern: `src/assets/videos/projects/[category]/[series-slug]/`

---

**Status:** ✅ Approved for implementation in Story 1.2

