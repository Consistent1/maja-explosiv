#!/usr/bin/env python3
"""
Comprehensive Paintings Extraction Script
Extracts ALL information for painting projects from TYPO3 database and filesystem
"""

import re
import json
import html as html_module
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

def clean_html(text):
    """Remove HTML tags and decode entities"""
    if not text:
        return ""
    # Fix encoding first
    text = fix_double_encoding(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html_module.unescape(text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    return text.strip()

def extract_painting_pages(sql_content):
    """Extract painting page records"""
    print("📖 Extracting painting pages...")
    
    # Find pages table structure
    pages_header = re.search(r"INSERT INTO `pages` \((.*?)\) VALUES", sql_content, re.DOTALL)
    if not pages_header:
        return []
    
    field_names = [f.strip().strip('`') for f in pages_header.group(1).split(',')]
    
    # Get field indices
    uid_idx = field_names.index('uid')
    pid_idx = field_names.index('pid')
    title_idx = field_names.index('title')
    deleted_idx = field_names.index('deleted')
    hidden_idx = field_names.index('hidden')
    sorting_idx = field_names.index('sorting')
    crdate_idx = field_names.index('crdate') if 'crdate' in field_names else None
    tstamp_idx = field_names.index('tstamp') if 'tstamp' in field_names else None
    
    # Find all pages with pid 874 (murals) or 875 (paper work)
    pages_pattern = r"INSERT INTO `pages`.*?VALUES\s+(.*?)(?=\nINSERT INTO|$)"
    
    painting_pages = []
    for match in re.finditer(pages_pattern, sql_content, re.DOTALL):
        values_str = match.group(1)
        
        # Parse records
        records = []
        current = ""
        depth = 0
        in_string = False
        escape = False
        
        for char in values_str:
            if escape:
                current += char
                escape = False
                continue
            if char == '\\':
                current += char
                escape = True
                continue
            if char == "'" and not escape:
                in_string = not in_string
            if not in_string:
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                    if depth == 0:
                        current += char
                        records.append(current.strip())
                        current = ""
                        continue
            if depth > 0:
                current += char
        
        for record in records:
            # Extract fields using regex
            fields = re.findall(r"'([^']*(?:''[^']*)*)'|(\d+)|NULL", record)
            
            if len(fields) < len(field_names):
                continue
            
            uid = fields[uid_idx][1] if fields[uid_idx][1] else None
            pid = fields[pid_idx][1] if fields[pid_idx][1] else None
            
            # Only process murals (874) and paper work (875)
            if pid not in ['874', '875']:
                continue
            
            # Skip UID 982 (Breath under Water)
            if uid == '982':
                continue
            
            title = fields[title_idx][0] if fields[title_idx][0] else ''
            deleted = fields[deleted_idx][1] if fields[deleted_idx][1] else '0'
            hidden = fields[hidden_idx][1] if fields[hidden_idx][1] else '0'
            sorting = fields[sorting_idx][1] if fields[sorting_idx][1] else '0'
            
            if deleted != '0' or hidden != '0':
                continue
            
            page_data = {
                'uid': uid,
                'pid': pid,
                'title': fix_double_encoding(title),
                'category': 'murals' if pid == '874' else 'paper work',
                'deleted': deleted,
                'hidden': hidden,
                'sorting': sorting,
                'crdate': fields[crdate_idx][1] if crdate_idx and fields[crdate_idx][1] else 'OMITTED',
                'tstamp': fields[tstamp_idx][1] if tstamp_idx and fields[tstamp_idx][1] else 'OMITTED',
            }
            
            painting_pages.append(page_data)
    
    print(f"  ✓ Found {len(painting_pages)} painting pages")
    return painting_pages

def extract_content_elements(sql_content, page_uids):
    """Extract tt_content elements for painting pages"""
    print("📝 Extracting content elements...")
    
    # Find tt_content table structure
    content_header = re.search(r"INSERT INTO `tt_content` \((.*?)\) VALUES", sql_content, re.DOTALL)
    if not content_header:
        return {}
    
    field_names = [f.strip().strip('`') for f in content_header.group(1).split(',')]
    
    # Get field indices
    uid_idx = field_names.index('uid')
    pid_idx = field_names.index('pid')
    header_idx = field_names.index('header') if 'header' in field_names else None
    bodytext_idx = field_names.index('bodytext') if 'bodytext' in field_names else None
    image_idx = field_names.index('image') if 'image' in field_names else None
    imagecaption_idx = field_names.index('imagecaption') if 'imagecaption' in field_names else None
    CType_idx = field_names.index('CType') if 'CType' in field_names else None
    list_type_idx = field_names.index('list_type') if 'list_type' in field_names else None
    pi_flexform_idx = field_names.index('pi_flexform') if 'pi_flexform' in field_names else None
    deleted_idx = field_names.index('deleted')
    hidden_idx = field_names.index('hidden')
    
    content_pattern = r"INSERT INTO `tt_content`.*?VALUES\s+(.*?)(?=\nINSERT INTO|$)"
    
    page_contents = defaultdict(list)
    
    for match in re.finditer(content_pattern, sql_content, re.DOTALL):
        values_str = match.group(1)
        
        # Parse records (simplified for now)
        # This is complex due to potential binary data in pi_flexform
        # We'll extract what we can
        
        for page_uid in page_uids:
            # Search for records with this pid
            pattern = rf"\((\d+),\s*0,\s*0,\s*0,\s*0,\s*0,\s*{page_uid},"
            if re.search(pattern, values_str):
                # Found content for this page
                # For now, mark as found
                page_contents[page_uid].append({
                    'found': True,
                    'note': 'Content exists but complex parsing needed'
                })
    
    print(f"  ✓ Found content for {len(page_contents)} pages")
    return dict(page_contents)

def scan_filesystem_images(base_path):
    """Scan filesystem for project images"""
    print("🖼️  Scanning filesystem for images...")
    
    image_dir = Path(base_path) / "old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja"
    uploads_dir = Path(base_path) / "old/TYPO3BU/_/uploads"
    
    projects_images = {}
    
    if image_dir.exists():
        for project_dir in image_dir.iterdir():
            if project_dir.is_dir():
                images = []
                for ext in ['*.jpg', '*.JPG', '*.jpeg', '*.png', '*.gif', '*.GIF']:
                    images.extend(list(project_dir.glob(ext)))
                
                if images:
                    projects_images[project_dir.name] = {
                        'directory': str(project_dir),
                        'image_count': len(images),
                        'images': [img.name for img in sorted(images)]
                    }
    
    print(f"  ✓ Found {len(projects_images)} project directories with images")
    return projects_images

def main():
    """Main extraction function"""
    print("=" * 70)
    print("COMPREHENSIVE PAINTINGS EXTRACTION")
    print("=" * 70)
    
    base_path = Path.cwd()
    sql_file = base_path / "old/usr_p51487_2.sql"
    
    # Read SQL file
    print("\n📖 Reading SQL file...")
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    print("  ✓ SQL file loaded")
    
    # Extract painting pages
    painting_pages = extract_painting_pages(sql_content)
    
    # Extract page UIDs
    page_uids = [p['uid'] for p in painting_pages]
    
    # Extract content elements
    page_contents = extract_content_elements(sql_content, page_uids)
    
    # Scan filesystem
    filesystem_images = scan_filesystem_images(base_path)
    
    # Combine data
    comprehensive_data = {
        'extraction_date': '2025-12-27',
        'total_paintings': len(painting_pages),
        'pages': painting_pages,
        'content_elements': page_contents,
        'filesystem_images': filesystem_images,
        'notes': [
            'UID 982 (Breath under Water) excluded per instructions',
            'Complex tt_content parsing requires more detailed extraction',
            'DAM table extraction needed for complete metadata',
            'FlexForm XML parsing needed for gallery settings'
        ]
    }
    
    # Save comprehensive data
    output_file = base_path / "project_docs/paintings_comprehensive_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(comprehensive_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Comprehensive data saved to: {output_file}")
    print(f"\nSummary:")
    print(f"  - Painting pages: {len(painting_pages)}")
    print(f"  - Pages with content: {len(page_contents)}")
    print(f"  - Project directories with images: {len(filesystem_images)}")
    
    # Display page details
    print(f"\n📋 Painting Pages:")
    for page in painting_pages:
        print(f"  UID {page['uid']}: {page['title']} ({page['category']}) - sorting {page['sorting']}")

if __name__ == '__main__':
    main()
