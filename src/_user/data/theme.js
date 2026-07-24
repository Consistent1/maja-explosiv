
// src/_user/data/theme.js
module.exports = {
  "colors": {
    /* Exact values from the Figma file's "Grey" variable collection
       (project_docs/design_screenshots/Colors.png), confirmed 2026-07-24.
       Figma variable name -> value, semantic role in parens: */
    "primary": "#222222",       /* Grey/800 - Primary Text Color */
    "text": "#222222",          /* Grey/800 - Primary Text Color */
    "text-secondary": "#525252",/* Grey/600 - Secondary Text Color */
    "muted": "#8E8E93",         /* Grey/500 - Inactive Element */
    "text-light": "#8E8E93",    /* Grey/500 - Inactive Element (alias, kept for existing CSS refs) */
    "dark-gray": "#373737",     /* Grey/700 (no semantic alias in Figma) */
    "sidebar": "#B8B8B8",       /* Grey/200 - Background. Figma defines a separate "Navigation
                                    Sidebar" variable (Grey/300 #B1B1B1) but the actual SideBar
                                    Navigation component instance has its fill bound to Background,
                                    confirmed by inspecting the component directly, 2026-07-24 */
    "background": "#B8B8B8",    /* Grey/200 - Background */
    "container": "#B8B8B8",     /* Grey/200 - Background (page content container) */
    "accent": "#EBEBEB",        /* Grey/0 - Off White */
    "surface": "#EBEBEB",       /* Grey/0 - Off White */
    "border": "#EBEBEB"         /* Grey/0 - Off White */
  },
  "typography": {
    /* Exact values read from Figma's Properties panel per text layer,
       confirmed 2026-07-24 (see project docs for method). All confirmed
       text uses the "Outfit" font family - the site was previously
       loading "Geist", which does not appear anywhere in the Figma file.
       Un-confirmed sizes (h4-h6) are kept as prior approximations. */
    "base-size": "16px",
    "line-height": "1.45",

    /* Hero "MAJA EXPLOSIV" wordmark - Outfit 700, uppercase */
    "hero-title": "140.77px",
    "hero-title-line-height": "92%",
    "hero-title-letter-spacing": "-0.03em",

    /* Sidebar/nav logo text - Outfit 700, uppercase (smaller instance of the same style) */
    "nav-title": "30px",
    "nav-title-line-height": "92%",
    "nav-title-letter-spacing": "-0.03em",

    /* Lead paragraph ("Maja Explosiv is a multidisciplinary artist...") - Outfit 500 */
    "lead": "40px",
    "lead-line-height": "110%",
    "lead-letter-spacing": "-0.025em",
    "lead-weight": "500",

    /* Body / tagline text ("For commissions, collaborations...") - Outfit 400 */
    "body-size": "32px",
    "body-line-height": "110%",
    "body-letter-spacing": "-0.025em",

    /* Section eyebrow label ("WHO WE ARE" etc, Figma style "Section title") -
       Outfit 700, uppercase, wide tracking. Distinct role from a generic h3. */
    "section-title": "29px",
    "section-title-line-height": "140%",
    "section-title-letter-spacing": "0.02em",

    /* Button label ("LETS GET IN TOUCH") - Geist 600, uppercase */
    "button-size": "16px",
    "button-line-height": "140%",

    /* Not yet confirmed against Figma - carried over from prior approximation.
       Per the design owner: treat as a guideline, not pixel-exact - these are
       reasonable descending steps rather than confirmed Figma values. */
    "h3": "32px",
    "h4": "26px",
    "h5": "18px",
    "h6": "16px"
  },
  "fonts": {
    /* Outfit confirmed from Figma for headings, nav, and body text.
       Geist confirmed from Figma for buttons specifically (not headings -
       that was the old, wrong assumption this site shipped with before). */
    "body": "'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "heading": "'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "button": "'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
  },
  "paths": {
    "header": "header.njk",
    "footer": "footer.njk"
  }
}
