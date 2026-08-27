# Explosive Website Template

**A flexible 11ty (Eleventy) website template featuring powerful collection management, responsive design, and comprehensive content organization capabilities.**

> **Note:** This website was built using the Explosive 11ty template.  
> The documentation below describes the base template features available to all sites using this template.  
> For site-specific changes and customizations, see [changes.md](changes.md).  
> The upstream repository containing the template can be forked from [https://github.com/Xpanda-org/explosive-11ty](https://github.com/Xpanda-org/explosive-11ty).  
> Changes to the upstream forked template can be fetched without causing merge conflicts.

An 11ty (Eleventy) website template which attempts to be customisable and flexible enough for most use cases while providing a reasonable developer experience.
The template’s collection management and layout systems leverage 11ty to handle complex content structures, Open Props provides theming, and Datastar powers front-end dynamic behaviour.

## Features

### Static Pages
- Individual page templates with customisable layouts
- Support for featured images, table of contents, and related pages
- Flexible content structure with optional components
- SEO-optimised with meta tags and social sharing

### Advanced Collections System
- Posts can belong to multiple collections using `postCollections` front matter
- Dynamic collection pages with automatic post filtering
- Nested collections support (e.g., tutorials → web-development, design)
- Rich collection metadata with descriptions, colours, and featured images
- Cross-referencing between collections and posts

### Dynamic Navigation
- Automatically generated navigation from static pages and collections
- Mobile-responsive hamburger menu with smooth animations
- Footer navigation with customizable links
- Breadcrumb navigation for nested collections
- Skip links for accessibility

### Modern Design System
- **Open Props integration** for consistent, scalable design tokens
- Mobile-first responsive design with CSS Grid and Flexbox
- Comprehensive design system with colours, typography, spacing, and animations
- Card-based layouts with hover effects and smooth transitions
- Typography system with web fonts
- Built-in normalize.css and button components from Open Props

### Performance & Accessibility
- Static site generation for fast loading
- Lazy loading for images and media
- Semantic HTML structure with ARIA labels
- Screen reader support and keyboard navigation
- Optimised asset handling and caching

## Quick Start

### Prerequisites
- Node.js 14 or higher
- npm or yarn package manager

### Installation

1. **Clone or download the template**
   ```bash
   git clone https://github.com/Xpanda-org/explosive-11ty.git my-explosive-site
   cd my-explosive-site
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run serve
   ```

4. **Build for production**
   ```bash
   npm run build
   ```
   Or **Build for GitHub Pages**
   ```bash
   npm run build:github
   ```

Your site will be available at `http://localhost:8080` during development.

## Serving, building and deploying — and how they interfere

The three commands above are **not independent**. They share one output directory and one
cache, and two of the ways they interact will make a change look like it did nothing. Both
have cost real debugging time, so they are written down here rather than rediscovered.

### 1. Editing a layout or include does not hot-reload — restart the server

`.eleventy.js` implements the override system (see *Customization Architecture* below) by
**copying** files into `.cache/` when Eleventy loads its config:

- `src/_layouts/` + `src/_user/layouts/` → `.cache/layouts/`
- `src/_includes/` + `src/_user/includes/` → `.cache/includes/`
- `src/_data/` + `src/_user/data/` → `.cache/data/`

Eleventy then builds from `.cache/`. Config runs **once per process**, so a server started
with `npm run serve` keeps rebuilding from the copies it made at startup. Edit
`src/_user/layouts/home.njk` and the browser will keep showing the old markup, with no error
and no warning — the file it is actually reading did not change.

**Restart the dev server after touching anything in `src/_user/layouts/`,
`src/_user/includes/`, `src/_user/data/`, `src/_layouts/`, `src/_includes/`, `src/_data/`, or
`.eleventy.js` itself.** Markdown, front matter and CSS *are* watched and do hot-reload —
`.eleventy.js` registers both `src/assets/css/` and `src/_user/assets/css/` as explicit watch
targets.

If a change seems to have no effect, check this before debugging the change.

### 2. Deploying is `git push`, and nothing else

Since 2026-08-26 the site is built and published by **GitHub Actions** —
`.github/workflows/deploy-pages.yml`, `path-prefix: /maja-explosiv/`, triggered by any push
to `main`. Settings → Pages → Source is set to **GitHub Actions**, and `docs/` is gitignored
and untracked. Nothing is built locally for a deploy and nothing built is committed.

Two consequences:

- **The local `_site` cannot reach the live site.** Actions builds its own copy from a clean
  checkout, so a stale or wrongly-prefixed local build is harmless.
- **`package-lock.json` is committed** and CI installs with `npm ci`. Change a dependency and
  you must commit the updated lockfile, or the build installs the old tree. See *A note on the
  lockfile* further down for the `cache: npm` trap that sits next to this.

### 3. Going back to the `docs/` route

**The `docs/` route is retired, not removed.** `build:github`, `copy:docs` and `deploy:github`
are all still in `package.json` and are kept deliberately — a fallback for the day Actions is
unavailable, out of minutes, or broken. Do not delete them.

Switching back takes three steps, and **all three are required**; doing fewer leaves Pages
serving whichever source it was last pointed at:

1. **Un-ignore `docs/`** — comment out the `/docs` line in `.gitignore`.
2. **Build and commit it** (stop the dev server first — see below):
   ```bash
   npm run deploy:github
   git add docs/ && git commit -m "Deploy" && git push
   ```
3. **Settings → Pages → Source: "Deploy from a branch" → `main` / `/docs`.**

To switch forward again, reverse all three: re-ignore `/docs`, `git rm -r --cached docs`, and
set Source back to **GitHub Actions**. Order matters in one direction only — never remove the
current source before the new one is live, or the site goes down in the gap.

#### Why the local build interferes, and only on this route

`npm run build:github` sets `ELEVENTY_PATH_PREFIX=/maja-explosiv/`, so **every internal URL in
the output gains that prefix** — `/assets/css/custom.css` becomes
`/maja-explosiv/assets/css/custom.css`. That is right for a project Pages site on a subpath and
wrong for `http://localhost:8080`, where those URLs 404 and the site renders unstyled. Both
builds write to the same `_site`, so:

- **Stop the dev server before deploying.** `copy:docs` does
  `rm -rf docs && cp -r _site docs && touch docs/.nojekyll`, and a watching server that rebuilds
  `_site` midway through the copy puts a half-written or unprefixed site into `docs/`.
- **Rebuild locally afterwards** (`npm run build`) or you will be looking at the prefixed build
  on localhost and wondering where the CSS went.

Checking you got it right: `grep -c '"/maja-explosiv/' docs/index.html` should be non-zero, and
the same grep against `_site/index.html` should be zero after the local rebuild.

None of this applies to the Actions route, which builds in CI and never touches your `_site`.

## Project Structure

```
src/
├── _includes/          # Reusable components
│   ├── header.njk      # Site header with navigation
│   └── footer.njk      # Site footer
├── _layouts/           # Page templates
│   ├── base.njk        # Base layout with HTML structure
│   ├── home.njk        # Homepage with hero and featured content
│   ├── page.njk        # Static page template
│   ├── post.njk        # Blog post template
│   ├── collection.njk  # Collection listing template
│   └── collections-overview.njk  # All collections overview
├── _data/              # Site configuration
│   ├── site.json       # Global site settings
│   ├── theme.js        # Theme configuration (colours, fonts, paths)
│   └── collectionData.json  # Collection metadata
├── _user/              # User customisations (override system)
│   ├── assets/        # Custom CSS, JS, and other assets
│   ├── data/          # Custom data files (merged with base)
│   ├── includes/      # Custom includes (override base)
│   └── layouts/       # Custom layouts (override base)
├── assets/             # Static assets
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   └── images/        # Image assets
├── posts/              # Blog posts and articles
├── pages/              # Static pages
├── collections/        # Collection overview pages
└── media/              # Media files for posts
```

## Content Creation

### Creating Posts

Create a new Markdown file in `src/posts/`:

```markdown
---
layout: post.njk
title: Your Post Title
description: Brief description for SEO and previews
date: 2024-01-15
author:
  name: Author Name
  avatar: /assets/images/authors/author.jpg
postCollections: [blog, tutorials]  # Can belong to multiple collections
tags: [javascript, web-development]
featuredImage: /assets/images/posts/featured.jpg
readingTime: 5
showShareButtons: true
showRelatedPosts: true
---

Your post content here...
```

### Creating Static Pages

Add pages to `src/pages/`:

```markdown
---
layout: page.njk
title: Page Title
description: Page description
navTitle: Nav Title  # Optional: different title for navigation
order: 1  # Optional: navigation order
showInNav: true
showInFooter: true
---

Your page content here...
```

### Configuring Collections

Edit `src/_data/collectionData.json` to customise collections:

```json
{
  "name": "tutorials",
  "displayName": "Tutorials",
  "description": "Step-by-step guides and how-to articles",
  "showInNav": true,
  "featuredImage": "/assets/images/collections/tutorials.jpg",
  "hasSubmenu": true,
  "submenuCollections": ["web-development", "design"],
  "color": "#e74c3c"
}
```

## Customization Architecture

This template uses a **User Directory** architecture to ensure that your custom changes do not create merge conflicts when pulling updates from the upstream template. All of your site's specific customisations should be placed in the `src/_user` directory.

The core template files are designed to be extended and overridden by files in `src/_user`.

### Override System Architecture

The template implements three parallel override systems that work at build time:

1. **Layout Override System** - Override template layouts
2. **Includes Override System** - Override reusable components
3. **Data Override System** - Override and merge configuration data

All three systems work the same way:
- Base files live in `src/_layouts/`, `src/_includes/`, and `src/_data/`
- User overrides live in `src/_user/layouts/`, `src/_user/includes/`, and `src/_user/data/`
- At build time, files are merged into `.cache/` directories
- Eleventy uses the merged cache directories
- No source files are ever modified - clean separation!

### How to Change Site Colours and Theme

The template uses a **Data Override System** that automatically merges your custom theme settings with the base theme. You can use either JavaScript (`.js`) or JSON (`.json`) files.

**How the Data Override System Works:**

The system uses a **deep merge** strategy at build time:

1. **Base data files** → `src/_data/` (template defaults)
2. **User data files** → `src/_user/data/` (your customizations)
3. **Build-time merge** → `.cache/data/` (merged result)
4. **Eleventy uses** → `.cache/data/` as the data directory

**Merge Behaviour:**
- **Nested objects** are merged recursively (property-level override)
- **Arrays** are replaced entirely (not merged)
- **You only specify what you want to change** - all other values are kept from base
- **No source files are modified** - clean separation prevents merge conflicts

**Example: Deep Merge in Action**

Base theme (`src/_data/theme.js`):
```javascript
{
  "colors": {
    "primary": "#333",
    "accent": "tomato",
    "background": "#fff"
  },
  "fonts": {
    "body": "Arial, sans-serif"
  }
}
```

Your override (`src/_user/data/theme.js`):
```javascript
module.exports = {
  "colors": {
    "primary": "#0056b3",      // Override primary
    "background": "#f8f9fa"    // Override background
  }
  // Note: accent color and fonts not specified
};
```

Merged result (`.cache/data/theme.js`):
```javascript
{
  "colors": {
    "primary": "#0056b3",      // ← Your override
    "accent": "tomato",         // ← Base value kept
    "background": "#f8f9fa"     // ← Your override
  },
  "fonts": {
    "body": "Arial, sans-serif" // ← Base value kept
  }
}
```

**Build Output:**

When you build, you'll see:
```
[Data Override] Merged user data: theme.js
```

This confirms your custom theme is being applied.

**Available Theme Properties:**

```javascript
{
  "colors": {
    "primary": "#333",      // Main brand colour
    "accent": "tomato",     // Accent/highlight colour
    "background": "#fff",   // Page background
    "text": "#333",         // Main text colour
    "text-light": "#666",   // Secondary text colour
    "border": "#ddd"        // Border colour
  },
  "fonts": {
    "body": "...",          // Body text font stack
    "heading": "..."        // Heading font stack
  },
  "paths": {
    "header": "header.njk", // Header template path
    "footer": "footer.njk"  // Footer template path
  }
}
```

These values are exposed as CSS custom properties:
- `var(--theme-colors-primary)`
- `var(--theme-colors-accent)`
- `var(--theme-fonts-body)`
- etc.

### How to Override Other Data Files

The Data Override System tries to stike a balance between ease of use and flexibility.
**Its main benefits are:**

**No merge conflicts** - User customizations separate from template
**Partial overrides** - Only specify what you want to change
**Type support** - Works with `.js` and `.json` files
**Automatic** - No manual configuration needed
**Consistent** - Same pattern as layouts/includes override system

The Data Override System works for **any** data file, not just `theme.js`:

**Override Site Configuration:**

```json
// src/_user/data/site.json
{
  "title": "My Custom Site Title",
  "description": "My custom description"
}
```

**Create New Data Files:**

You can also create entirely new data files in `src/_user/data/`:

```javascript
// src/_user/data/myCustomData.js
module.exports = {
  "setting": "value",
  "items": ["one", "two", "three"]
};
```

Access in templates: `{{ myCustomData.setting }}`

**Override Collection Data:**

```javascript
// src/_user/data/collectionData.json
[
  {
    "name": "blog",
    "displayName": "My Blog",
    "color": "#custom-color"
  }
]
```

### How to Add Custom CSS

1. Open `src/_user/assets/css/custom.css`.
2. Add any new CSS rules or overrides. This stylesheet is loaded after the main template stylesheet.

**Example: `src/_user/assets/css/custom.css`**
```css
.custom-hero {
  background: var(--theme-colors-primary);
  padding: 4rem 1rem;
  color: white;
}

/* Override existing styles */
body {
  font-family: var(--theme-fonts-body);
  background-color: var(--theme-colors-background);
}
```

**CSS Custom Properties from Theme:**

All theme values are automatically available as CSS custom properties:

```css
/* Use theme colors */
.my-element {
  color: var(--theme-colors-primary);
  background: var(--theme-colors-background);
  border-color: var(--theme-colors-border);
}

/* Use theme fonts */
.my-text {
  font-family: var(--theme-fonts-body);
}

.my-heading {
  font-family: var(--theme-fonts-heading);
}
```


### How to Override Layouts

This template allows you to override any of the default layouts (e.g., `post.njk`, `base.njk`) without modifying the core template files.

1. **Identify the layout** you want to override. The default layouts are in `src/_layouts/`.
2. **Create a new file** with the *same name* in the `src/_user/layouts/` directory.
3. **Add your custom content** to the new file. You can either write a completely new layout or extend the original.

**Example: Customizing the Post Layout**

```nunjucks
{# src/_user/layouts/post.njk #}
{% extends "theme/post.njk" %}

{% block post_header %}
  <div class="share-on-x">
    <a href="https://twitter.com/intent/tweet?text={{ title | urlencode }}">Share on X</a>
  </div>
  {{ super() }}
{% endblock %}
```

### How to Add Custom Includes

Create reusable template components in `src/_user/includes/`:

1. Create `src/_user/includes/my-component.njk`
2. Use it in any template with `{% include "my-component.njk" %}`

### How to Modify the Header

1. Create `src/_user/includes/my-header.njk`
2. Extend the base header and override specific blocks
3. Update `src/_user/data/theme.js`:

```javascript
module.exports = {
  "paths": {
    "header": "my-header.njk"
  }
};
```

### ⚙️ How to Add an Eleventy Plugin

1. Install: `npm install @11ty/eleventy-plugin-rss`
2. Edit `src/_user/config.js`:

```javascript
module.exports = {
  plugins: [
    {
      plugin: require("@11ty/eleventy-plugin-rss"),
      options: {}
    }
  ]
};
```

## Advanced Features

### Media Galleries

Add image galleries to posts:

```markdown
---
mediaGallery:
  - type: image
    url: /media/gallery/image1.jpg
    alt: Image description
    caption: Image caption
  - type: video
    url: /media/gallery/video.mp4
    poster: /media/gallery/video-poster.jpg
---
```

### Related Content

The template automatically suggests related posts based on collections and tags. You can also manually specify related pages:

```markdown
---
relatedPages: [about, contact]
---
```

### Custom Sections

Add custom sections to the homepage:

```markdown
---
customSections:
  - title: Custom Section
    class: my-custom-class
    content: |
      <p>Your custom HTML content here</p>
---
```

## Built-in Features

- **SEO Optimization**: Meta tags, Open Graph, Twitter Cards
- **Social Sharing**: Built-in sharing buttons for major platforms
- **Search Functionality**: Basic search implementation ready
- **Newsletter Signup**: Configurable newsletter form
- **Contact Forms**: Ready-to-use contact form with validation
- **Table of Contents**: Automatic TOC generation for long content
- **Reading Time**: Automatic reading time calculation
- **Breadcrumbs**: Navigation breadcrumbs for better UX
- **Image Carousel**: Flexible, accessible carousel component powered by Datastar

## 🎠 Image Carousel Component

The template includes a powerful and flexible image carousel component that can be added to any page type (posts, pages, collections, etc.).

### Features

- **Responsive Design**: Automatically adapts to all screen sizes
- **Touch Support**: Swipe gestures on mobile devices
- **Keyboard Navigation**: Arrow keys, Home, and End keys for navigation
- **Accessibility**: Full ARIA support for screen readers
- **Customizable**: Configure autoplay, intervals, dots, arrows, and more
- **Flexible Data Sources**: Define carousels in front matter, inline, or global data
- **Multiple Carousels**: Add multiple carousels to the same page
- **Image Metadata**: Support for captions, titles, alt text, and links

### Basic Usage

#### 1. Define Carousel in Front Matter

Add a carousel configuration to your page's front matter:

```yaml
---
title: My Page
carousels:
  hero:
    autoplay: true
    interval: 5000
    showDots: true
    showArrows: true
    height: 500px
    images:
      - src: /assets/images/slide1.jpg
        alt: First slide
        title: Welcome
        caption: This is the first slide
      - src: /assets/images/slide2.jpg
        alt: Second slide
        title: Features
        caption: Check out our features
---
```

#### 2. Use the Carousel Shortcode

In your page content, reference the carousel by its ID:

```markdown
{% carousel "hero" %}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `autoplay` | boolean | `false` | Automatically advance slides |
| `interval` | number | `5000` | Time between slides (ms) when autoplay is enabled |
| `showDots` | boolean | `true` | Show indicator dots at the bottom |
| `showArrows` | boolean | `true` | Show previous/next navigation arrows |
| `height` | string | `'auto'` | Fixed height (e.g., `'500px'`) or `'auto'` |
| `aspectRatio` | string | `null` | Aspect ratio (e.g., `'16/9'`, `'4/3'`, `'1/1'`, `'21/9'`) |

### Image Properties

Each image in the carousel can have the following properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `src` | string | Yes | Path to the image file |
| `alt` | string | Yes | Alternative text for accessibility |
| `title` | string | No | Title displayed as overlay |
| `caption` | string | No | Caption text displayed below title |
| `link` | string | No | URL to navigate to when image is clicked |
| `linkTarget` | string | No | Link target (e.g., `'_blank'`) |

### Usage Examples

#### Simple Carousel (Just Image Paths)

```yaml
carousels:
  simple:
    images:
      - /assets/images/img1.jpg
      - /assets/images/img2.jpg
      - /assets/images/img3.jpg
```

#### Full-Featured Carousel

```yaml
carousels:
  gallery:
    autoplay: false
    showDots: true
    showArrows: true
    aspectRatio: 4/3
    images:
      - src: /assets/images/product1.jpg
        alt: Product showcase
        title: Our Latest Product
        caption: Available now in stores
        link: /products/latest/
      - src: /assets/images/product2.jpg
        alt: Feature highlight
        title: Amazing Features
        caption: Discover what makes us different
```

#### Inline Carousel (No Front Matter)

You can also define a carousel inline:

```markdown
{% carousel images=[
  {src: "/assets/images/img1.jpg", alt: "Description 1"},
  {src: "/assets/images/img2.jpg", alt: "Description 2"}
] %}
```

### Multiple Carousels on One Page

You can add multiple carousels to the same page:

```yaml
---
carousels:
  hero:
    autoplay: true
    images: [...]
  gallery:
    autoplay: false
    images: [...]
  testimonials:
    showArrows: false
    images: [...]
---

{% carousel "hero" %}

## Our Gallery

{% carousel "gallery" %}

## What People Say

{% carousel "testimonials" %}
```

### Keyboard Navigation

When a carousel has focus:
- **Left Arrow**: Previous slide
- **Right Arrow**: Next slide
- **Home**: First slide
- **End**: Last slide

### Accessibility

The carousel component includes:
- ARIA labels and roles for screen readers
- Keyboard navigation support
- Focus indicators for interactive elements
- Reduced motion support for users with motion sensitivity
- Semantic HTML structure

### Customization

#### Custom Styling

Override carousel styles in your CSS:

```css
.carousel {
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.carousel-control {
  background: var(--brand-primary);
}

.carousel-indicator.active {
  background: var(--brand-accent);
}
```

#### Custom Aspect Ratios

The carousel supports common aspect ratios:
- `16/9` - Widescreen (default for video content)
- `4/3` - Standard
- `1/1` - Square
- `21/9` - Ultra-wide

Or set a custom height:

```yaml
carousels:
  custom:
    height: 600px
    images: [...]
```

### Best Practices

1. **Always provide alt text** for accessibility
2. **Optimize images** before adding them to carousels
3. **Use appropriate aspect ratios** for your content
4. **Limit autoplay** to avoid annoying users
5. **Test keyboard navigation** to ensure accessibility
6. **Keep captions concise** for better readability

## Development

### Available Scripts

- `npm run serve` - Start development server with live reload
- `npm run build` - Build for production
- `npm run debug` - Build with debug information
- `npm run build:github` - Build for GitHub Pages deployment
- `npm run copy:docs` - Copy _site contents to docs folder
- `npm run deploy:github` - Build and prepare for GitHub Pages

### Adding Custom Filters

Add custom Nunjucks filters in `.eleventy.js`:

```javascript
eleventyConfig.addFilter("myFilter", function(value) {
  return value.toUpperCase();
});
```

### Custom Collections

Create custom collections in `.eleventy.js`:

```javascript
eleventyConfig.addCollection("featured", function(collectionApi) {
  return collectionApi.getFilteredByGlob("src/posts/**/*.md")
    .filter(post => post.data.featured);
});
```

## Responsive images (optional)

The `image` shortcode emits responsive `<picture>` markup via
[`@11ty/eleventy-img`](https://www.11ty.dev/docs/plugins/image/) — **if the plugin is
installed**. If it is not, the same shortcode emits a plain `<img>` and the build succeeds
exactly as before.

This is deliberate. `@11ty/eleventy-img` depends on `sharp`, a native binary that not
every consumer wants in their CI image, so the template offers the capability without
imposing the dependency.

### Enabling it

```bash
npm install @11ty/eleventy-img
```

That is the whole setup. The shortcode detects the plugin at config time.

### Usage

```njk
{% image "/assets/images/projects/sculptures/kaethe/kaethe-01.jpg", "Käthe, welded steel portrait" %}

{# with a sizes hint and a class #}
{% image "/assets/images/hero.jpg", "Studio view", "(min-width: 60rem) 50vw, 100vw", "hero-image" %}
```

Arguments: `src`, `alt`, `sizes` (optional), `class` (optional). A site-absolute `src`
(`/assets/...`) resolves against the input directory.

`alt` is required. Omitting it logs a warning and renders `alt=""` rather than failing the
build — a missing alt is an accessibility defect, but it should not stop a deploy.

### Defaults

| Option | Default |
|---|---|
| `widths` | `[400, 800, 1200, 1600]` |
| `formats` | `["webp", "jpeg"]` — the last is the `<img>` fallback |
| `sizes` | `"100vw"` |
| `urlPath` / `outputDir` | `/img/` and `_site/img/` |
| `jpegQuality` / `webpQuality` | `82` / `80` |
| `loading` / `decoding` | `lazy` / `async` |

**Widths larger than the source are skipped** — the plugin does not upscale raster images.
Verified against v7.0.0: a 67px source with the default widths generates exactly one
variant at 67px, not four upscales. An 800px original yields 400px and 800px, not four. This means a
single width list can serve an archive of small legacy images and a stream of large modern
ones without special-casing either.

`ELEVENTY_PATH_PREFIX` is applied to generated URLs automatically, so images work under a
project-site prefix without extra configuration.

### Overriding per site

In `src/_user/config.js`:

```js
module.exports = {
  images: {
    widths: [400, 800, 1600, 2400],
    formats: ["avif", "webp", "jpeg"],
    webpQuality: 78
  }
};
```

Options merge over the defaults, so specify only what differs.

### When *not* to use it

If a set of images is already at final delivery size — a legacy archive of ~800px
photographs, say — generating variants adds build time and files for no benefit. Reference
those with a plain `<img>` and reserve the shortcode for material that has resolution to
spare.

## Deployment

The build produces static files in `_site/`, so any static host will serve it. The
recommended route is **GitHub Actions**, with ready-made workflows in
`.github/workflows/`.

### Why Actions rather than committing `docs/`

Earlier versions of this template built into `docs/` and committed it. That works, but it
commits **a second copy of every built file** — and because `deploy:github` does
`rm -rf docs && cp -r _site docs`, every deploy rewrites those files. Git stores each
rewrite as a new blob, so the repository grows by roughly the size of your assets **on
every deploy**, even when nothing changed.

For a text-heavy site that is tolerable. For an image-heavy one it is not: a thousand
photos at ~100 KB is ~100 MB duplicated, then re-committed on each deploy.

Building in Actions publishes the artifact directly. Nothing built is committed.

### Is GitHub Actions free?

**For public repositories, yes** — GitHub's billing documentation states Actions usage is
free for public repositories using standard GitHub-hosted runners. There is no minute cap
to manage.

**For private repositories there are limits**, and they matter:

| Plan | Included Actions minutes / month | Pages from a private repo |
|---|---|---|
| Free | 2,000 | **Not available** |
| Pro / Team | 3,000 / 3,000 | Available |
| Enterprise Cloud | 50,000 | Available |

Two consequences worth knowing before making a repository private:

- **Minutes become finite.** Builds are billed by the minute (rounded up per job), and
  non-Linux runners are billed at a multiplier — macOS is 10x, Windows 2x. Keep CI on
  `ubuntu-latest` unless you need otherwise.
- **GitHub Pages will stop working on a Free plan.** Publishing Pages from a private
  repository requires Pro or above. A public repo that goes private loses its site until
  the plan is upgraded or the site is moved elsewhere.

Storage for artifacts is also capped on private repos (500 MB on Free). The build workflow
here sets `retention-days: 7` to avoid accumulating old artifacts.

### Deploying to GitHub Pages

1. **Repository → Settings → Pages → Build and deployment → Source: `GitHub Actions`.**
   Without this the deploy step fails; it is the single most common mistake.
2. Edit `.github/workflows/deploy-pages.yml` and set `path-prefix` to `/<your-repo>/`
   for a project site, or `/` for a user site or custom domain.
3. Enable the trigger by uncommenting the `push:` block. It ships **manual-trigger only**
   so that adopting the template never publishes anything unexpectedly.

### Deploying to your own server

`.github/workflows/deploy-server.yml` builds the site and `rsync`s it over SSH. Also
manual-trigger only until you enable it.

**`rsync --delete` makes the server match the build exactly.** Anything under the target
path that the build does not produce **will be deleted**. Point it at a directory the site
owns outright — not at a home directory or a web root shared with something else.

#### Creating the deploy key

Use a **dedicated keypair**, not your personal SSH key. On your machine:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/deploy_mysite -N "" -C "github-actions-deploy"
```

That writes two files. The **public** half goes on the server:

```bash
ssh-copy-id -i ~/.ssh/deploy_mysite.pub deploy@example.com
# or append ~/.ssh/deploy_mysite.pub to ~/.ssh/authorized_keys by hand
```

Then capture the host key so the workflow is not trusting the server blindly:

```bash
ssh-keyscan -H example.com
```

#### Adding the secrets

In the repository: **Settings → Secrets and variables → Actions → New repository secret**.
Add each name exactly as written — they are case-sensitive and the workflow looks them up
by these names:

| Secret | Value | How to get it |
|---|---|---|
| `SSH_PRIVATE_KEY` | The **private** key, whole file | `cat ~/.ssh/deploy_mysite` — include the `-----BEGIN…` and `-----END…` lines and the trailing newline |
| `SSH_HOST` | `example.com` | your server's hostname or IP |
| `SSH_USER` | `deploy` | the user the key was installed for |
| `SSH_TARGET_PATH` | `/var/www/example.com/html` | absolute path to the web root |
| `SSH_PORT` | `22` | optional, omit for the default |
| `SSH_KNOWN_HOSTS` | output of `ssh-keyscan -H example.com` | optional but strongly recommended |

**Paste the private key, not the `.pub` file.** Pasting the public key produces an
authentication failure that reads like a server-side problem. Secrets are write-only —
GitHub will never show you the value again, so if you are unsure, replace it.

If `SSH_KNOWN_HOSTS` is absent the workflow logs a warning and falls back to
`ssh-keyscan` at run time, which trusts whatever answers on first contact. Acceptable for
a hobby box; not for anything that matters.

#### The runner IP range problem

GitHub-hosted runners come from **large, changing IP ranges** covering much of Azure. If
your server firewalls SSH to an allowlist, you cannot usefully allowlist "GitHub" — the
published list (`https://api.github.com/meta`, `actions` key) is thousands of prefixes and
changes without notice. Allowlisting all of it effectively means allowing the internet.

Four ways out, roughly in order of preference:

1. **A self-hosted runner** on your own infrastructure, or on the target server itself.
   The deploy becomes a local copy and SSH never crosses the internet. Best option when
   the server is yours. (Never use self-hosted runners on a **public** repo without
   restricting who can trigger workflows — a fork's pull request could otherwise run code
   on your machine.)
2. **A pull model.** The workflow publishes the artifact; the server fetches it on a
   schedule or via a webhook. No inbound SSH at all, and the firewall stays shut.
3. **A deploy service that already has an ingress** — Netlify, Vercel, Cloudflare Pages —
   pointed at the repository. Avoids the problem entirely.
4. **Accept broad SSH exposure**, but harden it: a key-only account with no shell
   (`command="rsync --server …"` in `authorized_keys`), `PasswordAuthentication no`, and
   `fail2ban`. This is the common choice and it is defensible, but it is a real widening
   of your attack surface and should be a decision rather than a default.

### A note on the lockfile

**`package-lock.json` is committed by default**, and both configurations are supported.
The build workflow installs with `npm ci` when a lockfile is present and falls back to
`npm install` when it is not, so **CI works either way without editing anything**.

| | Lockfile committed (default) | Lockfile gitignored |
|---|---|---|
| CI install | `npm ci` — reproducible | `npm install` — resolves fresh each run |
| Builds pinned? | Yes; a build today matches one next month | No; a patch release upstream can change output |
| `cache: npm` | Can be enabled | **Must stay off** — it hard-fails |
| Repo noise | One large file, churns on dependency changes | None |

**Committing it is recommended for any site you actually deploy.** Ignoring it is
reasonable for a template you only ever fork.

#### Switching between them

*To ignore the lockfile:* uncomment `/package-lock.json` in `.gitignore`,
`git rm --cached package-lock.json`, and leave `cache: npm` commented out in
`.github/workflows/build.yml`.

*To commit it (the default):* leave `/package-lock.json` commented out in `.gitignore`
and `git add package-lock.json`.

#### The `cache: npm` trap

`actions/setup-node`'s `cache: npm` is **commented out** in
`.github/workflows/build.yml`. This is deliberate: without a lockfile it does not degrade,
it **fails the job** with `Dependencies lock file is not found` — and it fails at the
`setup-node` step, *before* the install step's `npm install` fallback can run. Left off,
the one workflow serves both configurations.

If you keep the lockfile committed, uncomment it. It saves roughly 15–20 seconds a run.

### Legacy: the `docs/` folder route

**This site does not use it** — see *3. Going back to the `docs/` route* near the top of this
file for the full switch-back procedure, which is the fork-specific version of what the
template documents generically. The scripts are retained on purpose; do not delete them.

### Other hosts

- **Netlify / Vercel / Cloudflare Pages** — connect the repository; build command
  `npx eleventy`, publish directory `_site`.
- **Plain hosting** — upload `_site` by FTP/SFTP.

### Path prefix, in one line

`ELEVENTY_PATH_PREFIX` must match where the site is served from: `/<repo>/` for a GitHub
project site, `/` for a custom domain, a user site, or a server root.

## Example Content

The template includes sample content to demonstrate all features:

- **Welcome Post**: Introduction to the template with feature overview
- **11ty Tutorial**: Comprehensive beginner's guide to 11ty
- **CSS Grid Guide**: Advanced tutorial with code examples
- **About Page**: Template for company/personal information
- **Contact Page**: Contact form and information template

## Contributing

This repository does not accept any pull requests or issues, at least for the time being.

## Someday Maybe

### Search & Discovery
- [ ] **Full-text search**: Implement client-side search with Lunr.js or Fuse.js
- [ ] **Advanced filtering**: Add tag-based filtering and sorting options
- [ ] **Search suggestions**: Auto-complete search with popular queries
- [ ] **Related content algorithm**: Improve related posts using content similarity

### Analytics & Performance
- [ ] **Analytics integration**: Add Google Analytics 4 or privacy-focused alternatives
- [ ] **Performance monitoring**: Implement Core Web Vitals tracking
- [ ] **Image optimization**: Add responsive images with `@11ty/eleventy-img`
- [ ] **Bundle optimization**: Implement CSS/JS minification and bundling

### Enhanced UI/UX
- [ ] **Dark mode toggle**: Add user-controlled theme switching
- [ ] **Reading progress**: Show reading progress bar for long posts
- [ ] **Infinite scroll**: Implement pagination with infinite scroll
- [ ] **Print styles**: Add optimized print CSS for better printing

### Progressive Web App
- [ ] **Service Worker**: Add offline functionality and caching
- [ ] **Web App Manifest**: Make the site installable as a PWA
- [ ] **Push notifications**: Implement web push for new content alerts
- [ ] **Offline reading**: Cache posts for offline access

### Content Management
- [ ] **CMS integration**: Connect with Netlify CMS, Forestry, or Sanity
- [ ] **Draft system**: Add draft post functionality with preview
- [ ] **Content scheduling**: Implement future post publishing
- [ ] **Multi-author support**: Enhanced author profiles and management

### Internationalization
- [ ] **Multi-language support**: Add i18n with language switching
- [ ] **RTL support**: Right-to-left language compatibility
- [ ] **Localized URLs**: Language-specific URL structures
- [ ] **Translation management**: Workflow for content translation

### Communication Features
- [ ] **Newsletter integration**: Connect with Mailchimp, ConvertKit, or similar
- [ ] **Comment system**: Add Disqus, Utterances, or custom comments
- [ ] **Contact form backend**: Integrate with Netlify Forms or Formspree
- [ ] **Social media integration**: Auto-posting to social platforms

### Security & Privacy
- [ ] **Content Security Policy**: Implement CSP headers
- [ ] **Privacy compliance**: Add GDPR/CCPA compliance features
- [ ] **Spam protection**: Add reCAPTCHA or similar to forms
- [ ] **Security headers**: Implement security best practices

### SEO & Marketing
- [ ] **Advanced SEO**: Add JSON-LD structured data
- [ ] **Sitemap generation**: Automatic XML sitemap creation
- [ ] **RSS feeds**: Generate RSS feeds for collections
- [ ] **Social media cards**: Enhanced Open Graph and Twitter Card support

### Developer Experience
- [ ] **Storybook integration**: Component documentation and testing
- [ ] **Testing framework**: Add unit and integration tests
- [ ] **GitHub Actions**: Automated testing and deployment workflows
- [ ] **Documentation site**: Comprehensive documentation with examples

### Content Features
- [ ] **Series support**: Multi-part article series with navigation
- [ ] **Bookmarking**: User bookmarking functionality
- [ ] **Content ratings**: Star ratings or like/dislike system
- [ ] **Content recommendations**: AI-powered content suggestions

### Advanced Analytics
- [ ] **Heatmap tracking**: User interaction heatmaps
- [ ] **A/B testing**: Built-in A/B testing framework
- [ ] **Conversion tracking**: Goal and conversion analytics
- [ ] **User journey mapping**: Track user paths through content

## License

This template is open source and available under the MIT License.

---

**Built using 11ty (Eleventy), Datastar, and Open Props**
