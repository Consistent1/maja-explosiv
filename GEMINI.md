# GEMINI.md

## Project Overview

This is a static website project built with [Eleventy (11ty)](https://www.11ty.dev/), a flexible static site generator. It uses [Nunjucks](https://mozilla.github.io/nunjucks/) for templating and is designed to be a highly customizable theme. Frontend interactivity is powered by [Datastar.js](https://datastar.starfederation.org/), which is loaded from a CDN.

The project structure is organized as follows:
- `src`: Contains all source files, including content, layouts, and data.
- `_site`: The output directory where the generated static site is placed.
- `docs`: A copy of the `_site` directory, used for deploying to GitHub Pages.

The styling is managed through `src/assets/css/main.css` and leverages [Open Props](https://open-props.style/) for a consistent design system.

A key feature is the advanced collections system, allowing posts to belong to multiple collections dynamically. It also includes a powerful, accessible, and customizable image carousel component built with Datastar.js.

## Building and Running

The project uses `npm` for dependency management and running scripts.

- **Install Dependencies:**
  ```bash
  npm install
  ```

- **Run Development Server:**
  Starts a local server with live reloading at `http://localhost:8080`.
  ```bash
  npm run serve
  ```

- **Build for Production:**
  Generates the static site into the `_site` directory.
  ```bash
  npm run build
  ```

- **Deploy to GitHub Pages:**
  This is a two-step process:
  1.  Builds the site with the correct path prefix for GitHub Pages.
  2.  Copies the output from `_site` to the `docs` directory.
  ```bash
  npm run deploy:github
  ```
  After running this, you need to commit and push the `docs` directory.

## Development Conventions

- **Content:** All content is written in Markdown.
  - **Posts:** Located in `src/posts/`. Posts can be assigned to multiple collections via the `postCollections` front matter key.
  - **Static Pages:** Located in `src/pages/`.

- **Layouts:** Nunjucks templates in `src/_layouts/` define the structure of pages and posts. `base.njk` is the main HTML skeleton.

- **Data:** Global site data is stored in `src/_data/`.
  - `site.json`: Contains global site metadata like title, description, and social links.
  - `collectionData.json`: Defines metadata for the dynamic collections (e.g., display name, description).

- **Configuration:** The main Eleventy configuration is in `.eleventy.js`. This file defines:
  - Passthrough copies for static assets (`src/assets`, `src/media`).
  - Custom collections (`allPosts`, `pages`, `postCollections`).
  - A variety of Nunjucks filters for formatting dates, creating excerpts, and more.
  - The `carousel` shortcode for generating image carousels.

- **Customization:** The template is designed to be customized easily.
  - **Styling:** Override the default Open Props CSS variables in `src/assets/css/main.css`.
  - **Functionality:** Add custom filters, shortcodes, or collections in `.eleventy.js`.
