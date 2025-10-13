---
layout: page.njk
title: About Us
description: Learn more about the Explosive Website template and its features
navTitle: About
order: 1
showInNav: true
showInFooter: true
featuredImage: /assets/images/about-hero.jpg
featuredImageAlt: About us hero image
showLastModified: true
showTableOfContents: true
carousels:
  features:
    autoplay: true
    interval: 6000
    showDots: true
    showArrows: false
    height: 400px
    images:
      - src: /assets/images/carousel/hero/hero1.svg
        alt: Fast websites
        title: Lightning Fast
        caption: Built for speed and performance
      - src: /assets/images/carousel/hero/hero2.svg
        alt: Responsive design
        title: Fully Responsive
        caption: Perfect on any device
      - src: /assets/images/carousel/hero/hero3.svg
        alt: Easy to use
        title: Developer Friendly
        caption: Clean and maintainable code
---

# About Explosive Website

Welcome to the Explosive Website template - a powerful, flexible, and modern solution for building static websites with 11ty (Eleventy).

## Our Mission

We believe that creating beautiful, fast, and organized websites should be accessible to everyone. That's why we've built this template to be:

- **Easy to use** - Simple Markdown-based content creation
- **Highly flexible** - Customizable templates and layouts
- **Performance-focused** - Optimized for speed and SEO
- **Developer-friendly** - Clean, maintainable code structure

## Key Features

{% carousel "features" %}

### 🎯 Flexible Content Organization

Our template supports both static pages and dynamic collections, allowing you to organize your content exactly how you want it.

### 📝 Multiple Content Types

- **Static Pages**: Perfect for about pages, contact forms, and other standalone content
- **Blog Posts**: Full-featured blog posts with tags, categories, and media support
- **Collections**: Organize posts into themed collections that can be nested and cross-referenced

### 🎨 Customizable Design

Every aspect of the design can be customized through:

- CSS custom properties for easy theming
- Flexible template system
- Configurable navigation and footer
- Responsive design that works on all devices

### ⚡ Performance Optimized

Built with performance in mind:

- Static site generation for lightning-fast loading
- Optimized images and assets
- Clean, semantic HTML
- Minimal JavaScript footprint

## Technical Stack

This template is built using modern web technologies:

- **11ty (Eleventy)** - Static site generator
- **Nunjucks** - Templating engine
- **Markdown** - Content creation
- **CSS3** - Modern styling with custom properties
- **Vanilla JavaScript** - Lightweight interactivity

## Getting Started

Ready to build your own explosive website? Here's how to get started:

1. **Clone or download** this template
2. **Install dependencies** with `npm install`
3. **Start the development server** with `npm start`
4. **Customize** the content, design, and configuration to match your needs

## Support

If you need help or have questions about using this template, feel free to:

- Check out our documentation
- Browse the example content
- Reach out through our contact page

We're here to help you build something amazing!

---

*Last updated: {{ "now" | date("MMMM Do, YYYY") }}*
