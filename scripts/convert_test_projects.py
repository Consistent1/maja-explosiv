#!/usr/bin/env python3
"""
Convert selected test projects from TYPO3 to Eleventy Markdown format
"""

import json
import os
import re
from pathlib import Path

def generate_slug(title):
    """Generate URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[àáâãäå]', 'a', slug)
    slug = re.sub(r'[èéêë]', 'e', slug)
    slug = re.sub(r'[ìíîï]', 'i', slug)
    slug = re.sub(r'[òóôõö]', 'o', slug)
    slug = re.sub(r'[ùúûü]', 'u', slug)
    slug = re.sub(r'[ñ]', 'n', slug)
    slug = re.sub(r'[ç]', 'c', slug)
    slug = re.sub(r'[ß]', 'ss', slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

def clean_text(text):
    """Clean up text content"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Fix common HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    
    # Fix line breaks
    text = text.replace('\\r\\n', '\n')
    text = text.replace('\\r', '\n')
    text = text.replace('\\n', '\n')
    
    # Remove excessive whitespace
    text = re.sub(r'\n\n\n+', '\n\n', text)
    text = text.strip()
    
    return text

def create_markdown_file(project, category, output_dir):
    """Create a Markdown file for a project"""
    
    # Generate slug and filename
    slug = generate_slug(project['title'])
    filename = f"{slug}.md"
    filepath = output_dir / filename
    
    # Prepare front matter
    title = project['title']
    description = clean_text(project.get('description', ''))
    year = project.get('year', '')

    # Use current year if no year is specified
    if not year:
        year = '2000'  # Default year for projects without dates

    # Create front matter
    front_matter = f"""---
title: "{title}"
date: {year}-01-01
category: {category}
tags:
  - {category}
"""

    if project.get('year'):  # Only add year tag if it was in the original data
        front_matter += f"  - {project['year']}\n"

    front_matter += f"""layout: post.njk
---

"""
    
    # Create content
    content = front_matter
    
    if description:
        content += description + "\n\n"
    
    # Add placeholder for images
    if project.get('images'):
        content += "## Images\n\n"
        for img in project['images']:
            content += f"![{title}]({img})\n\n"
    else:
        content += "<!-- Images to be added -->\n\n"
    
    # Add metadata comment
    content += f"""
<!-- 
Source: TYPO3 page UID {project.get('source_uid', 'unknown')}
Category: {project.get('source_page', 'unknown')}
-->
"""
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def main():
    print("🚀 TYPO3 to Eleventy Test Project Converter")
    print("=" * 60)
    
    # Load extracted projects
    with open('project_docs/extracted-projects.json', 'r') as f:
        data = json.load(f)
    
    # Define selection criteria: 5 most recent from each category
    categories = {
        'sculptures': 'src/posts/projects/sculptures',
        'installations': 'src/posts/projects/installations',
        'performance': 'src/posts/projects/performance',
        'paintings': 'src/posts/projects/paintings'
    }
    
    total_converted = 0
    
    for category, output_path in categories.items():
        print(f"\n📁 Processing {category.upper()}...")
        
        # Get projects for this category
        projects = data.get(category, [])
        
        if not projects:
            print(f"  ⚠️  No projects found for {category}")
            continue
        
        # Select 5 most recent (with years) or first 5
        with_years = [p for p in projects if p.get('year')]
        without_years = [p for p in projects if not p.get('year')]
        
        selected = sorted(with_years, key=lambda x: x['year'], reverse=True)[:5]
        if len(selected) < 5:
            selected.extend(without_years[:5-len(selected)])
        
        print(f"  Selected {len(selected)} projects for conversion")
        
        # Create output directory
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert each project
        for project in selected:
            filename = create_markdown_file(project, category, output_dir)
            year_str = f"({project['year']})" if project.get('year') else "(no year)"
            print(f"    ✓ {project['title']} {year_str} → {filename}")
            total_converted += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Conversion complete! {total_converted} projects converted")
    print("\nNext steps:")
    print("  1. Review the generated Markdown files")
    print("  2. Add images to the appropriate asset directories")
    print("  3. Test the build: npm run build")
    print("  4. Review the output in the browser")

if __name__ == '__main__':
    main()

