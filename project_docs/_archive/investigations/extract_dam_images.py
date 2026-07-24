#!/usr/bin/env python3
"""
Extract DAM (Digital Asset Management) image associations
to determine which images belong to which galleries
"""

import re
import json
from pathlib import Path

def extract_dam_categories(sql_content):
    """Extract tx_dam_cat table data"""
    categories = {}
    
    # Find INSERT INTO tx_dam_cat statements
    pattern = r"INSERT INTO `tx_dam_cat`.*?VALUES\s+(.*?);"
    matches = re.findall(pattern, sql_content, re.DOTALL)
    
    for values_block in matches:
        # Parse individual records: (uid, pid, tstamp, ..., title, ...)
        records = re.findall(r"\(([^)]+)\)", values_block)
        for record in records:
            parts = [p.strip().strip("'") for p in record.split(',')]
            if len(parts) > 3:
                uid = parts[0]
                # Title is usually around index 4-6, need to find it
                # Look for non-numeric text that looks like a title
                for i, part in enumerate(parts[3:10], start=3):
                    if part and not part.isdigit() and part != '0' and len(part) > 1:
                        categories[uid] = part
                        break
    
    return categories

def extract_dam_files(sql_content):
    """Extract tx_dam table data (files)"""
    files = {}
    
    # Find INSERT INTO tx_dam statements  
    pattern = r"INSERT INTO `tx_dam`.*?VALUES\s+(.*?);"
    matches = re.findall(pattern, sql_content, re.DOTALL)
    
    for values_block in matches:
        # Parse individual records
        records = re.findall(r"\(([^)]+)\)", values_block)
        for record in records:
            # DAM records have many fields, file_path is one of them
            # Example: (uid, pid, ..., file_name, file_path, ...)
            parts = re.split(r",\s*(?='|[0-9])", record)
            uid = None
            file_path = None
            title = None
            
            for i, part in enumerate(parts):
                part = part.strip().strip("'")
                if i == 0 and part.isdigit():
                    uid = part
                # Look for file paths
                if 'fileadmin' in part or '.jpg' in part.lower() or '.png' in part.lower():
                    file_path = part
                # Look for potential titles (non-path strings)
                if part and not part.isdigit() and len(part) > 2 and 'fileadmin' not in part and '/' not in part and '.' not in part:
                    if not title:  # Take first reasonable string as title
                        title = part
            
            if uid and file_path:
                files[uid] = {
                    'path': file_path,
                    'title': title or Path(file_path).stem
                }
    
    return files

def extract_dam_mm_cat(sql_content):
    """Extract tx_dam_mm_cat table data (many-to-many relationships)"""
    associations = []
    
    # Find INSERT INTO tx_dam_mm_cat statements
    pattern = r"INSERT INTO `tx_dam_mm_cat`.*?VALUES\s+(.*?);"
    matches = re.findall(pattern, sql_content, re.DOTALL)
    
    for values_block in matches:
        # Parse individual records: (uid_local, uid_foreign, ...) where:
        # uid_local = DAM file UID
        # uid_foreign = Category UID
        records = re.findall(r"\(([^)]+)\)", values_block)
        for record in records:
            parts = [p.strip() for p in record.split(',')]
            if len(parts) >= 2:
                file_uid = parts[0]
                cat_uid = parts[1]
                associations.append({
                    'file_uid': file_uid,
                    'category_uid': cat_uid
                })
    
    return associations

def main():
    print("🔍 Extracting DAM Image Associations\n")
    
    # Read SQL file
    with open('old/usr_p51487_2.sql', 'r', encoding='latin1') as f:
        sql_content = f.read()
    
    print("Extracting DAM categories...")
    categories = extract_dam_categories(sql_content)
    print(f"  Found {len(categories)} categories")
    
    print("\nExtracting DAM files...")
    files = extract_dam_files(sql_content)
    print(f"  Found {len(files)} files")
    
    print("\nExtracting DAM category associations...")
    associations = extract_dam_mm_cat(sql_content)
    print(f"  Found {len(associations)} associations")
    
    # Build category -> files mapping
    category_files = {}
    for assoc in associations:
        cat_uid = assoc['category_uid']
        file_uid = assoc['file_uid']
        
        if cat_uid not in category_files:
            category_files[cat_uid] = []
        
        if file_uid in files:
            category_files[cat_uid].append({
                'uid': file_uid,
                **files[file_uid]
            })
    
    # Display results for key categories
    print("\n" + "="*80)
    print("CATEGORY → FILES MAPPING")
    print("="*80)
    
    # Show categories that painting projects use
    key_categories = {
        '10': 'Wohlgroth',
        '18': 'Felix und Regula',
        '12': 'Murals Europe',
        '7': 'Akwa',
        '15': 'Malaga la Vache',
    }
    
    for cat_id, project_name in key_categories.items():
        cat_name = categories.get(cat_id, 'Unknown')
        files_in_cat = category_files.get(cat_id, [])
        print(f"\nCategory {cat_id} ({cat_name}) - used by {project_name}:")
        print(f"  {len(files_in_cat)} images")
        if files_in_cat:
            print("  First 5:")
            for f in files_in_cat[:5]:
                print(f"    - {f['path']}")
    
    # Save full results
    output = {
        'categories': categories,
        'files': files,
        'associations': associations,
        'category_files': category_files
    }
    
    output_file = 'project_docs/dam-extraction-results.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Full results saved to {output_file}")

if __name__ == '__main__':
    main()
