// Collection configuration for Maja Explosiv portfolio
// This file overrides the base template collection configuration
module.exports = [
  {
    "name": "projects",
    "displayName": "Projects",
    "description": "Portfolio of artistic works",
    "showInNav": true,
    "featuredImage": "/assets/images/shared/general/projects-featured.jpg",
    "hasSubmenu": true,
    "submenuCollections": ["sculptures", "installations", "performance", "paintings"],
    "color": "#3498db"
  },
  {
    "name": "sculptures",
    "displayName": "Sculptures",
    "description": "Three-dimensional sculptural works",
    "showInNav": false, // Shown as submenu under Projects
    "featuredImage": "/assets/images/projects/sculptures/featured.jpg",
    "color": "#e74c3c"
  },
  {
    "name": "installations",
    "displayName": "Installations",
    "description": "Installation art pieces",
    "showInNav": false,
    "featuredImage": "/assets/images/projects/installations/featured.jpg",
    "color": "#9b59b6"
  },
  {
    "name": "performance",
    "displayName": "Performance",
    "description": "Performance art documentation",
    "showInNav": false,
    "featuredImage": "/assets/images/projects/performance/featured.jpg",
    "color": "#f39c12"
  },
  {
    "name": "paintings",
    "displayName": "Paintings",
    "description": "Two-dimensional painted works",
    "showInNav": false,
    "featuredImage": "/assets/images/projects/paintings/featured.jpg",
    "color": "#1abc9c"
  },
  {
    "name": "news",
    "displayName": "News",
    "description": "Latest updates and announcements",
    "showInNav": true,
    "featuredImage": "/assets/images/shared/general/news-featured.jpg",
    "color": "#2ecc71"
  }
]

