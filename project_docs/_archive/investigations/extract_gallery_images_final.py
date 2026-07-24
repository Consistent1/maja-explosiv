#!/usr/bin/env python3
"""
Final solution: Extract which images belong to which DAM folders
to determine displayed images for each gallery
"""

import re
import json
from pathlib import Path

def main():
    print("🔍 Extracting DAM hierarchy (parent_id relationships)\n")
    
    with open('old/usr_p51487_2.sql', 'r', encoding='latin1') as f:
        sql = f.read()
    
    # Extract tx_dam records - column order:
    # uid, pid, tstamp, crdate, cruser_id, parent_id, deleted, active, sorting, hidden, ...file_name, file_path, ...
    # The parent_id is the 6th column (index 5)
    # file_name is the 28th column (index 27)
    # file_path is the 29th column (index 28)
    
    dam_files = {}
    
    # Find all VALUES blocks for tx_dam
    pattern = r"INSERT INTO `tx_dam`.*?VALUES\s+(.*?);"
    matches = re.findall(pattern, sql, re.DOTALL)
    
    for values_block in matches:
        # Split by records (comma-separated in parens)
        # This is tricky because values contain commas too
        # Let's use a state machine approach
        
        records = []
        depth = 0
        current_record = []
        current_value = ""
        in_string = False
        
        for char in values_block:
            if char == "'" and (not current_value or current_value[-1] != '\\'):
                in_string = not in_string
            
            if not in_string:
                if char == '(':
                    if depth == 0:
                        current_record = []
                    else:
                        current_value += char
                    depth += 1
                elif char == ')':
                    depth -= 1
                    if depth == 0:
                        if current_value:
                            current_record.append(current_value.strip())
                        records.append(current_record)
                        current_value = ""
                    else:
                        current_value += char
                elif char == ',' and depth == 1:
                    current_record.append(current_value.strip())
                    current_value = ""
                else:
                    current_value += char
            else:
                current_value += char
        
        # Parse each record
        for record in records:
            if len(record) < 30:
                continue
            
            try:
                uid = record[0]
                parent_id = record[5]
                file_name = record[27].strip("'")
                file_path = record[28].strip("'")
                
                # Store with parent_id info
                dam_files[uid] = {
                    'parent_id': parent_id,
                    'file_name': file_name,
                    'file_path': file_path,
                    'full_path': file_path + file_name if file_path else file_name
                }
            except (IndexError, ValueError):
                continue
    
    print(f"Extracted {len(dam_files)} DAM records")
    
    # Group by parent_id
    by_parent = {}
    for uid, info in dam_files.items():
        parent = info['parent_id']
        if parent not in by_parent:
            by_parent[parent] = []
        by_parent[parent].append({
            'uid': uid,
            **info
        })
    
    # Check our key gallery folders
    gallery_folders = {
        '10': 'Wohlgroth',
        '18': 'Felix und Regula',
        '12': 'Murals Europe',
        '7': 'Akwa',
        '15': 'Malaga la Vache',
    }
    
    print("\n" + "="*80)
    print("GALLERY IMAGES")
    print("="*80)
    
    results = {}
    
    for folder_id, project_name in gallery_folders.items():
        images = []
        if folder_id in by_parent:
            for item in by_parent[folder_id]:
                # Only include actual image files
                if any(ext in item['file_name'].lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    images.append(item)
        
        results[project_name] = {
            'dam_folder_id': folder_id,
            'image_count': len(images),
            'images': images
        }
        
        print(f"\n{project_name} (DAM folder {folder_id}):")
        print(f"  {len(images)} images configured in gallery")
        if images:
            print("  Images:")
            for img in images[:10]:
                print(f"    - {img['full_path']}")
            if len(images) > 10:
                print(f"    ... and {len(images) - 10} more")
    
    # Save results
    output_file = 'project_docs/gallery-images-final.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to {output_file}")

if __name__ == '__main__':
    main()
