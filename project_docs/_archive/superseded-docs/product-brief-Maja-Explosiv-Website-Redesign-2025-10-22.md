# Maja Explosiv Website Redesign Product Brief

**Author:** Michael
**Date:** 2025-10-22
**Project Level:** 3
**Target Scale:** Comprehensive Product

---

## Executive Summary

This document outlines the product brief for the redesign of the Maja Explosiv website. The project is a necessary migration from an outdated and insecure TYPO3 platform to a modern, performant, and maintainable static website built with Eleventy (11ty). The primary goals are to ensure business continuity, improve security and performance, and empower the artist to manage content independently through a Git-based workflow. The initial launch (MVP) will focus on a desktop-first implementation of the new design with complete content migration, deferring responsive layouts and other optimizations to a later phase.

---

## 1. Problem Statement

The artist Maja Thommen requires a new portfolio website to replace her outdated TYPO3 site, which is no longer supported by the hosting provider due to security concerns. The current site is difficult to maintain and does not align with modern web standards. The core problem is the need for a secure, performant, and future-proof platform that effectively showcases the artist's work and can be updated.

---

## 2. Proposed Solution

The proposed solution is to build a new static portfolio website for the artist using the Eleventy (11ty) framework and the DataStar library for interactivity. This approach will provide a highly performant, secure, and maintainable solution with minimal to no hosting costs. Content will be managed via a simple Git-based workflow, allowing the artist to update the site independently. The architecture will be decoupled, with a core upstream template and a site-specific implementation, ensuring long-term maintainability.

---

## 3. Target Audience

*   **Primary Audience:** Potential clients, gallery curators, event organizers, and press who are interested in viewing, purchasing, or commissioning work from the artist.
*   **Secondary Audience:** The general public, students, and other artists interested in Maja Thommen's work and career.
*   **Content Manager:** Maja Thommen, the artist, who will manage the website's content via a Git-based workflow.

---

## 4. Project Goals & Success Metrics

*   **Primary Business Goal:** Rapidly develop and deploy the new website to ensure business continuity and mitigate security risks from the old platform.
*   **Primary Content Goal:** Successfully migrate 100% of the content from the old TYPO3 database and files, ensuring all posts and items are displayed in the correct, original order.
*   **Primary Design Goal:** Implement the user interface with high fidelity, accurately matching the provided Figma design mockups for the desktop view.
*   **Primary Technical Goal:** Achieve a Google PageSpeed score of 90 or higher for the deployed static site.

---

## 5. MVP Scope

### Core Features (Must-Haves)
1.  Full implementation of the new desktop design from Figma.
2.  Complete migration of all content from the old TYPO3 site.
3.  Conversion of all text content from its original encoding to UTF-8.
4.  All site sections, including interactive elements like carousels and news feeds, must be fully functional.
5.  The architecture must be structured to allow for implementing URL redirects from the old site in a future phase.

### Out of Scope (for this MVP)
1.  Implementation of the contact form.
2.  Automated image compression and optimization.
3.  The actual implementation of URL redirects.
4.  Responsive/mobile design implementation.

---

## 6. Post-MVP Vision (Phase 2 and Beyond)

*   **Immediate Follow-up:**
    *   Implementation of the responsive (mobile-friendly) design.
    *   Integration of a functional contact form.
    *   Implementation of an image compression and optimization pipeline.
    *   Configuration of redirects from old site URLs to preserve SEO value.
*   **Future Enhancements:**
    *   A user-facing search feature.
    *   An automatically generated sitemap.
    *   Addition of subtle, performant animations to enhance the user experience.

---

## 7. Technical Considerations

*   **Frameworks:** Eleventy (11ty) with DataStar for interactivity.
*   **Styling:** Foundation built on Open Props and `normalize.css`.
*   **Deployment:** Git-based automated deployment.
*   **Content Source:** Migration from a TYPO3 `.sql` database and file backup, with text converted to UTF-8. The live website at `https://www.maja-explosiv.com/` will serve as a critical reference to correlate database content, file structure, and the actual presentation and ordering of elements (e.g., images in carousels, news feeds) on the original site.
*   **Accessibility:** The site must adhere to modern accessibility standards (e.g., WCAG).
*   **Browser Support:** Target modern, evergreen browsers, ensuring graceful degradation on older mobile browsers.
*   **Images:** Use standard formats like JPG, with a preference for using the 11ty Image plugin to generate modern, optimized formats (like WebP/AVIF).

---

## 8. Risks & Open Questions

### Key Risks
1.  **Technical Risk:** The data migration from the TYPO3 backup could be significantly more complex than assumed.
2.  **Adoption Risk:** The artist may find the new Git-based content management workflow difficult or cumbersome.
3.  **Implementation Risk:** The new design may require features that the underlying 11ty template does not support, forcing major refactoring of the upstream template.

### Open Questions
1.  What is the definitive strategy for image optimization?
2.  Which hosting provider will be used for the final deployment?