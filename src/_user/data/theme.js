
// src/_user/data/theme.js
module.exports = {
  "colors": {
    /* Tokens matched to Figma Main Page CSS (Onepager) */
    "primary": "#222222",      /* main content text (used on light containers) */
    "accent": "#EBEBEB",       /* accents and light text on dark UI */
    "background": "#B8B8B8",   /* overall page chrome - set to Figma container gray */
    "container": "#B8B8B8",    /* main content container background (light gray) */
    "surface": "#EBEBEB",      /* card / surface */
    "text": "#222222",         /* primary content text */
    "text-light": "#8E8E93",   /* muted text */
    "muted": "#8E8E93",        /* secondary / meta */
    "dark-gray": "#373737",    /* darker gray for emphasis */
    "border": "#EBEBEB"
  },
  "typography": {
    /* Hero and display sizes taken from the provided Figma CSS */
    "base-size": "16px",
    "line-height": "1.45",
    "hero-title": "88.8976px",
    "hero-subtitle": "79.9508px",
    "display-1": "128px",
    "lead": "32px",
    "h1": "88.8976px",
    "h2": "79.9508px",
    "h3": "32px",
    "h4": "26px",
    "h5": "18px",
    "h6": "16px"
  },
  "fonts": {
    "body": "'Rethink Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "heading": "'Geist', 'Arial Narrow', 'Helvetica Condensed', sans-serif"
  },
  "paths": {
    "header": "header.njk",
    "footer": "footer.njk"
  }
}
