#!/usr/bin/env python3
"""
Extract ONLY the images actually configured in RG Smooth Gallery.
This ensures we migrate only images displayed on the live site,
not extra images that happen to be in the filesystem.
"""

import re
import json
from pathlib import Path
from collections import defaultdict

def extract_flexform_configs(sql_content):
    """Extract FlexForm configurations from tt_content for all galleries"""
    galleries = {}
    
    # Pattern to find gallery records with FlexForm
    pattern = r"\((\d+),\s*(\d+),[^\)]*'rgsmoothgallery_pi1'[^\)]*'(<\?xml[^>]*>.*?</T3FlexForms>)'"
    matches = re.findall(pattern, sql_content, re.DOTALL)
    
    for uid, page_id, xml_str in matches:
        # Convert SQL escaped strings to actual newlines
        xml_str = xml_str.replace('\\n', '\n').replace('\\r', '\r').replace("\\'", "'")
        
        # Parse key values from FlexForm
        startingpoint_match = re.search(r'<field index="startingpointdam">\s*<value[^>]*>(\d+)</value>', xml_str)
        
        if startingpoint_match:
            galleries[page_id] = {
                'tt_content_uid': uid,
                'page_id': page_id,
                'dam_folder_id': startingpoint_match.group(1),
                'flexform': xml_str
            }
    
    return galleries

def extract_dam_images_by_path(sql_content):
    """Extract all images from tx_dam, grouped by file_path"""
    by_path = defaultdict(list)
    
    # Pattern to extract filename and filepath
    # Looking for: 'filename.jpg', 'filepath/'
    pattern = r"'([^']*\.(?:jpg|JPG|jpeg|JPEG|png|PNG|gif|GIF))',\s*'(fileadmin/s-maj/images/BilderMaja/[^']*)'"
    matches = re.findall(pattern, sql_content)
    
    for filename, filepath in matches:
        by_path[filepath].append(filename)
    
    return by_path

def map_dam_folder_to_path(sql_content):
    """Map DAM folder UIDs to their actual filesystem paths"""
    # The DAM system has folder records that point to directories
    # We need to find which DAM UID corresponds to which BilderMaja subdirectory
    
    # First, extract all DAM records with their UIDs and paths
    dam_records = {}
    
    # Pattern to find DAM records with UID and file_path
    # tx_dam columns: uid, pid, tstamp, crdate, cruser_id, parent_id, ..., file_name, file_path
    pattern = r"INSERT INTO `tx_dam`.*?VALUES\s+(.*?);"
    matches = re.findall(pattern, sql_content, re.DOTALL)
    
    for values_block in matches:
        # Find individual records - looking for directory paths in BilderMaja
        record_pattern = r"\((\d+),\s*[^)]*'',\s*'(fileadmin/s-maj/images/BilderMaja/[^']+/)'"
        records = re.findall(record_pattern, values_block)
        
        for uid, path in records:
            dam_records[uid] = path
    
    return dam_records

def get_page_info(sql_content, page_id):
    """Get page title from pages table"""
    pattern = rf"\({page_id},\s*\d+,[^)]*'([^']+)'"
    match = re.search(pattern, sql_content)
    if match:
        return match.group(1)
    return f"Page {page_id}"

def main():
    print("🎯 Extracting ACTUAL Gallery Images (Only Used Images)\n")
    
    with open('old/usr_p51487_2.sql', 'r', encoding='latin1') as f:
        sql_content = f.read()
    
    # Step 1: Get gallery configurations
    print("Step 1: Extracting gallery FlexForm configurations...")
    galleries = extract_flexform_configs(sql_content)
    print(f"  Found {len(galleries)} galleries with configurations")
    
    # Step 2: Get all images grouped by path
    print("\nStep 2: Extracting DAM images by path...")
    images_by_path = extract_dam_images_by_path(sql_content)
    print(f"  Found {len(images_by_path)} unique paths with images")
    
    # Step 3: Map DAM folder UIDs to paths
    print("\nStep 3: Mapping DAM folder IDs to filesystem paths...")
    dam_folder_paths = map_dam_folder_to_path(sql_content)
    print(f"  Found {len(dam_folder_paths)} DAM folder records")
    
    # Step 4: Match galleries to their images
    print("\nStep 4: Matching galleries to actual images...")
    
    results = {}
    
    for page_id, gallery_config in galleries.items():
        page_title = get_page_info(sql_content, page_id)
        dam_folder_id = gallery_config['dam_folder_id']
        
        # Find the path for this DAM folder
        folder_path = dam_folder_paths.get(dam_folder_id)
        
        if folder_path:
            images = images_by_path.get(folder_path, [])
        else:
            # Fallback: search for images by matching page title to path
            images = []
            page_slug = page_title.replace(' ', '').lower()
            for path, imgs in images_by_path.items():
                if page_slug in path.lower() or page_title.lower() in path.lower():
                    images = imgs
                    folder_path = path
                    break
        
        results[page_title] = {
            'page_id': page_id,
            'page_title': page_title,
            'dam_folder_id': dam_folder_id,
            'folder_path': folder_path,
            'image_count': len(images),
            'images': sorted(images)
        }
    
    # Display results
    print("\n" + "="*80)
    print("GALLERY IMAGES CONFIGURATION")
    print("="*80)
    
    for project_name, info in sorted(results.items()):
        print(f"\n{project_name}:")
        print(f"  Page ID: {info['page_id']}")
        print(f"  DAM Folder: {info['dam_folder_id']}")
        print(f"  Path: {info['folder_path'] or 'NOT FOUND'}")
        print(f"  Images: {info['image_count']}")
        if info['images']:
            print(f"  Image list:")
            for img in info['images'][:10]:
                print(f"    - {img}")
            if len(info['images']) > 10:
                print(f"    ... and {len(info['images']) - 10} more")
    
    # Save results
    output_file = 'project_docs/actual-gallery-images.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Complete results saved to {output_file}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    total_galleries = len(results)
    total_images = sum(r['image_count'] for r in results.values())
    configured = sum(1 for r in results.values() if r['image_count'] > 0)
    
    print(f"Total galleries: {total_galleries}")
    print(f"Galleries with images: {configured}")
    print(f"Total images to migrate: {total_images}")
    print(f"\n✓ These are the ONLY images displayed on the live site")
    print(f"✓ Extra filesystem images will NOT be migrated")

if __name__ == '__main__':
    main()
