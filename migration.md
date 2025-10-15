# TYPO3 to 11ty Migration Plan
## maja-explosiv.com Website Migration

**Document Version:** 1.0  
**Last Updated:** 2025-10-13  
**Status:** Planning Phase

---

## Executive Summary

This document outlines the strategy for migrating the maja-explosiv.com website from TYPO3 4.2 to an 11ty (Eleventy) static site generator. The migration will be performed incrementally, with a focus on preserving content, maintaining SEO, and improving site performance.

### Available Resources
- **Live Site:** https://www.maja-explosiv.com/
- **TYPO3 File System:** Complete directory structure from the old installation
- **MySQL Database:** Full database backup from TYPO3 installation
- **Target Platform:** 11ty v3.1.2 static site generator (already configured)

### Migration Approach
**Incremental, data-driven migration** with automated extraction and transformation scripts, followed by manual review and refinement.

---

## Phase 1: Discovery & Analysis

### 1.1 TYPO3 Database Schema Analysis

**Objective:** Understand the TYPO3 data model and identify all content-bearing tables.

**Key Tables to Investigate:**
- `pages` - Page tree structure, metadata, and hierarchy
- `tt_content` - Content elements (text, images, plugins)
- `sys_file` - File references (FAL - File Abstraction Layer)
- `sys_file_reference` - Relationships between files and content
- `sys_file_metadata` - File metadata (alt text, captions, descriptions)
- `sys_category` - Categories and taxonomies
- `sys_category_record_mm` - Category-to-record relationships
- `tt_news` or similar - News/blog extensions (if installed)
- `fe_users` / `fe_groups` - Frontend users (if applicable)
- Custom extension tables (to be identified)

**Analysis Tasks:**
1. Export database schema (table structures, relationships, indexes)
2. Document table purposes and relationships
3. Identify which tables contain content vs. configuration
4. Map foreign key relationships and dependencies
5. Analyze content volume (row counts per table)
6. Identify multilingual content (if applicable)

**Deliverable:** Database schema documentation with ER diagrams and table descriptions

---

### 1.2 TYPO3 File System Analysis

**Objective:** Map the TYPO3 directory structure and locate all content assets.

**Key Directories to Investigate:**
- `fileadmin/` - User-uploaded files, images, documents
- `typo3conf/` - Configuration files, extensions
- `typo3temp/` - Temporary files (usually not needed)
- `uploads/` - Legacy upload directory (pre-FAL)
- Extension directories - Custom templates, plugins, resources

**Analysis Tasks:**
1. Document directory structure and purposes
2. Catalog media files (images, PDFs, videos, downloads)
3. Identify template files and their locations
4. Map file organization patterns
5. Assess file naming conventions
6. Identify duplicate or unused files
7. Calculate total storage requirements

**Deliverable:** File system inventory with categorization and size analysis

---

### 1.3 Content Type Identification

**Objective:** Catalog all types of content and their characteristics.

**Expected Content Types:**
- **Pages:** Standard content pages with text, images, and media
- **News/Blog Posts:** Articles with dates, authors, categories
- **Media Galleries:** Image collections, photo albums
- **Downloads:** PDFs, documents, files
- **Navigation Menus:** Main menu, footer, breadcrumbs
- **Forms:** Contact forms, newsletter signups (if applicable)
- **Special Content:** Plugins, custom elements, embedded content

**Analysis Tasks:**
1. Identify all content types in use
2. Document content structure and fields for each type
3. Analyze content relationships (parent-child, references)
4. Identify content that uses TYPO3-specific features
5. Catalog special functionality (search, forms, dynamic content)
6. Review URL structure and routing patterns

**Deliverable:** Content type catalog with field mappings and examples

---

### 1.4 Live Site Analysis

**Objective:** Understand the current site structure, navigation, and user experience.

**Analysis Tasks:**
1. Crawl site structure and create sitemap
2. Document navigation hierarchy
3. Identify page templates and layouts
4. Catalog interactive features
5. Review SEO elements (meta tags, structured data)
6. Analyze URL patterns and redirects needed
7. Document external integrations (analytics, social media, etc.)

**Deliverable:** Site structure documentation and feature inventory

---

## Phase 2: Mapping & Strategy

### 2.1 Content Type Mapping

**Objective:** Define how TYPO3 content types map to 11ty structures.

**Mapping Strategy:**

| TYPO3 Content Type | 11ty Structure | Storage Format |
|-------------------|----------------|----------------|
| Standard Pages | `src/pages/*.md` | Markdown with front matter |
| News/Blog Posts | `src/posts/*.md` | Markdown with front matter |
| Categories | `postCollections` in front matter + `src/_data/collectionData.json` | JSON metadata |
| Media Files | `src/assets/images/` or `src/media/` | Original files (optimized) |
| Navigation | `src/_data/navigation.json` | JSON data file |
| Site Settings | `src/_data/site.json` | JSON configuration |
| File Metadata | Front matter in markdown files | YAML/JSON |

**Considerations:**
- Preserve content hierarchy and relationships
- Maintain URL structure where possible (or create redirects)
- Convert rich text content to Markdown
- Handle TYPO3-specific shortcodes and plugins
- Preserve metadata (dates, authors, categories)

---

### 2.2 Data Extraction Strategy

**Objective:** Define how data will be extracted from TYPO3.

**Extraction Methods:**

1. **Database Extraction:**
   - SQL queries to export content from MySQL
   - Export to intermediate format (JSON/CSV)
   - Handle character encoding (UTF-8)
   - Preserve relationships via foreign keys

2. **File System Extraction:**
   - Copy media files from `fileadmin/` and `uploads/`
   - Organize by content type or date
   - Rename files if needed for consistency
   - Generate file inventory with metadata

3. **Live Site Scraping (Fallback):**
   - Use for content not easily accessible via database
   - Scrape rendered HTML and convert to Markdown
   - Extract metadata from HTML meta tags
   - Useful for validating database extraction

**Tools & Technologies:**
- Node.js scripts for data processing
- SQL queries for database extraction
- HTML-to-Markdown converters (e.g., Turndown)
- Image optimization tools (Sharp, ImageMagick)

---

### 2.3 Data Transformation Strategy

**Objective:** Define how extracted data will be transformed for 11ty.

**Transformation Pipeline:**

1. **Content Transformation:**
   - Convert HTML to Markdown
   - Transform TYPO3 shortcodes to 11ty shortcodes
   - Clean up formatting and whitespace
   - Handle special characters and encoding
   - Extract and format front matter

2. **Media Transformation:**
   - Optimize images (resize, compress)
   - Generate responsive image variants
   - Update file paths and references
   - Create alt text from metadata
   - Organize into logical directory structure

3. **Metadata Transformation:**
   - Map TYPO3 fields to 11ty front matter
   - Convert dates to ISO format
   - Transform categories to collections
   - Generate slugs from titles
   - Create breadcrumb data

4. **URL Transformation:**
   - Map old URLs to new URLs
   - Generate redirect rules
   - Preserve SEO-critical URLs
   - Handle query parameters if needed

**Output Format:**
- Markdown files with YAML front matter
- JSON data files for structured content
- Organized media directory
- Redirect configuration file

---

### 2.4 Migration Execution Strategy

**Objective:** Define the order and approach for migrating content.

**Phased Migration Approach:**

**Phase A: Foundation (Week 1-2)**
- Set up migration scripts and tools
- Extract and document database schema
- Create initial content type mappings
- Test extraction on sample content

**Phase B: Static Content (Week 3-4)**
- Migrate static pages (About, Contact, etc.)
- Set up navigation structure
- Configure site metadata
- Test page rendering and layouts

**Phase C: Dynamic Content (Week 5-6)**
- Migrate blog posts/news articles
- Set up collections and categories
- Implement post listings and pagination
- Test collection filtering and navigation

**Phase D: Media & Assets (Week 7-8)**
- Migrate and optimize images
- Migrate downloadable files
- Update all content references
- Implement image galleries/carousels

**Phase E: Refinement (Week 9-10)**
- Review all migrated content
- Fix broken links and references
- Optimize SEO elements
- Set up redirects
- Performance testing

**Phase F: Launch Preparation (Week 11-12)**
- Final content review
- User acceptance testing
- Deploy to staging environment
- Create deployment plan
- Prepare rollback strategy

---

## Phase 3: Technical Considerations

### 3.1 Data Extraction Challenges

**Potential Issues:**
- **Character Encoding:** TYPO3 may use different encoding than UTF-8
- **Rich Text Formatting:** Complex HTML structures may not convert cleanly to Markdown
- **Nested Content:** TYPO3 content elements may be deeply nested
- **File References:** FAL references need to be resolved to actual file paths
- **Broken References:** Missing files or orphaned database records
- **Multilingual Content:** If site uses multiple languages, need to handle translations
- **Custom Extensions:** Third-party extensions may store data in non-standard ways

**Mitigation Strategies:**
- Test extraction on small sample first
- Implement validation and error handling
- Create manual review checklist
- Keep original data as backup
- Document edge cases and exceptions

---

### 3.2 Content Transformation Challenges

**Potential Issues:**
- **HTML to Markdown Conversion:** Loss of formatting or structure
- **TYPO3 Shortcodes:** Custom plugins and shortcodes need manual conversion
- **Embedded Media:** Videos, iframes, and embeds may need special handling
- **Tables and Complex Layouts:** May not translate well to Markdown
- **Internal Links:** Need to update to new URL structure
- **Dynamic Content:** Database-driven content needs to become static

**Mitigation Strategies:**
- Use robust HTML-to-Markdown library
- Create custom transformation rules for common patterns
- Implement 11ty shortcodes for complex elements
- Manual review of complex content
- Test rendering of all content types

---

### 3.3 SEO & URL Preservation

**Critical Considerations:**
- Maintain existing URL structure where possible
- Create 301 redirects for changed URLs
- Preserve meta titles and descriptions
- Maintain heading hierarchy
- Keep image alt text and file names
- Preserve structured data (if present)
- Maintain sitemap.xml
- Update robots.txt if needed

**Implementation:**
- Generate redirect map from old to new URLs
- Configure redirects in hosting platform (Netlify, Vercel, etc.)
- Implement canonical URLs
- Add structured data to 11ty templates
- Generate XML sitemap via 11ty plugin

---

### 3.4 Performance Optimization

**Opportunities:**
- Static site generation = faster page loads
- Image optimization and responsive images
- Minification of CSS/JS
- CDN deployment
- Lazy loading for images
- Modern image formats (WebP, AVIF)

**Implementation:**
- Use 11ty image plugin for optimization
- Implement lazy loading attributes
- Configure build-time optimization
- Set up CDN deployment
- Monitor Core Web Vitals

---

## Phase 4: Quality Assurance

### 4.1 Content Validation

**Validation Checklist:**
- [ ] All pages migrated and accessible
- [ ] All images display correctly
- [ ] All links work (internal and external)
- [ ] All downloads available
- [ ] Navigation structure correct
- [ ] Search functionality (if applicable)
- [ ] Forms work correctly (if applicable)
- [ ] Mobile responsiveness
- [ ] Cross-browser compatibility
- [ ] Accessibility compliance

---

### 4.2 SEO Validation

**SEO Checklist:**
- [ ] All URLs resolve correctly
- [ ] Redirects in place for changed URLs
- [ ] Meta titles and descriptions present
- [ ] Heading hierarchy correct
- [ ] Image alt text present
- [ ] Sitemap.xml generated
- [ ] Robots.txt configured
- [ ] Structured data implemented
- [ ] Canonical URLs set
- [ ] Social sharing meta tags

---

## Phase 5: Deployment & Launch

### 5.1 Pre-Launch Checklist

- [ ] All content migrated and validated
- [ ] Redirects configured and tested
- [ ] Analytics tracking implemented
- [ ] Performance benchmarks met
- [ ] Security headers configured
- [ ] SSL certificate ready
- [ ] DNS records prepared
- [ ] Backup of old site created
- [ ] Rollback plan documented

---

### 5.2 Launch Strategy

**Recommended Approach:**
1. Deploy to staging environment
2. Final content review and testing
3. Set up DNS with low TTL
4. Deploy to production
5. Update DNS to point to new site
6. Monitor for issues
7. Keep old site accessible for rollback

---

## Next Steps

1. **Review this migration plan** and identify any gaps or concerns
2. **Access TYPO3 resources** (database backup, file system)
3. **Perform Phase 1 discovery** to gather detailed information
4. **Refine the plan** based on actual TYPO3 structure and content
5. **Create detailed task breakdown** for implementation
6. **Develop migration scripts** for data extraction and transformation
7. **Execute migration** in phases with continuous validation

---

## Open Questions & Decisions Needed

1. **Database Access:** How will we access the MySQL database? (Direct connection, SQL dump file, etc.)
2. **File System Access:** Where are the TYPO3 files located? (Local, remote server, archive)
3. **URL Structure:** Should we preserve the exact TYPO3 URL structure or optimize it?
4. **Content Priority:** Which content is most critical to migrate first?
5. **Timeline:** What is the target launch date?
6. **Hosting:** Where will the 11ty site be hosted? (Netlify, Vercel, GitHub Pages, etc.)
7. **Redirects:** How will redirects be implemented? (Server config, hosting platform, etc.)
8. **Forms:** How should contact forms be handled? (Third-party service, serverless functions, etc.)
9. **Search:** Does the site need search functionality? (Client-side, third-party service)
10. **Analytics:** What analytics platform should be integrated?

---

## Resources & References

### TYPO3 Documentation
- TYPO3 4.2 Database Schema Reference
- TYPO3 File Abstraction Layer (FAL) Documentation
- TYPO3 Content Element Types

### 11ty Documentation
- [11ty Official Documentation](https://www.11ty.dev/docs/)
- [11ty Data Files](https://www.11ty.dev/docs/data/)
- [11ty Collections](https://www.11ty.dev/docs/collections/)
- [11ty Plugins](https://www.11ty.dev/docs/plugins/)

### Migration Tools
- Node.js for scripting
- Turndown (HTML to Markdown)
- Sharp (Image optimization)
- MySQL client libraries
- CSV/JSON processing libraries

---

**End of Migration Plan v1.0**

