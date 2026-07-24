# TYPO3 Technical Findings & Implementation Details

**Date:** October 29, 2025  
**Project:** Maja Explosiv - TYPO3 to Eleventy Migration  
**Epic:** 1.3 Content Migration

---

## Database Structure Details

### SQL Dump Format (`old/usr_p51487_2.sql`)

**File Metadata:**
- **Database:** MySQL 5.0.96
- **PHP Version:** 5.6.40
- **Character Set:** `latin1_german1_ci` (Latin-1 German collation)
- **Created:** January 2, 2025
- **Size:** Large (contains 107 tables)

**INSERT Statement Format:**

The SQL dump uses a specific format that required careful parsing:

```sql
INSERT INTO `pages` (`uid`, `pid`, `t3ver_oid`, ...) VALUES
(3, 0, 0, ...),
(74, 0, 0, ...),
...
```

**Critical Parsing Details:**

1. **Field Name Format:**
   - Fields are wrapped in backticks: `` `uid`, `pid`, `title` ``
   - Separated by **comma + space**: `, ` (not just comma)
   - First field after opening parenthesis has no leading space
   - All subsequent fields have a leading space before the backtick

2. **Parsing Solution:**
   ```python
   # WRONG - only strips backticks, leaves leading spaces
   field_names = [f.strip('`') for f in raw_fields.split(',')]
   
   # CORRECT - strips whitespace THEN backticks
   field_names = [f.strip().strip('`') for f in raw_fields.split(',')]
   ```

3. **Multi-line INSERT Statements:**
   - The same table can have multiple INSERT statements throughout the file
   - Must use `re.DOTALL` flag to handle multi-line patterns
   - Must use `re.finditer()` to find all occurrences, not just the first

### Pages Table Structure

**Total Fields:** 71 fields

**Critical Fields for Migration:**
- `uid` - Unique page ID (primary key)
- `pid` - Parent ID (0 = root level)
- `title` - Page title
- `deleted` - Soft delete flag (0 = active, 1 = deleted)
- `hidden` - Visibility flag (0 = visible, 1 = hidden)
- `doktype` - Document type (1 = standard page, etc.)
- `sorting` - Sort order within parent

**Extracted Statistics:**
- Total pages in dump: 179 pages
- Active pages (not deleted): 94 pages
- Root level pages (pid=0): Multiple

### Content Elements Table (`tt_content`)

**Total Fields:** Not fully documented (to be added)

**Critical Fields:**
- `uid` - Unique content element ID
- `pid` - Parent page ID (references pages.uid)
- `CType` - Content type (text, textpic, header, etc.)
- `header` - Content header/title
- `bodytext` - Main content text (HTML format)
- `image` - Comma-separated list of image filenames
- `imagecaption` - Image captions (newline-separated)

**Extracted Statistics:**
- Total content elements: 443 elements

---

## Page Hierarchy & Categorization

### TYPO3 Site Structure

The old site uses a **hierarchical page tree** structure:

```
Root
├── sculptures (UID 870)
│   ├── sculptural work (UID 877)
│   │   ├── recent sculptures (UID 953)
│   │   └── [46 individual project pages]
│   └── collaborations (UID 878)
│       └── [8 individual project pages]
├── show (UID 868)
│   ├── performance (UID 872)
│   │   └── [6 individual project pages]
│   └── event organisation (UID 873)
│       └── [3 individual project pages]
└── painting (UID 869)
    ├── murals (UID 874)
    │   └── [3 individual project pages]
    └── paper work (UID 875)
        └── [5 individual project pages]
```

### Category Mapping Logic

**Old Structure → New Structure:**

| Old Category (UID) | Old Subcategory (UID) | New Category | Logic |
|-------------------|----------------------|--------------|-------|
| sculptures (870) | sculptural work (877) | sculptures OR installations | Keyword matching |
| sculptures (870) | collaborations (878) | sculptures OR installations | Keyword matching |
| show (868) | performance (872) | performance | Direct mapping |
| show (868) | event organisation (873) | performance | Direct mapping |
| painting (869) | murals (874) | paintings | Direct mapping |
| painting (869) | paper work (875) | paintings | Direct mapping |

**Installation Detection Keywords:**
```python
INSTALLATION_KEYWORDS = [
    'installation', 'gate', 'fence', 'bar', 'railing', 'door',
    'helix', 'channel', 'tubebox', 'weglampen', 'path illumination',
    'fountain', 'shower', 'wreck', 'suspended', 'kinetic'
]
```

**Categorization Algorithm:**
1. Find parent category page by UID
2. Find all descendant pages recursively (max depth: 5)
3. For each project page:
   - Extract content from `tt_content` table
   - If parent is "sculptural work" or "collaborations":
     - Check title and description for installation keywords
     - If found → installations
     - Else → sculptures
   - If parent is "performance" or "event organisation" → performance
   - If parent is "murals" or "paper work" → paintings

---

## Character Encoding Issues

### Problem

**Source Encoding:** `latin1_german1_ci` (Latin-1 German)  
**Target Encoding:** UTF-8

**Observed Issues:**

1. **German Umlauts:**
   - `Ã` appears instead of `ü` (u-umlaut)
   - `Ã` appears instead of `ä` (a-umlaut)
   - `Ã` appears instead of `ö` (o-umlaut)
   - `Ã` appears instead of `ß` (eszett/sharp s)

2. **Special Characters:**
   - `Ã¢â¬Ë` appears instead of `'` (smart quote)
   - Other Unicode characters may be corrupted

**Examples from Extracted Data:**
- "KÃÂ¤the" should be "Käthe"
- "ZÃÂ¼rich" should be "Zürich"
- "Lazy SuzanÃ¢â¬Ës" should be "Lazy Susan's"

### Root Cause

The SQL file is encoded in Latin-1, but when read with Python's default UTF-8 decoder, the multi-byte sequences are misinterpreted. The current code reads:

```python
with open('old/usr_p51487_2.sql', 'r', encoding='latin1') as f:
    content = f.read()
```

This correctly reads the Latin-1 file, but the **output** is written as UTF-8 without proper conversion, causing double-encoding issues.

### Solution Strategy (Proposed)

**Option 1: Fix During SQL Reading** ⭐ **RECOMMENDED**
- Read SQL file with `encoding='latin1'`
- Immediately decode to proper Unicode
- All subsequent processing uses correct UTF-8

**Option 2: Fix During Text Extraction**
- Read SQL as-is
- Apply encoding fixes in `clean_text()` function
- Convert when extracting from database fields

**Option 3: Fix During Markdown Generation**
- Extract data as-is
- Apply fixes when writing Markdown files
- Least preferred (too late in pipeline)

---

## Image Storage Patterns

### Database Storage

**Format:** Comma-separated filenames in `tt_content.image` field

Example:
```
"image1.jpg,image2.png,image3.gif"
```

**Image Captions:** Stored in `tt_content.imagecaption` field
- Newline-separated (one caption per image)
- May be empty

### Filesystem Storage

**Primary Location:** `old/TYPO3BU/_/fileadmin/s-maj/`
- Organized by project directory
- Directory names match year + project name pattern
- Example: `2024_Affenbande/`, `2008geier/`, `2013SisyphosGate/`

**Secondary Location:** `old/TYPO3BU/_/uploads/pics/`
- Flat directory structure
- Mixed content from various projects
- ~253 images

**Total Images:** ~1,440 images in fileadmin + ~253 in uploads = ~1,693 images

---

## Extraction Script Implementation

### Script: `scripts/extract_typo3_projects.py`

**Key Functions:**

1. **`extract_pages_data(sql_file)`**
   - Parses INSERT INTO pages statements
   - Handles multiple INSERT statements for same table
   - Returns list of page dictionaries

2. **`extract_content_elements(sql_file)`**
   - Parses INSERT INTO tt_content statements
   - Links content to pages via `pid` field
   - Returns dictionary: `{page_uid: [content_elements]}`

3. **`find_all_descendants(pages, parent_uid, max_depth=5)`**
   - Recursively finds all child pages
   - Prevents infinite loops with max_depth
   - Returns flat list of descendant pages

4. **`categorize_project(header, bodytext, parent_category)`**
   - Determines final category (sculptures/installations/performance/paintings)
   - Uses keyword matching for installation detection
   - Returns category string

5. **`clean_html(text)`**
   - Removes HTML tags
   - Fixes HTML entities
   - Normalizes whitespace
   - **NOTE:** Does NOT fix character encoding (to be added)

6. **`extract_year_from_text(header, bodytext)`**
   - Searches for 4-digit years in text
   - Validates year range (1990-2030)
   - Returns year string or None

### Conversion Script: `scripts/convert_test_projects.py`

**Key Functions:**

1. **`generate_slug(title)`**
   - Converts title to URL-friendly slug
   - Handles some special characters
   - **NOTE:** May need encoding fixes for proper slug generation

2. **`clean_text(text)`**
   - Removes HTML tags and entities
   - Normalizes line breaks
   - **NOTE:** Duplicate of extraction script function (should be unified)

3. **`create_markdown_file(project, category, output_dir)`**
   - Generates front matter (YAML)
   - Formats content as Markdown
   - Writes UTF-8 encoded file
   - Handles missing years (defaults to 2000-01-01)

---

## Extraction Results

### Statistics

**Total Projects Extracted:** 70 projects

**By Category:**
- Sculptures: 28 projects (40%)
- Installations: 26 projects (37%)
- Performance: 9 projects (13%)
- Paintings: 7 projects (10%)

**Projects with Years:** 54 projects (77%)  
**Projects without Years:** 16 projects (23%)

**Year Range:** 1995-2024 (29 years)

### Test Migration Selection

**Selection Criteria:**
- 5 most recent projects from each category
- Prioritize projects with years
- Fall back to projects without years if needed

**Total Test Projects:** 20 projects (29% of total)

---

## Build System Integration

### Layout Files

**Available Layouts:**
- `post.njk` - Used for project pages ✅
- `page.njk` - Used for static pages
- `home.njk` - Used for homepage
- `collection.njk` - Used for category listings
- `sidebar-layout.njk` - Custom user layout

**NOTE:** Initially tried to use `project.njk` but it doesn't exist. Changed to `post.njk`.

### Front Matter Format

```yaml
---
title: "Project Title"
date: YYYY-01-01
category: sculptures|installations|performance|paintings
tags:
  - category_name
  - year (if available)
layout: post.njk
---
```

### Build Success

**Command:** `npm run build`  
**Result:** ✅ Success  
**Output:** 54 HTML files generated  
**Time:** ~3.5 seconds

---

## Known Issues & Limitations

### 1. Character Encoding ⚠️ **HIGH PRIORITY**
- German umlauts corrupted (Ã instead of ü, ä, ö)
- Smart quotes corrupted
- Needs fixing during extraction phase

### 2. Missing Images
- Image filenames extracted but files not copied
- Need image extraction script
- Need path mapping (old → new structure)

### 3. Missing Years
- 16 projects have no year information
- Currently defaulting to 2000-01-01
- May need manual review

### 4. HTML Content
- Some content still contains HTML formatting
- Line breaks may need adjustment
- Video embed codes present (YouTube links)

### 5. Duplicate Code
- `clean_text()` function exists in both scripts
- Should be unified into shared utility module

---

## Next Steps

1. **Fix Character Encoding** ⭐ **CURRENT PRIORITY**
   - Implement proper Latin-1 → UTF-8 conversion
   - Apply during extraction phase
   - Test with German characters

2. **Image Extraction**
   - Create script to copy images from old site
   - Map old paths to new structure
   - Handle missing images gracefully

3. **Full Migration**
   - Convert remaining 50 projects
   - Review categorization accuracy
   - Validate all content

4. **Content Cleanup**
   - Remove remaining HTML tags
   - Fix line breaks and formatting
   - Handle video embeds

5. **Manual Review**
   - Check projects without years
   - Verify categorization (especially installations)
   - Review content accuracy

---

## Technical Lessons Learned

1. **SQL Parsing is Tricky**
   - Field names need careful whitespace handling
   - Multiple INSERT statements for same table
   - Must use proper regex flags (DOTALL)

2. **Character Encoding Matters**
   - Latin-1 vs UTF-8 causes corruption
   - Must handle at earliest point in pipeline
   - Python's default encoding can cause issues

3. **TYPO3 Structure**
   - Pages are hierarchical (tree structure)
   - Content elements linked to pages via pid
   - Soft deletes (deleted flag) must be filtered

4. **Eleventy Requirements**
   - Layouts must exist in _layouts directory
   - Front matter must have valid dates
   - UTF-8 encoding required for Markdown files

---

**Document Version:** 1.0  
**Last Updated:** October 29, 2025  
**Author:** Amelia (Developer Agent)

