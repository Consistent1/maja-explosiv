---
layout: post.njk
title: Image Carousel Demo
description: Demonstrating the image carousel component with beautiful galleries
date: 2024-01-20
author:
  name: Demo Author
postCollections: [blog]
tags: [demo, carousel, images]
carousels:
  gallery:
    autoplay: false
    interval: 4000
    showDots: true
    showArrows: true
    aspectRatio: 4/3
    images:
      - src: /assets/images/carousel/gallery/gallery1.svg
        alt: Beautiful gradient background with circle
        title: Gradient Design
        caption: Beautiful gradient designs with geometric shapes
      - src: /assets/images/carousel/gallery/gallery2.svg
        alt: Modern gradient background with square
        title: Geometric Patterns
        caption: Modern geometric patterns and layouts
      - src: /assets/images/carousel/gallery/gallery3.svg
        alt: Creative gradient background with triangle
        title: Visual Elements
        caption: Creative visual elements for your designs
---

## Introducing the Image Carousel

The Explosive Website template now includes a powerful and flexible image carousel component powered by Datastar. This component makes it easy to showcase images, galleries, and featured content on any page.

### Gallery Example

Here's a beautiful image gallery carousel:

{% carousel "gallery" %}

### Key Features

The carousel component includes:

- **Responsive Design**: Looks great on all devices
- **Touch Support**: Swipe gestures on mobile devices
- **Keyboard Navigation**: Use arrow keys to navigate
- **Accessibility**: Full ARIA support for screen readers
- **Customizable**: Configure autoplay, intervals, and appearance
- **Flexible**: Use on any page type (posts, pages, collections)

### How to Use

You can add a carousel to any page by defining it in the front matter and then using the shortcode:

```yaml
---
carousels:
  myCarousel:
    autoplay: true
    showDots: true
    images:
      - src: /path/to/image1.jpg
        alt: Description
        caption: Optional caption
---

{% carousel "myCarousel" %}
```

### Multiple Carousels

You can even have multiple carousels on the same page! Each carousel can have its own configuration and images.

Check out the [documentation](#) for more details on customizing your carousels.

