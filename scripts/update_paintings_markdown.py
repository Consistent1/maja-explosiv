#!/usr/bin/env python3
"""
Update painting Markdown files with actual copied image references
Replaces filesystem scan data with actual image arrays for the site
"""

import json
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

def update_markdown_with_images(painting, copy_results, markdown_dir):
    """Update a painting's Markdown file with actual copied images"""
    
    title = painting['title']
    slug = slugify(title)
    markdown_file = markdown_dir / f"{slug}.md"
    
    if not markdown_file.exists():
        print(f"   ⚠️  Markdown file not found: {markdown_file}")
        return False
    
    # Find the copy results for this project
    project_results = None
    for result in copy_results:
        if result['slug'] == slug:
            project_results = result
            break
    
    if not project_results:
        print(f"   ⚠️  No copy results found for {title}")
        return False
    
    # Read current markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract front matter and body
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        print(f"   ⚠️  Invalid markdown format")
        return False
    
    front_matter = parts[1]
    body = parts[2]
    
    # Build image array for front matter
    images_copied = project_results.get('images_copied', []) + project_results.get('uploads_copied', [])
    
    if not images_copied:
        # No images - add empty array
        if 'images:' not in front_matter:
            front_matter += "images: []\n"
    else:
        # Remove old filesystem_images_count and filesystem_directories
        front_matter = re.sub(r'filesystem_images_count:.*\n', '', front_matter)
        front_matter = re.sub(r'filesystem_directories:.*?(?=\n[a-z_]+:|$)', '', front_matter, flags=re.DOTALL)
        
        # Add images array
        if 'images:' in front_matter:
            # Replace existing images array
            images_yaml = "images:\n"
            for img in images_copied:
                img_path = f"/assets/images/projects/paintings/{slug}/{img['new_name']}"
                images_yaml += f"  - src: {img_path}\n"
                images_yaml += f"    original: {img['original_name']}\n"
                images_yaml += f"    size: {img['size_bytes']}\n"
            
            front_matter = re.sub(r'images:.*?(?=\n[a-z_]+:|$)', images_yaml.rstrip(), front_matter, flags=re.DOTALL)
        else:
            # Add new images array
            images_yaml = "images:\n"
            for img in images_copied:
                img_path = f"/assets/images/projects/paintings/{slug}/{img['new_name']}"
                images_yaml += f"  - src: {img_path}\n"
                images_yaml += f"    original: {img['original_name']}\n"
                images_yaml += f"    size: {img['size_bytes']}\n"
            
            front_matter += images_yaml
    
    # Update body - replace Images section
    if images_copied:
        new_images_section = f"""## Images

This project includes {len(images_copied)} images copied from the old site.

**Total size:** {format_size(project_results['total_size_bytes'])}

<details>
<summary>View all {len(images_copied)} images</summary>

| New Filename | Original Filename | Size |
|--------------|-------------------|------|
"""
        for img in images_copied:
            new_images_section += f"| `{img['new_name']}` | `{img['original_name']}` | {format_size(img['size_bytes'])} |\n"
        
        new_images_section += "\n</details>\n"
        
        # Replace the Images Found in Filesystem section
        body = re.sub(
            r'## Images Found in Filesystem.*?(?=\n## |$)',
            new_images_section,
            body,
            flags=re.DOTALL
        )
        
        # Also replace any standalone "## Images" section
        body = re.sub(
            r'## Images\n\n\*\*Status:\*\* OMITTED.*?(?=\n## |$)',
            new_images_section,
            body,
            flags=re.DOTALL
        )
    
    # Reassemble markdown
    new_content = f"---\n{front_matter}---\n{body}"
    
    # Write updated markdown
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def format_size(bytes_val):
    """Format file size"""
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    else:
        return f"{bytes_val / (1024 * 1024):.1f} MB"

def main():
    print("📝 UPDATING PAINTING MARKDOWN FILES WITH IMAGE REFERENCES")
    print("=" * 70)
    
    # Load comprehensive data
    data_file = Path("project_docs/paintings-comprehensive-data.json")
    print(f"\n📖 Loading painting data from: {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        paintings = json.load(f)
    
    print(f"   Found {len(paintings)} painting projects")
    
    # Load copy results
    results_file = Path("project_docs/paintings-image-copy-results.json")
    print(f"\n📖 Loading copy results from: {results_file}")
    
    with open(results_file, 'r', encoding='utf-8') as f:
        copy_results = json.load(f)
    
    print(f"   Found results for {len(copy_results)} projects")
    
    # Markdown directory
    markdown_dir = Path("src/posts/projects/paintings")
    print(f"\n📁 Markdown directory: {markdown_dir}")
    
    # Update each markdown file
    print("\n✏️  Updating Markdown files...")
    print("-" * 70)
    
    updated = 0
    failed = 0
    
    for idx, painting in enumerate(paintings, 1):
        title = painting['title']
        print(f"\n{idx}. {title}")
        
        if update_markdown_with_images(painting, copy_results, markdown_dir):
            print(f"   ✓ Updated")
            updated += 1
        else:
            print(f"   ✗ Failed")
            failed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 UPDATE SUMMARY:")
    print(f"   Files updated: {updated}")
    print(f"   Files failed: {failed}")
    print(f"\n✅ Markdown update complete!")

if __name__ == "__main__":
    main()
