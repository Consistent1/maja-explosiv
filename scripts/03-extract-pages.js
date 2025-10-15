#!/usr/bin/env node

/**
 * TYPO3 to 11ty Migration - Page Extraction Script
 * 
 * This script extracts pages from the TYPO3 database and exports them
 * to JSON format for further processing.
 * 
 * Usage: node scripts/03-extract-pages.js
 */

const mysql = require('mysql2/promise');
const fs = require('fs').promises;
const path = require('path');

// Database configuration
const DB_CONFIG = {
  host: 'localhost',
  user: 'root',
  password: '', // No password for fresh MySQL installation
  database: 'maja_typo3',
  charset: 'utf8mb4'
};

// Output directory
const OUTPUT_DIR = 'migration-data';

/**
 * Main extraction function
 */
async function extractPages() {
  console.log('========================================');
  console.log('TYPO3 Page Extraction');
  console.log('========================================\n');

  let connection;

  try {
    // Create output directory
    await fs.mkdir(OUTPUT_DIR, { recursive: true });
    console.log(`✓ Output directory created: ${OUTPUT_DIR}\n`);

    // Connect to database
    console.log('Connecting to database...');
    connection = await mysql.createConnection(DB_CONFIG);
    console.log('✓ Connected to database\n');

    // Extract pages
    console.log('Extracting pages...');
    const pages = await extractPagesData(connection);
    console.log(`✓ Extracted ${pages.length} pages\n`);

    // Extract content elements
    console.log('Extracting content elements...');
    const content = await extractContentData(connection);
    console.log(`✓ Extracted ${content.length} content elements\n`);

    // Extract news items
    console.log('Extracting news items...');
    const news = await extractNewsData(connection);
    console.log(`✓ Extracted ${news.length} news items\n`);

    // Extract DAM files
    console.log('Extracting DAM file references...');
    const damFiles = await extractDAMData(connection);
    console.log(`✓ Extracted ${damFiles.length} DAM file references\n`);

    // Build page tree
    console.log('Building page tree...');
    const pageTree = buildPageTree(pages);
    console.log('✓ Page tree built\n');

    // Map content to pages
    console.log('Mapping content to pages...');
    const pagesWithContent = mapContentToPages(pages, content);
    console.log('✓ Content mapped to pages\n');

    // Save extracted data
    console.log('Saving extracted data...');
    await saveJSON('pages.json', pagesWithContent);
    await saveJSON('page-tree.json', pageTree);
    await saveJSON('content.json', content);
    await saveJSON('news.json', news);
    await saveJSON('dam-files.json', damFiles);
    console.log('✓ Data saved\n');

    // Generate summary report
    console.log('Generating summary report...');
    const summary = generateSummary(pages, content, news, damFiles);
    await saveJSON('extraction-summary.json', summary);
    await saveSummaryText(summary);
    console.log('✓ Summary report generated\n');

    console.log('========================================');
    console.log('Extraction Complete!');
    console.log('========================================\n');
    console.log(`Output files saved to: ${OUTPUT_DIR}/`);
    console.log('- pages.json');
    console.log('- page-tree.json');
    console.log('- content.json');
    console.log('- news.json');
    console.log('- dam-files.json');
    console.log('- extraction-summary.json');
    console.log('- extraction-summary.txt\n');

  } catch (error) {
    console.error('Error during extraction:', error.message);
    process.exit(1);
  } finally {
    if (connection) {
      await connection.end();
    }
  }
}

/**
 * Extract pages from database
 */
async function extractPagesData(connection) {
  const [rows] = await connection.execute(`
    SELECT 
      uid,
      pid,
      title,
      doktype,
      hidden,
      deleted,
      nav_title,
      nav_hide,
      subtitle,
      keywords,
      description,
      abstract,
      author,
      media,
      sorting,
      crdate,
      tstamp
    FROM pages
    WHERE deleted = 0
    ORDER BY sorting
  `);
  return rows;
}

/**
 * Extract content elements from database
 */
async function extractContentData(connection) {
  const [rows] = await connection.execute(`
    SELECT 
      uid,
      pid,
      sorting,
      CType,
      header,
      header_layout,
      bodytext,
      image,
      imagewidth,
      imageheight,
      imagecaption,
      colPos,
      hidden,
      deleted,
      crdate,
      tstamp
    FROM tt_content
    WHERE deleted = 0
    ORDER BY pid, sorting
  `);
  return rows;
}

/**
 * Extract news items from database
 */
async function extractNewsData(connection) {
  const [rows] = await connection.execute(`
    SELECT 
      uid,
      pid,
      title,
      short,
      bodytext,
      datetime,
      author,
      keywords,
      image,
      imagecaption,
      hidden,
      deleted,
      crdate,
      tstamp
    FROM tt_news
    WHERE deleted = 0
    ORDER BY datetime DESC
  `);
  return rows;
}

/**
 * Extract DAM file references from database
 */
async function extractDAMData(connection) {
  const [rows] = await connection.execute(`
    SELECT 
      uid,
      pid,
      file_name,
      file_path,
      file_size,
      file_type,
      file_mime_type,
      title,
      description,
      keywords,
      caption,
      hidden,
      deleted
    FROM tx_dam
    WHERE deleted = 0
    ORDER BY file_name
  `);
  return rows;
}

/**
 * Build hierarchical page tree
 */
function buildPageTree(pages) {
  const pageMap = new Map();
  const rootPages = [];

  // Create map of all pages
  pages.forEach(page => {
    pageMap.set(page.uid, { ...page, children: [] });
  });

  // Build tree structure
  pages.forEach(page => {
    const pageNode = pageMap.get(page.uid);
    if (page.pid === 0) {
      rootPages.push(pageNode);
    } else {
      const parent = pageMap.get(page.pid);
      if (parent) {
        parent.children.push(pageNode);
      }
    }
  });

  return rootPages;
}

/**
 * Map content elements to their parent pages
 */
function mapContentToPages(pages, content) {
  const contentByPage = new Map();

  // Group content by page ID
  content.forEach(element => {
    if (!contentByPage.has(element.pid)) {
      contentByPage.set(element.pid, []);
    }
    contentByPage.get(element.pid).push(element);
  });

  // Add content to pages
  return pages.map(page => ({
    ...page,
    content: contentByPage.get(page.uid) || []
  }));
}

/**
 * Generate summary statistics
 */
function generateSummary(pages, content, news, damFiles) {
  return {
    timestamp: new Date().toISOString(),
    totals: {
      pages: pages.length,
      content_elements: content.length,
      news_items: news.length,
      dam_files: damFiles.length
    },
    pages_by_type: countByField(pages, 'doktype'),
    content_by_type: countByField(content, 'CType'),
    pages_with_content: pages.filter(p => 
      content.some(c => c.pid === p.uid)
    ).length,
    hidden_pages: pages.filter(p => p.hidden === 1).length,
    nav_hidden_pages: pages.filter(p => p.nav_hide === 1).length
  };
}

/**
 * Count items by field value
 */
function countByField(items, field) {
  const counts = {};
  items.forEach(item => {
    const value = item[field] || 'null';
    counts[value] = (counts[value] || 0) + 1;
  });
  return counts;
}

/**
 * Save data as JSON file
 */
async function saveJSON(filename, data) {
  const filepath = path.join(OUTPUT_DIR, filename);
  await fs.writeFile(filepath, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Save summary as text file
 */
async function saveSummaryText(summary) {
  const lines = [
    'TYPO3 Data Extraction Summary',
    '============================',
    '',
    `Extraction Date: ${summary.timestamp}`,
    '',
    'Totals:',
    `- Pages: ${summary.totals.pages}`,
    `- Content Elements: ${summary.totals.content_elements}`,
    `- News Items: ${summary.totals.news_items}`,
    `- DAM Files: ${summary.totals.dam_files}`,
    '',
    'Page Statistics:',
    `- Pages with content: ${summary.pages_with_content}`,
    `- Hidden pages: ${summary.hidden_pages}`,
    `- Navigation hidden: ${summary.nav_hidden_pages}`,
    '',
    'Pages by Type:',
    ...Object.entries(summary.pages_by_type).map(([type, count]) => 
      `- Type ${type}: ${count}`
    ),
    '',
    'Content by Type:',
    ...Object.entries(summary.content_by_type).map(([type, count]) => 
      `- ${type}: ${count}`
    ),
    ''
  ];

  const filepath = path.join(OUTPUT_DIR, 'extraction-summary.txt');
  await fs.writeFile(filepath, lines.join('\n'), 'utf8');
}

// Run extraction
extractPages();

