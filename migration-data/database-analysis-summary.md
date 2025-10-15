# Database Analysis Summary
## TYPO3 Database - maja_typo3

**Analysis Date:** 2025-10-13  
**Database:** maja_typo3  
**Tables:** 107

---

## Executive Summary

The database analysis reveals a **significantly larger and more complex site** than initially estimated:

- **179 pages** (vs. initial estimate of 50-100)
- **443 content elements** (vs. initial estimate of 24)
- **148 news items** (vs. initial estimate of 4)
- **2,312 DAM file references** (vs. initial estimate of ~5,400 physical files)

The site contains **multiple sub-sites** under different domains:
- maja-explosiv.com (main site)
- pyrofessor.de (fire performance site)
- Additional sub-sites (mhk, km, wtweb)

---

## 1. Pages Analysis

### Total Pages: 179

### Pages by Type:
- **Standard pages:** 168 (94%)
- **Folders:** 5 (3%)
- **Shortcuts:** 3 (2%)
- **Other types:** 3 (1%)

### Top-Level Pages (Main Sections):
1. **templates ext** (uid: 965) - Template storage
2. **maja** (uid: 860) - Main maja-explosiv.com site
3. **pyrofessor** (uid: 733) - Fire performance site
4. **Media** (uid: 766) - Media storage

### Pages with Most Content:
1. **Skulpturen** (15 content elements)
2. **Feuershow für Kids** (14 content elements)
3. **Logo & Eddie** (13 content elements)
4. **Elxt 90** (13 content elements)
5. **Casino Gitano** (12 content elements)

---

## 2. Content Elements Analysis

### Total Content Elements: 443

### Content by Type:
- **text:** 241 (54%) - Text content
- **list:** 122 (28%) - Plugin/list elements
- **image:** 40 (9%) - Image elements
- **html:** 27 (6%) - Raw HTML
- **menu:** 4 (1%) - Menu elements
- **textpic:** 4 (1%) - Text with images
- **search:** 2 (<1%) - Search boxes
- **mailform:** 1 (<1%) - Contact form
- **login:** 1 (<1%) - Login form
- **multimedia:** 1 (<1%) - Multimedia element

### Content Statistics:
- **Content with images:** 10 elements
- **Hidden content:** 111 elements (25%)

---

## 3. News/Blog Analysis

### Total News Items: 148

### Recent News Items (Last 10):
1. **Grosse Hafenszene** (2024-07-01)
2. **Wandskulptur Hinwil** (2023-04-30)
3. **Die Affenbande** (2022-09-19)
4. **Schiffszimmer** (2022-06-13)
5. **Blumenwolke** (2021-08-03)
6. **Lauschen statt Rauschen** (2021-01-19)
7. **Flower Power** (2019-11-23)
8. **The Wolf** (2019-08-17)
9. **ADM Soli Party** (2019-04-23) - HIDDEN
10. **The Raven and the Crow** (2018-10-23)

### News Date Range:
- **Oldest:** 1992 (Matura Typus D)
- **Newest:** 2024 (Grosse Hafenszene)
- **Span:** 32 years of work!

### News Categories:
- Auftritt (Performance)
- Performance
- Event Organisation
- Murals
- Sculptures
- Collaborations
- Paper work
- Ausbildung (Education)
- Elxt 90 (Band/Project)
- news
- other
- Aktuell (Current)

**Note:** Many categories appear duplicated (likely from migration or multi-language setup)

---

## 4. Media Files (DAM) Analysis

### Total DAM Files: 2,312

### Files by Type:
- **JPG:** 2,116 files (550.79 MB) - 91.5%
- **GIF:** 75 files (0.17 MB)
- **SWF (Flash):** 17 files (4.18 MB) - **DEPRECATED**
- **CSS:** 16 files (0.03 MB)
- **HTML:** 16 files (0.05 MB)
- **JPEG:** 12 files (3.27 MB)
- **HTM:** 10 files (0.02 MB)
- **T3D (TYPO3 Data):** 10 files (24.84 MB)
- **JS:** 8 files (0.13 MB)
- **PDF:** 7 files (8.49 MB)
- **TMPL:** 7 files (0.01 MB)
- **PNG:** 5 files (0.52 MB)
- **AVI:** 2 files (4.54 MB)
- **MOV:** 2 files (1.99 MB)
- **XML:** 2 files (0.86 MB)
- **Other:** 12 files (0.32 MB)

### Total DAM Size: ~600 MB

### DAM Categories:
- **pyrofessor** - Fire performance site
- **mhk** - Sub-project
- **km** - Sub-project
- **wtweb** - Web project
- **maja** - Main site with subcategories:
  - murals
  - poster
  - 2D
  - concept illustration
  - current work
- **website** - General website files

---

## 5. System Information

### Domains Configured:

**Pyrofessor (Fire Performance Site):**
- pyrofessor.de → https://www.pyrofessor.de
- www.pyrofessor.de
- pyrofessor.wtweb.com

**Maja Explosiv (Main Site):**
- maja.wtweb.com → https://www.maja-explosiv.com
- maja-explosiv.com → https://www.maja-explosiv.com
- maja-explosiv.net → https://www.maja-explosiv.com
- www.maja-explosiv.com (primary)
- www.maja-explosiv.net → https://www.maja-explosiv.com

### Templates: 22 TypoScript templates

Key templates:
- **maja** (root template for main site)
- **pyrofessor** (root template for fire performance site)
- Various extension templates (galleries, menus, etc.)

---

## 6. File References

### Content Elements with Images: 10

Sample image references:
- vulkan-2.jpg
- carsten_bad_minol.jpg
- Vogelpaarfrei2.jpg
- kartePariskl.jpg
- tuttifruttimigi_01.jpg, ichbarna_02.jpg, ehofjoeb2_01.jpg
- webthanksxy.jpg
- compilation6.jpg
- Jahrmarkt_Feuershow_foto_wendlandt.jpg
- feuerkrone_manstein.JPG
- 2_Vulkane.jpg

---

## 7. Special Content

### SEO Metadata:
- **Pages with keywords:** 0
- **Pages with descriptions:** 0
- **Pages with media:** 0

**Note:** Lack of SEO metadata suggests this should be added during migration.

---

## 8. Key Findings

### 1. Multi-Site Setup
The database contains **at least 2 separate websites**:
- **maja-explosiv.com** - Main artist portfolio
- **pyrofessor.de** - Fire performance/show site

**Decision needed:** Migrate both sites or only maja-explosiv.com?

### 2. Extensive News Archive
148 news items spanning 32 years (1992-2024) represent a **comprehensive portfolio archive**.
This is the primary content of the site, not just a blog.

### 3. Character Encoding Issues
Several entries show encoding problems (e.g., "fÃ¼r" instead of "für"):
- Feuershow fÃ¼r Kids
- PolkappenzÃ¼ndfonie
- Felix und Regula UnterfÃ¼hrung

**Action required:** UTF-8 conversion during extraction.

### 4. Hidden Content
- **111 hidden content elements** (25% of total)
- Some news items are hidden (e.g., "ADM Soli Party", "birds couple")

**Decision needed:** Include hidden content in migration or exclude?

### 5. Flash Content
17 Flash files (4.18 MB) need replacement or removal.

### 6. Duplicate News Entries
Many news items appear to be duplicated (same title, same date, different UIDs).
This may be due to:
- Multi-language setup
- Migration artifacts
- Category relationships

**Action required:** Deduplicate during extraction.

---

## 9. Migration Implications

### Content Volume Revision:
- **Original estimate:** Small site (~50 pages, 24 content elements)
- **Actual size:** Medium site (179 pages, 443 content elements, 148 news items)
- **Complexity:** Higher (multi-site, extensive archive)

### Timeline Impact:
- Original estimate: 5-9 weeks
- **Revised estimate:** 7-12 weeks (due to increased volume and complexity)

### Priority Decisions Needed:

1. **Which site(s) to migrate?**
   - Only maja-explosiv.com?
   - Both maja-explosiv.com and pyrofessor.de?
   - Merge both into one site?

2. **News/Portfolio handling:**
   - Migrate all 148 items?
   - Filter by date (e.g., only last 10 years)?
   - Deduplicate entries?

3. **Hidden content:**
   - Include or exclude?
   - Review individually?

4. **Multi-language:**
   - Is this a multi-language site?
   - If yes, which languages to migrate?

---

## 10. Next Steps

### Before Data Extraction:

1. **Review this analysis** and make decisions on:
   - Which site(s) to migrate
   - How to handle news duplicates
   - Whether to include hidden content
   - Date range for news items

2. **Verify character encoding** in sample content

3. **Identify primary vs. secondary content**

### After Decisions:

4. **Run data extraction** with filters based on decisions
5. **Review extracted JSON** for quality
6. **Develop transformation scripts** based on actual content structure

---

## 11. Questions for Decision

1. Should we migrate both maja-explosiv.com AND pyrofessor.de, or only maja-explosiv.com?
2. Should we migrate all 148 news items, or filter by date/relevance?
3. How should we handle duplicate news entries?
4. Should hidden content be included in the migration?
5. Is this a multi-language site? (German/English?)
6. Should we add SEO metadata during migration (currently missing)?
7. What to do with Flash content - remove or replace?

---

**End of Database Analysis Summary**

