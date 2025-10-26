const fs = require('fs');
const path = require('path');
const userConfigPath = './src/_user/config.js';

module.exports = function(eleventyConfig) {
  // Load user config
  let userConfig = {};
  if (fs.existsSync(userConfigPath)) {
    userConfig = require(userConfigPath);
  }

  // Apply user config
  if (userConfig.plugins) {
    userConfig.plugins.forEach(plugin => eleventyConfig.addPlugin(plugin.plugin, plugin.options || {}));
  }
  if (userConfig.shortcodes) {
    Object.keys(userConfig.shortcodes).forEach(name => eleventyConfig.addShortcode(name, userConfig.shortcodes[name]));
  }
  if (userConfig.filters) {
    Object.keys(userConfig.filters).forEach(name => eleventyConfig.addFilter(name, userConfig.filters[name]));
  }
  if (userConfig.passthroughCopy) {
    userConfig.passthroughCopy.forEach(target => eleventyConfig.addPassthroughCopy(target));
  }

  // ============================================================================
  // LAYOUT OVERRIDE SYSTEM
  // ============================================================================
  // This system allows users to override theme layouts without modifying the
  // base template files, preventing merge conflicts when pulling upstream updates.
  //
  // How it works:
  // 1. Base layouts live in src/_layouts/ (part of the template, tracked in git)
  // 2. Theme layouts live in src/_layouts/theme/ (copies for extending, tracked in git)
  // 3. User overrides live in src/_user/layouts/ (user customizations, tracked in git)
  // 4. At build time, we create .cache/layouts/ (git-ignored)
  // 5. We copy base layouts to .cache/layouts/
  // 6. We copy user overrides to .cache/layouts/ (overwriting base layouts)
  // 7. Eleventy uses .cache/layouts/ as the layouts directory
  // 8. No source files are ever modified - clean separation!
  // ============================================================================

  const baseLayoutsDir = 'src/_layouts';
  const userLayoutsDir = 'src/_user/layouts';
  const baseIncludesDir = 'src/_includes';
  const userIncludesDir = 'src/_user/includes';
  const cacheLayoutsDir = '.cache/layouts';
  const cacheIncludesDir = '.cache/includes';

  // Create cache directories for merged layouts and includes
  if (!fs.existsSync(cacheLayoutsDir)) {
    fs.mkdirSync(cacheLayoutsDir, { recursive: true });
  }
  if (!fs.existsSync(cacheIncludesDir)) {
    fs.mkdirSync(cacheIncludesDir, { recursive: true });
  }

  // Copy base layouts to cache
  // Also create a "theme" subdirectory with copies for user layouts to extend
  if (fs.existsSync(baseLayoutsDir)) {
    const cacheThemeDir = path.join(cacheLayoutsDir, 'theme');
    if (!fs.existsSync(cacheThemeDir)) {
      fs.mkdirSync(cacheThemeDir, { recursive: true });
    }

    fs.readdirSync(baseLayoutsDir).forEach(file => {
      const srcPath = path.join(baseLayoutsDir, file);
      const stat = fs.statSync(srcPath);

      // Only copy files (not subdirectories like theme/)
      if (stat.isFile()) {
        // Copy to cache root
        const destPath = path.join(cacheLayoutsDir, file);
        fs.copyFileSync(srcPath, destPath);

        // Also copy to theme subdirectory so user layouts can extend them
        const themeDestPath = path.join(cacheThemeDir, file);
        fs.copyFileSync(srcPath, themeDestPath);
      }
    });
  }

  // Copy user layouts to cache, overriding base layouts (but NOT into theme subdirectory)
  if (fs.existsSync(userLayoutsDir)) {
    fs.readdirSync(userLayoutsDir).forEach(file => {
      // Skip files that begin with a dot (like .gitkeep)
      if (file.startsWith('.')) {
        return;
      }

      const userFilePath = path.join(userLayoutsDir, file);
      const stat = fs.statSync(userFilePath);
      if (stat.isFile()) {
        const targetPath = path.join(cacheLayoutsDir, file);
        // Copy to root of cache layouts, not into theme subdirectory
        fs.copyFileSync(userFilePath, targetPath);
        console.log(`[Layout Override] Using user layout: ${file}`);
      }
    });
  }

  // Copy base includes to cache
  const copyRecursive = (srcDir, destDir) => {
    if (!fs.existsSync(destDir)) {
      fs.mkdirSync(destDir, { recursive: true });
    }

    fs.readdirSync(srcDir).forEach(file => {
      if (file.startsWith('.')) return;

      const srcPath = path.join(srcDir, file);
      const destPath = path.join(destDir, file);
      const stat = fs.statSync(srcPath);

      if (stat.isDirectory()) {
        copyRecursive(srcPath, destPath);
      } else if (stat.isFile()) {
        fs.copyFileSync(srcPath, destPath);
      }
    });
  };

  if (fs.existsSync(baseIncludesDir)) {
    copyRecursive(baseIncludesDir, cacheIncludesDir);
  }

  // Copy user includes to cache, overriding base includes
  if (fs.existsSync(userIncludesDir)) {
    copyRecursive(userIncludesDir, cacheIncludesDir);
  }

  // Configure Nunjucks to look in cache directories for templates
  // This allows {% extends %} and {% include %} to find templates
  const Nunjucks = require("nunjucks");
  const nunjucksEnvironment = new Nunjucks.Environment(
    new Nunjucks.FileSystemLoader([
      ".cache/includes",     // Merged includes (base + user overrides)
      ".cache/layouts"       // Merged layouts (base + user overrides)
    ]),
    {
      throwOnUndefined: false,
      autoescape: false
    }
  );

  eleventyConfig.setLibrary("njk", nunjucksEnvironment);

  // Copy static assets
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/media");
  eleventyConfig.addPassthroughCopy("src/_user/assets");

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
          // Use local date parts to avoid timezone bug
          const year = d.getFullYear();
          // getMonth() is 0-indexed, so add 1
          const month = (d.getMonth() + 1).toString().padStart(2, '0');
          const day = d.getDate().toString().padStart(2, '0');
          
          return `${year}-${month}-${day}`;
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
    // } else if (carouselIdOrOptions?.data) {
    //   // Method 3: Global data reference
    //   // This would need to be implemented with access to global data
    //   images = [];
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
      includes: "../.cache/includes",  // Use cache directory with merged includes
      layouts: "../.cache/layouts",    // Use cache directory with merged layouts
      data: "_data"
    },
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    pathPrefix: process.env.ELEVENTY_PATH_PREFIX || "/"
  };
};
