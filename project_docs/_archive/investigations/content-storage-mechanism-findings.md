# TYPO3 Content Storage Mechanism - Investigation Findings

**Date:** 2025-12-28  
**Investigation Focus:** Why page 982 "Breath under Water" was not migrated

## Executive Summary

Page 982 "Breath under Water" is the **ONLY** painting project page that lacks standard tt_content records. All other painting projects use the **RG Smooth Gallery** TYPO3 extension (`rgsmoothgallery_pi1`) to display image galleries.

## Key Findings

### 1. Page 982 is Unique

- **UID:** 982
- **Title:** "Breath under Water" (originally "The Whale")
- **Parent PID:** 875 (paper work category)
- **URL:** `/content/recent-work/the-whale.html`
- **tt_content Records:** **ZERO** ❌
- **Images on Filesystem:** 73 files in `fileadmin/s-maj/images/BilderMaja/2005TheWhale/`

### 2. Standard Pattern for Other Painting Pages

All other painting pages have **2 tt_content records each**:

| UID | Title | PID | Content Type | Records |
|-----|-------|-----|--------------|---------|
| 919 | Wohlgroth | 874 (murals) | `rgsmoothgallery_pi1` | 2 ✓ |
| 918 | Felix und Regula | 874 (murals) | `rgsmoothgallery_pi1` | 2 ✓ |
| 866 | Murals Europe | 874 (murals) | `rgsmoothgallery_pi1` | 2 ✓ |
| 920 | Poster/Graphics | 875 (paper work) | `rgsmoothgallery_pi1` | 2 ✓ |
| 921 | Akwa | 875 (paper work) | `rgsmoothgallery_pi1` | 2 ✓ |
| 922 | Malaga la Vache | 875 (paper work) | `rgsmoothgallery_pi1` | 2 ✓ |
| 923 | Concept Illustration | 875 (paper work) | `text` + `rgsmoothgallery_pi1` | 2 ✓ |
| **982** | **Breath under Water** | **875 (paper work)** | **NONE** | **0 ❌** |

### 3. RG Smooth Gallery Extension

The standard content element structure:
```
CType: 'list'
list_type: 'rgsmoothgallery_pi1'
header: [Project Title]
pi_flexform: [XML configuration for gallery settings]
```

### 4. Page History (from sys_log)

1. **2009-03-17 (UID 13437):** Created as "The Whale (Kopie 1)" under "recent work" (PID 867)
2. **2009-03-17 (UID 13444):** Updated
3. **2009-04-03 (UID 15242):** Renamed to "The Whale"
4. **2015-05-08 (UID 25678-25687):** Renamed to "Breath under Water"
5. **2019-11-23 (UID 28894-28895):** **MOVED** from "recent work" (867) to "paper work" (875)

### 5. URL Routing Anomaly

- **RealURL cache entry (UID 1125):** Maps page 982 to `/content/recent-work/the-whale`
- **Actual page location:** Under PID 875 (paper work), should be `/content/2d/paper-work/`
- **Conclusion:** URL path reflects original location before 2019 move; RealURL cache not updated

### 6. Content Storage Investigation

**Checked:**
- ✓ `tt_content` table: NO records
- ✓ `tx_dam` table: 22 whale-related records exist (general media, not page-specific)
- ✓ `tx_dam_mm_ref`: No direct links to page 982
- ✓ `cache_pages`: Cache existed but appears expired/cleared
- ✓ Filesystem: 73 images in `2005TheWhale/` directory

**Not using:**
- TemplaVoilà (tx_templavoila)
- DAM tt_content integration (tx_damttcontent)
- RG Slideshow (tx_rgslideshow)
- Standard image content elements

## Other Sections Analysis

### Sculpture Pages

**"Recent Sculptures" (PID 953):** Also uses `rgsmoothgallery_pi1` for individual projects:
- Pattern matches painting pages
- Each project has gallery plugin content

### Show Section

**Performance (PID 872):**
- 5 child pages WITH tt_content
- Uses `rgsmoothgallery_pi1` for projects

**Event Organisation (PID 873):**
- 3 child pages WITH tt_content
- Uses `rgsmoothgallery_pi1` for events

## Category Pages Have No Content

**Important Pattern:** All category/folder pages (murals, paper work, sculptures, etc.) have NO tt_content:
- PID 874 (Murals category): NO content
- PID 875 (Paper Work category): NO content  
- PID 877 (Sculptural Work category): NO content
- PID 953 (Recent Sculptures category): NO content

These are navigation containers only.

## Hypotheses for Page 982's Missing Content

### Theory 1: Incomplete Migration During Site Restructure
- Page was created under "recent work" 
- Moved to "paper work" in 2019
- Gallery content may have been lost during move
- URL cache retained old path

### Theory 2: Content Never Created
- Page was created as placeholder
- Images uploaded to filesystem
- Gallery plugin never configured
- Project remained "in progress"

### Theory 3: Alternative Rendering Method
- Content rendered via TypoScript only
- Images displayed directly from filesystem path
- No plugin configuration needed
- Would require checking TypoScript templates

### Theory 4: Manual Template Override
- Custom HTML template for this specific project
- Bypasses normal tt_content rendering
- Images hard-coded in template
- Would be in `fileadmin/s-maj/tpl/` directory

## Recommendations for Migration

### 1. Manual Content Creation Required
Since page 982 has no extractable content records:
- **Option A:** Create gallery from filesystem images
- **Option B:** Fetch content from live site via web scraping
- **Option C:** Mark as incomplete and gather requirements from client

### 2. Check Other "Missing" Projects
The original investigation found 17 painting pages in database but only 8 visible on live site:

**Visible on live site (8):**
- 3 Murals: Wohlgroth, Felix und Regula, Murals Europe
- 5 Paper Work: Concept Illustration, Graphical Work, Breath Under Water, Akwa, Malaga la Vache

**In database but not visible (9):**
- Need to check if these are drafts, hidden, or deleted

### 3. Verify TypoScript Configuration
Check if there's a TypoScript setup that renders images for page 982:
- Look in `typo3conf/` for setup.txt/constants.txt
- Check `fileadmin/s-maj/tpl/` for custom templates
- Examine sys_template record (UID 2 on page 3)

### 4. RG Smooth Gallery Data Structure
For migrating other projects, understand the gallery configuration:
- FlexForm XML contains gallery settings
- Images likely referenced via DAM or file references
- May need to extract image lists from plugin configuration

## Migration Impact

**Projects Successfully Extracted:** 70 (per existing extraction script)  
**Projects Needing Manual Migration:** At least 1 (page 982)  
**Projects Needing Review:** 9 (painting pages in database but not on live site)

## Next Steps

1. **Examine TypoScript** - Check `old/TYPO3BU/_/typo3conf/` for template configuration
2. **Parse RG Smooth Gallery FlexForms** - Extract image references from existing projects
3. **Verify Live Site** - Confirm which of the 17 database pages are actually published
4. **Create Migration Strategy** - For pages without tt_content records
5. **Client Consultation** - Determine if "Breath under Water" project should be included

## Files Examined

- `old/usr_p51487_2.sql` - TYPO3 database dump
- `old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja/2005TheWhale/` - 73 project images
- `old/TYPO3BU/_/typo3conf/` - TYPO3 configuration
- `scripts/extract_typo3_projects.py` - Original extraction script

## Tools/Extensions Identified

- **RealURL** - URL routing (tx_realurl_*)
- **RG Smooth Gallery** - Image gallery plugin (rgsmoothgallery_pi1)
- **DAM** - Digital Asset Management (tx_dam)
- **TYPO3 v4.2.0** - Core CMS version
