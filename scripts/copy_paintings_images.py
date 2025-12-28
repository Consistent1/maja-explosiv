#!/usr/bin/env python3
"""
Copy painting images to new site structure and update Markdown files
Follows asset organization strategy: src/assets/images/projects/paintings/{slug}/
"""

import json
import shutil
import re
from pathlib import Path

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[äæ]', 'ae', text)
    text = re.sub(r'[öœ]', 'oe', text)
    text = re.sub(r'[ü]', 'ue', text)
    text = re.sub(r'[ß]', 'ss', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def copy_images_for_project(painting, base_output_dir, dry_run=False):
    """Copy images for a single project to new structure"""
    
    title = painting['title']
    slug = slugify(title)
    fs_scan = painting.get('filesystem_scan', {})
    project_dirs = fs_scan.get('project_directories', [])
    related_uploads = fs_scan.get('related_uploads', [])
    
    # Create project directory
    project_dir = base_output_dir / slug
    
    results = {
        'project': title,
        'slug': slug,
        'target_dir': str(project_dir),
        'images_copied': [],
        'uploads_copied': [],
        'errors': [],
        'total_copied': 0,
        'total_size_bytes': 0
    }
    
    if not project_dirs and not related_uploads:
        results['errors'].append('No images or uploads found')
        return results
    
    if not dry_run:
        project_dir.mkdir(parents=True, exist_ok=True)
        print(f"   Created directory: {project_dir}")
    
    # Copy images from project directories
    for dir_info in project_dirs:
        source_dir = Path(dir_info['absolute_path'])
        
        if not source_dir.exists():
            results['errors'].append(f"Source directory not found: {source_dir}")
            continue
        
        # Get all images from this directory
        images = dir_info.get('images', [])
        
        for idx, img_info in enumerate(images, 1):
            source_file = source_dir / img_info['filename']
            
            if not source_file.exists():
                results['errors'].append(f"Source file not found: {source_file}")
                continue
            
            # Generate new filename with zero-padding
            ext = img_info['extension']
            # Use directory name as prefix if there are multiple source directories
            if len(project_dirs) > 1:
                dir_prefix = slugify(dir_info['directory_name'])
                new_filename = f"{dir_prefix}-{idx:03d}{ext}"
            else:
                new_filename = f"{slug}-{idx:03d}{ext}"
            
            target_file = project_dir / new_filename
            
            if not dry_run:
                try:
                    shutil.copy2(source_file, target_file)
                    results['images_copied'].append({
                        'source': str(source_file),
                        'target': str(target_file),
                        'original_name': img_info['filename'],
                        'new_name': new_filename,
                        'size_bytes': img_info['size_bytes']
                    })
                    results['total_size_bytes'] += img_info['size_bytes']
                    results['total_copied'] += 1
                except Exception as e:
                    results['errors'].append(f"Failed to copy {source_file}: {str(e)}")
            else:
                # Dry run - just record what would be copied
                results['images_copied'].append({
                    'source': str(source_file),
                    'target': str(target_file),
                    'original_name': img_info['filename'],
                    'new_name': new_filename,
                    'size_bytes': img_info['size_bytes']
                })
                results['total_size_bytes'] += img_info['size_bytes']
                results['total_copied'] += 1
    
    # Copy related uploads
    for idx, upload in enumerate(related_uploads, len(results['images_copied']) + 1):
        source_file = Path(upload['path'])
        
        if not source_file.exists():
            results['errors'].append(f"Upload file not found: {source_file}")
            continue
        
        ext = Path(upload['filename']).suffix
        new_filename = f"{slug}-upload-{idx:03d}{ext}"
        target_file = project_dir / new_filename
        
        if not dry_run:
            try:
                shutil.copy2(source_file, target_file)
                results['uploads_copied'].append({
                    'source': str(source_file),
                    'target': str(target_file),
                    'original_name': upload['filename'],
                    'new_name': new_filename,
                    'size_bytes': upload['size_bytes']
                })
                results['total_size_bytes'] += upload['size_bytes']
                results['total_copied'] += 1
            except Exception as e:
                results['errors'].append(f"Failed to copy upload {source_file}: {str(e)}")
        else:
            results['uploads_copied'].append({
                'source': str(source_file),
                'target': str(target_file),
                'original_name': upload['filename'],
                'new_name': new_filename,
                'size_bytes': upload['size_bytes']
            })
            results['total_size_bytes'] += upload['size_bytes']
            results['total_copied'] += 1
    
    return results

def format_size(bytes_val):
    """Format file size"""
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    else:
        return f"{bytes_val / (1024 * 1024):.1f} MB"

def main():
    print("🖼️  COPYING PAINTING IMAGES TO NEW SITE STRUCTURE")
    print("=" * 70)
    
    # Load comprehensive data
    data_file = Path("project_docs/paintings-comprehensive-data.json")
    print(f"\n📖 Loading data from: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        paintings = json.load(f)
    
    print(f"   Found {len(paintings)} painting projects")
    
    # Base output directory
    base_output_dir = Path("src/assets/images/projects/paintings")
    print(f"\n📁 Target directory: {base_output_dir}")
    
    # Ask for confirmation
    print("\n⚠️  This will copy images from the old site to the new structure.")
    print("   Continue? (y/n): ", end='')
    response = input().strip().lower()
    
    if response != 'y':
        print("\n❌ Cancelled by user")
        return
    
    # Copy images
    print("\n📋 Copying images...")
    print("-" * 70)
    
    all_results = []
    total_copied = 0
    total_size = 0
    total_errors = 0
    
    for idx, painting in enumerate(paintings, 1):
        title = painting['title']
        print(f"\n{idx}. {title}")
        
        results = copy_images_for_project(painting, base_output_dir, dry_run=False)
        all_results.append(results)
        
        if results['total_copied'] > 0:
            print(f"   ✓ Copied {results['total_copied']} files ({format_size(results['total_size_bytes'])})")
            total_copied += results['total_copied']
            total_size += results['total_size_bytes']
        else:
            print(f"   ⚠️  No files to copy")
        
        if results['errors']:
            print(f"   ⚠️  {len(results['errors'])} errors:")
            for error in results['errors'][:3]:  # Show first 3 errors
                print(f"      - {error}")
            total_errors += len(results['errors'])
    
    # Save results
    results_file = Path("project_docs/paintings-image-copy-results.json")
    print(f"\n💾 Saving results to: {results_file}")
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 COPY SUMMARY:")
    print(f"   Total files copied: {total_copied}")
    print(f"   Total size: {format_size(total_size)}")
    print(f"   Total errors: {total_errors}")
    print(f"\n✅ Image copy complete!")
    print(f"   Results saved to: {results_file}")

if __name__ == "__main__":
    main()
