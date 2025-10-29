# TYPO3 Database Analysis

**Database File:** `old/usr_p51487_2.sql`  
**Database Name:** `usr_p51487_2`  
**TYPO3 Version:** 4.2.14  
**Total Tables:** 107  
**Analysis Date:** 2025-10-29

---

## Executive Summary

The TYPO3 database contains 107 tables. For content migration to Eleventy, we need to focus on **3 primary tables**:

1. **`pages`** - Page structure and hierarchy
2. **`tt_content`** - Page content elements (text, images, etc.)
3. **`tt_news`** - News/blog entries

---

## Critical Tables for Migration

### 1. `pages` Table

**Purpose:** Stores the page tree structure and page metadata.

**Key Columns:**
- `uid` - Unique page ID
- `pid` - Parent page ID (for hierarchy)
- `title` - Page title
- `doktype` - Document type (1=standard page, 4=shortcut, etc.)
- `hidden` - Visibility flag (0=visible, 1=hidden)
- `deleted` - Deletion flag (0=active, 1=deleted)
- `crdate` - Creation date (Unix timestamp)
- `tstamp` - Last modified timestamp
- `sorting` - Sort order
- `subtitle` - Page subtitle
- `description` - Page description/meta description
- `keywords` - Page keywords
- `media` - Associated media files

**Migration Strategy:**
- Extract pages where `deleted=0` and `hidden=0`
- Build page hierarchy using `pid` relationships
- Map to Eleventy static pages in `src/pages/`
- Convert timestamps to ISO dates

---

### 2. `tt_content` Table

**Purpose:** Stores content elements that appear on pages (the actual content).

**Key Columns:**
- `uid` - Unique content element ID
- `pid` - Page ID this content belongs to
- `CType` - Content type ('text', 'textpic', 'image', 'list', etc.)
- `header` - Content header/title
- `subheader` - Subheader
- `bodytext` - Main text content (HTML/rich text)
- `image` - Comma-separated list of image filenames
- `imagecaption` - Image captions (one per image, newline-separated)
- `altText` - Alt text for images
- `titleText` - Title text for images
- `imageorient` - Image orientation/position
- `sorting` - Sort order on page
- `colPos` - Column position
- `hidden` - Visibility flag
- `deleted` - Deletion flag
- `crdate` - Creation date
- `tstamp` - Last modified timestamp
- `sys_language_uid` - Language ID (0=default)

**Content Types (CType):**
- `text` - Plain text
- `textpic` - Text with images
- `image` - Images only
- `list` - Plugin/list (e.g., news list)
- `html` - Raw HTML

**Migration Strategy:**
- Extract content where `deleted=0` and `pid` matches valid pages
- Group by `pid` to assemble full page content
- Parse `bodytext` HTML and convert to Markdown
- Extract image references and map to new asset structure
- Handle multiple content elements per page (combine by `sorting`)

---

### 3. `tt_news` Table

**Purpose:** Stores news/blog entries (from tt_news extension).

**Key Columns:**
- `uid` - Unique news ID
- `pid` - Storage folder ID
- `title` - News title
- `datetime` - Publication date (Unix timestamp)
- `short` - Short description/teaser
- `bodytext` - Full news text (HTML)
- `image` - Comma-separated list of image filenames
- `imagecaption` - Image captions
- `imagealttext` - Alt text for images
- `imagetitletext` - Title text for images
- `author` - Author name
- `author_email` - Author email
- `category` - Category ID (links to `tt_news_cat`)
- `keywords` - Keywords
- `hidden` - Visibility flag
- `deleted` - Deletion flag
- `crdate` - Creation date
- `tstamp` - Last modified timestamp

**Migration Strategy:**
- Extract news where `deleted=0` and `hidden=0`
- Convert to Markdown files in `src/posts/news/`
- Map categories to collections
- Convert timestamps to ISO dates
- Extract and map image references

---

## Supporting Tables

### 4. `tt_news_cat` Table

**Purpose:** News categories.

**Key Columns:**
- `uid` - Category ID
- `title` - Category name
- `description` - Category description

**Migration Use:** Map news categories to Eleventy collections.

---

### 5. `tt_news_cat_mm` Table

**Purpose:** Many-to-many relationship between news and categories.

**Key Columns:**
- `uid_local` - News UID
- `uid_foreign` - Category UID

**Migration Use:** Determine which categories each news item belongs to.

---

## Image Reference Format

**In Database:**
- Images stored as comma-separated filenames: `image1.jpg,image2.jpg,image3.jpg`
- Captions stored as newline-separated text (one per image)
- Images physically located in `uploads/pics/` or `uploads/tx_ttnews/` directories

**Example:**
```
image: "sculpture01.jpg,sculpture02.jpg,sculpture03.jpg"
imagecaption: "Front view\nSide view\nDetail"
```

---

## Character Encoding

**Current Encoding:** `latin1_german1_ci` (Latin-1 German collation)  
**Target Encoding:** UTF-8

**Migration Requirement:**
- Convert all text content from Latin-1 to UTF-8
- Handle special characters (ä, ö, ü, ß, etc.)
- Test conversion with sample data first

---

## Data Extraction Queries

### Extract All Active Pages

```sql
SELECT uid, pid, title, subtitle, description, keywords, crdate, tstamp, sorting, doktype
FROM pages
WHERE deleted = 0 AND hidden = 0
ORDER BY sorting;
```

### Extract Content for a Specific Page

```sql
SELECT uid, CType, header, subheader, bodytext, image, imagecaption, altText, sorting
FROM tt_content
WHERE pid = [PAGE_ID] AND deleted = 0
ORDER BY sorting;
```

### Extract All Active News

```sql
SELECT uid, title, datetime, short, bodytext, image, imagecaption, author, category, crdate
FROM tt_news
WHERE deleted = 0 AND hidden = 0
ORDER BY datetime DESC;
```

### Extract News Categories

```sql
SELECT c.uid, c.title, c.description
FROM tt_news_cat c
WHERE c.deleted = 0;
```

### Extract News-Category Relationships

```sql
SELECT uid_local AS news_uid, uid_foreign AS category_uid
FROM tt_news_cat_mm;
```

---

## Tables NOT Needed for Migration

The following tables are TYPO3 system tables and NOT needed for content migration:

- `be_*` - Backend user/session tables
- `cache_*` - Cache tables
- `fe_sessions`, `fe_session_data` - Frontend session tables
- `sys_*` - System tables (logs, history, etc.)
- `tx_cal_*` - Calendar extension tables
- `tx_dam_*` - Digital Asset Management tables
- `tx_realurl_*` - URL rewriting cache tables
- `static_*` - Static reference data

---

## Migration Mapping

### TYPO3 → Eleventy Mapping

| TYPO3 Table | TYPO3 Field | Eleventy Location | Eleventy Field |
|-------------|-------------|-------------------|----------------|
| `pages` | `title` | Front matter | `title` |
| `pages` | `description` | Front matter | `description` |
| `pages` | `crdate` | Front matter | `date` |
| `tt_content` | `bodytext` | Markdown body | (converted to Markdown) |
| `tt_content` | `image` | Front matter | `images[].src` |
| `tt_content` | `imagecaption` | Front matter | `images[].caption` |
| `tt_news` | `title` | Front matter | `title` |
| `tt_news` | `datetime` | Front matter | `date` |
| `tt_news` | `bodytext` | Markdown body | (converted to Markdown) |
| `tt_news` | `category` | Front matter | `postCollections` |

---

## Next Steps

1. ✅ **Database analysis complete** (this document)
2. ⏳ **Filesystem analysis** (see `typo3-filesystem-analysis.md`)
3. ⏳ **Test extraction script** (5 posts per category)
4. ⏳ **Validate conversion quality**
5. ⏳ **Full migration**

---

## Notes

- Database dump created: January 2, 2025
- MySQL version: 5.0.96
- PHP version: 5.6.40
- All timestamps are Unix timestamps (seconds since 1970-01-01)
- HTML content in `bodytext` fields needs conversion to Markdown
- Image paths need to be mapped from TYPO3 structure to new asset organization

---

**Status:** ✅ Analysis Complete  
**Ready for:** Filesystem Analysis

