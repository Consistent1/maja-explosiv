
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
    "border": "#EBEBEB",        /* Grey/0 - Off White */

    /* CTA button, from the redesigned homepage CTA (Figma 388:5771
       "hover-interaction-3", the visible instance). Both are OFF-PALETTE and
       bound to no Figma variable - rendered as the design has them per
       CLAUDE.md §3, with the inconsistency flagged in PLAN.md's open items.
       Do not "snap" either to a palette value. */
    "cta-fill": "#1B1B1B",      /* disc fill and label colour; nearest palette value is #222222 */
    "cta-chevron": "#FFCC00"    /* chevron stroke; the palette has no yellow at all */
  },
  "typography": {
    /* CORRECTED 2026-07-24 (round 2). The first extraction pass read values
       from the wrong Figma frame - a stale draft, not the canonical one.
       The owner pointed to the exact right location: big heading "Onepager
       Solution" -> sub-heading "Updated Components" -> the "Main container"
       section beneath it. Every value below is re-verified directly from
       that frame (and, for the sidebar, cross-checked against the
       Assets/Components library's component marked "In Use").

       Font family corrected: it's Geist everywhere (headings AND body),
       not Outfit - Outfit doesn't appear to be used anywhere in the
       correct frame; the prior "Outfit" conclusion came from the wrong
       location too. */
    "base-size": "16px",
    "line-height": "1.45",

    /* Hero "MAJA" line - Geist 700 Bold, from Title node in Main container */
    "hero-title": "85.94px",
    "hero-title-line-height": "74%",
    "hero-title-letter-spacing": "-0.02em",

    /* Hero "EXPLOSIV" line - Geist 500 Medium, from Subtitle node (distinct
       weight/size from the Title line, not identical as first assumed) */
    "hero-subtitle": "77.29px",
    "hero-subtitle-line-height": "74%",
    "hero-subtitle-letter-spacing": "-0.02em",
    "hero-subtitle-weight": "500",

    /* Sidebar/nav logo text ("MAJA EXPLOSIV" wordmark, smaller instance) -
       not re-verified from the correct frame this round; font corrected to
       Geist for consistency, size/spacing kept as prior approximation */
    "nav-title": "30px",
    "nav-title-line-height": "92%",
    "nav-title-letter-spacing": "-0.03em",

    /* Lead paragraph - CONFIRMED 2026-07-30 from the canonical homepage frame,
       node 254:2943 inside `Description container`. This closes the round-3 gap
       that had it flagged as "not re-verified": it was carrying 40px/110%/-2.5%
       from the wrong-frame extraction. */
    "lead": "31.73px",
    "lead-line-height": "130%",
    "lead-letter-spacing": "-0.03em",
    "lead-weight": "500",

    /* Body / tagline text ("For commissions, collaborations...") - Geist
       400 Regular, from Description node in Main container */
    "body-size": "22.45px",
    "body-line-height": "110%",
    "body-letter-spacing": "-0.025em",

    /* Section eyebrow label ("WHO WE ARE" etc) - not re-verified from the
       correct frame this round, font corrected to Geist for consistency,
       size/spacing kept as prior approximation */
    "section-title": "29px",
    "section-title-line-height": "140%",
    "section-title-letter-spacing": "0.02em",

    /* Button label ("LETS GET IN TOUCH"). The two dark-pill Button instances
       that gave 16px/600 are `visible: false` in Figma - drafts. The visible
       CTA (388:5771) sets its label at 16.24px / 500 / 121% / uppercase, and
       in Inter rather than Geist. Size, weight, case and line-height are taken
       from it; the family is not - see the Inter entry in PLAN.md's open items. */
    "button-size": "16.24px",
    "button-weight": "500",
    "button-line-height": "121%",

    /* CTA icon: a 40.65px disc with a chevron. Figma 388:5730 exports as a
       30x30 circle (rx=15), so the geometry is scaled, not redrawn. */
    "cta-icon-size": "40.65px",
    "cta-icon-gap": "8.12px",

    /* Not yet confirmed against Figma at all - carried over as prior
       approximation. Per the design owner: treat as a guideline, not
       pixel-exact - reasonable descending steps, not confirmed values. */
    "h3": "32px",
    "h4": "26px",
    "h5": "18px",
    "h6": "16px"
  },
  "fonts": {
    /* Geist confirmed from the correct Figma frame for headings, body, AND
       buttons - a single font family throughout, not a heading/button
       split as previously (wrongly) concluded. Outfit removed. */
    "body": "'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "heading": "'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "button": "'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
  },
  "paths": {
    "header": "header.njk",
    "footer": "footer.njk"
  }
}
