# Maja Explosiv Website Redesign - Epic Breakdown

**Author:** Michael
**Date:** 2025-10-23
**Project Level:** 3
**Target Scale:** Comprehensive Product

---

## Overview

This document provides the detailed epic breakdown for Maja Explosiv Website Redesign, expanding on the high-level epic list in the [PRD](./PRD.md).

Each epic includes:

- Expanded goal and value proposition
- Complete story breakdown with user stories
- Acceptance criteria for each story
- Story sequencing and dependencies

**Epic Sequencing Principles:**

- Epic 1 establishes foundational infrastructure and initial functionality
- Subsequent epics build progressively, each delivering significant end-to-end value
- Stories within epics are vertically sliced and sequentially ordered
- No forward dependencies - each story builds only on previous work

---

### Epic 1: Project Foundation & Content Migration (Revised)

**Expanded Goal:** To validate the upstream template against the new design, enhance it if necessary, and then execute the full content and asset migration from the old TYPO3 site.

---

**Story 1.1: Template Gap Analysis & Enhancement**

*   **As a:** Template Maintainer
*   **I want:** To analyze the new website design against the capabilities of the upstream `explosive-11ty` template
*   **So that:** I can identify and implement any necessary structural or functional enhancements in the template to support the design's specific requirements.

**Acceptance Criteria:**
1.  A thorough review of the Figma design is completed, comparing its requirements (e.g., carousel behavior, news feed structure, asset organization) against the template's existing features.
2.  A list of required enhancements for the upstream template is created.
3.  (If necessary) The upstream `explosive-11ty` template is updated with the required enhancements.
4.  (If necessary) This project repository is synced with the latest version of the upstream template.
5.  The template is confirmed to fully support all structural and functional requirements of the new design before content migration begins.

---

**Story 1.2: Implement Site-Specific Content Structure**

*   **As a:** Developer
*   **I want:** To configure this project's content files and data models according to the design, using the conventions provided by the (now validated) upstream template
*   **So that:** The project is correctly organized and ready for the incoming migrated content.

**Acceptance Criteria:**
1.  Eleventy collections for "projects" and "news" are defined in the project's local configuration.
2.  The content directory (`src/posts`, `src/pages`) is populated with placeholder Markdown files that match the site's information architecture.
3.  Global data files (e.g., `src/_data/site.js`) are configured with site-specific information like the site title and navigation structure.
4.  The local development server correctly builds and serves the placeholder structure without errors.

---

**Story 1.3: Script and Execute Content Migration**

*   **As a:** Developer
*   **I want:** To extract all text content from the TYPO3 SQL database and convert it into Markdown files
*   **So that:** All written content from the old site is preserved and transformed into a usable format.

**Acceptance Criteria:**
1.  A script is created to parse the `.sql` database backup.
2.  The script correctly extracts all relevant page and post content.
3.  All extracted text is converted to UTF-8.
4.  A separate Markdown file is created for each piece of content.

---

**Story 1.4: Migrate Static Assets**

*   **As a:** Developer
*   **I want:** To copy all images and other static files from the TYPO3 backup into the new project
*   **So that:** All non-textual assets are available for use in the new site.

**Acceptance Criteria:**
1.  All files from the old backup are copied into the project's `assets` directory.
2.  The original file structure is maintained where possible.

---

**Story 1.5: Link Migrated Content and Assets**

*   **As a:** Developer
*   **I want:** To update the new Markdown files to correctly reference the migrated images and other pages
*   **So that:** The content is displayed with its corresponding media and internal navigation works.

**Acceptance Criteria:**
1.  Image paths in Markdown files are updated to point to their new location.
2.  Internal links between pages are updated to use Eleventy's URL structure.
3.  The site builds successfully with all content and assets correctly referenced.

---

**Story 1.6: Verify Migration Integrity**

*   **As a:** Content Manager
*   **I want:** To review the migrated content on the local development server
*   **So that:** I can confirm that all text and images are displayed correctly and in their original order.

**Acceptance Criteria:**
1.  All pages and posts from the old site are present and accessible.
2.  All text content is correctly formatted.
3.  All associated images and media are displayed correctly.
4.  The chronological and categorical order of content matches the original site.

---

### Epic 2: Desktop UI Implementation & Interactivity

**Expanded Goal:** To translate the high-fidelity Figma designs into a fully functional and styled desktop website, implementing all layouts, components, and interactive elements on top of the migrated content.

---

**Story 2.1: Implement Global Styles & Layouts**

*   **As a:** Developer
*   **I want:** To implement the core page layouts (header, footer, content wells) and global CSS styles defined in the Figma design
*   **So that:** All pages share a consistent and foundational visual structure.

**Acceptance Criteria:**
1.  The base Nunjucks layouts (`base.njk`, etc.) are updated to match the design's primary structure.
2.  Global CSS variables for colors, typography, and spacing are defined and applied.
3.  The site-wide header and footer are implemented with correct navigation links and styling.

---

**Story 2.2: Build the Homepage**

*   **As a:** Developer
*   **I want:** To build the homepage with its unique layout and content modules as specified in the Figma design
*   **So that:** It serves as an engaging and accurate entry point to the website.

**Acceptance Criteria:**
1.  The homepage layout template is created.
2.  The template correctly pulls and displays featured content (e.g., selected projects, recent news).
3.  All elements on the homepage are styled with high fidelity to the design mockups.

---

**Story 2.3: Build Project & Collection Pages**

*   **As a:** Developer
*   **I want:** To create the templates for the "Projects" overview and the individual "Collection" pages
*   **So that:** Users can browse the artist's portfolio at both a high level and a detailed level.

**Acceptance Criteria:**
1.  The "Projects" page template displays a grid or list of all available collections.
2.  The "Collection" page template displays all the individual items within a single collection.
3.  Layout, typography, and spacing for both page types match the Figma design.

---

**Story 2.4: Build the Post/Item Detail Page**

*   **As a:** Developer
*   **I want:** To build the template for displaying a single artwork or project
*   **So that:** Each piece of work can be viewed in detail with its accompanying information.

**Acceptance Criteria:**
1.  The layout for a single post/item is implemented.
2.  The template correctly displays the item's title, description, images, and other metadata.
3.  The styling is consistent with the Figma design for this view.

---

**Story 2.5: Implement Interactive Image Carousel**

*   **As a:** Developer
*   **I want:** To implement the image carousel component using DataStar as defined in the design
*   **So that:** Users can easily and intuitively browse through a series of images for a single project.

**Acceptance Criteria:**
1.  The carousel is fully functional and correctly displays a series of images from a project's data.
2.  Carousel navigation elements (e.g., next/previous buttons, thumbnails) are implemented and styled as per the design.
3.  The carousel is successfully integrated into the Post/Item Detail Page template.

---

**Story 2.6: Implement the News Feed**

*   **As a:** Developer
*   **I want:** To implement the news feed component that displays recent news items
*   **So that:** Visitors can see the latest updates and announcements from the artist.

**Acceptance Criteria:**
1.  The news feed correctly queries and displays a chronological list of news items.
2.  The layout and styling of the news feed and its individual items match the Figma design.
3.  The feed is successfully integrated into the homepage or its designated location.

---

**Story 2.7: Build Static About & Contact Pages**

*   **As a:** Developer
*   **I want:** To build the static "About" and "Contact" pages
*   **So that:** Users can access important information about the artist.

**Acceptance Criteria:**
1.  The layout and styling of the "About" page match the Figma design.
2.  The "Contact" page is styled according to the design, including a placeholder note that the form is not yet functional.

---

**Story 2.8: Final Design & UI Review**

*   **As a:** Designer
*   **I want:** To conduct a comprehensive review of the implemented desktop site against the Figma mockups
*   **So that:** I can ensure high fidelity and identify any final UI tweaks needed before launch.

**Acceptance Criteria:**
1.  Every page and interactive component is reviewed on a live development server.
2.  A list of any visual inconsistencies or bugs is created.
3.  All identified UI issues are addressed and resolved by the developer.

---

## Story Guidelines Reference

**Story Format:**

```
**Story [EPIC.N]: [Story Title]**

As a [user type],
I want [goal/desire],
So that [benefit/value].

**Acceptance Criteria:**
1. [Specific testable criterion]
2. [Another specific criterion]
3. [etc.]

**Prerequisites:** [Dependencies on previous stories, if any]
```

**Story Requirements:**

- **Vertical slices** - Complete, testable functionality delivery
- **Sequential ordering** - Logical progression within epic
- **No forward dependencies** - Only depend on previous work
- **AI-agent sized** - Completable in 2-4 hour focused session
- **Value-focused** - Integrate technical enablers into value-delivering stories

---

**For implementation:** Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown.
