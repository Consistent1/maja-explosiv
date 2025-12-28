#!/usr/bin/env python3
"""
Generate comprehensive Markdown files for painting projects
Includes ALL extracted information with proper structure
"""

import json
from pathlib import Path
import re

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

def format_size(bytes_val):
    """Format file size in human-readable format"""
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    else:
        return f"{bytes_val / (1024 * 1024):.1f} MB"

def generate_markdown(painting, output_dir):
    """Generate comprehensive Markdown file for a painting project"""
    
    title = painting['title']
    slug = slugify(title)
    year = painting.get('year') or 'OMITTED'
    description = painting.get('description', 'OMITTED')
    source_uid = painting.get('source_uid', 'OMITTED')
    source_page = painting.get('source_page', 'OMITTED')
    category = painting.get('category', 'paintings')
    
    # Filesystem data
    fs_scan = painting.get('filesystem_scan', {})
    project_dirs = fs_scan.get('project_directories', [])
    related_uploads = fs_scan.get('related_uploads', [])
    total_images = fs_scan.get('total_images_found', 0)
    
    # Build front matter
    front_matter = f"""---
title: "{title}"
date: {year + '-01-01' if year != 'OMITTED' else '2000-01-01'}
year: {year}
category: {category}
tags:
  - {category}
"""
    
    if year != 'OMITTED':
        front_matter += f"  - {year}\n"
    
    front_matter += f"""layout: post.njk
source_uid: {source_uid}
source_page: {source_page}
migration_status: comprehensive_extraction
extraction_date: 2025-12-27
"""
    
    # Add filesystem information if available
    if project_dirs:
        front_matter += f"filesystem_images_count: {total_images}\n"
        front_matter += "filesystem_directories:\n"
        for dir_info in project_dirs:
            front_matter += f"  - name: {dir_info['directory_name']}\n"
            front_matter += f"    path: {dir_info['absolute_path']}\n"
            front_matter += f"    image_count: {dir_info['total_count']}\n"
    
    front_matter += "---\n"
    
    # Build content
    content = []
    
    # Description
    if description != 'OMITTED':
        content.append(description)
        content.append("")
    
    # Filesystem images section
    if project_dirs:
        content.append("## Images Found in Filesystem")
        content.append("")
        content.append(f"**Total images found:** {total_images}")
        content.append("")
        
        for dir_info in project_dirs:
            content.append(f"### Directory: `{dir_info['directory_name']}`")
            content.append("")
            content.append(f"**Location:** `{dir_info['absolute_path']}`  ")
            content.append(f"**Total images:** {dir_info['total_count']}")
            content.append("")
            
            if dir_info.get('by_extension'):
                content.append("**Image types:**")
                for ext, count in dir_info['by_extension'].items():
                    content.append(f"- {ext}: {count} files")
                content.append("")
            
            if dir_info['images']:
                content.append("<details>")
                content.append(f"<summary>View all {dir_info['total_count']} images</summary>")
                content.append("")
                content.append("| Filename | Size |")
                content.append("|----------|------|")
                
                for img in dir_info['images']:
                    content.append(f"| `{img['filename']}` | {format_size(img['size_bytes'])} |")
                
                content.append("")
                content.append("</details>")
                content.append("")
    else:
        content.append("## Images")
        content.append("")
        content.append("**Status:** OMITTED - No images found in filesystem scan")
        content.append("")
    
    # Related uploads
    if related_uploads:
        content.append("## Related Files in Uploads Directory")
        content.append("")
        content.append(f"**Total files:** {len(related_uploads)}")
        content.append("")
        content.append("| Filename | Size | Location |")
        content.append("|----------|------|----------|")
        
        for upload in related_uploads:
            content.append(f"| `{upload['filename']}` | {format_size(upload['size_bytes'])} | `{upload['path']}` |")
        
        content.append("")
    
    # Database images (if any)
    db_images = painting.get('database_images', [])
    if db_images:
        content.append("## Database Image References")
        content.append("")
        for img in db_images:
            content.append(f"- `{img}`")
        content.append("")
    else:
        content.append("## Database Image References")
        content.append("")
        content.append("**Status:** OMITTED - No image references found in database")
        content.append("")
    
    # DAM references
    dam_refs = painting.get('dam_references', [])
    if dam_refs:
        content.append("## Digital Asset Management (DAM) References")
        content.append("")
        for ref in dam_refs:
            content.append(f"- Type: `{ref.get('type', 'unknown')}`")
        content.append("")
    else:
        content.append("## Digital Asset Management (DAM) References")
        content.append("")
        content.append("**Status:** OMITTED - No DAM references found")
        content.append("")
    
    # Migration notes
    content.append("---")
    content.append("")
    content.append("## Migration Notes")
    content.append("")
    content.append("**Extraction Method:** Comprehensive filesystem and database scan  ")
    content.append("**Extraction Date:** 2025-12-27  ")
    content.append(f"**Source TYPO3 UID:** {source_uid}  ")
    content.append(f"**Source Category:** {source_page}  ")
    content.append(f"**Migration Status:** {painting.get('metadata', {}).get('status', 'UNKNOWN')}")
    content.append("")
    content.append("**Data Completeness:**")
    content.append(f"- Title: {'✓' if title else '✗'}")
    content.append(f"- Description: {'✓' if description != 'OMITTED' else '✗ OMITTED'}")
    content.append(f"- Year: {'✓' if year != 'OMITTED' else '✗ OMITTED'}")
    content.append(f"- Filesystem Images: {'✓ ' + str(total_images) + ' found' if total_images > 0 else '✗ OMITTED'}")
    content.append(f"- Database Images: {'✓' if db_images else '✗ OMITTED'}")
    content.append(f"- DAM References: {'✓' if dam_refs else '✗ OMITTED'}")
    content.append("")
    
    # Combine everything
    full_content = front_matter + "\n" + "\n".join(content)
    
    # Write file
    output_file = output_dir / f"{slug}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    return output_file

def main():
    print("📝 GENERATING COMPREHENSIVE PAINTING MARKDOWN FILES")
    print("=" * 70)
    
    # Load comprehensive data
    data_file = Path("project_docs/paintings-comprehensive-data.json")
    print(f"\n📖 Loading data from: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        paintings = json.load(f)
    
    print(f"   Found {len(paintings)} painting projects")
    
    # Output directory
    output_dir = Path("src/posts/projects/paintings")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Output directory: {output_dir}")
    
    # Generate markdown files
    print("\n✍️  Generating Markdown files...")
    print("-" * 70)
    
    generated_files = []
    for idx, painting in enumerate(paintings, 1):
        title = painting['title']
        output_file = generate_markdown(painting, output_dir)
        generated_files.append(output_file)
        
        fs_count = painting.get('filesystem_scan', {}).get('total_images_found', 0)
        print(f"{idx}. {title}")
        print(f"   → {output_file.name}")
        print(f"   Images: {fs_count if fs_count > 0 else 'OMITTED'}")
    
    print("\n" + "=" * 70)
    print(f"✅ Generated {len(generated_files)} comprehensive Markdown files")
    print(f"\nFiles created in: {output_dir}")
    for f in generated_files:
        print(f"  - {f.name}")

if __name__ == "__main__":
    main()
