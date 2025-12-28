#!/usr/bin/env python3
"""
Enhance paintings data with comprehensive filesystem and database information
Uses the already-extracted paintings data and adds all missing details
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def scan_project_directory(project_dir):
    """Scan a project directory and return comprehensive file information"""
    if not project_dir.exists():
        return None
    
    files_info = {
        'directory_name': project_dir.name,
        'absolute_path': str(project_dir),
        'images': [],
        'total_count': 0,
        'by_extension': defaultdict(int)
    }
    
    # Scan all image files
    for ext in ['*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.PNG', '*.gif', '*.GIF']:
        for img_file in project_dir.glob(ext):
            stat = img_file.stat()
            files_info['images'].append({
                'filename': img_file.name,
                'size_bytes': stat.st_size,
                'size_kb': round(stat.st_size / 1024, 2),
                'extension': img_file.suffix.lower()
            })
            files_info['by_extension'][img_file.suffix.lower()] += 1
    
    files_info['total_count'] = len(files_info['images'])
    files_info['by_extension'] = dict(files_info['by_extension'])
    
    # Sort images by filename
    files_info['images'].sort(key=lambda x: x['filename'])
    
    return files_info

def search_dam_references(sql_content, project_uid):
    """Search for DAM references for a project"""
    dam_refs = []
    
    # Search for rgsmoothgallery or other gallery plugins referencing this page
    pattern = rf"pid.*?{project_uid}.*?rgsmoothgallery"
    if re.search(pattern, sql_content, re.IGNORECASE):
        dam_refs.append({'type': 'rgsmoothgallery', 'found': True})
    
    return dam_refs

def extract_images_from_content(content_text):
    """Extract image references from content"""
    images = []
    
    # Look for image field values (comma-separated)
    img_pattern = r"image.*?'([^']*\.(?:jpg|png|gif))'"
    matches = re.findall(img_pattern, content_text, re.IGNORECASE)
    
    for match in matches:
        # Split comma-separated values
        for img in match.split(','):
            img = img.strip()
            if img:
                images.append(img)
    
    return images

def main():
    print("🎨 ENHANCING PAINTINGS DATA WITH COMPREHENSIVE INFORMATION")
    print("=" * 70)
    
    # Load already extracted paintings data
    extracted_file = Path("project_docs/extracted-projects.json")
    print(f"\n📖 Loading extracted data: {extracted_file}")
    
    with open(extracted_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    paintings = all_data.get('paintings', [])
    print(f"   Found {len(paintings)} painting projects")
    
    # Load SQL for additional searches
    sql_file = Path("old/usr_p51487_2.sql")
    print(f"\n📖 Loading SQL file for additional data...")
    with open(sql_file, 'r', encoding='utf-8', errors='replace') as f:
        sql_content = f.read()
    print(f"   ✓ Loaded {len(sql_content):,} characters")
    
    # Base paths for filesystem scanning
    base_img_path = Path("old/TYPO3BU/_/fileadmin/s-maj/images/BilderMaja")
    uploads_path = Path("old/TYPO3BU/_/uploads")
    
    # Enhanced paintings data
    enhanced_paintings = []
    
    print("\n🔍 Processing each painting project...")
    print("-" * 70)
    
    for idx, painting in enumerate(paintings, 1):
        title = painting.get('title', 'Unknown')
        uid = painting.get('source_uid')
        year = painting.get('year')
        
        print(f"\n{idx}. {title} (UID: {uid}, Year: {year or 'OMITTED'})")
        
        enhanced = {
            **painting,  # Copy all existing data
            'filesystem_scan': {
                'project_directories': [],
                'related_uploads': [],
                'total_images_found': 0
            },
            'dam_references': [],
            'database_images': painting.get('images', []),
            'metadata': {
                'extraction_date': '2025-12-27',
                'extraction_method': 'enhanced_comprehensive',
                'status': 'COMPLETE' if painting.get('images') else 'PARTIAL'
            }
        }
        
        # Search filesystem for related directories
        print(f"   📁 Scanning filesystem...")
        
        # Search by year and keywords from title
        search_terms = []
        if year:
            search_terms.append(year)
        
        # Add title keywords
        title_keywords = title.lower().split()
        search_terms.extend([kw for kw in title_keywords if len(kw) > 3])
        
        found_dirs = []
        for search_dir in base_img_path.iterdir():
            if search_dir.is_dir():
                dir_lower = search_dir.name.lower()
                # Check if any search term matches
                for term in search_terms:
                    if term.lower() in dir_lower:
                        dir_info = scan_project_directory(search_dir)
                        if dir_info and dir_info['total_count'] > 0:
                            found_dirs.append(dir_info)
                            print(f"      ✓ {search_dir.name}: {dir_info['total_count']} images")
                        break
        
        enhanced['filesystem_scan']['project_directories'] = found_dirs
        enhanced['filesystem_scan']['total_images_found'] = sum(d['total_count'] for d in found_dirs)
        
        # Search uploads directory for related files
        print(f"   📤 Scanning uploads directory...")
        upload_files = []
        for ext in ['*.jpg', '*.png', '*.gif']:
            for upload_file in uploads_path.glob(ext):
                # Check if filename contains project keywords
                file_lower = upload_file.name.lower()
                for term in search_terms:
                    if term.lower() in file_lower:
                        stat = upload_file.stat()
                        upload_files.append({
                            'filename': upload_file.name,
                            'size_bytes': stat.st_size,
                            'path': str(upload_file)
                        })
                        break
        
        if upload_files:
            print(f"      ✓ Found {len(upload_files)} files in uploads/")
        enhanced['filesystem_scan']['related_uploads'] = upload_files
        
        # Search for DAM references
        print(f"   🗄️  Searching for DAM references...")
        dam_refs = search_dam_references(sql_content, uid)
        if dam_refs:
            print(f"      ✓ Found {len(dam_refs)} DAM references")
        enhanced['dam_references'] = dam_refs
        
        enhanced_paintings.append(enhanced)
    
    # Save enhanced data
    output_file = Path("project_docs/paintings-comprehensive-data.json")
    print(f"\n💾 Saving comprehensive data to: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_paintings, f, indent=2, ensure_ascii=False)
    
    print("\n📊 SUMMARY:")
    print("=" * 70)
    print(f"Total painting projects processed: {len(enhanced_paintings)}")
    print(f"Projects with filesystem images: {sum(1 for p in enhanced_paintings if p['filesystem_scan']['total_images_found'] > 0)}")
    print(f"Total images found: {sum(p['filesystem_scan']['total_images_found'] for p in enhanced_paintings)}")
    print(f"\n✅ Enhancement complete!")
    print(f"   Output: {output_file}")

if __name__ == "__main__":
    main()
