# TYPO3 to 11ty Migration - Discovery Report
## maja-explosiv.com Website Analysis

**Report Date:** 2025-10-13  
**TYPO3 Version:** 4.2.14  
**Database Size:** 47 MB  
**Total File System Size:** ~700 MB

---

## Executive Summary

This discovery report documents the findings from analyzing the TYPO3 4.2.14 installation for maja-explosiv.com. The site is a portfolio/artist website featuring sculptures, paintings, and recent work by Maja Thommen (a.k.a. Maja Explosiv). The analysis reveals a relatively small but media-rich website with extensive image galleries and custom templates.

### Key Findings

- **Content Volume:** Small (24 content elements, 4 news items)
- **Media Volume:** Large (5,409 image files totaling ~700 MB)
- **Site Complexity:** Medium (custom templates, multiple extensions)
- **Database Tables:** 109 tables
- **Primary Content Type:** Image galleries and portfolio work
- **Special Features:** Flash animations (deprecated), custom templates, news system

---

## 1. File System Analysis

### 1.1 Directory Structure Overview

```
old/TYPO3BU/_/
├── fileadmin/          # User content and media (700+ MB)
├── typo3conf/          # Configuration and extensions
├── typo3_src-4.2.14/   # TYPO3 core files
├── typo3temp/          # Temporary files (can be ignored)
└── uploads/            # Legacy uploads directory
```

### 1.2 Key Directories in `fileadmin/`

| Directory | Size | Purpose | Priority |
|-----------|------|---------|----------|
| `s-maj/` | 475 MB | Main image gallery (Maja's work) | **HIGH** |
| `images/` | 60 MB | General site images | **HIGH** |
| `s-pf/` | 33 MB | Portfolio images | **HIGH** |
| `db-jdfas87/` | 33 MB | Database backups (can ignore) | LOW |
| `downloads/` | 15 MB | Downloadable files | MEDIUM |
| `flash/` | 7.4 MB | Flash animations (deprecated) | LOW |
| `Flash2/` | 2.6 MB | More Flash files (deprecated) | LOW |
| `s-mhk/` | 2.8 MB | Additional gallery | MEDIUM |
| `s-wt/` | 1.6 MB | Additional gallery | MEDIUM |
| `free_template/` | 304 KB | Template files | MEDIUM |
| `css/` | 204 KB | Stylesheets | MEDIUM |
| `TS/` | 116 KB | TypoScript files | MEDIUM |

### 1.3 Media File Inventory

**Total Image Files:**
- `fileadmin/`: 3,687 images (JPG, PNG, GIF)
- `uploads/`: 1,722 images (mostly RTE magic images)
- **Total:** ~5,409 image files

**Image Organization Patterns:**
- Images organized by project/gallery (s-maj, s-pf, s-mhk, s-wt)
- RTE (Rich Text Editor) images in `uploads/` with naming pattern `RTEmagicC_*.jpg` and `RTEmagicP_*.jpg`
- Multiple image sizes/variants for same image (thumbnails, resized versions)

**Other Media:**
- Flash files (.swf) - **DEPRECATED, needs conversion or removal**
- Audio files (.mp3) in `downloads/media/`
- PDF documents in `downloads/`
- Fonts in `fileadmin/fonts/`

### 1.4 Template and Configuration Files

**TypoScript Templates:**
- Located in `fileadmin/TS/`
- Multiple template files for different layouts
- Custom menu configurations
- YAML-based templates

**CSS Files:**
- Located in `fileadmin/css/`
- Multiple layout variations (2-column, 3-column)
- Custom navigation styles

**HTML Templates:**
- Located in `fileadmin/free_template/`
- Custom page templates
- Form templates (MailformPlus)
- News templates

---

## 2. Database Analysis

### 2.1 Database Overview

**Database Name:** usr_p51487_2  
**Size:** 47 MB  
**Character Set:** latin1_german1_ci (needs UTF-8 conversion)  
**Total Tables:** 109

### 2.2 Core TYPO3 Tables

**Pages Table (`pages`):**
- Contains page tree structure
- Estimated rows: ~50-100 pages (based on INSERT statements)
- Fields include: title, doktype, hidden, nav_title, keywords, description, etc.

**Content Elements Table (`tt_content`):**
- Contains page content elements
- **24 content element records** (INSERT statements counted)
- Content types: text, images, plugins, etc.
- Fields include: header, bodytext, image, layout, colPos, etc.

### 2.3 Extension Tables

**News Extension (`tt_news`):**
- **4 news records** found
- Tables: `tt_news`, `tt_news_cat`, `tt_news_cat_mm`, `tt_news_related_mm`
- Used for blog/news functionality

**Calendar Extension (`tx_cal_*`):**
- Multiple calendar-related tables
- Tables: `tx_cal_event`, `tx_cal_calendar`, `tx_cal_category`, `tx_cal_location`, `tx_cal_organizer`
- May not be actively used (needs verification)

**DAM (Digital Asset Management) (`tx_dam_*`):**
- Tables: `tx_dam`, `tx_dam_cat`, `tx_dam_file_tracking`, `tx_dam_log_index`
- Used for managing media files
- Important for understanding file references

**Other Extensions:**
- `tx_andshadowbox_content` - Lightbox/image viewer
- `tx_rgslideshow` - Image slideshow
- `tx_rgsmoothgallery` - Image gallery
- `tt_address` - Address management
- Various backend/admin extensions

### 2.4 Important Observations

1. **Character Encoding:** Database uses `latin1_german1_ci` collation
   - **Action Required:** Convert to UTF-8 during migration
   - May contain German special characters (ä, ö, ü, ß)

2. **Content Volume:** Very small content volume (24 elements, 4 news items)
   - Migration will be straightforward
   - Focus should be on media files

3. **File References:** Need to map DAM references to actual files
   - `tx_dam` table contains file metadata
   - `sys_file` tables may contain file references

---

## 3. Live Site Analysis

### 3.1 Site Structure

**Homepage:** https://www.maja-explosiv.com/

**Main Navigation Sections:**
- SHOW
- SCULPTURES
- PAINTING
- RECENT WORK

**Additional Pages:**
- CONTACT
- BIO
- PRESS
- LINKS
- Sitemap
- Search
- Datenschutz (Privacy Policy)

### 3.2 Content Types Identified

1. **Portfolio/Gallery Pages**
   - Primary content type
   - Heavy use of images
   - Organized by category (sculptures, paintings, shows)

2. **Text Pages**
   - Bio
   - Contact
   - Press
   - Links

3. **News/Blog** (if active)
   - 4 news items in database
   - May not be prominently displayed

### 3.3 Design and Layout

**Current Design:**
- Clean, minimalist layout
- Image-focused design
- Simple navigation
- Responsive elements (needs verification)

**Technical Stack:**
- TYPO3 4.2.14 (very outdated)
- Flash animations (deprecated - needs replacement)
- Custom CSS layouts
- JavaScript for interactivity

---

## 4. Content Type Mapping

### 4.1 TYPO3 to 11ty Content Mapping

| TYPO3 Content | 11ty Structure | Notes |
|---------------|----------------|-------|
| Pages (standard) | `src/pages/*.md` | Static pages (Bio, Contact, etc.) |
| Pages (gallery) | `src/collections/*.md` or custom structure | Portfolio galleries |
| tt_news | `src/posts/*.md` | News/blog posts (if needed) |
| tt_content (text) | Markdown content | Convert HTML to Markdown |
| tt_content (images) | Front matter + shortcodes | Image galleries, carousels |
| Media files | `src/assets/images/` or `src/media/` | Organized by category |
| Flash animations | **Needs replacement** | Convert to HTML5/CSS/JS or remove |

### 4.2 Recommended 11ty Structure

```
src/
├── pages/
│   ├── bio.md
│   ├── contact.md
│   ├── press.md
│   └── links.md
├── collections/
│   ├── sculptures.md
│   ├── paintings.md
│   ├── shows.md
│   └── recent-work.md
├── posts/ (optional)
│   └── [news items if needed]
├── assets/
│   └── images/
│       ├── sculptures/
│       ├── paintings/
│       ├── shows/
│       └── recent-work/
└── _data/
    ├── site.json
    ├── navigation.json
    └── galleries.json
```

---

## 5. Technical Challenges and Considerations

### 5.1 Character Encoding

**Issue:** Database uses `latin1_german1_ci` collation  
**Impact:** German special characters may not display correctly  
**Solution:** Convert to UTF-8 during extraction  
**Tools:** MySQL charset conversion, iconv, or manual replacement

### 5.2 Flash Content

**Issue:** Site uses Flash animations (.swf files)  
**Impact:** Flash is deprecated and not supported in modern browsers  
**Solution Options:**
1. Remove Flash content entirely
2. Replace with static images
3. Convert to HTML5/CSS animations
4. Use video format (if animations are complex)

**Recommendation:** Replace with static images or simple CSS animations

### 5.3 Image Optimization

**Issue:** 5,409 images totaling ~700 MB  
**Impact:** Large file sizes, slow page loads  
**Solution:**
1. Remove duplicate/unused images
2. Optimize image sizes (compress, resize)
3. Generate responsive image variants
4. Implement lazy loading
5. Consider modern formats (WebP, AVIF)

**Estimated Reduction:** 50-70% size reduction possible

### 5.4 RTE Magic Images

**Issue:** TYPO3's RTE creates multiple image variants with cryptic names  
**Pattern:** `RTEmagicC_*.jpg` (cropped/resized), `RTEmagicP_*.jpg` (original)  
**Solution:**
1. Map RTE images to original files
2. Rename to meaningful names
3. Re-optimize for web
4. Update content references

### 5.5 File References

**Issue:** Need to resolve file references from database to actual files  
**Tables:** `tx_dam`, `sys_file`, `sys_file_reference`  
**Solution:**
1. Export file metadata from database
2. Map database IDs to file paths
3. Update content with correct file paths
4. Verify all images are accessible

---

## 6. Extension Functionality Analysis

### 6.1 Active Extensions (from typo3conf/ext/)

**Content/Media Extensions:**
- `dam` - Digital Asset Management
- `dam_catedit`, `dam_index`, `dam_info`, `dam_ttcontent` - DAM modules
- `rgsmoothgallery` - Image gallery
- `rgslideshow` - Image slideshow
- `ko_imageflow` - Image flow viewer
- `cfa_mooflow` - MooTools-based image flow

**News/Blog:**
- `tt_news` - News extension

**Calendar:**
- `date2cal` - Calendar functionality
- `tx_cal_*` tables in database

**Forms:**
- `th_mailformplus` - Advanced form handling

**Backend/Admin:**
- `timtab` - Backend theme
- `realurl` - SEO-friendly URLs
- `static_info_tables` - Country/language data

### 6.2 Functionality to Replicate in 11ty

1. **Image Galleries**
   - Use 11ty image plugin
   - Create custom shortcodes for galleries
   - Implement lightbox (e.g., GLightbox, PhotoSwipe)

2. **News/Blog** (if needed)
   - Use 11ty collections
   - Create post templates
   - Implement pagination

3. **Contact Form**
   - Use third-party service (Formspree, Netlify Forms)
   - Or implement serverless function

4. **Search**
   - Client-side search (Lunr.js, Pagefind)
   - Or third-party service (Algolia)

5. **SEO-Friendly URLs**
   - Configure in 11ty
   - Create redirect map for old URLs

---

## 7. Migration Priorities

### 7.1 High Priority

1. ✅ **Static Pages** (Bio, Contact, Press, Links)
   - Simple text content
   - Easy to migrate
   - Foundation for site structure

2. ✅ **Main Image Galleries** (s-maj/, images/)
   - Core content of the site
   - 475 MB + 60 MB = 535 MB
   - Needs optimization

3. ✅ **Navigation Structure**
   - Define main menu
   - Create breadcrumbs
   - Set up routing

### 7.2 Medium Priority

4. **Portfolio Galleries** (s-pf/, s-mhk/, s-wt/)
   - Additional gallery content
   - ~38 MB total
   - Can be migrated after main galleries

5. **Downloads** (if needed)
   - 15 MB of files
   - Verify which are still relevant

6. **News/Blog** (if needed)
   - Only 4 items
   - May not be necessary

### 7.3 Low Priority

7. **Flash Content**
   - Deprecated technology
   - Decide: remove, replace, or convert

8. **Calendar** (if used)
   - Verify if actively used
   - May not be needed

---

## 8. Estimated Content Volume

### 8.1 Pages

- **Total Pages:** ~50-100 (estimated from database)
- **Main Sections:** 4 (Show, Sculptures, Painting, Recent Work)
- **Static Pages:** ~5-10 (Bio, Contact, Press, Links, etc.)
- **Gallery Pages:** ~40-90 (individual artwork pages)

### 8.2 Content Elements

- **Total Content Elements:** 24
- **Average per Page:** <1 (many pages may be image-only)

### 8.3 Media Files

- **Images:** 5,409 files (~700 MB)
- **Audio:** ~10 MP3 files
- **Documents:** Unknown (in downloads/)
- **Flash:** ~20 SWF files (to be removed/replaced)

---

## 9. Next Steps and Recommendations

### 9.1 Immediate Actions

1. **Database Access Decision**
   - Decide on method: Import to local MySQL, use SQL dump directly, or query-based extraction
   - **Recommendation:** Import to local MySQL for easier querying

2. **Content Audit**
   - Review live site thoroughly
   - Identify all page types and content patterns
   - Document special features or functionality

3. **Image Audit**
   - Identify which images are actually used
   - Remove duplicates and unused files
   - Plan optimization strategy

### 9.2 Migration Strategy Refinement

1. **URL Mapping**
   - Extract all page URLs from database
   - Create old-to-new URL mapping
   - Plan redirect strategy

2. **Content Extraction Scripts**
   - Develop Node.js scripts for database extraction
   - Create HTML-to-Markdown conversion pipeline
   - Build file organization automation

3. **Template Development**
   - Design 11ty layouts based on current site
   - Create gallery/portfolio templates
   - Implement responsive design

### 9.3 Questions for Decision

1. **News/Blog:** Keep or remove the 4 news items?
2. **Calendar:** Is calendar functionality needed?
3. **Flash Content:** Remove, replace with images, or convert?
4. **Search:** Implement client-side search or use service?
5. **Forms:** Which third-party form service to use?
6. **Hosting:** Where will the 11ty site be hosted? (affects redirect strategy)
7. **Image Galleries:** Preferred lightbox/gallery solution?
8. **URL Structure:** Preserve exact TYPO3 URLs or optimize?

---

## 10. Risk Assessment

### 10.1 Low Risk

- ✅ Small content volume (easy to migrate manually if needed)
- ✅ Simple site structure
- ✅ Standard TYPO3 tables (well-documented)

### 10.2 Medium Risk

- ⚠️ Character encoding conversion (German characters)
- ⚠️ Large number of images (time-consuming to process)
- ⚠️ RTE magic images (complex naming, need mapping)
- ⚠️ File reference resolution (DAM system)

### 10.3 High Risk

- ❌ Flash content (deprecated, needs replacement)
- ❌ Image optimization (700 MB needs significant reduction)
- ❌ Broken file references (if files are missing)

---

## 11. Conclusion

The maja-explosiv.com website is a **small, media-rich portfolio site** that is well-suited for migration to 11ty. The primary challenge is managing and optimizing the large volume of images (~5,400 files, 700 MB), while the content migration itself will be straightforward due to the small number of pages and content elements.

**Key Success Factors:**
1. Efficient image processing and optimization
2. Proper character encoding handling (German text)
3. Clean URL mapping and redirects
4. Replacement strategy for Flash content
5. Effective gallery/portfolio presentation in 11ty

**Estimated Migration Timeline:**
- **Phase 1 (Setup & Extraction):** 1-2 weeks
- **Phase 2 (Content Migration):** 1-2 weeks
- **Phase 3 (Media Processing):** 2-3 weeks
- **Phase 4 (Testing & Refinement):** 1-2 weeks
- **Total:** 5-9 weeks

---

## 12. Migration Scripts Created

The following scripts have been created to facilitate the migration:

### Database Setup
- **`scripts/01-setup-database.sh`** - Imports SQL dump to MySQL
  - Creates `maja_typo3` database
  - Converts to UTF-8 encoding
  - Displays import statistics

### Database Analysis
- **`scripts/02-analyze-database.sql`** - Comprehensive database analysis
  - Page structure and hierarchy
  - Content element breakdown
  - Media file inventory
  - Navigation tree visualization

### Data Extraction
- **`scripts/03-extract-pages.js`** - Node.js extraction script
  - Exports pages to JSON
  - Builds page tree structure
  - Maps content to pages
  - Extracts news and DAM references

### Documentation
- **`MIGRATION-README.md`** - Step-by-step migration guide
- **`migration.md`** - High-level migration strategy
- **`discovery-report.md`** - This document

---

## 13. Ready to Proceed

### Immediate Next Steps

1. **Import Database:**
   ```bash
   cd scripts
   ./01-setup-database.sh
   ```

2. **Install Script Dependencies:**
   ```bash
   cd scripts
   npm install
   ```

3. **Analyze Database:**
   ```bash
   npm run analyze-db > ../migration-data/database-analysis.txt
   ```

4. **Extract Data:**
   ```bash
   npm run extract-pages
   ```

5. **Review Extracted Data:**
   ```bash
   cat migration-data/extraction-summary.txt
   ```

### What Happens Next

After data extraction, we will:
1. Develop content transformation scripts (HTML → Markdown)
2. Create media migration and optimization scripts
3. Build 11ty templates based on current design
4. Implement URL mapping and redirects
5. Test and deploy

---

**End of Discovery Report**

