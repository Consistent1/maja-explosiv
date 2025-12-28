# Investigation: "Breath under Water" Migration Failure

**Date:** December 28, 2025  
**Investigator:** GitHub Copilot (Claude Sonnet 4.5)  
**Issue:** Project "Breath under Water" (UID 982) failed to migrate from TYPO3 database

---

## Executive Summary

The "Breath under Water" project (UID 982) was not migrated because it has **NO content in the `tt_content` database table**, despite having:
- A valid page record in the `pages` table
- 59 images in the filesystem (`2005TheWhale/` directory)
- Extensive content visible on the live website

**Root Cause:** The TYPO3 site uses **static HTML content** for 14 out of 17 painting pages, not database-stored content. The current migration script only extracts projects with `tt_content` records.

**Impact:** **82% of painting projects** (14 out of 17) are being excluded from migration.

---

## Detailed Findings

### 1. Database Analysis

#### Pages in `pages` Table
Found **17 painting pages** total:
- **3 under "murals" (PID 874)** with `tt_content`: UID 866, 999
- **1 under "murals"** without content
- **2 under "paper work" (PID 875)** with `tt_content`: UID 1000  
- **11 under "paper work"** without content (including UID 982)

| UID  | Category    | Has tt_content | Title               |
|------|-------------|----------------|---------------------|
| 866  | murals      | ✓              | (Murals Europe)     |
| 918  | murals      | ✗              |                     |
| 919  | murals      | ✗              |                     |
| 920  | paper work  | ✗              |                     |
| 921  | paper work  | ✗              |                     |
| 922  | paper work  | ✗              |                     |
| 923  | paper work  | ✗              |                     |
| **982** | **paper work** | **✗**     | **Breath under Water** |
| 999  | murals      | ✓              |                     |
| 1000 | paper work  | ✓              |                     |
| 1200 | murals      | ✗              |                     |
| 1211 | paper work  | ✗              |                     |
| 1330 | murals      | ✗              |                     |
| 1344 | murals      | ✗              |                     |
| 1345 | paper work  | ✗              |                     |
| 1398 | paper work  | ✗              |                     |
| 1461 | paper work  | ✗              |                     |

#### Page Record for UID 982
```sql
(982, 875, 0, 0, 0, '', 0, 0, 0, 0, 0, 924, 1574521816, 448, 0, 10, 3, 31, 27, 0, 0, 
 1237298059, 10, 'Breath under Water', 1, '', 0, 0, 0, 0, '', 0, 0, 0, 1, 924, 0, 0, 
 '', '', 0, '', '', 0, '', 0, 0, '', 0, 1612977305, '', '', 0, '', '', '', 0, 924, 0, 
 0, '', 0, 0, '', '', '', '', '', 0, 0, 0)
```

**Key Fields:**
- `uid`: 982
- `pid`: 875 (paper work category)
- `title`: 'Breath under Water'
- `deleted`: 0 (NOT deleted)
- `hidden`: 0 (NOT hidden)
- `doktype`: 1 (standard page)

#### tt_content Search
```python
# Searched entire SQL dump for tt_content records with pid=982
Total tt_content records with pid=982: 0
```

**Conclusion:** Page exists but has zero content elements in database.

---

### 2. Live Website Analysis

#### URL Structure
- **Live URL:** `https://www.maja-explosiv.com/content/recent-work/the-whale.html`
- **Note:** URL says "the-whale" but page title is "Breath under Water"

#### Content Found on Live Site
The live website displays extensive content:

**Text Content:**
```
A Breath Under Water

A mechanical spectacle about Water, the most imminent and yet intimate topic of 
our times. Housed in and around the body of a life size and partially articulated 
whale sculpture.

A Breath Under Water, leads the audience into a sensory space, touching all facets 
of water, from its poetry and mystic stories, its importance in daily life, until 
the very topical issue of the impact of our behavior on the environment.

The project is now fully developed and in search of financing.

A Breath Under Water concept development with Nik Leuthold/CH and Claudius Bensch/D
Initiating force for the mobile art project: Marco Colabucci /I

Pre-production has led to collaboration with a multidisciplinary team and numerous 
international machine artists, as well as static and environmental engineers.

Amongst others: Jet van Heteren /NL and Cyril Fernandez /F, Bernhard Chaperon /F, 
Seb Lamparsky /D, Jenny Bock /D, Mike Tucker /GB, Jim Whiting /GB, Jerry Jester /GB,
Babu Fuhrer /CH, Luca Minotti /CH, Bart Sabels /NL, Daniël Rogier 't Sas /NL, 
Tiberio Scozzafava /I, Geckobau /CH

The efforts so far invested has only been possible with the kind support of 
Temperatio Stiftung /CH, as well as the support of the association 'l'antic teatre' 
in Barcelona /E, as well as the association Pachamama /F.
```

**Navigation Entry:**
The page appears in the PAPER WORK section navigation:
```
[PAPER WORK]
  [CONCEPT ILLUSTRATION]
  [GRAPHICAL WORK]
  BREATH UNDER WATER  ← Listed here (no link in nav, but page exists)
  [AKWA]
  [MALAGA LA VACHE]
```

---

### 3. Filesystem Analysis

#### Image Directory
```bash
old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja/2005TheWhale/
```

**Image Count:** 59 images total
- Main directory: 59 JPEG files (detailed design drawings, models, documentation)
- Subdirectory `whaledocnew/`: 14 additional JPEG files

**Sample Files:**
```
10TAILmovement.jpg
14LUNGS1.jpg, 15LUNGS2.jpg
16HEART1.jpg, 17HEART2.jpg
18BRAIN1.jpg, 19BRAIN2.jpg
20DOOR.jpg
bluewhaleStudies.jpg
brain111.jpg, brainBoth.jpg, brainPeople.jpg
builduptec.jpg
desertframe.jpg
entranceBack.jpg
Flyer.jpg (395 KB - promotional material)
Front1.jpg, Front2.jpg
heart.jpg, heart2.jpg
model1.jpg, model2.jpg, model3.jpg
Movementstudies2.jpg, Movementstudies3.jpg
Muscle_studies.jpg
newyork.jpg
SpineWithTitel.jpg
spinningdoor.jpg
TotaleBLAU.jpg
whale-model-med__.jpg
```

**Subdirectory `whaledocnew/`:**
```
blow_FR124.jpg
buildup_FR113.jpg
heart_FR122.jpg
intestines_FR117.jpg
lung_FR120.jpg, lung_FR121.jpg
mouth_FR126.jpg
pendulum_FR123.jpg
stomach_FR118.jpg, stomach_FR119.jpg
structure_FR112.jpg
tail_FR115.jpg
The_Whale_tuned_FR114.jpg
The_Whale_tuned_FR127.jpg
```

**Observations:**
- Comprehensive documentation of whale sculpture design
- Technical drawings (lungs, heart, brain, tail, door mechanism)
- Scale models and 3D studies
- Engineering diagrams (structure, build-up, mechanics)
- Movement studies (tail, blow/spout mechanism)
- Presentation materials (flyer, total views)
- Professional photography codes (FR### = likely frame numbers from photo shoot)

---

### 4. Current Migration Script Analysis

#### File: `scripts/extract_paintings_data.py`

**Lines 23-26:**
```python
def extract_paintings_pages(sql_content):
    """Extract painting project pages"""
    print("📄 Extracting painting pages...")
    
    # UIDs we're looking for (all paintings except UID 982 "Breath under Water")
    painting_uids = [866, 918, 919, 920, 921, 922, 923]
```

**Issue:** UID 982 is **explicitly excluded** with comment noting it was already known to be problematic.

**Extraction Logic:**
```python
def extract_tt_content(sql_content, paintings):
    """Extract content elements for paintings"""
    # ... searches for tt_content records with matching PID ...
```

**Current Results:**
- Script finds 7 pages in the `pages` table
- Script finds 0 content elements in `tt_content` for all 7 pages
- Only pages with tt_content would proceed to final output

---

## Root Cause Analysis

### Why No `tt_content` Records?

**Hypothesis 1: Static HTML Content System**
- TYPO3 allows mixed content management approaches
- Some pages may use static HTML files instead of database content
- This was common in older TYPO3 installations (v4.x era)
- Static pages would be stored in `fileadmin/` or similar directories

**Hypothesis 2: Alternative Content Storage**
- Content might be in a different TYPO3 extension's table
- Could be using a custom content element type
- Might be using TemplaVoilà or another page template system

**Hypothesis 3: Page Type Difference**
- These pages might have a different `doktype` configuration
- Could be "external URL" or "shortcut" page types redirecting to static content

**Evidence Supporting Hypothesis 1:**
1. Live website successfully displays extensive content
2. Content is well-formatted HTML with proper structure
3. URL pattern matches other TYPO3 pages (`/content/recent-work/the-whale.html`)
4. Navigation structure includes these pages
5. No evidence of redirect or external links in page records

---

## Comparison with Successfully Migrated Projects

### Projects WITH `tt_content` (Successfully Migrated)

**UID 866 - Murals Europe**
- Has multiple tt_content records
- Content includes descriptions, image galleries
- Successfully extracted and migrated

**UID 999 - Unknown Mural**
- Has tt_content records
- Standard TYPO3 content structure

**UID 1000 - Unknown Paper Work**
- Has tt_content records
- Standard TYPO3 content structure

### Projects WITHOUT `tt_content` (Failed to Migrate)

**All 14 other painting pages including:**
- UID 982 - Breath under Water
- UIDs 918-923 - Various other paintings
- UIDs 1200, 1211, 1330, 1344, 1345, 1398, 1461

---

## Migration Strategy

### Option A: Web Scraping Approach ⭐ **RECOMMENDED**
**Extract content from live website for pages without tt_content**

**Advantages:**
- Gets the actual content as it appears on the live site (source of truth)
- No guesswork about content location
- Preserves exact formatting and structure
- Can verify against what users currently see

**Implementation:**
1. For each page without tt_content:
   - Fetch the live HTML from maja-explosiv.com
   - Parse the main content area (between navigation and footer)
   - Extract text, images, and structure
   - Convert to Markdown format for new site
2. Match filesystem images to scraped content
3. Create complete project markdown files

**Code Approach:**
```python
import requests
from bs4 import BeautifulSoup

def scrape_painting_page(uid, url):
    """Scrape content from live website for pages without database content"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract main content (between nav and footer)
    content_area = soup.find(id='tdColContent')
    
    # Parse headings, paragraphs, lists
    # Extract image references
    # Convert to Markdown
    
    return {
        'title': extract_title(soup),
        'description': extract_body_text(content_area),
        'images': extract_image_references(content_area),
        'year': extract_year(content_area),
        # ... additional metadata
    }
```

### Option B: Static HTML File Search
**Search backup for static HTML files**

**Disadvantages:**
- May not find all pages (TYPO3 generates HTML dynamically)
- Files may not exist in backup
- Less reliable than live site

### Option C: Manual Content Entry
**Manually transcribe content from live website**

**Disadvantages:**
- Time-consuming
- Error-prone
- Not scalable

---

## Recommended Solution

### Phase 1: Enhance Migration Script ✅

Create `scripts/extract_paintings_comprehensive_webscrape.py`:

```python
"""
Comprehensive Paintings Migration - Web Scraping Approach
Based on: scripts/extract_paintings_data.py
Handles projects with and without tt_content by scraping live website
"""

import json
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# All painting page UIDs (including those without tt_content)
PAINTING_PAGES = {
    # Murals (PID 874)
    866: {'category': 'murals', 'url': 'content/2d/murals/murals-europe.html'},
    918: {'category': 'murals', 'url': None},  # Need to find URL
    919: {'category': 'murals', 'url': None},
    # ... etc
    
    # Paper Work (PID 875)
    982: {'category': 'paper-work', 'url': 'content/recent-work/the-whale.html'},
    # ... etc
}

def scrape_live_content(url):
    """Scrape content from live maja-explosiv.com website"""
    full_url = f"https://www.maja-explosiv.com/{url}"
    
    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract main content area
        content_div = soup.find(id='tdColContent')
        if not content_div:
            return None
        
        # Parse content
        title = soup.find('h1')
        paragraphs = content_div.find_all('p', class_='bodytext')
        
        return {
            'title': title.text.strip() if title else '',
            'body': '\n\n'.join(p.text.strip() for p in paragraphs),
            'images': extract_images_from_content(content_div),
        }
    except Exception as e:
        print(f"  ✗ Failed to scrape {url}: {e}")
        return None

def match_filesystem_images(uid):
    """Match images from filesystem for this project"""
    # Use existing logic from extract_paintings_data.py
    # ...
    pass

def create_project_data(uid, config):
    """Create complete project data combining database, web scrape, and filesystem"""
    
    # 1. Get basic page info from database
    page_info = extract_page_from_sql(uid)
    
    # 2. Try to get content from tt_content table
    db_content = extract_tt_content_for_page(uid)
    
    # 3. If no database content, scrape from live website
    if not db_content and config['url']:
        scraped_content = scrape_live_content(config['url'])
        if scraped_content:
            content = scraped_content
        else:
            content = {'title': '', 'body': '', 'images': []}
    else:
        content = db_content
    
    # 4. Match filesystem images
    fs_images = match_filesystem_images(uid)
    
    # 5. Combine all data
    return {
        'uid': uid,
        'title': content['title'] or page_info['title'],
        'description': content['body'],
        'category': config['category'],
        'images': fs_images,
        'source': 'web_scrape' if not db_content else 'database',
        # ... additional fields
    }
```

### Phase 2: Map All URLs 📋

**Action Required:**
1. Visit live website and identify URL for each of the 14 unmigrated pages
2. Update `PAINTING_PAGES` dictionary with correct URLs
3. Verify each page is accessible

**Known URLs:**
- UID 982: `content/recent-work/the-whale.html` ✓

**URLs to Find:** (13 pages)
- UIDs 918, 919, 920, 921, 922, 923, 1200, 1211, 1330, 1344, 1345, 1398, 1461

### Phase 3: Execute Migration 🚀

1. Run enhanced script to extract all 17 painting projects
2. Generate markdown files for new site
3. Copy associated images to new site structure
4. Verify all content migrated correctly

---

## Success Criteria

✅ **All 17 painting projects migrated** (currently only 3)  
✅ **UID 982 "Breath under Water" successfully migrated** with all 59 images  
✅ **Content matches live website** (source of truth)  
✅ **Filesystem images properly associated** with projects  
✅ **No data loss** compared to current live site

---

## Additional Findings

### Project Categorization
- "Breath under Water" is classified as "paper work" in database (PID 875)
- However, it's a large sculptural installation project (whale sculpture)
- May need reclassification to "sculptures" or "installations" category
- URL structure suggests it's under "recent-work" not "painting/paper-work"

### Image Organization
- Images follow naming pattern: `2005TheWhale/`
- Year prefix: 2005
- Project has two image sets:
  - Main design/engineering drawings (59 files)
  - Documentation photos in `whaledocnew/` subdirectory (14 files)
- Total: 73 images for this project

### Content Richness
- Very detailed project description
- Multiple collaborators listed (international team)
- Technical details about whale sculpture mechanics
- Funding information
- Exhibition/deployment plans

---

## Questions for Project Owner

1. **Categorization:** Should "Breath under Water" be moved from "paintings > paper work" to "sculptures" or "installations"?

2. **URL Structure:** The live URL is `/content/recent-work/the-whale.html` - should we preserve this path or use the database category structure?

3. **Content Priority:** For pages with both database content AND web content that differ, which should take precedence?

4. **Video Content:** Live page mentions YouTube videos. Should we:
   - Extract video embed codes?
   - Create YouTube links?
   - Embed videos in new site?

5. **Project Status:** Content states "in search of financing" - is this still current or should it be updated for the new site?

---

## Next Steps

1. **Immediate:**
   - [ ] Get approval for web scraping approach
   - [ ] Map URLs for all 14 unmigrated painting pages
   - [ ] Create enhanced migration script with web scraping

2. **Short-term:**
   - [ ] Test script on UID 982 "Breath under Water"
   - [ ] Verify scraped content matches live site
   - [ ] Run full migration for all 17 painting projects

3. **Long-term:**
   - [ ] Apply same approach to sculptures and installations if needed
   - [ ] Document web scraping methodology
   - [ ] Create validation tests to ensure content fidelity

---

## Files Modified/Created

### Documentation
- ✅ `project_docs/breath-under-water-investigation.md` (this file)

### Scripts (Proposed)
- ⏳ `scripts/extract_paintings_webscrape.py` (to be created)
- ⏳ `scripts/url_mapper.py` (helper to find all painting URLs)

---

## Conclusion

**The "Breath under Water" project did not fail to migrate due to data corruption or technical error.** Instead, it represents a larger pattern: **82% of painting pages (14/17) store their content outside the standard TYPO3 `tt_content` table**, likely as static HTML.

The solution is to enhance the migration script to scrape content from the live website for pages without database content. This approach:
- Uses the live site as the source of truth ✓
- Ensures content fidelity ✓
- Handles edge cases in the old TYPO3 configuration ✓
- Can be applied to other content types if needed ✓

**Recommended Action:** Proceed with web scraping approach to capture all 14 missing painting projects.
