#!/usr/bin/env python3
"""
Analyze RG Smooth Gallery configurations to determine which images are actually displayed
vs which images are just in the filesystem
"""

import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

def extract_flexform_xml(sql_content, page_uid):
    """Extract FlexForm XML from tt_content for a page"""
    # Find tt_content records for this page with rgsmoothgallery
    # The pi_flexform field contains the XML directly with escaped newlines
    # Pattern: (uid, pid, ... 'rgsmoothgallery_pi1', ... '<?xml...')
    
    # Look for the pattern in INSERT INTO tt_content statements
    pattern = rf"\((\d+),\s*{page_uid},[^\)]*'rgsmoothgallery_pi1'[^\)]*'(<\?xml[^>]*>.*?</T3FlexForms>)'"
    
    matches = re.findall(pattern, sql_content, re.DOTALL)
    
    if not matches:
        return None
    
    # Get the first match (there should typically be only one gallery per page)
    uid, xml_str = matches[0]
    
    # Convert SQL escaped strings to actual newlines
    xml_str = xml_str.replace('\\n', '\n').replace('\\r', '\r').replace("\\'", "'")
    
    return xml_str

def parse_flexform(xml_str):
    """Parse FlexForm XML to extract gallery configuration"""
    if not xml_str:
        return {}
    
    try:
        root = ET.fromstring(xml_str)
        config = {}
        
        # Extract all field values
        for field in root.findall('.//field'):
            index = field.get('index')
            value_elem = field.find('value')
            if value_elem is not None and value_elem.text:
                config[index] = value_elem.text
        
        return config
    except Exception as e:
        print(f"  ⚠️  Error parsing FlexForm: {e}")
        return {}

def get_filesystem_images(project_name):
    """Get all images in filesystem for a project"""
    base_path = Path('old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja')
    
    images = []
    
    # Try different directory name patterns
    patterns = [
        project_name,
        project_name.replace(' ', ''),
        project_name.replace(' ', '_'),
        project_name.lower(),
        project_name.lower().replace(' ', ''),
    ]
    
    for pattern in patterns:
        for dir_path in base_path.glob(f'*{pattern}*'):
            if dir_path.is_dir():
                for img_file in dir_path.rglob('*'):
                    if img_file.is_file() and img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                        images.append({
                            'path': str(img_file.relative_to('old/TYPO3BU/_')),
                            'filename': img_file.name,
                            'size': img_file.stat().st_size
                        })
    
    return images

def analyze_gallery(sql_content, page_uid, page_title):
    """Analyze a specific gallery page"""
    print(f"\n{'='*80}")
    print(f"Analyzing: {page_title} (UID {page_uid})")
    print(f"{'='*80}")
    
    # Extract FlexForm
    flexform_xml = extract_flexform_xml(sql_content, page_uid)
    
    if not flexform_xml:
        print("  ❌ No FlexForm found - page may not have gallery configured")
        return {
            'uid': page_uid,
            'title': page_title,
            'has_gallery': False
        }
    
    print(f"  ✓ Found FlexForm XML ({len(flexform_xml)} chars)")
    
    # Parse configuration
    config = parse_flexform(flexform_xml)
    
    print("\n  Gallery Configuration:")
    for key, value in sorted(config.items()):
        print(f"    {key}: {value}")
    
    # Get filesystem images
    fs_images = get_filesystem_images(page_title)
    
    print(f"\n  Filesystem Images: {len(fs_images)} files found")
    if fs_images:
        print("    First 5:")
        for img in fs_images[:5]:
            print(f"      - {img['filename']}")
    
    # Determine which images are configured
    # RG Smooth Gallery typically uses DAM categories or file references
    startingpoint_dam = config.get('startingpointdam', 'not set')
    mode = config.get('mode', 'not set')
    
    result = {
        'uid': page_uid,
        'title': page_title,
        'has_gallery': True,
        'flexform_config': config,
        'filesystem_images_count': len(fs_images),
        'filesystem_images': fs_images,
        'dam_startingpoint': startingpoint_dam,
        'gallery_mode': mode
    }
    
    return result

def main():
    print("🔍 Analyzing RG Smooth Gallery Configurations\n")
    
    # Read SQL file
    with open('old/usr_p51487_2.sql', 'r', encoding='latin1') as f:
        sql_content = f.read()
    
    # Pages to analyze (painting projects that should have galleries)
    pages = [
        ('919', 'Wohlgroth'),
        ('918', 'Felix und Regula'),
        ('866', 'Murals Europe'),
        ('920', 'Graphical Work'),
        ('921', 'Akwa'),
        ('922', 'Malaga la Vache'),
        ('923', 'Concept Illustration'),
    ]
    
    results = []
    
    for uid, title in pages:
        result = analyze_gallery(sql_content, uid, title)
        results.append(result)
    
    # Save results
    output_file = 'project_docs/gallery-analysis-results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'analysis_date': '2025-12-28',
            'total_galleries': len(results),
            'galleries': results
        }, f, indent=2)
    
    print(f"\n✅ Analysis complete! Results saved to {output_file}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    for r in results:
        status = "✓ Has gallery" if r['has_gallery'] else "✗ No gallery"
        fs_count = r.get('filesystem_images_count', 0)
        dam_point = r.get('dam_startingpoint', 'unknown')
        print(f"{r['title']:20} {status:15} | FS: {fs_count:3} imgs | DAM: {dam_point}")

if __name__ == '__main__':
    main()
