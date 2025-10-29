# TYPO3 Filesystem Analysis

**Backup Location:** `old/TYPO3BU/_/`  
**TYPO3 Version:** 4.2.14  
**Analysis Date:** 2025-10-29

---

## Executive Summary

The TYPO3 backup contains approximately **1,693 image files** across multiple directories. The primary content is located in:

1. **`fileadmin/s-maj/`** - Maja's portfolio images (~1,440 images)
2. **`uploads/pics/`** - General uploaded images (~253 images)
3. **`uploads/tx_ttnews/`** - News-related images

---

## Directory Structure Overview

```
old/TYPO3BU/_/
├── fileadmin/              # User-uploaded files and site assets
│   ├── s-maj/              # ⭐ MAJA'S PORTFOLIO (PRIMARY)
│   ├── s-km/               # Other user content (not Maja)
│   ├── s-mhk/              # Other user content (not Maja)
│   ├── s-pf/               # Other user content (not Maja)
│   ├── s-wt/               # Other user content (not Maja)
│   ├── css/                # Stylesheets (not needed)
│   ├── images/             # General site images
│   ├── template/           # Template files (not needed)
│   └── ...                 # Other directories
├── uploads/                # TYPO3 system uploads
│   ├── pics/               # ⭐ GENERAL IMAGES (SECONDARY)
│   ├── tx_ttnews/          # ⭐ NEWS IMAGES (TERTIARY)
│   ├── media/              # Media files
│   └── ...                 # Extension-specific uploads
├── typo3conf/              # TYPO3 configuration (not needed)
├── typo3temp/              # Temporary files (not needed)
└── typo3_src-4.2.14/       # TYPO3 core files (not needed)
```

---

## Critical Directories for Migration

### 1. `fileadmin/s-maj/` ⭐ PRIMARY

**Purpose:** Maja Thommen's portfolio images and content.

**Structure:**
```
fileadmin/s-maj/
├── images/
│   └── BilderMaja/         # Main portfolio directory
│       ├── 1994muralsFassaden/
│       ├── 1995Eurokot/
│       ├── 1997Bagger/
│       ├── 2000Elxt90/
│       ├── 2001Elxt90/
│       ├── 2003CasinoGitano/
│       ├── 2005TheWhale/
│       ├── 2008Kalandraka/
│       ├── 2010Mikz/
│       ├── 2013SisyphosGate/
│       ├── 2015NovaTwo/
│       ├── 2018_Portrait/
│       ├── 2020_Affenhorde/
│       ├── 2022_Affenbande/
│       ├── 2024_Hafensszene/
│       ├── aafront/        # Front page images
│       ├── concepts/       # Concept sketches
│       ├── picsMaja/       # Personal photos
│       ├── poster/         # Posters
│       ├── presse/         # Press images
│       └── thumbs/         # Thumbnails (can be regenerated)
└── tpl/                    # Templates (not needed)
```

**Total Images:** ~1,440 files  
**Total Project Directories:** 68 directories

**File Types:**
- `.jpg` / `.jpeg` - Primary format
- `.png` - Some images
- `.gif` - Rare

**Naming Patterns:**
- Year-based: `1994muralsFassaden`, `2005TheWhale`, `2024_Hafensszene`
- Project-based: `Kalandraka`, `SisyphosGate`, `NovaTwo`
- Mixed: Year + Project name

**Migration Strategy:**
- ✅ **Extract:** All images from project directories
- ✅ **Categorize:** Map to sculptures/installations/performance/paintings
- ✅ **Organize:** Use approved asset organization (category → series → images)
- ❌ **Skip:** `thumbs/` directory (regenerate with Eleventy Image plugin later)
- ❌ **Skip:** `tpl/` directory (templates not needed)

---

### 2. `uploads/pics/` ⭐ SECONDARY

**Purpose:** General uploaded images referenced in `tt_content` table.

**Total Images:** ~253 files

**File Types:**
- `.jpg` / `.jpeg`
- `.png`
- `.gif`

**Migration Strategy:**
- ✅ **Extract:** Images referenced in database
- ✅ **Map:** Cross-reference with `tt_content.image` field
- ✅ **Organize:** Place in appropriate category based on content context
- ❌ **Skip:** Unreferenced images (orphaned files)

---

### 3. `uploads/tx_ttnews/` ⭐ TERTIARY

**Purpose:** Images uploaded through tt_news extension (news articles).

**Migration Strategy:**
- ✅ **Extract:** Images referenced in `tt_news` table
- ✅ **Map:** Cross-reference with `tt_news.image` field
- ✅ **Organize:** Place in `src/assets/images/news/[year]/[slug]/`
- ❌ **Skip:** Unreferenced images

---

## Directories NOT Needed for Migration

### System Directories ❌

- `typo3_src-4.2.14/` - TYPO3 core files
- `typo3conf/` - TYPO3 configuration
- `typo3temp/` - Temporary/cache files
- `cgi-bin/` - CGI scripts
- `stats/` - Statistics files

### Other User Directories ❌

- `fileadmin/s-km/` - Not Maja's content
- `fileadmin/s-mhk/` - Not Maja's content
- `fileadmin/s-pf/` - Not Maja's content
- `fileadmin/s-wt/` - Not Maja's content

### Template/Style Directories ❌

- `fileadmin/css/` - Old stylesheets (new design in Eleventy)
- `fileadmin/template/` - Old templates (not needed)
- `fileadmin/CssMenue/` - Old menu styles
- `fileadmin/DhtmlHMenue/` - Old DHTML menu
- `fileadmin/flash/` - Flash files (obsolete)
- `fileadmin/Flash2/` - Flash files (obsolete)

### Extension Upload Directories ❌

- `uploads/tx_cal/` - Calendar extension
- `uploads/tx_dam/` - Digital Asset Management
- `uploads/tx_slideshow/` - Slideshow extension
- `uploads/tx_rgsmoothgallery/` - Gallery extension
- `uploads/tx_*` - Other extension uploads (not needed)

---

## Project Directory Categorization

Based on directory names and typical artist portfolio structure, here's a preliminary categorization:

### Sculptures (3D Works)
- `1997Bagger` - Excavator sculpture
- `2008geier` - Vulture sculpture
- `2008pleitegeier` - Bankrupt vulture
- `2008juraBird` - Jura bird
- `2009elefant` - Elephant
- `2009vogelpaar` - Bird pair
- `2010VogelEffi` - Bird Effi
- `2010VogelSuter` - Bird Suter
- `2012WackenScull` - Wacken skull
- `2012WOA_Bull` - Wacken bull
- `2013Schutzengel` - Guardian angel
- `2014Lionfish` - Lionfish
- `2014Seamonster` - Sea monster
- `2015GongTrophy` - Gong trophy
- `2016BillParooka` - Bill Parooka
- `2017_Nelly_Bird` - Nelly bird
- `2019_Wolf` - Wolf
- `2020_Affenhorde` - Monkey horde
- `2022_Affenbande` - Monkey gang

### Installations
- `1995Eurokot` - Eurokot installation
- `1996EurokonAllg` - Eurokon installation
- `1998Dorfbachschiff` - Dorfbach ship
- `2000Elxt90` - Elxt90 installation
- `2001Elxt90` - Elxt90 continuation
- `2002FreeRSpannwerk` - Free R Spannwerk
- `2003CasinoGitano` - Casino Gitano
- `2003ForgetMeNot` - Forget Me Not
- `2003Sihlpapier` - Sihlpapier
- `2004Mantelheizung` - Mantel heating
- `2004Troy` - Troy
- `2005Akwa` - Akwa
- `2005TheWhale` - The Whale
- `2006AlchemyBar` - Alchemy Bar
- `2007WheelOfPower` - Wheel of Power
- `2008Kalandraka` - Kalandraka
- `2009carwreck` - Car wreck
- `2009nova3` - Nova 3
- `2010duschfass` - Shower barrel
- `2010Mikz` - Mikz
- `2010OdonischeFeuer` - Odonic fire
- `2013FifthEstate` - Fifth Estate
- `2013SisyphosGate` - Sisyphos Gate
- `2013TubeRail` - Tube Rail
- `2014ApocaypseFence` - Apocalypse Fence
- `2015NovaTwo` - Nova Two
- `2015Weglampen` - Path lamps
- `2017Weglampen` - Path lamps (2017)
- `2021BlumenWolke` - Flower cloud
- `2024_Hafensszene` - Harbor scene

### Performance
- `1997Xix` - Xix performance
- `2007 handofman` - Hand of Man
- `2008soldierErico` - Soldier Erico
- `2008tcc` - TCC

### Paintings/Murals
- `1994muralsFassaden` - Murals/Facades
- `2005Malaga` - Malaga
- `2018_Portrait` - Portraits
- `2019_Flowerpower` - Flower power

**Note:** This categorization is preliminary and should be verified against the actual database content during migration.

---

## Image Reference Mapping

### Database → Filesystem Mapping

**Pattern 1: Direct filename reference**
```
Database: image = "sculpture01.jpg"
Filesystem: uploads/pics/sculpture01.jpg
```

**Pattern 2: Relative path reference**
```
Database: image = "fileadmin/s-maj/images/BilderMaja/2005TheWhale/whale01.jpg"
Filesystem: fileadmin/s-maj/images/BilderMaja/2005TheWhale/whale01.jpg
```

**Pattern 3: Multiple images (comma-separated)**
```
Database: image = "img1.jpg,img2.jpg,img3.jpg"
Filesystem: uploads/pics/img1.jpg, uploads/pics/img2.jpg, uploads/pics/img3.jpg
```

---

## Migration Workflow

### Phase 1: Inventory
1. Extract all image references from database (`tt_content.image`, `tt_news.image`)
2. Build complete list of referenced images
3. Verify all referenced images exist in filesystem
4. Identify orphaned images (in filesystem but not referenced)

### Phase 2: Categorization
1. Map each project directory to category (sculptures/installations/performance/paintings)
2. Create mapping file: `old_path → new_path`
3. Validate categorization with Michael

### Phase 3: Migration
1. Copy images to new asset structure
2. Rename following naming conventions (kebab-case, sequential numbering)
3. Update database references to new paths
4. Generate Markdown files with correct image paths

---

## Estimated Migration Scope

| Category | Estimated Projects | Estimated Images |
|----------|-------------------|------------------|
| Sculptures | ~20 projects | ~400 images |
| Installations | ~30 projects | ~800 images |
| Performance | ~5 projects | ~100 images |
| Paintings/Murals | ~5 projects | ~100 images |
| News | TBD | ~50 images |
| Shared/Profile | N/A | ~50 images |
| **TOTAL** | **~60 projects** | **~1,500 images** |

---

## Next Steps

1. ✅ **Database analysis complete** (see `typo3-database-analysis.md`)
2. ✅ **Filesystem analysis complete** (this document)
3. ⏳ **Create test extraction script** (5 posts per category)
4. ⏳ **Validate conversion quality**
5. ⏳ **Full migration**

---

**Status:** ✅ Analysis Complete  
**Ready for:** Test Migration Script

