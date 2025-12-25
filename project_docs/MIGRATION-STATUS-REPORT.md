# Migration Status Report and Roadmap
**Maja Explosiv: TYPO3 to Eleventy Migration**

**Document Created:** December 23, 2025  
**Last Updated:** October 29, 2025  
**Project Status:** IN PROGRESS - Content Extraction Phase  
**Completion:** ~35% (Foundation & Initial Content Migration)

---

## Executive Summary

The migration from TYPO3 to Eleventy is progressing steadily with critical infrastructure and initial content extraction completed. The project successfully resolved major technical challenges including character encoding issues and database parsing complexities. Currently, 70 projects have been extracted from the TYPO3 database with one project requiring investigation before proceeding to full migration.

**Current Phase:** Epic 1.3 - Content Migration (Partial)  
**Next Milestone:** Complete investigation of missing project, then proceed with image extraction and full content migration

---

## Migration-Related Files Inventory

### Core Documentation Files

#### [project_docs/RESUME-WORK-HERE.md](project_docs/RESUME-WORK-HERE.md)
- **Content Description:** Quick-start guide for resuming work on the migration
- **Relevance Status:** Current (Last updated October 29, 2025)
- **Key Information:**
  - Fast-track resume instructions (30 seconds)
  - Priority task: Investigate missing "Breath under Water" project
  - Current build status: ✅ Success (55 files generated)
  - Investigation commands and next steps provided

#### [project_docs/SESSION-2025-10-29-SUMMARY.md](project_docs/SESSION-2025-10-29-SUMMARY.md)
- **Content Description:** Comprehensive work session summary from October 29, 2025
- **Relevance Status:** Current
- **Key Information:**
  - Character encoding issue resolved ✅
  - 70 projects extracted (7 paintings, 28 sculptures, 26 installations, 9 performance)
  - Missing project investigation (UID 982 "Breath under Water")
  - Detailed "How to Resume Work" section
  - All files modified during session documented

#### [project_docs/typo3-technical-findings.md](project_docs/typo3-technical-findings.md)
- **Content Description:** Complete technical documentation of TYPO3 database structure and migration findings
- **Relevance Status:** Current (891 lines, comprehensive)
- **Key Information:**
  - **Database Structure:** MySQL 5.0.96, 107 tables, Latin-1 German collation
  - **Parsing Details:** Multi-line INSERT statement handling, field extraction logic
  - **Page Hierarchy:** Complete TYPO3 site structure with UIDs and parent relationships
  - **Character Encoding:** Double-encoded UTF-8 issue fully documented with solution
  - **Installation Detection:** Keyword-based algorithm for sculptures vs installations
  - **Category Mapping:** Old TYPO3 structure → New Eleventy collections mapping
  - **Image Storage Patterns:** Database format and filesystem locations documented

#### [project_docs/encoding-fix-summary.md](project_docs/encoding-fix-summary.md)
- **Content Description:** Detailed summary of character encoding fix implementation
- **Relevance Status:** Current
- **Key Information:**
  - Problem: Double-encoded UTF-8 (e.g., "Käthe" → "KÃ¤the")
  - Root Cause: UTF-8 bytes misinterpreted as Latin-1, then re-encoded
  - Solution: `fix_double_encoding()` function that reverses the double-encoding
  - Verification: All German characters now display correctly
  - Before/after examples and byte-level analysis

#### [project_docs/typo3-database-analysis.md](project_docs/typo3-database-analysis.md)
- **Content Description:** Executive analysis of TYPO3 database tables and migration strategy
- **Relevance Status:** Current
- **Key Information:**
  - **Critical Tables:** `pages` (structure), `tt_content` (content), `tt_news` (news)
  - **Field Mappings:** TYPO3 fields → Eleventy front matter mappings
  - **Extraction Queries:** SQL queries for extracting active content
  - **Image References:** Comma-separated format in database
  - **Encoding:** Latin-1 German → UTF-8 conversion requirement
  - **Tables to Skip:** System tables (be_*, cache_*, sys_*, etc.)

#### [project_docs/typo3-filesystem-analysis.md](project_docs/typo3-filesystem-analysis.md)
- **Content Description:** Analysis of TYPO3 backup filesystem structure
- **Relevance Status:** Current
- **Key Information:**
  - **Total Images:** ~1,693 files
  - **Primary Location:** `old/TYPO3BU/_/fileadmin/s-maj/` (~1,440 images)
  - **Secondary Location:** `old/TYPO3BU/_/uploads/pics/` (~253 images)
  - **Directory Structure:** 68 project directories organized by year and project name
  - **File Naming Patterns:** Year-based (e.g., `2005TheWhale`, `2024_Hafensszene`)
  - **Migration Scope:** ~60 projects, ~1,500 images estimated
  - **Directories to Skip:** System dirs, other users' content, obsolete Flash files

#### [project_docs/asset-organization-strategy.md](project_docs/asset-organization-strategy.md)
- **Content Description:** Approved strategy for organizing assets in the new site
- **Relevance Status:** Current (Approved by Winston, October 29, 2025)
- **Key Information:**
  - **Design Principles:** No giant directories, conceptual organization, flexible reuse
  - **Structure:** `src/assets/images/projects/{category}/{series-slug}/`
  - **Naming Convention:** Kebab-case slugs, zero-padded numbers (e.g., `urban-fragments-01.jpg`)
  - **Categories:** sculptures, installations, performance, paintings, news, shared
  - **Benefits:** Maintainability, migration-friendly, scalable growth

#### [project_docs/PRD.md](project_docs/PRD.md)
- **Content Description:** Product Requirements Document for the website redesign
- **Relevance Status:** Current (Project level 3, comprehensive)
- **Key Information:**
  - **Goals:** Business continuity, modern/performant/secure site, Git-based workflow, 100% content migration, 90+ PageSpeed score
  - **Functional Requirements:** Complete migration (FR001-002), UTF-8 encoding (FR003), correct order (FR004), Eleventy + DataStar stack
  - **Non-Functional:** Performance (NFR001), security (NFR002), maintainability (NFR003), accessibility (NFR004)
  - **User Journeys:** Gallery curator exploration, artist adding new project
  - **Out of Scope:** Mobile design, contact form, image optimization pipeline, URL redirects

#### [project_docs/epics.md](project_docs/epics.md)
- **Content Description:** Detailed epic and story breakdown for the migration project
- **Relevance Status:** Current
- **Key Information:**
  - **Epic 1:** Project Foundation & Content Migration (6 stories)
    - Story 1.1: Template Gap Analysis ✅ (Completed)
    - Story 1.2: Site-Specific Content Structure ✅ (Completed)
    - Story 1.3: Script and Execute Content Migration 🔄 (In Progress)
    - Story 1.4: Migrate Static Assets ⏳ (Pending)
    - Story 1.5: Link Content and Assets ⏳ (Pending)
    - Story 1.6: Verify Migration Integrity ⏳ (Pending)
  - **Epic 2:** Desktop UI Implementation & Interactivity (6 stories)
    - All stories pending (awaiting Epic 1 completion)

### Data and Extraction Files

#### [project_docs/extracted-projects.json](project_docs/extracted-projects.json)
- **Content Description:** JSON output from extraction script containing all 70 extracted projects
- **Relevance Status:** Current (Regenerated with encoding fix)
- **Key Information:**
  - 28 sculptures projects
  - 26 installations projects
  - 9 performance projects
  - 7 paintings projects (3 murals + 4 paper work)
  - Each project includes: title, description, year, category, source_page, source_uid, images array
  - German characters correctly encoded (ä, ö, ü, ß)

#### [project_docs/typo3-page-structure.json](project_docs/typo3-page-structure.json)
- **Content Description:** JSON export of TYPO3 page hierarchy
- **Relevance Status:** Reference (Used during analysis phase)
- **Key Information:**
  - Complete page tree with UIDs and parent-child relationships
  - Category structure (sculptures, show, painting with subcategories)
  - Used for understanding TYPO3 organization

### Scripts

#### [scripts/extract_typo3_projects.py](scripts/extract_typo3_projects.py)
- **Content Description:** Main extraction script for pulling projects from TYPO3 SQL dump
- **Relevance Status:** Current (Modified October 29, 2025)
- **Key Information:**
  - **Functions:**
    - `extract_pages_data()` - Parses pages table with multi-INSERT handling
    - `extract_content_elements()` - Parses tt_content table
    - `find_all_descendants()` - Recursively finds child pages
    - `categorize_project()` - Determines category using keyword matching
    - `fix_double_encoding()` - Reverses UTF-8 double-encoding
    - `clean_html()` - Strips HTML tags and cleans text
  - **Category Mapping:** UID-based mapping with installation keyword detection
  - **Encoding Fix Applied:** Lines 35, 195 (UTF-8 reading), 179, 258, 261, 332 (fix application)
  - **Installation Keywords:** gate, fence, installation, suspended, fountain, kinetic, etc.

#### [scripts/convert_test_projects.py](scripts/convert_test_projects.py)
- **Content Description:** Script to convert extracted JSON to Markdown files (test subset)
- **Relevance Status:** Current (Used for initial 20-project test)
- **Key Information:**
  - Selects 5 most recent projects per category
  - Generates slug from title (transliteration for German characters)
  - Creates front matter with title, date, category, tags
  - Outputs to `src/posts/projects/{category}/{slug}.md`
  - Adds source metadata as HTML comment

#### [scripts/analyze_typo3_structure.py](scripts/analyze_typo3_structure.py)
- **Content Description:** Analysis script for exploring TYPO3 database structure
- **Relevance Status:** Reference (Used during investigation phase)
- **Key Information:**
  - Extracts pages and builds hierarchy tree
  - Identifies category pages by keywords
  - Prints tree structure with UIDs
  - Helped understand TYPO3 organization before extraction

### Database and File Backups

#### [old/usr_p51487_2.sql](old/usr_p51487_2.sql)
- **Content Description:** Complete TYPO3 database dump
- **Relevance Status:** Current (Source of truth for content)
- **Key Information:**
  - **Database:** MySQL 5.0.96 dump
  - **Character Set:** `latin1_german1_ci` (but contains UTF-8 encoded text)
  - **Created:** January 2, 2025
  - **Total Tables:** 107 tables
  - **Size:** Large multi-megabyte SQL file
  - **Critical Tables:** pages (179 pages), tt_content (443 elements)

#### [old/TYPO3BU/](old/TYPO3BU/)
- **Content Description:** Complete TYPO3 filesystem backup
- **Relevance Status:** Current (Source for all images and assets)
- **Key Information:**
  - `_/fileadmin/s-maj/` - Maja's portfolio images (~1,440 files)
  - `_/uploads/pics/` - General images (~253 files)
  - `_/uploads/tx_ttnews/` - News images
  - 68 project directories with year+name patterns
  - System directories to skip (typo3conf, typo3temp, typo3_src-4.2.14)

### Planning and Status Files

#### [project_docs/product-brief-Maja-Explosiv-Website-Redesign-2025-10-22.md](project_docs/product-brief-Maja-Explosiv-Website-Redesign-2025-10-22.md)
- **Content Description:** Original product brief for the redesign project
- **Relevance Status:** Reference
- **Key Information:**
  - Project context and business drivers
  - High-level requirements and goals
  - Predecessor to PRD.md

#### [project_docs/ux-specification.md](project_docs/ux-specification.md)
- **Content Description:** UX specifications for the new design
- **Relevance Status:** Current (Design reference)
- **Key Information:**
  - User flows and interaction patterns
  - Design principles and constraints

#### [project_docs/ui-phase-b.md](project_docs/ui-phase-b.md)
- **Content Description:** UI implementation phase B details
- **Relevance Status:** Future (Post-migration)
- **Key Information:**
  - Next phase of UI work after content migration

#### [project_docs/homepage-changes.md](project_docs/homepage-changes.md) & [project_docs/homepage-changes-plan.md](project_docs/homepage-changes-plan.md)
- **Content Description:** Documentation of homepage changes from template
- **Relevance Status:** Current (Implemented changes)
- **Key Information:**
  - Customizations to homepage layout and design
  - One-page experience with tabbed sections

#### [project_docs/pending-changes.md](project_docs/pending-changes.md)
- **Content Description:** List of pending changes and improvements
- **Relevance Status:** Current (Active task list)
- **Key Information:**
  - Outstanding work items
  - Future enhancements

#### [project_docs/bmm-workflow-status.md](project_docs/bmm-workflow-status.md)
- **Content Description:** BMM workflow status documentation
- **Relevance Status:** Reference (Related to build/migration/management workflows)

#### [project_docs/story-1.2-completion-report.md](project_docs/story-1.2-completion-report.md) & [project_docs/story-1.2-handoff.md](project_docs/story-1.2-handoff.md)
- **Content Description:** Completion documentation for Story 1.2 (Site-Specific Content Structure)
- **Relevance Status:** Historical (Completed story)
- **Key Information:**
  - Story 1.2 completed successfully
  - Foundation ready for content migration

### Supporting Documentation

#### [README.md](README.md)
- **Content Description:** Comprehensive documentation of the Eleventy template system
- **Relevance Status:** Current (Essential reference)
- **Key Information:**
  - **Template Features:** Collection management, static pages, dynamic navigation, Open Props design system
  - **Project Structure:** Detailed directory layout (`src/_includes`, `_layouts`, `_data`, etc.)
  - **Override System:** User directory architecture (`src/_user/`) for conflict-free customization
  - **Content Creation:** Markdown file formats for posts, pages, and collections
  - **Build Process:** Development server, production build commands
  - **Data Override:** JSON/JS file merging for theme configuration

#### [changes.md](changes.md)
- **Content Description:** Site-specific customizations to the upstream Explosive 11ty template
- **Relevance Status:** Current (402 lines)
- **Key Information:**
  - **Fixed Sidebar Layout:** 250px width, persistent navigation, no scrollbars
  - **Custom Layouts:** Home, project, page, post, collection layouts all extend sidebar
  - **CSS Customizations:** Box model reset, compact spacing, reduced font sizes, tab styling
  - **Eleventy Config Fix:** Passthrough copy object syntax for user assets
  - **Navigation:** PROJECTS and ABOUT clickable section headers with tab integration
  - **Files Modified:** custom.css, left-nav.njk, .eleventy.js, index.md

---

## Migration Summary

### What Has Been Completed ✅

1. **Infrastructure Setup**
   - Eleventy project initialized with Explosive 11ty template
   - User directory override system configured
   - Fixed sidebar layout implemented
   - Build system verified and functional

2. **Database Analysis**
   - Complete TYPO3 database structure documented
   - 107 tables catalogued, critical tables identified
   - Page hierarchy mapped (179 total pages, 94 active)
   - Content elements analyzed (443 elements)
   - Character encoding issue identified and solved

3. **Filesystem Analysis**
   - Complete backup directory structure documented
   - ~1,693 images catalogued across multiple directories
   - 68 project directories identified and categorized
   - Asset organization strategy approved

4. **Content Extraction Scripts**
   - `extract_typo3_projects.py` - Fully functional with encoding fix
   - `convert_test_projects.py` - Creates Markdown files from JSON
   - `analyze_typo3_structure.py` - Database exploration tool
   - Multi-INSERT statement parsing solved
   - Recursive page hierarchy traversal implemented
   - Installation vs sculpture keyword detection working

5. **Character Encoding Resolution**
   - Double-encoded UTF-8 issue identified at byte level
   - `fix_double_encoding()` function implemented
   - Applied to all text extraction points
   - Verified: German characters (ä, ö, ü, ß) display correctly
   - No encoding errors in 70 extracted projects

6. **Initial Content Extraction**
   - **70 projects extracted** from TYPO3 database:
     - 28 sculptures
     - 26 installations
     - 9 performance
     - 7 paintings (3 murals + 4 paper work)
   - All projects include title, description, year, category, source metadata
   - `extracted-projects.json` generated with correct encoding

7. **Test Migration**
   - 20 test projects converted to Markdown (5 per category)
   - Markdown files generated in correct directory structure
   - Build succeeds: 55 files generated
   - Front matter correctly formatted
   - Slug generation working (transliterates German characters)

### Current Status & Blockers 🔄

1. **Missing Project Investigation Required**
   - **Project:** "Breath under Water" (UID 982)
   - **Issue:** Page exists in database but has NO content in `tt_content` table
   - **Evidence:** Cached HTML shows extensive content about whale sculpture
   - **Status:** Awaiting investigation (cross-reference database with website files)
   - **Questions:**
     - Where is the actual content stored?
     - Should this be categorized as paintings or installations?
     - Should it be included in migration?

2. **Content Count Discrepancy**
   - User reported: 8 paintings projects (3 murals + 5 paper work)
   - Script extracted: 7 paintings projects (3 murals + 4 paper work)
   - Difference: 1 project (the missing UID 982)

### What Remains To Be Done ⏳

#### Immediate Next Steps (Epic 1.3 - Content Migration)

1. **Investigate Missing Project (High Priority)**
   - Search website files in `old/TYPO3BU/` for "Breath under Water" content
   - Cross-reference UID 982 in other database tables
   - Determine content source and categorization
   - Decide: Include or exclude from migration

2. **Complete Content Extraction**
   - Resolve missing project issue
   - Re-run extraction if needed
   - Convert remaining 50 projects to Markdown (70 total - 20 test = 50)
   - Verify all 70+ projects are present

#### Subsequent Epic 1 Stories

3. **Story 1.4: Migrate Static Assets (Image Extraction)**
   - Extract all image references from `tt_content.image` fields
   - Map image filenames to filesystem paths
   - Copy images from `old/TYPO3BU/` to new asset structure
   - Follow asset organization strategy (category → series → images)
   - Rename files to match naming conventions (kebab-case, zero-padded)
   - Handle multiple images per project (comma-separated format)
   - Extract and preserve image captions

4. **Story 1.5: Link Migrated Content and Assets**
   - Update Markdown front matter with image references
   - Create image arrays with src and caption fields
   - Update internal page links to use Eleventy URL structure
   - Verify all image paths are correct
   - Test image display in development server

5. **Story 1.6: Verify Migration Integrity**
   - Review all migrated content in development server
   - Verify text formatting is correct
   - Verify all images display correctly
   - Verify chronological order matches old site
   - Verify categorical organization is correct
   - Compare against original TYPO3 site for accuracy
   - Document any discrepancies or issues

#### Epic 2: Desktop UI Implementation & Interactivity

6. **Story 2.1: Implement Global Styles & Layouts**
   - Finalize base layouts (header, footer, content wells)
   - Apply global CSS variables
   - Ensure consistency across all page types

7. **Story 2.2-2.4: Build Page Templates**
   - Homepage with featured content
   - Projects overview and collection pages
   - Post/item detail pages with full content

8. **Story 2.5-2.6: Interactive Components**
   - Image carousel implementation (DataStar)
   - News feed component
   - Tab switching functionality
   - Mobile responsiveness (deferred to later phase)

---

## Technical Context

### Eleventy Templating System

**Template Engine:** Nunjucks (.njk files)

**Key Concepts:**
- **Collections:** Dynamic groupings of content (sculptures, installations, performance, paintings)
- **Front Matter:** YAML metadata at top of Markdown files (title, date, category, tags, etc.)
- **Layouts:** Nunjucks templates that wrap content (base.njk → sidebar-layout.njk → specific layouts)
- **Includes:** Reusable components (header, footer, navigation)
- **Data Files:** Global configuration (site.json, theme.js, collectionData.json)

**Override System:**
- Base files: `src/_layouts/`, `src/_includes/`, `src/_data/`
- User overrides: `src/_user/layouts/`, `src/_user/includes/`, `src/_user/data/`
- Build-time merging: User files take precedence, no source modifications

**Build Process:**
```bash
npm run serve  # Development server with live reload (localhost:8080)
npm run build  # Production build to _site/
```

**Asset Pipeline:**
- User assets: `src/_user/assets/` → `_site/assets/` (overrides base)
- Passthrough copy: Uses object mapping `{ "src/_user/assets": "assets" }`

### Migration-Specific Technical Considerations

#### Database Parsing Challenges

1. **Multi-line INSERT Statements**
   - Same table can have multiple INSERT statements throughout SQL file
   - Must use `re.finditer()` to find all occurrences
   - Must use `re.DOTALL` flag for multi-line pattern matching

2. **Field Extraction Complexity**
   - Fields wrapped in backticks with inconsistent spacing
   - Must strip whitespace THEN backticks: `f.strip().strip('`')`
   - Quoted values may contain commas, parentheses, escaped quotes

3. **Value Parsing**
   - Handle escaped characters (\\, \', '')
   - Track string delimiters to avoid splitting quoted values
   - Handle NULL values vs empty strings

#### Character Encoding Strategy

**Problem:** Double-encoded UTF-8
- Original: UTF-8 bytes (e.g., `c3a4` for 'ä')
- Misinterpretation: Bytes read as Latin-1 characters ('Ã¤')
- Re-encoding: Latin-1 chars encoded as UTF-8 (4 bytes: `c383c2a4`)

**Solution:** Reverse double-encoding
```python
def fix_double_encoding(text):
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text
```

**Application Points:**
- Page titles during extraction
- Content headers and body text
- All text processed through `clean_html()`

#### Category Determination Logic

**Hierarchical Mapping:**
1. Find parent category page by UID (870=sculptures, 868=show, 869=painting)
2. Find all descendant pages recursively
3. For sculptures/collaborations: Apply keyword detection

**Installation Keywords:**
```python
['installation', 'gate', 'fence', 'bar', 'railing', 'door',
 'helix', 'channel', 'tubebox', 'weglampen', 'path illumination',
 'fountain', 'shower', 'wreck', 'suspended', 'kinetic']
```

**Logic:** If parent is sculptural work AND keywords found → installations, else → sculptures

#### Image Reference Format

**In Database:**
- Format: `"image1.jpg,image2.jpg,image3.jpg"` (comma-separated)
- Captions: Newline-separated in `imagecaption` field (one per image)

**In Filesystem:**
- Direct filenames: `uploads/pics/image1.jpg`
- Relative paths: `fileadmin/s-maj/images/BilderMaja/2005TheWhale/whale01.jpg`

**In New Site:**
- Array in front matter:
  ```yaml
  images:
    - src: /assets/images/projects/installations/the-whale/the-whale-01.jpg
      caption: "Front view of whale sculpture"
  ```

#### Asset Organization Requirements

**Constraints:**
- No single directory with hundreds of files
- Must support flexible image reuse across posts
- Must be migration-friendly (map from TYPO3 structure)
- Must be maintainable long-term

**Approved Structure:**
```
src/assets/images/
├── projects/
│   ├── {category}/          # sculptures, installations, performance, paintings
│   │   └── {series-slug}/   # e.g., the-whale, affenbande
│   │       └── {series-slug}-{number}.jpg  # e.g., the-whale-01.jpg
├── news/
│   └── {year}/
│       └── {event-slug}/
└── shared/
    ├── profile/
    ├── press/
    └── general/
```

**Naming:**
- Directories: kebab-case, lowercase, no special chars
- Files: `{series-slug}-{zero-padded-number}.{ext}`
- Sequential numbering: 01, 02, 03, ... (not 1, 2, 3)

---

## Migration Strategy

### Project Migration Sequence

As specified by the user, the migration will proceed in this order:

1. **Projects** (First Priority)
   - Four project types as templates: sculptures, installations, performance, paintings
   - Each old project belonged to a subcategory → retain as tags in metadata
   - All images associated with each project must be migrated
   - Scripts create MD files in correct directory for project type

2. **Bio** (Second Priority)
   - About/bio content
   - Timeline information

3. **Press** (Third Priority)
   - Press releases and coverage
   - Press images

4. **Timeline** (Fourth Priority)
   - Chronological event information

### Test-First Approach

For each template type, migration will follow this pattern:

1. **Small Test Migration**
   - Select 1-3 projects of that type
   - Verify all info from old site can populate new template
   - Validate template requirements are met
   - Identify and fix any issues

2. **Full Migration**
   - Once test succeeds, migrate all projects of that type
   - Apply same process to remaining content types

### Metadata Preservation

**Subcategory Information:**
- Old site: Projects belonged to subcategories (e.g., "murals", "paper work", "sculptural work")
- New site: Retain as tags in front matter
  ```yaml
  tags:
    - paintings
    - murals
    - 2005
  ```

**Image Associations:**
- All images linked to project in old site must be linked in new site
- Preserve image order
- Preserve captions if present
- Support multiple images per project

**Source Tracking:**
- Include source metadata in Markdown files as HTML comment:
  ```html
  <!-- 
  Source: TYPO3 page UID 982
  Category: paper work
  -->
  ```

---

## Recommended Next Steps

### Priority 1: Resolve Missing Project (Immediate)

**Estimated Time:** 1-2 hours

**Tasks:**
1. Search website files for "Breath under Water" content
   ```bash
   find old/TYPO3BU/ -type f -name "*breath*" -o -name "*whale*"
   grep -r "Breath under Water" old/TYPO3BU/ | head -20
   ```

2. Cross-reference UID 982 in other database tables
   ```bash
   grep -a "982" old/usr_p51487_2.sql | grep -v "INSERT INTO \`pages\`" | head -20
   ```

3. Analyze cached HTML content (already found in `cache_pages` table)
   - Determine if content should be extracted from cache
   - Or if it exists elsewhere in database/filesystem

4. Make decision:
   - Include in migration → determine source and category
   - Exclude from migration → document reason

5. Update extraction script if necessary

### Priority 2: Complete Content Extraction (1-2 days)

**Estimated Time:** 1-2 days

**Tasks:**
1. Resolve missing project issue (see Priority 1)
2. Run full extraction (if not already done):
   ```bash
   python3 scripts/extract_typo3_projects.py
   ```
3. Convert ALL projects to Markdown:
   ```bash
   python3 scripts/convert_test_projects.py --all  # May need to modify script
   ```
4. Verify count: Should have 70-71 projects total
5. Verify build:
   ```bash
   npm run build
   ```

**Acceptance Criteria:**
- All projects from database are converted to Markdown
- All files build without errors
- All German characters display correctly
- Correct directory structure (category-based)

### Priority 3: Image Extraction and Migration (3-5 days)

**Estimated Time:** 3-5 days

**Tasks:**
1. Create image extraction script
   - Query DAM tables to get image folder contents by `startingpointdam` ID
   - For DAM gallery projects: Extract all images from DAM folder
   - For simple image field projects: Parse `image` field (comma-separated filenames)
   - Extract captions from `imagecaption` field (if using simple image field)
   - **Featured Image:** The first image in the DAM folder (or first in comma-separated list)

2. Organize images following asset strategy
   - Create directory structure: `src/assets/images/projects/{category}/{series-slug}/`
   - Copy images from old backup filesystem
   - Rename following convention: `{series-slug}-{number}.jpg`
   - Preserve original order (critical for featured image)

3. Update Markdown files with image references
   - Add `images` array to front matter
   - Add `featuredImage` field pointing to first image
   - Include src and caption for each image
   - Preserve image order from DAM folder

4. Verify image display
   - Run development server
   - Check each project's images
   - Verify featured image displays correctly
   - Fix broken paths

**Acceptance Criteria:**
- All images copied to new location
- All images renamed following convention
- Featured image correctly identified for each project
- All Markdown files updated with image arrays
- All images display correctly in development server
- No broken image links

### Priority 4: Verify Migration Integrity (1-2 days)

**Estimated Time:** 1-2 days

**Tasks:**
1. Manual review of migrated content
   - Compare new site against old TYPO3 site
   - Verify text accuracy and formatting
   - Verify image display and order
   - Verify categorization

2. Automated checks
   - Count projects per category
   - Check for missing images
   - Validate front matter format
   - Test build process

3. Document discrepancies
   - Note any intentional changes
   - List any content that couldn't be migrated
   - Document decisions made

**Acceptance Criteria:**
- All content from old site is present (or exclusions documented)
- Text formatting is correct and readable
- Images display correctly with proper captions
- Chronological and categorical order matches original
- Build succeeds without warnings or errors

### Priority 5: Epic 2 - UI Implementation (2-3 weeks)

**Estimated Time:** 2-3 weeks

**Tasks:**
1. Implement remaining UI components (carousel, news feed)
2. Polish styling to match Figma designs
3. Test interactivity and user flows
4. Performance optimization
5. Accessibility review

**Acceptance Criteria:**
- All Epic 2 stories completed
- PageSpeed score 90+
- Design matches Figma mockups
- All interactive components functional

---

## Known Issues and Risks

### Current Issues

1. **Missing Project "Breath under Water"**
   - **Impact:** Content count discrepancy (7 vs 8 paintings)
   - **Status:** Investigation required
   - **Risk:** Low (likely resolvable with database/filesystem investigation)

2. **No Images Extracted Yet**
   - **Impact:** All projects currently show placeholder for images
   - **Status:** Planned for Priority 3
   - **Risk:** Medium (requires complex mapping and file operations)

### Potential Risks

1. **Image Filename Collisions**
   - **Risk:** Multiple projects may have images with same filename
   - **Mitigation:** Asset organization strategy uses unique directories per series
   - **Status:** Design addresses this risk

2. **Content Formatting Issues**
   - **Risk:** HTML in `bodytext` may not convert cleanly to Markdown
   - **Mitigation:** `clean_html()` function strips tags and fixes entities
   - **Status:** Tested in 20-project migration, appears stable

3. **Missing Images in Filesystem**
   - **Risk:** Database may reference images that don't exist in backup
   - **Mitigation:** Verification step will identify and document missing images
   - **Status:** To be assessed during Priority 3

4. **Performance with Many Images**
   - **Risk:** ~1,500 images may impact build time or site performance
   - **Mitigation:** Static site generation, CDN deployment, lazy loading
   - **Status:** Low risk, standard for static sites

---

## Success Metrics

### Completed Metrics ✅

- ✅ Database structure fully documented
- ✅ Filesystem structure fully documented  
- ✅ Character encoding issue resolved
- ✅ 70 projects extracted with correct encoding
- ✅ Test migration of 20 projects successful
- ✅ Build succeeds without errors (55 files)

### In-Progress Metrics 🔄

- 🔄 All projects extracted: 70/71 (98%)
- 🔄 Projects converted to Markdown: 20/70 (29%)
- 🔄 Images migrated: 0/~1,500 (0%)

### Pending Metrics ⏳

- ⏳ All images linked in Markdown: 0/70 (0%)
- ⏳ Migration integrity verified: Not started
- ⏳ PageSpeed score: Not measured (target: 90+)
- ⏳ Epic 1 completion: ~35%
- ⏳ Epic 2 completion: 0%
- ⏳ Project completion: ~35%

---

## Project Timeline

### Completed Work (October - December 2025)

- **October 22:** Product brief and PRD created
- **October 23:** Epic breakdown defined
- **October 29:** 
  - Major work session
  - Character encoding issue resolved
  - 70 projects extracted
  - Test migration completed
  - Session paused for investigation

### Estimated Remaining Timeline

- **Week 1 (Now):** 
  - Resolve missing project investigation
  - Complete content extraction
  - **Deliverable:** All 70+ projects as Markdown files

- **Weeks 2-3:**
  - Image extraction and migration
  - Link images in Markdown files
  - **Deliverable:** All content with images migrated

- **Week 4:**
  - Verify migration integrity
  - Document discrepancies
  - **Deliverable:** Epic 1 complete, verified migration

- **Weeks 5-7:**
  - Epic 2: UI implementation
  - Interactive components
  - Polish and testing
  - **Deliverable:** Functional website ready for deployment

**Total Estimated Time:** 7 weeks from current point

---

## Conclusion

The TYPO3 to Eleventy migration is progressing steadily with solid technical foundations in place. The critical encoding issue has been resolved, and the extraction infrastructure is proven to work. With 70 projects successfully extracted and tested, the remaining work is primarily operational: investigating one missing project, completing the extraction, migrating images, and verifying integrity.

The approved asset organization strategy provides a clear path for the image migration phase. The Eleventy template system is well understood and ready to receive the migrated content. All documentation is current and comprehensive, making it easy to resume work at any time.

**Current Status:** Ready to resume with clear next steps  
**Blocking Issues:** 1 (missing project investigation)  
**Overall Health:** Good ✅

**Next Action:** Execute Priority 1 investigation, then proceed with full content extraction and image migration.

---

**Document End**  
For questions or to resume work, see [RESUME-WORK-HERE.md](RESUME-WORK-HERE.md)
