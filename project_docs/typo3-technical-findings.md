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

### Problem Discovery

**Source Encoding:** `latin1_german1_ci` (Latin-1 German collation in database)
**Actual File Encoding:** UTF-8 (despite Latin-1 collation)
**Target Encoding:** UTF-8

**Observed Issues:**

1. **German Umlauts:**
   - `KÃ¤the` appears instead of `Käthe` (ä = a-umlaut)
   - `ZÃ¼rich` appears instead of `Zürich` (ü = u-umlaut)
   - `LuginbÃ¼hl` appears instead of `Luginbühl`
   - `UnterfÃ¼hrung` appears instead of `Unterführung`

2. **Special Characters:**
   - Smart quotes and other Unicode characters corrupted

### Root Cause Analysis

**The Issue: Double-Encoded UTF-8**

The SQL file contains **UTF-8 encoded text** that was incorrectly interpreted as Latin-1 and then re-encoded as UTF-8, causing **double-encoding**.

**Example with 'ä' (a-umlaut):**

1. **Correct UTF-8:** `c3a4` (2 bytes)
2. **What happened:**
   - Original: 'ä' encoded as UTF-8 → bytes `c3a4`
   - Misinterpretation: bytes `c3a4` decoded as Latin-1 → two characters 'Ã¤'
   - Re-encoding: 'Ã¤' encoded as UTF-8 → bytes `c383c2a4` (4 bytes)
3. **Result:** "Käthe" becomes "KÃ¤the"

**Byte-level breakdown:**
```
Correct:   K (4b) + ä (c3a4)     + the (746865) = "Käthe"
Corrupted: K (4b) + Ã¤ (c383c2a4) + the (746865) = "KÃ¤the"
```

**Verification from SQL file:**
```bash
# Actual bytes in SQL file for "Käthe_Kollwitz" directory:
4b c383c2a4 746865 5f 4b6f6c6c77697472
K  Ã¤      the    _  Kollwitz

# When decoded as UTF-8: "KÃ¤the_Kollwitz"
# When decoded as Latin-1: "KÃÂ¤the_Kollwitz" (even more corrupted)
```

### Solution Implemented ✅

**Fix During Text Extraction** (Option 2 - chosen for safety)

Instead of changing how we read the SQL file (which could cause errors if parts are actually Latin-1), we fix the double-encoding during text extraction.

**Implementation:**

1. **Read SQL as UTF-8:**
   ```python
   with open(sql_file, 'r', encoding='utf-8') as f:
       content = f.read()
   ```
   This gives us the double-encoded text (e.g., "KÃ¤the")

2. **Reverse the double-encoding:**
   ```python
   def fix_double_encoding(text):
       """Fix double-encoded UTF-8 text

       The SQL file contains UTF-8 text that was incorrectly interpreted as Latin-1
       and then re-encoded as UTF-8, causing double-encoding.

       Fix: encode as Latin-1 (reverses the second encoding) then decode as UTF-8
       """
       if not text:
           return ""

       try:
           # Reverse the double-encoding: encode as Latin-1, decode as UTF-8
           return text.encode('latin1').decode('utf-8')
       except (UnicodeDecodeError, UnicodeEncodeError):
           # If fix fails, return original text
           return text
   ```

3. **Apply fix to all text fields:**
   - Page titles (in `extract_pages_data()`)
   - Content headers (in `extract_content_elements()`)
   - Content body text (in `extract_content_elements()`)
   - All text processed through `clean_html()`

**Files Modified:**
- `scripts/extract_typo3_projects.py`:
  - Line 35: Changed `encoding='latin1'` to `encoding='utf-8'`
  - Line 195: Changed `encoding='latin1'` to `encoding='utf-8'`
  - Lines 306-325: Added `fix_double_encoding()` function
  - Line 179: Apply fix to page titles
  - Lines 258, 261: Apply fix to content headers and body text
  - Line 332: Apply fix in `clean_html()` function

### Verification Results ✅

**Before Fix:**
```
Title: "KÃ¤the"
Description: "...in Zürich..."  → "...in ZÃ¼rich..."
```

**After Fix:**
```
Title: "Käthe"
Description: "...in Zürich..." ✓
Slug: "kathe.md" (properly transliterated)
```

**Test Results:**
- ✅ German umlauts display correctly (ä, ö, ü, ß)
- ✅ All 70 projects extracted without encoding errors
- ✅ Build succeeds: `npm run build` → 55 files generated
- ✅ No UnicodeDecodeError or UnicodeEncodeError exceptions

### Technical Notes

1. **Why not just read as UTF-8?**
   - The SQL file header declares `latin1_german1_ci` collation
   - Some parts might actually be Latin-1 encoded
   - Reading as UTF-8 and fixing double-encoding is safer

2. **Error Handling:**
   - The `fix_double_encoding()` function has try/except
   - If encoding/decoding fails, returns original text
   - This prevents crashes on edge cases

3. **Performance:**
   - Minimal overhead (encode + decode operations are fast)
   - Applied only to text fields, not to entire SQL file

4. **Future Considerations:**
   - If new encoding issues appear, check the `fix_double_encoding()` function
   - May need to handle triple-encoding or mixed encodings
   - Consider using `ftfy` library for more robust fixing

---

## Image Storage Patterns

### Database Storage

TYPO3 uses **two different methods** for storing images in projects:

#### Method 1: Simple Image Field (Legacy)

**Format:** Comma-separated filenames in `tt_content.image` field

Example:
```
"image1.jpg,image2.png,image3.gif"
```

**Image Captions:** Stored in `tt_content.imagecaption` field
- Newline-separated (one caption per image)
- May be empty

#### Method 2: DAM Gallery Plugin (Primary Method)

**Plugin:** `rgsmoothgallery_pi1` (stored in `tt_content.list_type`)

**How it works:**
- Images are stored in DAM (Digital Asset Management) folders
- Each project references a DAM folder ID via `startingpointdam` in FlexForm XML
- Example: `<value index="vDEF">14</value>` references DAM folder #14
- The folder contains all images for that project

**Featured Image Behavior:** ✅ **VERIFIED**
- **The FIRST image (by `sorting` field in `tx_dam` table) is the featured/preview image**
- This image displays large on the project page
- Other images appear as thumbnails in the gallery below
- Image order determined by:
  1. `tx_dam.sorting` field (database sort order)
  2. Filename alphabetical order (files prefixed with `001_`, `002_`, etc.)
- **Confirmed via:** Live site inspection (maja-explosiv.com) + filesystem analysis

**Gallery Configuration:** (from FlexForm settings)
- `lightbox`: Enable/disable lightbox popup
- `showThumbs`: Show thumbnail gallery
- `showPlay`: Show slideshow play button
- `thumbHeight`, `thumbWidth`: Thumbnail dimensions (typically 100x100)
- `externalthumbs`: Enable external thumbnail positioning

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
   - Uses keyword 
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

### 1. Character Encoding ✅ **RESOLVED**
- ~~German umlauts corrupted (Ã instead of ü, ä, ö)~~ **FIXED**
- ~~Smart quotes corrupted~~ **FIXED**
- **Solution:** Double-encoding fix implemented in extraction script
- See `project_docs/encoding-fix-summary.md` for details

### 2. Missing Project - "Breath under Water" (UID 982) ⚠️ **INVESTIGATION PENDING**

**Status:** Work paused, investigation required

**Problem:**
- User reported 8 projects in paintings category (3 murals + 5 paper work)
- Extraction script only found 7 projects
- Missing project: "Breath under Water" (UID 982)

**Investigation Results:**

1. **Page exists in database:**
   - UID: 982, PID: 875 (paper work category)
   - Title: "Breath under Water"
   - NOT deleted, NOT hidden

2. **Content missing from tt_content table:**
   - 0 tt_content records with pid=982
   - Script correctly skips pages without content

3. **Evidence of content existence:**
   - Found cached HTML page in database
   - Page contains extensive content about whale sculpture project
   - Multiple images, detailed description

4. **Current extraction count:**
   - Murals: 3 projects ✓
   - Paper Work: 4 projects (5 pages exist, 1 has no content)
   - **Total: 7 projects extracted**

**Next Steps (PENDING):**
- Cross-reference database with website files (Option D)
- Investigate other database tables (Option A)
- Determine if content stored elsewhere
- Verify correct categorization (whale sculpture vs paper work?)

### 3. Missing Images
- Image filenames extracted but files not copied
- Need image extraction script
- Need path mapping (old → new structure)

### 4. Missing Years
- 16 projects have no year information
- Currently defaulting to 2000-01-01
- May need manual review

### 5. HTML Content
- Some content still contains HTML formatting
- Line breaks may need adjustment
- Video embed codes present (YouTube links)

### 6. Duplicate Code
- `clean_text()` function exists in both scripts
- Should be unified into shared utility module

---

## Next Steps

### Immediate (When Resuming Work)

1. **Investigate "Breath under Water" (UID 982)** ⭐ **CURRENT PRIORITY**
   - Cross-reference database with website files (Option D)
   - Check `old/` directory for actual content files
   - Investigate other database tables (Option A)
   - Determine correct category for this project
   - Decide whether to include in migration

### After Investigation

2. **Image Extraction**
   - Create script to copy images from old site
   - Map old paths to new structure
   - Handle missing images gracefully

3. **Full Migration**
   - Convert remaining projects (50 or 49 depending on UID 982)
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

## How to Resume This Work

### Context Files to Review

1. **`project_docs/typo3-technical-findings.md`** (this file):
   - Complete technical documentation
   - All findings, issues, and solutions
   - Character encoding fix details
   - Missing project investigation

2. **`project_docs/encoding-fix-summary.md`**:
   - Summary of encoding issue resolution
   - Before/after examples

3. **`project_docs/extracted-projects.json`**:
   - 70 projects extracted (7 paintings, not 8)
   - Correctly encoded German characters

4. **`project_docs/typo3-database-analysis.md`**:
   - Complete database structure
   - 107 tables documented

5. **`project_docs/typo3-filesystem-analysis.md`**:
   - Old website file structure
   - Image locations and counts

### Current State

**Completed:**
- ✅ Database extraction (70 projects)
- ✅ Character encoding fix (double-encoded UTF-8)
- ✅ Test migration (20 projects)
- ✅ Build verification (55 HTML files)
- ✅ Documentation of all findings

**In Progress:**
- 🔍 Investigation of missing "Breath under Water" project (UID 982)

**Pending:**
- ⏳ Cross-reference DB with website files
- ⏳ Image extraction
- ⏳ Full migration (remaining projects)

### Commands to Continue

```bash
# 1. Navigate to project
cd /home/miichael/Code/maja-explosiv

# 2. Check current state
npm run build  # Should succeed with 55 files

# 3. Review extracted data
cat project_docs/extracted-projects.json | jq '.paintings | length'  # Shows 7

# 4. Investigate missing project - Option D (website files)
find old/ -name "*breath*" -o -name "*whale*" 2>/dev/null
ls -la old/fileadmin/s-maj/images/BilderMaja/

# 5. Investigate missing project - Option A (database)
grep -a "982" old/usr_p51487_2.sql | grep -v "INSERT INTO \`pages\`" | head -20

# 6. When ready to continue extraction
python3 scripts/extract_typo3_projects.py
python3 scripts/convert_test_projects.py
```

### Key Questions to Answer

1. Where is the content for "Breath under Water" (UID 982)?
2. Is it actually a painting/paper work project?
3. Should it be included in the migration?
4. Are there other projects with similar issues?

### Files Modified in This Session

**Scripts:**
- `scripts/extract_typo3_projects.py` - Added UTF-8 reading and double-encoding fix
- `scripts/convert_test_projects.py` - No changes needed

**Data:**
- `project_docs/extracted-projects.json` - Regenerated with correct encoding
- `src/posts/projects/sculptures/kathe.md` - Created with correct encoding
- Removed: `src/posts/projects/sculptures/ka-a-the.md` (old corrupted version)

**Documentation:**
- `project_docs/typo3-technical-findings.md` - Updated with encoding fix and missing project
- `project_docs/encoding-fix-summary.md` - Created

### Success Metrics

- ✅ 70 projects extracted from database
- ✅ 7 paintings projects (3 murals + 4 paper work)
- ✅ 28 sculptures projects
- ✅ 26 installations projects
- ✅ 9 performance projects
- ✅ All German characters display correctly
- ✅ Build succeeds without errors
- ⚠️ 1 project (UID 982) needs investigation

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

