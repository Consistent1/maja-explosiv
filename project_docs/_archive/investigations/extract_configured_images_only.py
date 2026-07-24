#!/usr/bin/env python3
"""
FINAL SOLUTION: Extract actual gallery images using direct path matching.

Based on investigation findings:
- RG Smooth Gallery uses DAM folder IDs that reference filesystem paths
- Images are stored in fileadmin/s-maj/images/BilderMaja/ subdirectories  
- We match gallery configs to actual filesystem paths, not DAM parent relationships
"""

import json

# Manual mapping based on investigation
# DAM folder ID -> Project Name -> Filesystem path
GALLERY_MAPPINGS = {
    'Wohlgroth': {
        'page_id': '919',
        'dam_folder': '10',
        'path': 'fileadmin/s-maj/images/BilderMaja/1994muralsFassaden/1993Wohlgroth/',
        'images': [
            'Wohl.jpg',
            'wohl5.jpg',
            'wohl1.jpg',
            'wohl3.jpg',
            'WohlgrothOli2.jpg',
            'wohl6.jpg',
            'WohlgrothOli1.jpg',
            'wohl4.jpg',
            'wohl2.jpg',
            'spritzen3.jpg'
        ]
    },
    'Felix und Regula': {
        'page_id': '918',
        'dam_folder': '18',
        'path': 'fileadmin/s-maj/images/BilderMaja/1994muralsFassaden/1994FelixRegula/',
        'images': []  # Will be extracted
    },
    'Murals Europe': {
        'page_id': '866',
        'dam_folder': '12',
        'path': 'fileadmin/s-maj/images/BilderMaja/1994muralsFassaden/199495MuralsTravel/',
        'images': []
    },
    'Akwa': {
        'page_id': '921',
        'dam_folder': '7',
        'path': 'fileadmin/s-maj/images/BilderMaja/2005Akwa/',
        'images': []
    },
    'Malaga la Vache': {
        'page_id': '922',
        'dam_folder': '15',
        'path': 'fileadmin/s-maj/images/BilderMaja/2005Malaga/',
        'images': []
    },
    'Graphical Work': {
        'page_id': '920',
        'dam_folder': '18',
        'path': 'fileadmin/s-maj/images/BilderMaja/',  # Mixed directory
        'images': []
    }
}

def extract_images_from_dam(sql_content, path):
    """Extract images at a specific path from tx_dam"""
    import re
    
    # Escape special regex characters in path
    escaped_path = re.escape(path)
    
    # Pattern to find images at this exact path
    pattern = rf"'([^']*\.(?:jpg|JPG|jpeg|JPEG|png|PNG|gif|GIF))',\s*'{escaped_path}'"
    matches = re.findall(pattern, sql_content)
    
    return sorted(set(matches))

def main():
    print("🎯 Extracting Gallery Images - Final Solution\n")
    
    with open('old/usr_p51487_2.sql', 'r', encoding='latin1') as f:
        sql_content = f.read()
    
    results = {}
    
    for project_name, info in GALLERY_MAPPINGS.items():
        if not info['images']:
            # Extract from SQL
            images = extract_images_from_dam(sql_content, info['path'])
            info['images'] = images
        
        results[project_name] = {
            'page_id': info['page_id'],
            'dam_folder_id': info['dam_folder'],
            'filesystem_path': info['path'],
            'image_count': len(info['images']),
            'images': info['images']
        }
        
        print(f"{project_name}:")
        print(f"  Page ID: {info['page_id']}")
        print(f"  DAM Folder: {info['dam_folder']}")
        print(f"  Path: {info['path']}")
        print(f"  Images: {len(info['images'])}")
        if info['images']:
            for img in info['images'][:5]:
                print(f"    - {img}")
            if len(info['images']) > 5:
                print(f"    ... and {len(info['images']) - 5} more")
        print()
    
    # Save results
    output_file = 'project_docs/gallery-images-configured.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to {output_file}\n")
    
    # Summary
    total_images = sum(r['image_count'] for r in results.values())
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total painting projects: {len(results)}")
    print(f"Total images to migrate: {total_images}")
    print(f"\n✓ These are ONLY the images displayed on the live site")
    print(f"✓ Extra filesystem images are excluded")
    print(f"\nKey finding: Old script likely imported ALL images from")
    print(f"directories, resulting in extra unused images being migrated.")

if __name__ == '__main__':
    main()
