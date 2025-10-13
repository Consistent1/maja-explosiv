module.exports = function(eleventyConfig) {
  // Copy static assets
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/media");

  // Datastar is loaded from CDN, no need to copy from node_modules
  
  // Watch for changes in CSS
  eleventyConfig.addWatchTarget("src/assets/css/");
  
  // Create collections for posts
  eleventyConfig.addCollection("allPosts", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/posts/**/*.md").reverse();
  });

  // Create collection for pages
  eleventyConfig.addCollection("pages", function(collectionApi) {
    return collectionApi.getFilteredByGlob("src/pages/**/*.md");
  });
  
  // Create dynamic collections based on postCollections
  eleventyConfig.addCollection("postCollections", function(collectionApi) {
    const posts = collectionApi.getFilteredByGlob("src/posts/**/*.md");
    const collections = {};

    posts.forEach(post => {
      const tags = post.data.postCollections || [];
      tags.forEach(tag => {
        if (!collections[tag]) {
          collections[tag] = [];
        }
        collections[tag].push(post);
      });
    });

    return collections;
  });
  
  // Filter to get posts by collection
  eleventyConfig.addFilter("getPostsByCollection", function(posts, collectionName) {
    return posts.filter(post => {
      const collections = post.data.postCollections || [];
      return collections.includes(collectionName);
    });
  });

  // Filter to get unique collections
  eleventyConfig.addFilter("getUniqueCollections", function(posts) {
    const collections = new Set();
    posts.forEach(post => {
      const postCollections = post.data.postCollections || [];
      postCollections.forEach(collection => collections.add(collection));
    });
    return Array.from(collections);
  });
  
  // Date filter
  eleventyConfig.addFilter("dateDisplay", function(date) {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  });

  // Date filter for ISO format
  eleventyConfig.addFilter("date", function(date, format) {
    let d;
    if (date === 'now') {
      d = new Date();
    } else {
      d = new Date(date);
    }

    if (isNaN(d.getTime())) {
      return date; // Return original if invalid date
    }

    if (format === 'YYYY-MM-DD') {
      return d.toISOString().split('T')[0];
    }
    if (format === 'YYYY') {
      return d.getFullYear().toString();
    }
    if (format === 'MMMM Do, YYYY') {
      return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
    return d.toISOString();
  });
  
  // Excerpt filter
  eleventyConfig.addFilter("excerpt", function(content, length = 150) {
    const text = content.replace(/<[^>]*>/g, '');
    return text.length > length ? text.substring(0, length) + '...' : text;
  });

  // Slug filter
  eleventyConfig.addFilter("slug", function(str) {
    return str.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  });

  // Find filter
  eleventyConfig.addFilter("find", function(array, key, value) {
    if (!array || !Array.isArray(array)) return null;
    return array.find(item => item && item[key] === value);
  });

  // Limit filter
  eleventyConfig.addFilter("limit", function(array, limit) {
    return array.slice(0, limit);
  });

  // Related posts filter
  eleventyConfig.addFilter("getRelatedPosts", function(allPosts, currentCollections, currentTags, limit = 3) {
    if (!currentCollections && !currentTags) return [];

    const related = allPosts.filter(post => {
      if (post.data.postCollections) {
        return post.data.postCollections.some(collection =>
          currentCollections && currentCollections.includes(collection)
        );
      }
      if (post.data.tags && currentTags) {
        return post.data.tags.some(tag => currentTags.includes(tag));
      }
      return false;
    });

    return related.slice(0, limit);
  });

  // URL filter for handling relative paths and GitHub Pages deployment
  eleventyConfig.addFilter("url", function(url) {
    // Get path prefix from environment variable or default to "/"
    const pathPrefix = process.env.ELEVENTY_PATH_PREFIX || "/";

    // Don't modify external URLs or if path prefix is root
    if (!url || url.startsWith("http") || url.startsWith("//") || pathPrefix === "/") {
      return url;
    }

    // Remove leading slash and prepend path prefix
    const cleanUrl = url.replace(/^\//, "");
    return pathPrefix.replace(/\/$/, "") + "/" + cleanUrl;
  });

  // Carousel shortcode for image carousels
  eleventyConfig.addShortcode("carousel", function(carouselIdOrOptions, options = {}) {
    const pathPrefix = process.env.ELEVENTY_PATH_PREFIX || "/";

    // Helper function to apply URL filter
    const applyUrl = (url) => {
      if (!url || url.startsWith("http") || url.startsWith("//") || pathPrefix === "/") {
        return url;
      }
      const cleanUrl = url.replace(/^\//, "");
      return pathPrefix.replace(/\/$/, "") + "/" + cleanUrl;
    };

    let images = [];
    let config = {
      autoplay: false,
      interval: 5000,
      showDots: true,
      showArrows: true,
      height: 'auto',
      aspectRatio: null
    };

    // Determine input method and extract images
    if (typeof carouselIdOrOptions === 'string') {
      // Method 1: Reference from front matter (e.g., {% carousel "hero" %})
      // Access carousels from the context (this.ctx contains all page data)
      const carouselData = this.ctx?.carousels?.[carouselIdOrOptions];
      if (carouselData) {
        images = carouselData.images || [];
        config = { ...config, ...carouselData };
        delete config.images; // Remove images from config
      }
    } else if (carouselIdOrOptions?.images) {
      // Method 2: Inline images array
      images = carouselIdOrOptions.images;
      config = { ...config, ...carouselIdOrOptions };
      delete config.images;
    } else if (carouselIdOrOptions?.data) {
      // Method 3: Global data reference
      // This would need to be implemented with access to global data
      images = [];
    }

    // Merge any additional options passed as second parameter
    config = { ...config, ...options };

    if (!images || images.length === 0) {
      return '<!-- Carousel: No images provided -->';
    }

    // Normalize images to objects
    const normalizedImages = images.map(img => {
      if (typeof img === 'string') {
        return { src: img, alt: '' };
      }
      return img;
    });

    // Generate unique ID for this carousel
    const carouselId = `carousel-${Math.random().toString(36).substring(2, 11)}`;

    // Build carousel HTML with Datastar signals (all on one line to avoid Markdown processing issues)
    // Using String.raw or escaping $ to prevent template literal interpolation
    const autoplayAttr = config.autoplay ? `data-on-interval__duration.${config.interval}ms="$currentSlide = ($currentSlide + 1) % $totalSlides"` : '';
    const heightAttr = config.height !== 'auto' ? `style="height: ${config.height}"` : '';
    const aspectRatioAttr = config.aspectRatio ? `data-aspect-ratio="${config.aspectRatio}"` : '';

    let html = `<div class="carousel" id="${carouselId}" data-signals="{currentSlide: 0, totalSlides: ${normalizedImages.length}}" ${autoplayAttr} ${aspectRatioAttr} role="region" aria-label="Image carousel" aria-roledescription="carousel" tabindex="0"><div class="carousel-inner" ${heightAttr}>`;

    // Add slides (compact HTML to avoid Markdown processing)
    normalizedImages.forEach((img, index) => {
      const imgSrc = applyUrl(img.src);
      const linkOpen = img.link ? `<a href="${applyUrl(img.link)}"${img.linkTarget ? ` target="${img.linkTarget}"` : ''}>` : '';
      const linkClose = img.link ? '</a>' : '';
      const titleAttr = img.title ? `title="${img.title}"` : '';
      const caption = (img.caption || img.title) ? `<div class="carousel-caption">${img.title ? `<h3 class="carousel-title">${img.title}</h3>` : ''}${img.caption ? `<p class="carousel-caption-text">${img.caption}</p>` : ''}</div>` : '';

      // Use data-show with proper Datastar syntax
      // First slide should not have display:none to avoid flash of empty content
      const initialDisplay = index === 0 ? '' : ' style="display: none"';
      html += `<div class="carousel-slide" data-show="$currentSlide === ${index}"${initialDisplay} role="group" aria-roledescription="slide" aria-label="Slide ${index + 1} of ${normalizedImages.length}">${linkOpen}<img src="${imgSrc}" alt="${img.alt || ''}" loading="lazy" ${titleAttr}>${linkClose}${caption}</div>`;
    });

    html += `</div>`;

    // Add navigation arrows (compact HTML)
    if (config.showArrows) {
      html += `<button class="carousel-control carousel-control-prev" data-on-click="$currentSlide = ($currentSlide - 1 + $totalSlides) % $totalSlides" aria-label="Previous slide"><span class="carousel-control-icon" aria-hidden="true">‹</span></button>`;
      html += `<button class="carousel-control carousel-control-next" data-on-click="$currentSlide = ($currentSlide + 1) % $totalSlides" aria-label="Next slide"><span class="carousel-control-icon" aria-hidden="true">›</span></button>`;
    }

    // Add indicator dots (compact HTML)
    if (config.showDots) {
      html += `<div class="carousel-indicators" role="tablist">`;
      normalizedImages.forEach((_, index) => {
        html += `<button class="carousel-indicator" data-class="{active: $currentSlide === ${index}}" data-on-click="$currentSlide = ${index}" role="tab" aria-label="Go to slide ${index + 1}"></button>`;
      });
      html += `</div>`;
    }

    html += `</div>`;

    return html;
  });
  
  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts",
      data: "_data"
    },
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    pathPrefix: process.env.ELEVENTY_PATH_PREFIX || "/"
  };
};
