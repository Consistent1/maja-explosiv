# Explosive Website Template

A flexible 11ty (Eleventy) website template featuring powerful collection management, responsive design, and comprehensive content organization capabilities.

## 🎯 Overview

The Explosive Website Template is designed to handle complex content structures with ease. It supports both static pages and dynamic collections, allowing posts to belong to multiple collections while maintaining clean, organized navigation and consistent presentation.

## ✨ Features

### 📄 Static Pages
- Individual page templates with customizable layouts
- Support for featured images, table of contents, and related pages
- Flexible content structure with optional components
- SEO-optimized with meta tags and social sharing

### 📝 Advanced Collections System
- Posts can belong to multiple collections using `postCollections` front matter
- Dynamic collection pages with automatic post filtering
- Nested collections support (e.g., tutorials → web-development, design)
- Rich collection metadata with descriptions, colors, and featured images
- Cross-referencing between collections and posts

### 🧭 Dynamic Navigation
- Automatically generated navigation from static pages and collections
- Mobile-responsive hamburger menu with smooth animations
- Footer navigation with customizable links
- Breadcrumb navigation for nested collections
- Skip links for accessibility

### 🎨 Modern Design System
- **Open Props integration** for consistent, scalable design tokens
- Mobile-first responsive design with CSS Grid and Flexbox
- Comprehensive design system with colors, typography, spacing, and animations
- Card-based layouts with hover effects and smooth transitions
- Typography system with web fonts and optimal readability
- Built-in normalize.css and button components from Open Props

### 📱 Performance & Accessibility
- Static site generation for lightning-fast loading
- Lazy loading for images and media
- Semantic HTML structure with ARIA labels
- Screen reader support and keyboard navigation
- Optimized asset handling and caching

## 🚀 Quick Start

### Prerequisites
- Node.js 14 or higher
- npm or yarn package manager

### Installation

1. **Clone or download the template**
   ```bash
   git clone <repository-url> my-explosive-site
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

Your site will be available at `http://localhost:8080` during development.

## 📁 Project Structure

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
│   └── collectionData.json  # Collection metadata
├── assets/             # Static assets
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   └── images/        # Image assets
├── posts/              # Blog posts and articles
├── pages/              # Static pages
├── collections/        # Collection overview pages
└── media/              # Media files for posts
```

## 📝 Content Creation

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

Edit `src/_data/collectionData.json` to customize collections:

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

## 🎨 Customization Architecture

This template uses a **User Directory** architecture to ensure that your custom changes do not create merge conflicts when pulling updates from the upstream template. All of your site's specific customizations should be placed in the `src/_user` directory.

The core template files are designed to be extended and overridden by files in `src/_user`.

### How to Change Site Colors

1.  Open `src/_user/data/theme.json` (if it's empty, you can copy the contents of `src/_data/theme.json` to start).
2.  Modify the color values. Eleventy will automatically merge this file with the base theme, with your values taking precedence.

**Example: `src/_user/data/theme.json`**
```json
{
  "colors": {
    "primary": "#0056b3",
    "accent": "#ffc107"
  }
}
```

### How to Add Custom CSS

1.  Open `src/_user/assets/css/custom.css`.
2.  Add any new CSS rules or overrides. This stylesheet is loaded after the main template stylesheet.

**Example: `src/_user/assets/css/custom.css`**
```css
.custom-hero {
  background: var(--theme-colors-primary);
  padding: 4rem 1rem;
  color: white;
}
```

### How to Override Layouts

This template allows you to override any of the default layouts (e.g., `post.njk`, `base.njk`) without modifying the core template files. This is useful for making structural changes to your site while still being able to pull in upstream updates.

1.  **Identify the layout** you want to override. The default layouts are in `src/_layouts/`.
2.  **Create a new file** with the *same name* in the `src/_user/layouts/` directory. For example, to override the main post layout, create `src/_user/layouts/post.njk`.
3.  **Add your custom content** to the new file. You can either write a completely new layout or extend the original and modify specific parts.

**Example: Customizing the Post Layout**

Let's say you want to add a "Share on X" link at the top of every blog post.

1.  Create the file `src/_user/layouts/post.njk`.
2.  In this file, extend the original `post.njk` layout and add your changes.

```nunjucks
{# src/_user/layouts/post.njk #}
{% extends "theme/post.njk" %}

{# The original post.njk is located in src/_layouts/ #}
{# We can now override any block defined in it. #}

{% block post_header %}
  {# Add a share link before the original header content #}
  <div class="share-on-x">
    <a href="https://twitter.com/intent/tweet?text={{ title | urlencode }}&url={{ page.url | urlencode }}">Share on X</a>
  </div>

  {# Render the original header block content #}
  {{ super() }}
{% endblock %}
```

Eleventy will automatically detect your new layout and use it instead of the default one for all pages that specify `layout: post`.

### How to Add Custom Includes

You can create reusable template components in `src/_user/includes/` that can be included in your layouts or pages. These files are merged with the base includes and can override base includes with the same name.

**Example: Create a custom component**

1. Create `src/_user/includes/my-component.njk`
2. Use it in any template with `{% include "my-component.njk" %}`

User includes can also extend base includes using `{% extends "base-include-name.njk" %}`.

**Note:** If you override a base include by using the same filename, you must rebuild the site (`npm run build`) for the changes to take effect. The `--watch` mode will not detect changes to files in `src/_user/includes/`.

### How to Modify the Header

1.  Create a new file: `src/_user/includes/my-header.njk`.
2.  In this file, extend the base header and override a specific block, like the navigation.

**Example: `src/_user/includes/my-header.njk`**
```nunjucks
{% extends "header.njk" %}

{# Replace the main navigation with a simpler one #}
{% block header_navigation %}
<nav class="main-navigation" aria-label="Main navigation">
    <ul class="nav-menu">
        <li class="nav-item"><a href="/" class="nav-link">Home</a></li>
        <li class="nav-item"><a href="/about/" class="nav-link">About Us</a></li>
    </ul>
</nav>
{% endblock %}
```
3.  Tell the theme to use your new header by editing `src/_user/data/theme.json`:

**Example: `src/_user/data/theme.json`**
```json
{
  "paths": {
    "header": "_user/includes/my-header.njk"
  }
}
```

### How to Add an Eleventy Plugin

1.  Install the plugin via npm: `npm install @11ty/eleventy-plugin-rss`.
2.  Open `src/_user/config.js`.
3.  Require the plugin and add it to the `plugins` array.

**Example: `src/_user/config.js`**
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

## 🛠 Advanced Features

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

## 📊 Built-in Features

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
| `src` | string | ✅ Yes | Path to the image file |
| `alt` | string | ✅ Yes | Alternative text for accessibility |
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

## 🔧 Development

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

## 🚀 Deployment

The template generates static files in the `_site` directory, making it compatible with any static hosting service:

### GitHub Pages Deployment

This template is optimized for GitHub Pages deployment using the docs folder approach:

1. **Configure the repository name** in `package.json`:
   ```bash
   # Update the path prefix in package.json build:github script
   # Replace 'explosive-11ty' with your repository name
   "build:github": "ELEVENTY_PATH_PREFIX=/your-repo-name/ eleventy"
   ```

2. **Build and deploy**:
   ```bash
   npm run deploy:github
   ```

3. **Commit and push**:
   ```bash
   git add docs/
   git commit -m "Deploy to GitHub Pages"
   git push origin main
   ```

4. **Configure GitHub Pages**:
   - Go to your repository settings
   - Navigate to "Pages" section
   - Set source to "Deploy from a branch"
   - Select "main" branch and "/docs" folder
   - Save the settings

Your site will be available at `https://username.github.io/repository-name/`

### Other Deployment Options

- **Netlify**: Connect your Git repository for automatic deployments
- **Vercel**: Import your project for instant deployment
- **Traditional Hosting**: Upload the `_site` folder via FTP

### Local Development vs Production

- **Local development**: All paths work from root (`/`)
- **GitHub Pages**: Paths are automatically prefixed with repository name
- **Custom domain**: Update `ELEVENTY_PATH_PREFIX` to `/` for root domain deployment

### Important: Local Server After GitHub Build

**Note**: After running `npm run build:github`, your local development server will not work correctly because the `_site` folder contains GitHub Pages paths (e.g., `/repo-name/assets/css/main.css`) instead of local paths (e.g., `/assets/css/main.css`).

**Recommended Development Workflow**:

```bash
# 1. Develop locally
npm run serve

# 2. When ready to deploy to GitHub Pages
npm run deploy:github

# 3. Commit and push to GitHub
git add docs/
git commit -m "Deploy to GitHub Pages"
git push origin main

# 4. To continue local development, rebuild for local paths
npm run build
npm run serve
```

This ensures your local development environment works correctly while maintaining proper GitHub Pages deployment.

## 📚 Example Content

The template includes sample content to demonstrate all features:

- **Welcome Post**: Introduction to the template with feature overview
- **11ty Tutorial**: Comprehensive beginner's guide to 11ty
- **CSS Grid Guide**: Advanced tutorial with code examples
- **About Page**: Template for company/personal information
- **Contact Page**: Contact form and information template

## 🤝 Contributing

This template is designed to be extended and customized. Feel free to:

- Add new layout templates
- Create additional filters and shortcodes
- Enhance the styling and design
- Add new functionality and features

## 🔮 Suggested Next Steps

Here are recommended enhancements to further improve the template:

### 🔍 Search & Discovery
- [ ] **Full-text search**: Implement client-side search with Lunr.js or Fuse.js
- [ ] **Advanced filtering**: Add tag-based filtering and sorting options
- [ ] **Search suggestions**: Auto-complete search with popular queries
- [ ] **Related content algorithm**: Improve related posts using content similarity

### 📊 Analytics & Performance
- [ ] **Analytics integration**: Add Google Analytics 4 or privacy-focused alternatives
- [ ] **Performance monitoring**: Implement Core Web Vitals tracking
- [ ] **Image optimization**: Add responsive images with `@11ty/eleventy-img`
- [ ] **Bundle optimization**: Implement CSS/JS minification and bundling

### 🎨 Enhanced UI/UX
- [ ] **Dark mode toggle**: Add user-controlled theme switching
- [ ] **Reading progress**: Show reading progress bar for long posts
- [ ] **Infinite scroll**: Implement pagination with infinite scroll
- [ ] **Print styles**: Add optimized print CSS for better printing

### 📱 Progressive Web App
- [ ] **Service Worker**: Add offline functionality and caching
- [ ] **Web App Manifest**: Make the site installable as a PWA
- [ ] **Push notifications**: Implement web push for new content alerts
- [ ] **Offline reading**: Cache posts for offline access

### 🔐 Content Management
- [ ] **CMS integration**: Connect with Netlify CMS, Forestry, or Sanity
- [ ] **Draft system**: Add draft post functionality with preview
- [ ] **Content scheduling**: Implement future post publishing
- [ ] **Multi-author support**: Enhanced author profiles and management

### 🌐 Internationalization
- [ ] **Multi-language support**: Add i18n with language switching
- [ ] **RTL support**: Right-to-left language compatibility
- [ ] **Localized URLs**: Language-specific URL structures
- [ ] **Translation management**: Workflow for content translation

### 📧 Communication Features
- [ ] **Newsletter integration**: Connect with Mailchimp, ConvertKit, or similar
- [ ] **Comment system**: Add Disqus, Utterances, or custom comments
- [ ] **Contact form backend**: Integrate with Netlify Forms or Formspree
- [ ] **Social media integration**: Auto-posting to social platforms

### 🛡️ Security & Privacy
- [ ] **Content Security Policy**: Implement CSP headers
- [ ] **Privacy compliance**: Add GDPR/CCPA compliance features
- [ ] **Spam protection**: Add reCAPTCHA or similar to forms
- [ ] **Security headers**: Implement security best practices

### 📈 SEO & Marketing
- [ ] **Advanced SEO**: Add JSON-LD structured data
- [ ] **Sitemap generation**: Automatic XML sitemap creation
- [ ] **RSS feeds**: Generate RSS feeds for collections
- [ ] **Social media cards**: Enhanced Open Graph and Twitter Card support

### 🔧 Developer Experience
- [ ] **Storybook integration**: Component documentation and testing
- [ ] **Testing framework**: Add unit and integration tests
- [ ] **GitHub Actions**: Automated testing and deployment workflows
- [ ] **Documentation site**: Comprehensive documentation with examples

### 🎯 Content Features
- [ ] **Series support**: Multi-part article series with navigation
- [ ] **Bookmarking**: User bookmarking functionality
- [ ] **Content ratings**: Star ratings or like/dislike system
- [ ] **Content recommendations**: AI-powered content suggestions

### 📊 Advanced Analytics
- [ ] **Heatmap tracking**: User interaction heatmaps
- [ ] **A/B testing**: Built-in A/B testing framework
- [ ] **Conversion tracking**: Goal and conversion analytics
- [ ] **User journey mapping**: Track user paths through content

## 📄 License

This template is open source and available under the MIT License.

---

**Built with ❤️ using 11ty (Eleventy)**
