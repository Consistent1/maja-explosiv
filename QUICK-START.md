# Quick Start Guide
## TYPO3 to 11ty Migration - maja-explosiv.com

**Last Updated:** 2025-10-13

---

## 🚀 Get Started in 5 Minutes

This guide will help you set up the migration environment and begin extracting data from the TYPO3 installation.

---

## Prerequisites Check

Before starting, verify you have the required software:

```bash
# Check Node.js (need 14+)
node --version

# Check npm
npm --version

# Check MySQL (need 8.0+)
mysql --version

# Check MySQL server is running
mysqladmin ping
```

If any of these fail, install the missing software before proceeding.

---

## Step 1: Install Dependencies

### Install 11ty Project Dependencies

```bash
# From project root
npm install
```

### Install Migration Script Dependencies

```bash
# Navigate to scripts directory
cd scripts

# Install dependencies
npm install

# Return to project root
cd ..
```

---

## Step 2: Import TYPO3 Database

### Option A: Automated Import (Recommended)

```bash
cd scripts
./01-setup-database.sh
```

**What this does:**
- Creates a new MySQL database called `maja_typo3`
- Imports the 47 MB SQL dump from `old/usr_p51487_2.sql`
- Converts character encoding to UTF-8
- Shows basic statistics

**You will be prompted for:**
- MySQL root password (3 times - for create, import, and verify)

**Expected output:**
```
✓ Database created
✓ SQL dump imported
✓ Tables imported: 109
```

### Option B: Manual Import

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE maja_typo3 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Import SQL dump (this takes a few minutes)
mysql -u root -p maja_typo3 < old/usr_p51487_2.sql

# Verify import
mysql -u root -p maja_typo3 -e "SHOW TABLES;" | wc -l
# Should output: 109
```

---

## Step 3: Analyze Database

Run comprehensive database analysis:

```bash
cd scripts
npm run analyze-db > ../migration-data/database-analysis.txt
```

**You will be prompted for:**
- MySQL root password

**This creates:**
- `migration-data/database-analysis.txt` - Full database analysis report

**View the results:**

```bash
cat migration-data/database-analysis.txt
```

**What you'll see:**
- Total pages, content elements, news items
- Page hierarchy and structure
- Content types breakdown
- Media file inventory
- Navigation tree

---

## Step 4: Extract Data

Extract all data from the database to JSON files:

```bash
cd scripts
npm run extract-pages
```

**This creates files in `migration-data/`:**
- `pages.json` - All pages with metadata
- `page-tree.json` - Hierarchical page structure
- `content.json` - All content elements
- `news.json` - News/blog items
- `dam-files.json` - Media file references
- `extraction-summary.json` - Statistics (JSON)
- `extraction-summary.txt` - Statistics (human-readable)

**View the summary:**

```bash
cat migration-data/extraction-summary.txt
```

---

## Step 5: Review Extracted Data

### View Summary Statistics

```bash
cat migration-data/extraction-summary.txt
```

### Explore Page Structure

```bash
# View page tree (requires jq)
cat migration-data/page-tree.json | jq '.'

# Count total pages
cat migration-data/pages.json | jq 'length'

# View first page
cat migration-data/pages.json | jq '.[0]'
```

### Check Content Elements

```bash
# Count content elements
cat migration-data/content.json | jq 'length'

# View content types
cat migration-data/content.json | jq '.[].CType' | sort | uniq -c
```

### Review News Items

```bash
# Count news items
cat migration-data/news.json | jq 'length'

# View news titles
cat migration-data/news.json | jq '.[].title'
```

---

## What's Next?

After completing these steps, you have:

✅ **Database imported** - TYPO3 data accessible in MySQL  
✅ **Data analyzed** - Understanding of content structure  
✅ **Data extracted** - JSON files ready for transformation  

### Next Phase: Content Transformation

The next phase involves:

1. **Develop transformation scripts**
   - HTML to Markdown converter
   - Image reference resolver
   - Front matter generator

2. **Transform content**
   - Convert pages to Markdown
   - Map images to new locations
   - Generate 11ty-compatible files

3. **Migrate media**
   - Copy and organize images
   - Optimize file sizes
   - Update references

4. **Build 11ty templates**
   - Create layouts based on current design
   - Implement galleries and carousels
   - Set up navigation

5. **Test and deploy**
   - Local testing
   - Create redirects
   - Deploy to production

---

## Troubleshooting

### MySQL Connection Failed

**Error:** `Access denied for user 'root'@'localhost'`

**Solution:**
```bash
# Reset MySQL root password
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
EXIT;
```

### Script Permission Denied

**Error:** `Permission denied: ./01-setup-database.sh`

**Solution:**
```bash
chmod +x scripts/01-setup-database.sh
```

### npm install fails

**Error:** Various npm errors

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Try again
npm install
```

### Database already exists

**Error:** `Database 'maja_typo3' already exists`

**Solution:**
```bash
# Drop existing database
mysql -u root -p -e "DROP DATABASE maja_typo3;"

# Run setup script again
./01-setup-database.sh
```

---

## File Locations

### Source Files
- `old/usr_p51487_2.sql` - TYPO3 database dump (47 MB)
- `old/TYPO3BU/_/` - TYPO3 file system (~700 MB)

### Scripts
- `scripts/01-setup-database.sh` - Database import
- `scripts/02-analyze-database.sql` - Database analysis
- `scripts/03-extract-pages.js` - Data extraction

### Output
- `migration-data/` - Extracted data (created by scripts)

### Documentation
- `QUICK-START.md` - This file
- `MIGRATION-README.md` - Detailed migration guide
- `migration.md` - Migration strategy
- `discovery-report.md` - Discovery findings

---

## Quick Reference Commands

```bash
# Import database
cd scripts && ./01-setup-database.sh

# Analyze database
cd scripts && npm run analyze-db > ../migration-data/database-analysis.txt

# Extract data
cd scripts && npm run extract-pages

# View summary
cat migration-data/extraction-summary.txt

# View page tree
cat migration-data/page-tree.json | jq '.'

# Count pages
cat migration-data/pages.json | jq 'length'

# Test 11ty build
npm run build

# Start 11ty dev server
npm run serve
```

---

## Getting Help

1. **Check documentation:**
   - `MIGRATION-README.md` - Detailed guide
   - `discovery-report.md` - Analysis findings
   - `migration.md` - Strategy overview

2. **Review extracted data:**
   - `migration-data/extraction-summary.txt`
   - `migration-data/database-analysis.txt`

3. **Check logs:**
   - Script output shows detailed progress
   - MySQL errors are displayed during import

---

## Success Criteria

After completing this quick start, you should have:

- ✅ MySQL database `maja_typo3` with 109 tables
- ✅ `migration-data/` directory with JSON files
- ✅ Database analysis report
- ✅ Extraction summary showing:
  - ~50-100 pages
  - ~24 content elements
  - ~4 news items
  - DAM file references

---

**Ready to proceed?** Run the commands above and review the output!

**Questions?** Check `MIGRATION-README.md` for detailed information.

