#!/bin/bash

# TYPO3 to 11ty Migration - Database Setup Script
# This script creates a MySQL database and imports the TYPO3 SQL dump

set -e  # Exit on error

# Configuration
DB_NAME="maja_typo3"
DB_USER="root"
SQL_DUMP="old/usr_p51487_2.sql"

echo "========================================="
echo "TYPO3 Database Setup"
echo "========================================="
echo ""

# Check if SQL dump exists
if [ ! -f "$SQL_DUMP" ]; then
    echo "Error: SQL dump file not found: $SQL_DUMP"
    exit 1
fi

echo "SQL dump file found: $SQL_DUMP"
echo "Size: $(du -h $SQL_DUMP | cut -f1)"
echo ""

# Create database
echo "Creating database: $DB_NAME"
sudo mysql -u $DB_USER -e "DROP DATABASE IF EXISTS $DB_NAME;"
sudo mysql -u $DB_USER -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo "✓ Database created"
echo ""

# Import SQL dump
echo "Importing SQL dump (this may take a few minutes)..."
echo "Note: You may see warnings about character set conversion - this is expected."
sudo mysql -u $DB_USER $DB_NAME < $SQL_DUMP
echo "✓ SQL dump imported"
echo ""

# Verify import
echo "Verifying import..."
TABLE_COUNT=$(sudo mysql -u $DB_USER -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '$DB_NAME';")
echo "✓ Tables imported: $TABLE_COUNT"
echo ""

# Show some basic stats
echo "Database Statistics:"
echo "-------------------"
sudo mysql -u $DB_USER $DB_NAME <<EOF
SELECT 'Pages' as Table_Name, COUNT(*) as Row_Count FROM pages WHERE deleted = 0
UNION ALL
SELECT 'Content Elements', COUNT(*) FROM tt_content WHERE deleted = 0
UNION ALL
SELECT 'News Items', COUNT(*) FROM tt_news WHERE deleted = 0
UNION ALL
SELECT 'DAM Files', COUNT(*) FROM tx_dam WHERE deleted = 0;
EOF

echo ""
echo "========================================="
echo "Database setup complete!"
echo "========================================="
echo ""
echo "Database name: $DB_NAME"
echo "You can now query the database with:"
echo "  mysql -u $DB_USER $DB_NAME"
echo ""

