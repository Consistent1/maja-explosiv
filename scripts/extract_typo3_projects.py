#!/usr/bin/env python3
"""
TYPO3 to Eleventy Content Extractor
Extracts projects from TYPO3 database and converts to Markdown
"""

import re
import json
import html
from pathlib import Path
from datetime import datetime

# Category mapping configuration
CATEGORY_MAPPING = {
    # Page UID -> New category mapping
    877: 'sculptures',      # sculptural work
    953: 'sculptures',      # recent sculptures
    878: 'sculptures',      # collaborations (may contain installations)
    872: 'performance',     # performance
    873: 'performance',     # event organisation
    874: 'paintings',       # murals
    875: 'paintings',       # paper work
}

# Keywords to identify installations (vs sculptures)
INSTALLATION_KEYWORDS = [
    'installation', 'gate', 'fence', 'bar', 'railing', 'door',
    'helix', 'channel', 'tubebox', 'weglampen', 'path illumination',
    'fountain', 'shower', 'wreck', 'suspended', 'kinetic'
]

def extract_pages_data(sql_file):
    """Extract pages data from SQL dump"""
    print("📖 Reading SQL file...")
    # Read as UTF-8 (the SQL file contains UTF-8 encoded text despite latin1 collation)
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the INSERT INTO pages statement - get the field list first
    pages_header = re.search(r"INSERT INTO `pages` \((.*?)\) VALUES", content, re.DOTALL)
    if not pages_header:
        print("❌ Could not find pages INSERT statement")
        return []

    # Extract field names - they're in format `field1`, `field2`, etc.
    field_names = [f.strip().strip('`') for f in pages_header.group(1).split(',')]
    print(f"📋 Found {len(field_names)} fields in pages table")

    # Find indices of important fields
    uid_idx = field_names.index('uid')
    pid_idx = field_names.index('pid')
    title_idx = field_names.index('title')
    deleted_idx = field_names.index('deleted')
    hidden_idx = field_names.index('hidden')

    # Find all VALUES sections for pages table
    pages_pattern = r"INSERT INTO `pages`[^V]*VALUES\s+(.*?)(?=\nINSERT INTO|$)"
    matches = re.finditer(pages_pattern, content, re.DOTALL)

    pages = []
    for match in matches:
        values_str = match.group(1)

        # Split into individual records more carefully
        records = []
        current_record = ""
        paren_depth = 0
        in_string = False
        escape_next = False

        for i, char in enumerate(values_str):
            if escape_next:
                current_record += char
                escape_next = False
                continue

            if char == '\\':
                current_record += char
                escape_next = True
                continue

            if char == "'" and not escape_next:
                in_string = not in_string

            if not in_string:
                if char == '(':
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                    if paren_depth == 0:
                        current_record += char
                        records.append(current_record.strip())
                        current_record = ""
                        continue

            if paren_depth > 0:
                current_record += char

        # Parse each record
        for record in records:
            if not record or len(record) < 10:
                continue

            # Extract values more carefully
            values = []
            current_value = ""
            in_string = False
            escape_next = False
            paren_depth = 0

            # Remove outer parentheses
            record = record.strip()
            if record.startswith('('):
                record = record[1:]
            if record.endswith(')'):
                record = record[:-1]

            i = 0
            while i < len(record):
                char = record[i]

                if escape_next:
                    current_value += char
                    escape_next = False
                    i += 1
                    continue

                if char == '\\':
                    current_value += char
                    escape_next = True
                    i += 1
                    continue

                if char == "'":
                    if in_string:
                        # Check for escaped quote ''
                        if i + 1 < len(record) and record[i + 1] == "'":
                            current_value += "''"
                            i += 2
                            continue
                        else:
                            in_string = False
                            i += 1
                            continue
                    else:
                        in_string = True
                        i += 1
                        continue

                if not in_string and char == ',':
                    values.append(current_value.strip())
                    current_value = ""
                    i += 1
                    continue

                current_value += char
                i += 1

            # Add last value
            if current_value:
                values.append(current_value.strip())

            # Extract fields
            try:
                if len(values) <= max(uid_idx, pid_idx, title_idx, deleted_idx, hidden_idx):
                    continue

                uid = int(values[uid_idx]) if values[uid_idx].isdigit() else None
                pid = int(values[pid_idx]) if values[pid_idx].isdigit() else None
                deleted = int(values[deleted_idx]) if values[deleted_idx].isdigit() else 0
                hidden = int(values[hidden_idx]) if values[hidden_idx].isdigit() else 0

                # Title is a string value
                title = values[title_idx]
                if title.startswith("'") and title.endswith("'"):
                    title = title[1:-1]
                title = title.replace("''", "'")
                # Fix double-encoding in title
                title = fix_double_encoding(title)

                if uid and title and not deleted:
                    pages.append({
                        'uid': uid,
                        'pid': pid,
                        'title': title,
                        'hidden': hidden
                    })
            except (ValueError, IndexError) as e:
                continue

    print(f"✅ Extracted {len(pages)} pages")
    return pages

def extract_content_elements(sql_file):
    """Extract tt_content records from SQL dump"""
    print("📖 Extracting content elements...")
    # Read as UTF-8 (the SQL file contains UTF-8 encoded text despite latin1 collation)
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all INSERT INTO tt_content statements
    content_pattern = r"INSERT INTO `tt_content`.*?VALUES\s+(.*?)(?=INSERT INTO|$)"
    matches = re.finditer(content_pattern, content, re.DOTALL)
    
    elements = []
    for match in matches:
        values_str = match.group(1)
        
        # Split into individual records
        records = []
        current_record = ""
        paren_depth = 0
        
        for char in values_str:
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
                if paren_depth == 0:
                    current_record += char
                    records.append(current_record)
                    current_record = ""
                    continue
            
            if paren_depth > 0:
                current_record += char
        
        # Parse each record
        for record in records:
            try:
                # Extract key fields
                # tt_content structure: uid, pid, ..., CType, header, ..., bodytext, image, ...
                fields_match = re.findall(r"'([^']*(?:''[^']*)*)'|(\d+)|NULL|0x[0-9a-fA-F]+", record)
                
                if len(fields_match) < 20:
                    continue
                
                uid = int(fields_match[0][1]) if fields_match[0][1] else None
                pid = int(fields_match[1][1]) if fields_match[1][1] else None
                
                # Find CType (around field 14)
                ctype = None
                header = None
                bodytext = None
                image = None
                deleted = 0
                hidden = 0
                
                # Parse fields more carefully
                for i, field in enumerate(fields_match):
                    val = field[0] if field[0] else field[1]
                    
                    # CType is typically 'text', 'image', 'list', etc.
                    if i == 14 and field[0]:
                        ctype = field[0]
                    elif i == 15 and field[0]:  # header
                        header = field[0].replace("''", "'")
                        header = fix_double_encoding(header)
                    elif i == 17 and field[0]:  # bodytext
                        bodytext = field[0].replace("''", "'")
                        bodytext = fix_double_encoding(bodytext)
                    elif i == 18 and field[0]:  # image
                        image = field[0].replace("''", "'")
                    elif i == 12 and field[1]:  # hidden
                        hidden = int(field[1])
                    elif i == 26 and field[1]:  # deleted
                        deleted = int(field[1])
                
                if uid and pid and not deleted:
                    elements.append({
                        'uid': uid,
                        'pid': pid,
                        'ctype': ctype,
                        'header': header,
                        'bodytext': bodytext,
                        'image': image,
                        'hidden': hidden
                    })
            except (ValueError, IndexError) as e:
                continue
    
    print(f"✅ Extracted {len(elements)} content elements")
    return elements

def categorize_project(header, bodytext, parent_category):
    """Determine if a project is sculpture, installation, performance, or painting"""
    
    # Performance is straightforward
    if parent_category == 'performance':
        return 'performance'
    
    # Paintings are straightforward
    if parent_category == 'paintings':
        return 'paintings'
    
    # For sculptures category, need to distinguish sculptures vs installations
    if parent_category == 'sculptures':
        text = f"{header or ''} {bodytext or ''}".lower()
        
        # Check for installation keywords
        for keyword in INSTALLATION_KEYWORDS:
            if keyword in text:
                return 'installations'
        
        # Default to sculptures
        return 'sculptures'
    
    return parent_category

def fix_double_encoding(text):
    """Fix double-encoded UTF-8 text

    The SQL file contains UTF-8 text that was incorrectly interpreted as Latin-1
    and then re-encoded as UTF-8, causing double-encoding.

    Example: 'Käthe' (UTF-8: c3a4) -> interpreted as Latin-1 'Ã¤' ->
             re-encoded as UTF-8: c383c2a4 -> displays as 'KÃ¤the'

    Fix: encode as Latin-1 (reverses the second encoding) then decode as UTF-8
    """
    if not text:
        return ""

    try:
        # Reverse the double-encoding: encode as Latin-1, decode as UTF-8
        return text.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        # If fix fails, return original text
        return text

def clean_html(text):
    """Remove HTML tags and clean up text"""
    if not text:
        return ""

    # Fix double-encoding first
    text = fix_double_encoding(text)

    # Decode HTML entities
    text = html.unescape(text)

    # Remove HTML tags
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)

    # Clean up whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    text = text.strip()

    return text

def extract_year_from_text(header, bodytext):
    """Extract year from project title or description"""
    text = f"{header or ''} {bodytext or ''}"
    
    # Look for 4-digit years (1990-2024)
    years = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', text)
    
    if years:
        # Return the most recent year found
        return max(years)
    
    return None

def generate_slug(title):
    """Generate URL-friendly slug from title"""
    if not title:
        return "untitled"
    
    # Convert to lowercase
    slug = title.lower()
    
    # Remove special characters
    slug = re.sub(r'[^\w\s-]', '', slug)
    
    # Replace spaces with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug or "untitled"

def find_child_pages(pages, parent_uid):
    """Find all child pages of a given parent"""
    return [p for p in pages if p['pid'] == parent_uid and not p.get('hidden')]

def find_all_descendants(pages, parent_uid, max_depth=5):
    """Recursively find all descendant pages"""
    descendants = []

    def recurse(pid, depth=0):
        if depth >= max_depth:
            return
        children = find_child_pages(pages, pid)
        for child in children:
            descendants.append(child)
            recurse(child['uid'], depth + 1)

    recurse(parent_uid)
    return descendants

def main():
    """Main extraction process"""
    print("🚀 TYPO3 to Eleventy Content Extractor")
    print("=" * 60)

    sql_file = Path("old/usr_p51487_2.sql")
    output_dir = Path("src/posts/projects")

    if not sql_file.exists():
        print(f"❌ SQL file not found: {sql_file}")
        return

    # Extract data
    pages = extract_pages_data(sql_file)
    content_elements = extract_content_elements(sql_file)

    # Build page lookup
    page_lookup = {p['uid']: p for p in pages}

    # Group content by page
    content_by_page = {}
    for elem in content_elements:
        pid = elem['pid']
        if pid not in content_by_page:
            content_by_page[pid] = []
        content_by_page[pid].append(elem)

    # Process category pages
    projects_by_category = {
        'sculptures': [],
        'installations': [],
        'performance': [],
        'paintings': []
    }

    print("\n📊 Processing projects by category...")

    for page_uid, base_category in CATEGORY_MAPPING.items():
        page_title = page_lookup.get(page_uid, {}).get('title', f'Page {page_uid}')
        print(f"\n📄 Processing category: {page_title} (UID {page_uid})")

        # Find all descendant pages (individual projects)
        descendant_pages = find_all_descendants(pages, page_uid)
        print(f"   Found {len(descendant_pages)} child pages")

        # Process each descendant page as a potential project
        for page in descendant_pages:
            page_uid_child = page['uid']
            page_title_child = page['title']

            # Get content for this page
            if page_uid_child not in content_by_page:
                # Page with no content - might just be a container
                continue

            elements = content_by_page[page_uid_child]

            # Look for text or image content
            project_description = ""
            project_images = []

            for elem in elements:
                if elem['ctype'] in ['text', 'textpic', 'image']:
                    if elem['bodytext']:
                        project_description += clean_html(elem['bodytext']) + "\n\n"
                    if elem['image']:
                        project_images.extend(elem['image'].split(','))

            # Skip if no meaningful content
            if not project_description.strip() and not project_images:
                continue

            # Determine final category
            category = categorize_project(page_title_child, project_description, base_category)

            # Extract year
            year = extract_year_from_text(page_title_child, project_description)

            project = {
                'title': page_title_child,
                'description': project_description.strip(),
                'year': year,
                'category': category,
                'source_page': page_title,
                'source_uid': page_uid_child,
                'images': [img.strip() for img in project_images if img.strip()]
            }

            projects_by_category[category].append(project)
            print(f"  ✓ {page_title_child} → {category}" + (f" ({year})" if year else ""))

    # Summary
    print("\n" + "=" * 60)
    print("📈 EXTRACTION SUMMARY:")
    print("=" * 60)
    for cat, projects in projects_by_category.items():
        print(f"{cat.upper():15} : {len(projects):3} projects")

    total = sum(len(p) for p in projects_by_category.values())
    print(f"{'TOTAL':15} : {total:3} projects")

    # Save results to JSON for review
    output_file = Path("project_docs/extracted-projects.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(projects_by_category, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Results saved to: {output_file}")
    print("\n✅ Extraction complete!")

if __name__ == "__main__":
    main()

