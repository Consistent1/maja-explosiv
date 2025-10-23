# Project Overview

This project is an Eleventy (11ty) static site generator template, forked from `https://github.com/Xpanda-org/explosive-11ty`. It is designed to create flexible and content-rich websites with a focus on organized content, modern design, and performance.

**Key Technologies:**
*   **Eleventy (11ty):** Static site generator.
*   **Nunjucks:** Templating language for layouts and includes.
*   **Markdown:** Used for writing content (posts, pages).
*   **CSS:** Utilizes CSS Grid, Flexbox, and Open Props for a modern and responsive design system.
*   **Datastar:** A lightweight library used for interactive components, specifically the image carousel.

**Architecture:**
The project employs a "User Directory" architecture (`src/_user`) to facilitate customizations without causing merge conflicts when updating the base template from its upstream source. This allows for overriding styles, data, includes, and Eleventy configurations.

**Content Structure:**
Content is organized into:
*   `src/posts/`: Markdown files for blog posts and articles.
*   `src/pages/`: Markdown files for static pages (e.g., About, Contact).
*   `src/collections/`: Markdown files that define collection overview pages.
*   Dynamic collections are generated based on `postCollections` front matter in posts.

**Key Features:**
*   Advanced collections system allowing posts to belong to multiple collections.
*   Dynamic navigation, including mobile-responsive menus and breadcrumbs.
*   Modern design system with Open Props integration.
*   Focus on performance and accessibility.
*   Flexible image carousel component with extensive configuration options.
*   SEO optimization, social sharing, and other built-in features.

# Building and Running

This project uses `npm` for dependency management and script execution.

**Prerequisites:**
*   Node.js 14 or higher
*   npm or yarn package manager

**Installation:**
1.  Clone the repository:
    ```bash
    git clone <repository-url> my-explosive-site
    cd my-explosive-site
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

**Available Commands:**

*   **Start Development Server (with live reload):**
    ```bash
    npm run serve
    ```
    Your site will be available at `http://localhost:8080` during development.

*   **Build for Production:**
    ```bash
    npm run build
    ```
    This generates static files in the `_site` directory.

*   **Build for GitHub Pages Deployment:**
    ```bash
    npm run build:github
    ```
    This command builds the site with a path prefix suitable for GitHub Pages (e.g., `/maja-explosiv/`).

*   **Deploy to GitHub Pages:**
    ```bash
    npm run deploy:github
    ```
    This command first runs `build:github` and then copies the generated `_site` content to the `docs/` folder, which is typically used for GitHub Pages deployment.

*   **Debug Build:**
    ```bash
    npm run debug
    ```
    Builds the site with Eleventy debug information.

**Deployment:**
The generated static files in `_site` (or `docs` for GitHub Pages) can be deployed to any static hosting service (GitHub Pages, Netlify, Vercel, etc.). Refer to the `README.md` for detailed GitHub Pages deployment instructions.

# Development Conventions

**Content Creation:**
*   **Posts:** Create Markdown files in `src/posts/` with front matter defining layout, title, description, date, author, `postCollections`, tags, and featured images.
*   **Static Pages:** Create Markdown files in `src/pages/` with front matter for layout, title, description, navigation title, order, and visibility in navigation/footer.
*   **Collections:** Configure collection metadata in `src/_data/collectionData.json`.

**Customization:**
All custom changes should be placed within the `src/_user` directory to ensure compatibility with upstream updates. This directory mirrors the main `src` directory structure.

*   **Custom CSS:** Add rules to `src/_user/assets/css/custom.css`.
*   **Theme Overrides:** Modify `src/_user/data/theme.json` to override colors, paths, or other theme settings.
*   **Custom Includes/Layouts:** Create files in `src/_user/includes/` or `src/_user/layouts/` and reference them in `src/_user/data/theme.json` or directly in content.
*   **Eleventy Configuration:** Add plugins, shortcodes, filters, or passthrough copies in `src/_user/config.js`.

**Templating:**
*   Nunjucks is used for templating. Layouts are in `src/_layouts/` and reusable components are in `src/_includes/`.
*   Custom filters and shortcodes can be added via `.eleventy.js` or `src/_user/config.js`.

**Styling:**
*   The project integrates **Open Props** for consistent design tokens.
*   Mobile-first responsive design is implemented using CSS Grid and Flexbox.

**Image Carousel:**
*   Carousels can be defined in page front matter, global data, or inline.
*   The `{% carousel "id" %}` shortcode is used to embed carousels in content.
*   Extensive configuration options are available for autoplay, navigation, height, aspect ratio, and image properties.

**File Naming:**
*   Markdown files for content typically use kebab-case (e.g., `my-post-title.md`).

**Testing:**
No explicit testing framework or scripts were identified in `package.json` or `README.md`. Development relies on local server (`npm run serve`) for live preview and manual verification.
