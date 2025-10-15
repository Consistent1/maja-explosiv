# TYPO3 to 11ty Migration Guide
## maja-explosiv.com

This document provides step-by-step instructions for migrating the maja-explosiv.com website from TYPO3 4.2.14 to 11ty (Eleventy).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Database Setup](#phase-1-database-setup)
3. [Phase 2: Data Extraction](#phase-2-data-extraction)
4. [Phase 3: Content Transformation](#phase-3-content-transformation)
5. [Phase 4: Media Migration](#phase-4-media-migration)
6. [Phase 5: Testing & Deployment](#phase-5-testing--deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Node.js** 14+ (for 11ty and migration scripts)
- **MySQL** 8.0+ (for database import and querying)
- **Git** (for version control)

### Verify Installation

```bash
node --version    # Should be 14+
npm --version
mysql --version   # Should be 8.0+
```

### Install Dependencies

```bash
# Install 11ty project dependencies
npm install

# Install migration script dependencies
cd scripts
npm install
cd ..
```

---

## Phase 1: Database Setup

### Step 1.1: Import TYPO3 Database

The SQL dump is located at `old/usr_p51487_2.sql` (47 MB).

**Option A: Using the provided script (recommended)**

```bash
cd scripts
./01-setup-database.sh
```

This script will:
- Create a new database called `maja_typo3`
- Import the SQL dump
- Convert character encoding to UTF-8
- Display basic statistics

**Option B: Manual import**

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE maja_typo3 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Import SQL dump
mysql -u root -p maja_typo3 < old/usr_p51487_2.sql
```

### Step 1.2: Verify Import

```bash
# Check table count (should be 109)
mysql -u root -p maja_typo3 -e "SHOW TABLES;" | wc -l

# Check page count
mysql -u root -p maja_typo3 -e "SELECT COUNT(*) FROM pages WHERE deleted = 0;"
```

### Step 1.3: Run Database Analysis

```bash
cd scripts
npm run analyze-db
```

This will output detailed statistics about:
- Page structure and hierarchy
- Content elements by type
- News items
- Media files (DAM)
- Navigation structure

**Save the output for reference:**

```bash
npm run analyze-db > ../migration-data/database-analysis.txt
```

---

## Phase 2: Data Extraction

### Step 2.1: Extract Pages and Content

```bash
cd scripts
npm run extract-pages
```

This script extracts data from MySQL and creates JSON files in `migration-data/`:

- `pages.json` - All pages with metadata
- `page-tree.json` - Hierarchical page structure
- `content.json` - All content elements
- `news.json` - News/blog items
- `dam-files.json` - Media file references
- `extraction-summary.json` - Statistics
- `extraction-summary.txt` - Human-readable summary

### Step 2.2: Review Extracted Data

```bash
# View summary
cat migration-data/extraction-summary.txt

# View page tree structure
cat migration-data/page-tree.json | jq '.'

# Count pages
cat migration-data/pages.json | jq 'length'
```

### Step 2.3: Identify Content Patterns

Review the extracted data to understand:
- Which pages have content
- What content types are used (text, images, plugins)
- How images are referenced
- Navigation structure

---

## Phase 3: Content Transformation

### Step 3.1: Create Transformation Scripts

(To be developed in next phase)

Scripts needed:
- HTML to Markdown converter
- Image reference resolver
- URL mapper
- Front matter generator

### Step 3.2: Transform Pages to Markdown

(To be developed)

For each page:
1. Extract metadata (title, description, keywords)
2. Convert HTML content to Markdown
3. Resolve image references
4. Generate front matter
5. Save as `.md` file in appropriate directory

### Step 3.3: Handle Special Content

- **Flash animations:** Replace with static images or remove
- **Galleries:** Convert to 11ty carousel shortcodes
- **News items:** Convert to blog posts (if needed)

---

## Phase 4: Media Migration

### Step 4.1: Inventory Media Files

```bash
# Count images in fileadmin
find old/TYPO3BU/_/fileadmin -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" \) | wc -l

# Count images in uploads
find old/TYPO3BU/_/uploads -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" \) | wc -l

# Calculate total size
du -sh old/TYPO3BU/_/fileadmin
du -sh old/TYPO3BU/_/uploads
```

### Step 4.2: Organize Media Files

Create directory structure:

```
src/assets/images/
├── sculptures/
├── paintings/
├── shows/
├── recent-work/
└── general/
```

### Step 4.3: Copy and Optimize Images

(Script to be developed)

For each image:
1. Identify source location
2. Determine destination based on content
3. Optimize (resize, compress)
4. Generate responsive variants
5. Copy to destination
6. Update references in content

### Step 4.4: Handle RTE Magic Images

RTE magic images have pattern: `RTEmagicC_*.jpg` (cropped) and `RTEmagicP_*.jpg` (original)

Strategy:
1. Use original (`RTEmagicP_`) when available
2. Rename to meaningful names
3. Update content references

---

## Phase 5: Testing & Deployment

### Step 5.1: Build 11ty Site

```bash
npm run build
```

### Step 5.2: Test Locally

```bash
npm run serve
```

Visit http://localhost:8080 and verify:
- All pages load correctly
- Images display properly
- Navigation works
- Links are not broken
- Mobile responsiveness

### Step 5.3: Create Redirects

Map old TYPO3 URLs to new 11ty URLs:

```
# Example redirects (Netlify format)
/index.php?id=123  /sculptures/  301
/index.php?id=456  /paintings/   301
```

### Step 5.4: Deploy to Staging

Deploy to staging environment for review.

### Step 5.5: Final Review

- Content accuracy
- Image quality
- SEO metadata
- Performance (Lighthouse scores)
- Accessibility

### Step 5.6: Production Deployment

Deploy to production and update DNS.

---

## Current Status

### ✅ Completed

- [x] Discovery and analysis
- [x] Database import scripts created
- [x] Data extraction scripts created
- [x] File system inventory

### 🔄 In Progress

- [ ] Database import and analysis
- [ ] Data extraction execution

### ⏳ Pending

- [ ] Content transformation scripts
- [ ] Media migration scripts
- [ ] 11ty template development
- [ ] URL mapping and redirects
- [ ] Testing and deployment

---

## File Structure

```
maja-explosiv/
├── old/                          # Original TYPO3 files
│   ├── TYPO3BU/                 # TYPO3 installation
│   └── usr_p51487_2.sql         # Database dump
├── scripts/                      # Migration scripts
│   ├── 01-setup-database.sh     # Database setup
│   ├── 02-analyze-database.sql  # Database analysis queries
│   ├── 03-extract-pages.js      # Page extraction
│   └── package.json             # Script dependencies
├── migration-data/               # Extracted data (generated)
│   ├── pages.json
│   ├── content.json
│   ├── news.json
│   └── ...
├── src/                          # 11ty source files
│   ├── pages/
│   ├── collections/
│   ├── posts/
│   └── assets/
├── migration.md                  # Migration plan
├── discovery-report.md           # Discovery findings
└── MIGRATION-README.md          # This file
```

---

## Important Notes

### Character Encoding

The TYPO3 database uses `latin1_german1_ci` collation. The import script converts to UTF-8, but verify German special characters (ä, ö, ü, ß) display correctly.

### Flash Content

Flash files (.swf) are deprecated and won't work in modern browsers. Options:
1. Remove entirely
2. Replace with static images
3. Convert to HTML5/CSS animations

### Image Optimization

Original images total ~700 MB. Target reduction: 50-70% through:
- Removing duplicates
- Compression
- Resizing to appropriate dimensions
- Modern formats (WebP)

### URL Preservation

Create comprehensive redirect map to maintain SEO:
- Extract all page URLs from database
- Map to new 11ty URLs
- Implement 301 redirects

---

## Next Steps

1. **Run database import:**
   ```bash
   cd scripts
   ./01-setup-database.sh
   ```

2. **Analyze database:**
   ```bash
   npm run analyze-db > ../migration-data/database-analysis.txt
   ```

3. **Extract data:**
   ```bash
   npm run extract-pages
   ```

4. **Review extracted data:**
   ```bash
   cat migration-data/extraction-summary.txt
   ```

5. **Develop transformation scripts** (next phase)

---

## Troubleshooting

### MySQL Connection Issues

If you get "Access denied" errors:

```bash
# Reset MySQL root password
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
EXIT;
```

### Character Encoding Issues

If German characters display incorrectly:

```bash
# Check database charset
mysql -u root -p maja_typo3 -e "SHOW VARIABLES LIKE 'character_set%';"

# Should show utf8mb4 for most variables
```

### Large File Import

If SQL import times out:

```bash
# Increase MySQL timeout
mysql -u root -p -e "SET GLOBAL max_allowed_packet=1073741824;"
mysql -u root -p -e "SET GLOBAL net_read_timeout=600;"
```

---

## Support and Questions

For questions or issues during migration:
1. Check this README
2. Review discovery-report.md
3. Check migration.md for strategy
4. Consult TYPO3 and 11ty documentation

---

**Last Updated:** 2025-10-13

