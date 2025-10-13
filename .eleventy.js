module.exports = function(eleventyConfig) {
  // Copy static assets
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/media");
  
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
