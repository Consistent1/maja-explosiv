// Custom theme configuration for Maja Explosiv website
// Overrides the default theme settings from src/_data/theme.js
// 
// Font Stack Strategy:
// - Primary (Geist): Clean, modern sans-serif for headings and primary text
// - Secondary (Rethink Sans): Versatile sans-serif for body text and secondary elements
// - Buttons (Inter): Reserved exclusively for CTA buttons per design specification
//
// See homepage.png in project_docs/design_screenshots for design reference

module.exports = {
  "colors": {
    "primary": "#333",
    "accent": "tomato",
    "background": "#C8C8C8",
    "text": "#000000",
    "text-light": "#666",
    "border": "#ddd"
  },
  "fonts": {
    // Primary font for body text - Geist with Rethink Sans fallback
    "body": "'Geist', 'Rethink Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    // Heading font - Geist with Rethink Sans fallback
    "heading": "'Geist', 'Rethink Sans', sans-serif",
    // Button font - Inter (reserved for CTA buttons only)
    "button": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
  },
  "paths": {
    "header": "header.njk",
    "footer": "footer.njk"
  }
}
