// Collection configuration for Maja Explosiv portfolio
// This file overrides the base template collection configuration
//
// featuredImage is intentionally EMPTY (2026-08-26). The six paths that were here
// pointed at files that have never existed in this repo -- per-category fallbacks
// (projects/<cat>/featured.jpg) and shared/general/{news,projects}-featured.jpg.
// The templates guard with `{% if collectionData.featuredImage %}`, so an empty
// string renders nothing rather than a broken image. Fill these in once Stages 6-11
// have migrated real project images.
module.exports = [
  {
    "name": "projects",
    "displayName": "Projects",
    "description": "Portfolio of artistic works",
    "showInNav": true,
    "featuredImage": "",
    "hasSubmenu": true,
    "submenuCollections": ["sculptures", "installations", "performance", "paintings"],
    "color": "#3498db"
  },
  {
    "name": "sculptures",
    "displayName": "Sculptures",
    "description": "Three-dimensional sculptural works",
    "showInNav": false, // Shown as submenu under Projects
    "featuredImage": "",
    "color": "#e74c3c"
  },
  {
    "name": "installations",
    "displayName": "Installations",
    "description": "Installation art pieces",
    "showInNav": false,
    "featuredImage": "",
    "color": "#9b59b6"
  },
  {
    "name": "performance",
    "displayName": "Performance",
    "description": "Performance art documentation",
    "showInNav": false,
    "featuredImage": "",
    "color": "#f39c12"
  },
  {
    "name": "paintings",
    "displayName": "Paintings",
    "description": "Two-dimensional painted works",
    "showInNav": false,
    "featuredImage": "",
    "color": "#1abc9c"
  },
  {
    "name": "news",
    "displayName": "News",
    "description": "Latest updates and announcements",
    "showInNav": true,
    "featuredImage": "",
    "color": "#2ecc71"
  }
]

