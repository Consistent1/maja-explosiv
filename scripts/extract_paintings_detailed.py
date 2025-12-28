#!/usr/bin/env python3
"""
Detailed Paintings Content Extraction
Extracts complete tt_content, DAM, and filesystem data for paintings
"""

import re
import json
import os
from pathlib import Path
from collections import defaultdict

def fix_double_encoding(text):
    """Fix double-encoded UTF-8 text"""
    if not text:
        return ""
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text

# The 7 painting page UIDs (excluding 982)
PAINTING_UIDS = ['866', '918', '919', '920', '921', '922', '923']

def extract_tt_content_for_paintings(sql_file):
    """Extract ALL tt_content records for painting pages"""
    print("📝 Extracting detailed tt_content...")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    page_content = {}
    
    for uid in PAINTING_UIDS:
        print(f"  Searching for UID {uid}...")
        
        # Search for all tt_content records with pid matching this page
        # Pattern: Look for records in tt_content table
        pattern = rf"INSERT INTO `tt_content`.*?VALUES.*?(\(\d+,\s*\d+,\s*\d+,\s*\d+,\s*\d+,\s*\d+,\s*{uid},.*?\))(?=,\s*\(|\);)"
        
        matches = re.findall(pattern, content, re.DOTALL)
        
        if matches:
            page_content[uid] = {
                'record_count': len(matches),
                'raw_records': matches[:2]  # Save first 2 for inspection
            }
            print(f"    ✓ Found {len(matches)} content records")
        else:
            # Try extracting line by line from SQL dump
            lines_with_pid = []
            for line in content.split('\n'):
                if f',{uid},' in line and 'tt_content' in line:
                    lines_with_pid.append(line[:200])  # First 200 chars
            
            if lines_with_pid:
                page_content[uid] = {
                    'record_count': len(lines_with_pid),
                    'found_in_lines': lines_with_pid[:2]
                }
                print(f"    ✓ Found {len(lines_with_pid)} lines containing pid {uid}")
            else:
                page_content[uid] = {
                    'record_count': 0,
                    'status': 'NO_CONTENT_FOUND'
                }
                print(f"    ⚠ No content found")
    
    return page_content

def extract_images_and_captions(sql_file):
    """Extract image filenames and captions from tt_content"""
    print("\n🖼️  Extracting images and captions...")
    
    with open(sql_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    images_data = {}
    
    for uid in PAINTING_UIDS:
        # Look for image fields in tt_content records for this pid
        # tt_content has 'image' and 'imagecaption' fields
        
        # Search for patterns like: ,'image1.jpg,image2.jpg',
        pattern = rf",{uid},[^)]*?'([^']*\.(?:jpg|jpeg|png|gif)(?:,[^']*?\.(?:jpg|jpeg|png|gif))*)'[^)]*?'([^']*)'[^)]*?\)"
        
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        if matches:
            for image_list, caption in matches:
                if uid not in images_data:
                    images_data[uid] = []
                
                images = [img.strip() for img in image_list.split(',') if img.strip()]
                captions = [c.strip() for c in caption.split('\n') if c.strip()]
                
                images_data[uid].append({
                    'images': images,
                    'captions': captions
                })
            
            print(f"  UID {uid}: Found {len(images_data[uid])} image sets")
        else:
            images_data[uid] = []
            print(f"  UID {uid}: No images found")
    
    return images_data

def extract_dam_data(sql_file):
    """Extract DAM (Digital Asset Management) data"""
    print("\n💾 Extracting DAM data...")
    
    with open(sql_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Look for tx_dam table entries
    # This contains file metadata including sorting order
    
    dam_data = {}
    
    # Extract tx_dam INSERT statements
    dam_pattern = r"INSERT INTO `tx_dam`.*?VALUES\s+(.*?)(?=\nINSERT INTO|$)"
    matches = re.finditer(dam_pattern, content, re.DOTALL)
    
    total_dam_records = 0
    for match in matches:
        total_dam_records += len(re.findall(r'\(\d+,', match.group(1)))
    
    dam_data['total_dam_records'] = total_dam_records
    dam_data['note'] = 'DAM parsing requires field mapping - this needs detailed implementation'
    
    print(f"  ✓ Found ~{total_dam_records} DAM records in database")
    
    return dam_data

def scan_painting_project_images():
    """Scan for painting-specific project directories"""
    print("\n🎨 Scanning for painting project images...")
    
    base = Path("old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja")
    
    # Known painting-related directories (based on project names)
    painting_keywords = [
        'mural', 'facade', 'wall', 'painting', 'paint',
        'graphical', 'comic', 'illustration', 'draw', 'sketch'
    ]
    
    painting_dirs = {}
    
    if base.exists():
        for dir_path in base.iterdir():
            if dir_path.is_dir():
                dir_name_lower = dir_path.name.lower()
                
                # Check if directory might be painting-related
                is_painting = any(keyword in dir_name_lower for keyword in painting_keywords)
                
                if is_painting or True:  # Scan all for now
                    images = []
                    for ext in ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']:
                        images.extend(dir_path.glob(f'*.{ext}'))
                        # Also check subdirectories
                        images.extend(dir_path.glob(f'*/*.{ext}'))
                    
                    if images:
                        painting_dirs[dir_path.name] = {
                            'path': str(dir_path),
                            'image_count': len(images),
                            'images': sorted([img.name for img in images])
                        }
    
    print(f"  ✓ Found {len(painting_dirs)} directories with images")
    
    return painting_dirs

def map_projects_to_images():
    """Attempt to map project titles to image directories"""
    print("\n🔗 Mapping projects to image directories...")
    
    # Load the extracted projects
    with open('project_docs/extracted-projects.json', 'r') as f:
        projects = json.load(f)
    
    paintings = projects.get('paintings', [])
    
    mappings = {}
    for project in paintings:
        uid = str(project['source_uid'])
        title = project['title']
        
        # Try to find matching directory
        # Common patterns: year + title, title variations, etc.
        potential_matches = []
        
        # Check filesystem
        base = Path("old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja")
        if base.exists():
            for dir_path in base.iterdir():
                if dir_path.is_dir():
                    dir_name = dir_path.name
                    title_words = title.lower().replace('-', ' ').split()
                    
                    # Check if any title words are in directory name
                    if any(word in dir_name.lower() for word in title_words if len(word) > 3):
                        potential_matches.append(dir_name)
        
        mappings[uid] = {
            'title': title,
            'potential_image_dirs': potential_matches
        }
        
        if potential_matches:
            print(f"  UID {uid} ({title}): {len(potential_matches)} potential matches")
        else:
            print(f"  UID {uid} ({title}): No directory matches found")
    
    return mappings

def main():
    print("=" * 70)
    print("DETAILED PAINTINGS EXTRACTION")
    print("=" * 70)
    
    sql_file = "old/usr_p51487_2.sql"
    
    # Extract detailed content
    tt_content = extract_tt_content_for_paintings(sql_file)
    images_captions = extract_images_and_captions(sql_file)
    dam_data = extract_dam_data(sql_file)
    project_images = scan_painting_project_images()
    project_mappings = map_projects_to_images()
    
    # Combine all data
    detailed_data = {
        'extraction_date': '2025-12-27',
        'painting_uids': PAINTING_UIDS,
        'tt_content_records': tt_content,
        'images_and_captions': images_captions,
        'dam_data': dam_data,
        'filesystem_directories': project_images,
        'project_to_image_mappings': project_mappings
    }
    
    # Save
    output_file = "project_docs/paintings_detailed_extraction.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(detailed_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Detailed extraction saved to: {output_file}")
    print(f"\nSummary:")
    print(f"  - Painting UIDs processed: {len(PAINTING_UIDS)}")
    print(f"  - Pages with tt_content: {sum(1 for v in tt_content.values() if v['record_count'] > 0)}")
    print(f"  - Pages with images: {sum(1 for v in images_captions.values() if v)}")
    print(f"  - Filesystem directories: {len(project_images)}")

if __name__ == '__main__':
    main()
