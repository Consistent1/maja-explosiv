#!/usr/bin/env python3
"""
Analyze TYPO3 database structure to extract page hierarchy and categorization.
"""

import re
import json

def extract_pages(sql_file):
    """Extract pages from SQL dump."""
    with open(sql_file, 'r', encoding='latin-1', errors='ignore') as f:
        content = f.read()
    
    # Find INSERT INTO pages section
    pages_pattern = r"INSERT INTO `pages`[^;]+VALUES\s+(.*?);"
    match = re.search(pages_pattern, content, re.DOTALL)
    
    if not match:
        print("Could not find pages INSERT statement")
        return []
    
    values_text = match.group(1)
    
    # Parse individual rows - this is tricky with nested quotes
    # We'll use a simple approach: split by "),(" and clean up
    rows_text = values_text.strip()
    if rows_text.startswith('('):
        rows_text = rows_text[1:]
    if rows_text.endswith(')'):
        rows_text = rows_text[:-1]
    
    # Split by pattern "),\n("
    row_strings = re.split(r'\),\s*\(', rows_text)
    
    pages = []
    for row_str in row_strings:
        # Extract key fields: uid, pid, title, deleted, hidden
        # Format: uid, pid, ... (many fields) ..., title, ...
        parts = row_str.split(',', 25)  # Split first 25 fields
        
        if len(parts) < 24:
            continue
            
        try:
            uid = int(parts[0].strip())
            pid = int(parts[1].strip())
            deleted = int(parts[14].strip())
            
            # Title is field 23 (0-indexed)
            title_match = re.search(r"'([^']*)'", parts[23])
            title = title_match.group(1) if title_match else ""
            
            # Hidden is field 31
            if len(parts) > 31:
                hidden = int(parts[31].strip())
            else:
                hidden = 0
            
            if deleted == 0 and title:
                pages.append({
                    'uid': uid,
                    'pid': pid,
                    'title': title,
                    'hidden': hidden
                })
        except (ValueError, IndexError, AttributeError) as e:
            continue
    
    return pages

def build_hierarchy(pages):
    """Build page hierarchy tree."""
    # Create lookup dict
    pages_dict = {p['uid']: p for p in pages}
    
    # Add children lists
    for page in pages:
        page['children'] = []
    
    # Build tree
    root_pages = []
    for page in pages:
        if page['pid'] == 0:
            root_pages.append(page)
        elif page['pid'] in pages_dict:
            pages_dict[page['pid']]['children'].append(page)
    
    return root_pages

def print_tree(pages, indent=0):
    """Print page tree."""
    for page in pages:
        hidden_marker = " [HIDDEN]" if page['hidden'] else ""
        print(f"{'  ' * indent}{page['uid']:4} | {page['title']}{hidden_marker}")
        if page['children']:
            print_tree(page['children'], indent + 1)

def find_category_pages(pages):
    """Find pages that represent categories."""
    categories = {
        'sculptures': [],
        'installations': [],
        'performance': [],
        'paintings': []
    }
    
    for page in pages:
        title_lower = page['title'].lower()
        
        # Check for category keywords
        if 'sculptur' in title_lower:
            categories['sculptures'].append(page)
        if 'installation' in title_lower:
            categories['installations'].append(page)
        if 'performance' in title_lower or 'show' in title_lower:
            categories['performance'].append(page)
        if 'painting' in title_lower or 'mural' in title_lower:
            categories['paintings'].append(page)
    
    return categories

if __name__ == '__main__':
    print("Analyzing TYPO3 database structure...")
    print("=" * 80)
    
    # Extract pages
    pages = extract_pages('old/usr_p51487_2.sql')
    print(f"\nFound {len(pages)} active pages")
    
    # Build hierarchy
    root_pages = build_hierarchy(pages)
    print(f"Found {len(root_pages)} root pages\n")
    
    # Print tree
    print("Page Hierarchy:")
    print("-" * 80)
    print_tree(root_pages)
    
    # Find category pages
    print("\n" + "=" * 80)
    print("Category Pages:")
    print("-" * 80)
    categories = find_category_pages(pages)
    for cat_name, cat_pages in categories.items():
        print(f"\n{cat_name.upper()}:")
        for page in cat_pages:
            print(f"  UID {page['uid']:4} | {page['title']}")
            if page['children']:
                for child in page['children']:
                    print(f"    └─ UID {child['uid']:4} | {child['title']}")
    
    # Save to JSON for further processing
    with open('project_docs/typo3-page-structure.json', 'w', encoding='utf-8') as f:
        json.dump({
            'pages': pages,
            'root_pages': root_pages,
            'categories': {k: [p['uid'] for p in v] for k, v in categories.items()}
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("Page structure saved to: project_docs/typo3-page-structure.json")

