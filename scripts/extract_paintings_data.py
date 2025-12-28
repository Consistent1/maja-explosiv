#!/usr/bin/env python3
"""
Comprehensive Paintings Data Extractor
Extracts ALL information for paintings projects from TYPO3 database
"""

import re
import json
from pathlib import Path

def fix_double_encoding(text):
    """Fix double-encoded UTF-8 text"""
    if not text:
        return ""
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text

def extract_paintings_pages(sql_content):
    """Extract painting project pages"""
    print("📄 Extracting painting pages...")
    
    # UIDs we're looking for (all paintings except UID 982 "Breath under Water")
    painting_uids = [866, 918, 919, 920, 921, 922, 923]
    
    paintings = {}
    
    # Find pages data - simpler regex
    for uid in painting_uids:
        # Search for the specific UID in pages table
        pattern = rf"\(({uid}),\s*(\d+),.*?'([^']*(?:''[^']*)*)'"
        match = re.search(pattern, sql_content)
        
        if match:
            page_uid = int(match.group(1))
            pid = int(match.group(2))
            title = fix_double_encoding(match.group(3).replace("''", "'"))
            
            paintings[page_uid] = {
                'uid': page_uid,
                'pid': pid,
                'title': title,
                'parent': 'murals' if pid == 874 else 'paper work',
                'content_elements': [],
                'images': [],
                'dam_references': [],
                'filesystem_images': []
            }
            print(f"  ✓ Found: {title} (UID {page_uid})")
        else:
            print(f"  ✗ Not found: UID {uid}")
    
    return paintings

def extract_tt_content(sql_content, paintings):
    """Extract content elements for paintings"""
    print("\n📝 Extracting content elements...")
    
    # Extract tt_content for each painting
    for uid in paintings.keys():
        # Look for INSERT INTO tt_content with pid matching our UID
        pattern = rf"INSERT INTO `tt_content`.*?VALUES.*?\({uid},.*?\)(?=,\s*\(|\);)"
        
        # Simpler approach: find all tt_content records
        content_pattern = r"INSERT INTO `tt_content`[^V]*VALUES\s+(.*?);"
        match = re.search(content_pattern, sql_content, re.DOTALL)
        
        if match:
            values = match.group(1)
            # Look for records with our PID
            record_pattern = rf"\((\d+),\s*{uid},.*?\)"
            
            for rec_match in re.finditer(record_pattern, values, re.DOTALL):
                paintings[uid]['content_elements'].append({
                    'raw': rec_match.group(0)[:500]  # First 500 chars for debugging
                })
    
    print(f"  Found content for {sum(1 for p in paintings.values() if p['content_elements'])} projects")
    return paintings

def scan_filesystem(paintings):
    """Scan filesystem for project images"""
    print("\n🖼️  Scanning filesystem for images...")
    
    base_path = Path("/home/miichael/Code/maja-explosiv/old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja/")
    
    if not base_path.exists():
        print("  ✗ Base path not found")
        return paintings
    
    # Map project names to UIDs (manual mapping based on known projects)
    project_dirs = {
        'murals': ['europe', 'felix', 'zurich', 'wohlgroth'],
        'paper': ['graphical', 'akwa', 'malaga', 'concept']
    }
    
    # Scan all directories
    for dir_path in base_path.iterdir():
        if dir_path.is_dir():
            dir_name = dir_path.name.lower()
            images = list(dir_path.glob("*.jpg")) + list(dir_path.glob("*.png")) + list(dir_path.glob("*.gif"))
            
            if images:
                print(f"  📁 {dir_path.name}: {len(images)} images")
                
                # Try to match to projects (this is approximate)
                for uid, project in paintings.items():
                    # Store all directory info for manual review
                    project['filesystem_images'].append({
                        'directory': str(dir_path),
                        'name': dir_path.name,
                        'image_count': len(images),
                        'images': [img.name for img in images[:10]]  # First 10 images
                    })
    
    return paintings

def main():
    sql_file = Path("/home/miichael/Code/maja-explosiv/old/usr_p51487_2.sql")
    output_file = Path("/home/miichael/Code/maja-explosiv/project_docs/paintings-data-extracted.json")
    
    print("🎨 COMPREHENSIVE PAINTINGS DATA EXTRACTION")
    print("=" * 60)
    
    # Read SQL file once
    print(f"\n📖 Reading SQL file: {sql_file.name}")
    print("   (This may take a minute...)")
    
    with open(sql_file, 'r', encoding='utf-8', errors='replace') as f:
        sql_content = f.read()
    
    print(f"   ✓ Read {len(sql_content):,} characters")
    
    # Extract data
    paintings = extract_paintings_pages(sql_content)
    paintings = extract_tt_content(sql_content, paintings)
    paintings = scan_filesystem(paintings)
    
    # Save results
    print(f"\n💾 Saving to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(paintings, f, indent=2, ensure_ascii=False)
    
    print("\n✅ EXTRACTION COMPLETE")
    print(f"   Extracted {len(paintings)} painting projects")
    print(f"   Output: {output_file}")

if __name__ == "__main__":
    main()
