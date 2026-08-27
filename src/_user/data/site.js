// Site-specific configuration for Maja Explosiv
// This file overrides the base template configuration
module.exports = {
  "title": "Maja Explosiv",
  "description": "Portfolio website for artist Maja Thommen",
  "url": "https://consistent1.github.io/maja-explosiv/",
  "tagline": "Contemporary Artist",
  "author": "Maja Thommen",
  "language": "en",
  "locale": "en_US",
  // Site logo path. Use an SVG so the browser receives the correct MIME type.
  // Replace this with your final logo when ready.
  "logo": "/assets/images/shared/site/logo.svg",
  "enableSearch": false, // Deferred to Phase 2
  "showNewsletter": false, // Not applicable for artist portfolio
  "socialLinks": [
    // To be populated with actual social media links
  ],
  "customNavLinks": [
    {
      "title": "Projects",
      "url": "/#projects"
    },
    {
      "title": "About",
      "url": "/#about"
    },
    {
      "title": "Contact",
      "url": "/contact/"
    }
  ],
  "footerLinks": [],
  "footerBottomLinks": [],
  "contactInfo": {
    // Corrected 2026-08-27 from the migrated source (tt_content 1311, pid 973) and
    // confirmed against the live site. The previous values were placeholders:
    // email was "info@maja-explosiv.com" and phone was empty.
    "email": "m-e@maja-explosiv.com",
    "phone": "0049 (0)30 505 970 27",
    "address": "" // no postal address is published in the source
  },
  "copyrightText": "© 2024 Maja Thommen. All rights reserved."
}

