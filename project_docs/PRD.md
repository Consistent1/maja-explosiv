# Maja Explosiv Website Redesign Product Requirements Document (PRD)

**Author:** Michael
**Date:** 2025-10-23
**Project Level:** 3
**Target Scale:** Comprehensive Product

---

## Goals and Background Context

### Goals

*   Ensure business continuity by replacing the outdated and insecure TYPO3 platform.
*   Deliver a modern, performant, and secure portfolio website.
*   Empower the artist to manage content independently through a Git-based workflow.
*   Successfully migrate 100% of the existing content, preserving its original order and integrity.
*   Achieve a Google PageSpeed score of 90+ for the deployed site.

### Background Context

The artist Maja Thommen's current portfolio website, built on TYPO3, is no longer supported by the hosting provider due to significant security vulnerabilities and lack of maintenance. This poses a direct threat to her online presence and business continuity. The platform's outdated architecture also makes content updates cumbersome and does not align with modern web performance or design standards.

The proposed solution is to migrate the site to a new static platform using Eleventy (11ty). This will create a highly performant, secure, and future-proof website that effectively showcases the artist's work. By moving to a Git-based workflow for content management, the artist will be empowered to make updates independently, reducing reliance on technical support and ensuring the site can evolve with her career.

---

## Requirements

### Functional Requirements

*   FR001: The system must migrate all existing content from the TYPO3 database.
*   FR002: The system must migrate all existing files (images, documents) from the TYPO3 file backup.
*   FR003: All text content must be converted to UTF-8 encoding during migration.
*   FR004: The system must display all migrated content in the correct, original order as seen on the live site.
*   FR005: The system must implement the desktop UI design with high fidelity to the provided Figma mockups.
*   FR006: The system must provide a functional image carousel for showcasing series of works.
*   FR007: The system must provide a functional news feed.
*   FR008: The system must allow the artist to add new content via a Git-based workflow.
*   FR009: The system must allow the artist to edit existing content via a Git-based workflow.
*   FR010: The system must allow the artist to delete content via a Git-based workflow.
*   FR011: The system architecture must support the future implementation of URL redirects from the old site.
*   FR012: The system must generate all pages as static HTML files.
*   FR013: The system must use the Eleventy (11ty) static site generator.
*   FR014: The system must use the DataStar library for interactive components.

### Non-Functional Requirements

*   NFR001: The website must achieve a Google PageSpeed score of 90 or higher.
*   NFR002: The website must be secure against common web vulnerabilities.
*   NFR003: The website must be maintainable, with a clear separation between the core template and site-specific implementation.
*   NFR004: The website must adhere to modern accessibility standards (WCAG).
*   NFR005: The Git-based content management workflow must be simple enough for a non-technical user to manage.

---

## User Journeys

#### Journey 1: Gallery Curator Explores and Inquires About Work

*   **Persona:** A curator at a contemporary art gallery looking for new artists to feature.
*   **Goal:** To evaluate the artist's work and inquire about a specific series for an upcoming exhibition.

**Steps:**

1.  **Discovery:** The curator discovers Maja's website through a link in an art-focused newsletter.
2.  **First Impression:** The curator lands on the homepage and is met with a clean, professional design that showcases a featured piece.
3.  **Exploration:** The curator navigates to the "Projects" section to see the breadth of the artist's portfolio. They filter or browse to a specific collection that catches their eye.
4.  **Deep Dive:** The curator clicks into a series and uses the image carousel to view all the pieces within it, reading the accompanying descriptions for each.
5.  **Inquiry:** Impressed by the work, the curator navigates to the "About" page to learn more about the artist's background and then looks for a way to get in touch.
6.  **Action:** The curator finds the artist's contact information (or a note indicating the contact form is coming soon) and sends an email to inquire about the availability of the series they viewed.

#### Journey 2: The Artist Adds a New Project to the Portfolio

*   **Persona:** Maja Thommen, the artist.
*   **Goal:** To upload a new series of work, including images and a description, to her website.

**Steps:**

1.  **Preparation:** The artist prepares the images for her new series, ensuring they are in a web-friendly format, and writes a description for the project.
2.  **Access:** The artist opens her local project folder, which is a clone of the website's Git repository.
3.  **Content Creation:** She creates a new Markdown file in the `src/posts/` directory for her new project.
4.  **Adding Metadata:** In the Markdown file, she adds the necessary front matter, including the title, date, description, and specifies which collection the new work belongs to.
5.  **Adding Content:** She adds the images to the correct folder and references them within the Markdown file, perhaps configuring a new carousel.
6.  **Preview:** The artist runs the local development server (`npm run serve`) to preview her changes on her own computer, ensuring everything looks correct.
7.  **Build:** The artist runs the build command (`npm run build`) to ensure the site builds without errors.
8.  **Deployment:** Satisfied with the build, she uses a Git client to commit her changes and push them to the main branch of the repository.
9.  **Verification:** The automated deployment process builds the new version of the site. The artist visits the live website to see her new project beautifully displayed.

---

## UX and UI Vision

#### UX Principles
*   **Clarity and Focus:** The design must prioritize showcasing the artwork without distraction, ensuring the user's attention is on the content.
*   **Modern & Professional:** The aesthetic should be clean, contemporary, and reflect the high quality of the artist's work.
*   **Intuitive Navigation:** Users should be able to easily find their way around the site and discover new content with a minimal number of clicks.
*   **Performant:** The site must load quickly to provide a seamless and engaging experience.

#### Platform & Screens
*   **Platform:** Desktop-first web application.
*   **Core Screens / Views:**
    *   Homepage (featuring selected works)
    *   Projects (an overview of all collections/categories)
    *   Collection Page (a gallery of items within a single collection)
    *   Post/Item Detail Page (a view of a single artwork or project)
    *   About Page
    *   Contact Page

#### Design Constraints
*   The implementation must adhere with high fidelity to the provided Figma design mockups.
*   The styling must be built upon the existing foundation of Open Props and `normalize.css`.
*   The design must be achievable within the technical capabilities of the Eleventy and DataStar stack.

---

## Epic List

*   **Epic 1: Project Foundation & Content Migration**
    *   **Goal:** Establish the core Eleventy project structure, migrate 100% of the content and files from the old TYPO3 backup, and ensure all data is correctly structured and accessible.
    *   **Estimated Stories:** 5-8

*   **Epic 2: Desktop UI Implementation & Interactivity**
    *   **Goal:** Implement the full desktop UI from the Figma designs, including all layouts, styling, and interactive components like image carousels and news feeds, ensuring a high-fidelity match to the mockups.
    *   **Estimated Stories:** 7-10

> **Note:** Detailed epic breakdown with full story specifications is available in [epics.md](./epics.md)

---

## Out of Scope

*   **Responsive / Mobile Design:** The initial launch will be focused exclusively on the desktop experience.
*   **Contact Form Implementation:** A functional contact form will be added in a later phase.
*   **Image Optimization Pipeline:** Automated compression and generation of next-gen image formats (e.g., WebP/AVIF) is deferred.
*   **URL Redirects:** The architecture will be prepared for redirects, but the actual implementation of the redirect rules is out of scope.
*   **User-Facing Search:** A site search feature is not part of the MVP.
*   **Automated Sitemap:** An XML sitemap for search engines will be considered in a future update.
*   **UI Animations:** Any subtle or complex animations are deferred to focus on core functionality.
