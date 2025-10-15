-- TYPO3 to 11ty Migration - Database Analysis Queries
-- Run this after importing the database to understand the content structure

-- ============================================
-- 1. PAGES ANALYSIS
-- ============================================

SELECT '=== PAGES OVERVIEW ===' as '';

-- Total pages count
SELECT 'Total Pages' as Metric, COUNT(*) as Count 
FROM pages 
WHERE deleted = 0;

-- Pages by type
SELECT 
    'Pages by Type' as Analysis,
    doktype,
    CASE doktype
        WHEN 1 THEN 'Standard'
        WHEN 3 THEN 'External URL'
        WHEN 4 THEN 'Shortcut'
        WHEN 199 THEN 'Menu Separator'
        WHEN 254 THEN 'Folder'
        ELSE CONCAT('Other (', doktype, ')')
    END as Page_Type,
    COUNT(*) as Count
FROM pages
WHERE deleted = 0
GROUP BY doktype
ORDER BY Count DESC;

-- Top level pages (main navigation)
SELECT 
    'Top Level Pages' as Analysis,
    uid,
    title,
    nav_title,
    hidden,
    nav_hide
FROM pages
WHERE pid = 0 AND deleted = 0
ORDER BY sorting;

-- Pages with most content
SELECT 
    'Pages with Most Content' as Analysis,
    p.uid,
    p.title,
    COUNT(c.uid) as content_elements
FROM pages p
LEFT JOIN tt_content c ON c.pid = p.uid AND c.deleted = 0
WHERE p.deleted = 0
GROUP BY p.uid, p.title
ORDER BY content_elements DESC
LIMIT 10;

-- ============================================
-- 2. CONTENT ELEMENTS ANALYSIS
-- ============================================

SELECT '=== CONTENT ELEMENTS OVERVIEW ===' as '';

-- Total content elements
SELECT 'Total Content Elements' as Metric, COUNT(*) as Count 
FROM tt_content 
WHERE deleted = 0;

-- Content by type (CType)
SELECT 
    'Content by Type' as Analysis,
    CType,
    COUNT(*) as Count
FROM tt_content
WHERE deleted = 0
GROUP BY CType
ORDER BY Count DESC;

-- Content with images
SELECT 
    'Content with Images' as Metric,
    COUNT(*) as Count
FROM tt_content
WHERE deleted = 0 AND image != '';

-- Hidden content
SELECT 
    'Hidden Content' as Metric,
    COUNT(*) as Count
FROM tt_content
WHERE deleted = 0 AND hidden = 1;

-- ============================================
-- 3. NEWS ANALYSIS
-- ============================================

SELECT '=== NEWS/BLOG ANALYSIS ===' as '';

-- Total news items
SELECT 'Total News Items' as Metric, COUNT(*) as Count 
FROM tt_news 
WHERE deleted = 0;

-- News items details
SELECT 
    'News Items' as Analysis,
    uid,
    title,
    datetime,
    hidden,
    type
FROM tt_news
WHERE deleted = 0
ORDER BY datetime DESC;

-- News categories
SELECT 
    'News Categories' as Analysis,
    uid,
    title,
    parent_category
FROM tt_news_cat
WHERE deleted = 0;

-- ============================================
-- 4. MEDIA/DAM ANALYSIS
-- ============================================

SELECT '=== MEDIA FILES (DAM) ANALYSIS ===' as '';

-- Total DAM files
SELECT 'Total DAM Files' as Metric, COUNT(*) as Count 
FROM tx_dam 
WHERE deleted = 0;

-- DAM files by type
SELECT 
    'DAM Files by Type' as Analysis,
    file_type,
    COUNT(*) as Count,
    ROUND(SUM(file_size)/1024/1024, 2) as Total_MB
FROM tx_dam
WHERE deleted = 0
GROUP BY file_type
ORDER BY Count DESC;

-- DAM categories
SELECT 
    'DAM Categories' as Analysis,
    uid,
    title,
    parent_id
FROM tx_dam_cat
WHERE deleted = 0;

-- ============================================
-- 5. SYSTEM INFORMATION
-- ============================================

SELECT '=== SYSTEM INFORMATION ===' as '';

-- Domains
SELECT 
    'Domains' as Analysis,
    uid,
    pid,
    domainName,
    redirectTo
FROM sys_domain;

-- Templates
SELECT 
    'Templates' as Analysis,
    uid,
    pid,
    title,
    root
FROM sys_template
WHERE deleted = 0;

-- ============================================
-- 6. FILE REFERENCES
-- ============================================

SELECT '=== FILE REFERENCES ===' as '';

-- Content elements with images
SELECT 
    'Content with Image References' as Analysis,
    c.uid,
    c.header,
    c.image,
    p.title as page_title
FROM tt_content c
JOIN pages p ON c.pid = p.uid
WHERE c.deleted = 0 AND c.image != ''
ORDER BY c.uid
LIMIT 20;

-- ============================================
-- 7. SPECIAL FIELDS
-- ============================================

SELECT '=== SPECIAL CONTENT ===' as '';

-- Pages with keywords
SELECT 
    'Pages with Keywords' as Metric,
    COUNT(*) as Count
FROM pages
WHERE deleted = 0 AND keywords != '';

-- Pages with descriptions
SELECT 
    'Pages with Descriptions' as Metric,
    COUNT(*) as Count
FROM pages
WHERE deleted = 0 AND description != '';

-- Pages with media
SELECT 
    'Pages with Media' as Metric,
    COUNT(*) as Count
FROM pages
WHERE deleted = 0 AND media != '';

-- ============================================
-- 8. NAVIGATION STRUCTURE
-- ============================================

SELECT '=== NAVIGATION STRUCTURE ===' as '';

-- Build page tree (2 levels)
SELECT 
    'Page Tree (2 levels)' as Analysis,
    CONCAT(
        REPEAT('  ', 0),
        p1.uid, ': ', p1.title,
        IF(p1.nav_hide = 1, ' [HIDDEN]', '')
    ) as Page_Tree
FROM pages p1
WHERE p1.pid = 0 AND p1.deleted = 0
ORDER BY p1.sorting

UNION ALL

SELECT 
    '',
    CONCAT(
        REPEAT('  ', 1),
        '└─ ', p2.uid, ': ', p2.title,
        IF(p2.nav_hide = 1, ' [HIDDEN]', '')
    )
FROM pages p2
JOIN pages p1 ON p2.pid = p1.uid
WHERE p1.pid = 0 AND p1.deleted = 0 AND p2.deleted = 0
ORDER BY p1.sorting, p2.sorting;

-- ============================================
-- 9. SUMMARY STATISTICS
-- ============================================

SELECT '=== SUMMARY STATISTICS ===' as '';

SELECT 
    'Summary' as Category,
    'Total Pages' as Item,
    COUNT(*) as Value
FROM pages WHERE deleted = 0
UNION ALL
SELECT '', 'Total Content Elements', COUNT(*) FROM tt_content WHERE deleted = 0
UNION ALL
SELECT '', 'Total News Items', COUNT(*) FROM tt_news WHERE deleted = 0
UNION ALL
SELECT '', 'Total DAM Files', COUNT(*) FROM tx_dam WHERE deleted = 0
UNION ALL
SELECT '', 'Total Templates', COUNT(*) FROM sys_template WHERE deleted = 0;

-- ============================================
-- END OF ANALYSIS
-- ============================================

SELECT '=== ANALYSIS COMPLETE ===' as '';

