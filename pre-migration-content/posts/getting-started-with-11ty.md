---
layout: post.njk
title: Getting Started with 11ty - A Beginner's Guide
description: Learn the basics of 11ty (Eleventy) static site generator and how to build your first website
date: 2024-01-10
author:
  name: Alex Tutorial
  avatar: /assets/images/authors/alex.jpg
postCollections: [tutorials, web-development]
tags: [11ty, beginner, static-site-generator, tutorial]
featuredImage: /assets/images/posts/11ty-guide.jpg
featuredImageAlt: 11ty logo and code editor
readingTime: 8
showShareButtons: true
showRelatedPosts: true
mediaGallery:
  - type: image
    url: /assets/images/posts/11ty-setup.jpg
    alt: 11ty project setup
    caption: Setting up your first 11ty project
  - type: image
    url: /assets/images/posts/11ty-templates.jpg
    alt: 11ty template structure
    caption: Understanding 11ty's template system
---

# Getting Started with 11ty - A Beginner's Guide

[11ty (Eleventy)](https://www.11ty.dev/) is a fantastic static site generator that's been gaining popularity among developers for its simplicity, flexibility, and performance. In this comprehensive guide, we'll walk through everything you need to know to get started with 11ty.

## What is 11ty?

11ty is a static site generator that transforms your content (written in Markdown, HTML, or other formats) into a fast, static website. Unlike dynamic websites that generate pages on-the-fly, static sites are pre-built, making them incredibly fast and secure.

### Why Choose 11ty?

- **Zero config**: Works out of the box with sensible defaults
- **Flexible**: Supports multiple template languages
- **Fast**: Generates sites quickly and efficiently
- **Simple**: Easy to learn and use
- **Powerful**: Extensible with plugins and custom functionality

## Installation and Setup

Let's create your first 11ty project:

### Prerequisites

Make sure you have Node.js installed (version 14 or higher):

```bash
node --version
npm --version
```

### Creating a New Project

1. **Create a new directory**:
   ```bash
   mkdir my-11ty-site
   cd my-11ty-site
   ```

2. **Initialize npm**:
   ```bash
   npm init -y
   ```

3. **Install 11ty**:
   ```bash
   npm install --save-dev @11ty/eleventy
   ```

4. **Add build scripts** to your `package.json`:
   ```json
   {
     "scripts": {
       "build": "eleventy",
       "serve": "eleventy --serve"
     }
   }
   ```

## Project Structure

A typical 11ty project structure looks like this:

```
my-11ty-site/
├── _site/              # Generated output (don't edit)
├── src/
│   ├── _includes/      # Reusable templates
│   ├── _layouts/       # Page layouts
│   ├── _data/          # Global data files
│   ├── posts/          # Blog posts
│   ├── pages/          # Static pages
│   └── assets/         # CSS, JS, images
├── .eleventy.js        # Configuration file
└── package.json
```

## Creating Your First Page

Let's create a simple home page:

**src/index.md**:
```markdown
---
layout: base.njk
title: Welcome to My Site
---

# Hello, World!

This is my first 11ty website. Pretty cool, right?

## What I Can Do

- Write content in Markdown
- Use powerful templating
- Build fast static sites
```

## Creating a Layout

Layouts wrap your content with common HTML structure:

**src/_layouts/base.njk**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - My 11ty Site</title>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/about/">About</a>
            <a href="/blog/">Blog</a>
        </nav>
    </header>
    
    <main>
        <h1>{{ title }}</h1>
        {{ content | safe }}
    </main>
    
    <footer>
        <p>&copy; 2024 My 11ty Site</p>
    </footer>
</body>
</html>
```

## Working with Collections

Collections are groups of related content. Let's create a blog:

**src/posts/my-first-post.md**:
```markdown
---
layout: post.njk
title: My First Blog Post
date: 2024-01-10
tags: [blog, first-post]
---

This is my first blog post using 11ty!
```

**src/_layouts/post.njk**:
```html
---
layout: base.njk
---

<article>
    <time>{{ date | date("MMMM Do, YYYY") }}</time>
    {{ content | safe }}
    
    {% if tags %}
        <div class="tags">
            {% for tag in tags %}
                <span class="tag">{{ tag }}</span>
            {% endfor %}
        </div>
    {% endif %}
</article>
```

## Configuration

The `.eleventy.js` file lets you customize 11ty's behavior:

```javascript
module.exports = function(eleventyConfig) {
    // Copy static assets
    eleventyConfig.addPassthroughCopy("src/assets");
    
    // Add a date filter
    eleventyConfig.addFilter("date", function(date, format) {
        return new Date(date).toLocaleDateString();
    });
    
    // Create a collection of blog posts
    eleventyConfig.addCollection("blog", function(collectionApi) {
        return collectionApi.getFilteredByGlob("src/posts/*.md");
    });
    
    return {
        dir: {
            input: "src",
            output: "_site"
        }
    };
};
```

## Building and Deploying

### Development

Start the development server:

```bash
npm run serve
```

Your site will be available at `http://localhost:8080` with live reload.

### Production Build

Generate the production site:

```bash
npm run build
```

The generated files will be in the `_site` directory, ready for deployment.

### Deployment Options

11ty sites can be deployed anywhere that serves static files:

- **Netlify**: Drag and drop the `_site` folder
- **Vercel**: Connect your Git repository
- **GitHub Pages**: Use GitHub Actions
- **Traditional hosting**: Upload via FTP

## Next Steps

Now that you understand the basics, here are some areas to explore:

### Advanced Features

- **Data files**: Store site-wide data in JSON/YAML files
- **Shortcodes**: Create reusable content snippets
- **Plugins**: Extend functionality with community plugins
- **Filters**: Transform content with custom functions

### Popular Plugins

- `@11ty/eleventy-plugin-syntaxhighlight`: Code syntax highlighting
- `@11ty/eleventy-plugin-rss`: RSS feed generation
- `@11ty/eleventy-img`: Image optimization
- `@11ty/eleventy-plugin-bundle`: Asset bundling

### Learning Resources

- [Official 11ty Documentation](https://www.11ty.dev/docs/)
- [11ty Rocks](https://11ty.rocks/) - Community tutorials
- [Eleventy Excellent](https://github.com/madrilene/eleventy-excellent) - Starter template

## Conclusion

11ty is an excellent choice for building fast, maintainable static websites. Its simplicity makes it perfect for beginners, while its flexibility satisfies advanced use cases.

The key to mastering 11ty is to start simple and gradually add complexity as you need it. Begin with basic Markdown files and layouts, then explore collections, data files, and plugins as your site grows.

Happy building! 🚀

---

*Want to learn more about 11ty? Check out our [advanced 11ty techniques](/posts/advanced-11ty-techniques/) post or browse our [web development tutorials](/collections/web-development/).*
