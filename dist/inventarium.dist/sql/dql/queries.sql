-- ============================================
-- INVENTARIUM - Control Queries
-- Usage: sqlite3 inventarium.db ".read queries.sql"
-- ============================================

.headers on
.mode column

-- 1. STOCK (top 20)
SELECT '=== STOCK TOP 20 ===' AS '';
SELECT
    p.reference AS code,
    p.description AS product,
    pk.packaging,
    s.description AS supplier,
    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock
FROM products p
JOIN packages pk ON pk.product_id = p.product_id
LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
LEFT JOIN batches b ON b.package_id = pk.package_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
GROUP BY pk.package_id
HAVING in_stock > 0
ORDER BY in_stock DESC
LIMIT 20;

-- 2. UPCOMING EXPIRATIONS (90 days)
SELECT '';
SELECT '=== UPCOMING EXPIRATIONS 90 DAYS ===' AS '';
SELECT
    p.description AS product,
    b.description AS lot,
    b.expiration,
    CAST(julianday(b.expiration) - julianday('now') AS INTEGER) AS days
FROM batches b
JOIN packages pk ON pk.package_id = b.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE b.expiration IS NOT NULL
  AND b.expiration >= date('now')
  AND b.expiration <= date('now', '+90 days')
ORDER BY b.expiration
LIMIT 20;

-- 3. EXPIRED PRODUCTS
SELECT '';
SELECT '=== EXPIRED PRODUCTS ===' AS '';
SELECT
    p.description AS product,
    b.description AS lot,
    b.expiration,
    CAST(julianday('now') - julianday(b.expiration) AS INTEGER) AS days_expired
FROM batches b
JOIN packages pk ON pk.package_id = b.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE b.expiration < date('now')
  AND b.status = 1
ORDER BY b.expiration DESC
LIMIT 20;

-- 4. OPEN REQUESTS
SELECT '';
SELECT '=== OPEN REQUESTS ===' AS '';
SELECT
    r.reference AS request,
    r.issued AS date,
    COUNT(i.item_id) AS lines,
    SUM(i.quantity) AS qty_ordered,
    COALESCE(SUM(d.quantity), 0) AS qty_delivered
FROM requests r
JOIN items i ON i.request_id = r.request_id
LEFT JOIN deliveries d ON d.item_id = i.item_id
WHERE r.status = 1
GROUP BY r.request_id
ORDER BY r.issued DESC;

-- 5. RECENT DELIVERIES
SELECT '';
SELECT '=== LAST 10 DELIVERIES ===' AS '';
SELECT
    d.ddt,
    d.delivered AS date,
    p.description AS product,
    d.quantity AS qty
FROM deliveries d
JOIN items i ON i.item_id = d.item_id
JOIN packages pk ON pk.package_id = i.package_id
JOIN products p ON p.product_id = pk.product_id
ORDER BY d.delivered DESC
LIMIT 10;

-- 6. SUPPLIERS
SELECT '';
SELECT '=== SUPPLIERS ===' AS '';
SELECT
    supplier_id AS id,
    description AS supplier,
    reference AS code
FROM suppliers
WHERE status = 1
ORDER BY description;

-- 7. PRODUCT CATEGORIES
SELECT '';
SELECT '=== PRODUCT CATEGORIES ===' AS '';
SELECT
    category_id AS id,
    description AS category
FROM categories
WHERE reference_id = 1 AND status = 1
ORDER BY description;

-- 8. LOCATION CATEGORIES
SELECT '';
SELECT '=== LOCATION CATEGORIES ===' AS '';
SELECT
    category_id AS id,
    description AS type
FROM categories
WHERE reference_id = 3 AND status = 1
ORDER BY description;

-- 9. STORAGE CONDITIONS
SELECT '';
SELECT '=== STORAGE CONDITIONS ===' AS '';
SELECT * FROM conservations WHERE status = 1;

-- 10. GENERAL STATISTICS
SELECT '';
SELECT '=== STATISTICS ===' AS '';
SELECT
    (SELECT COUNT(*) FROM products WHERE status = 1) AS products,
    (SELECT COUNT(*) FROM packages WHERE status = 1) AS packages,
    (SELECT COUNT(*) FROM batches WHERE status = 1) AS batches,
    (SELECT COUNT(*) FROM labels WHERE status = 1) AS active_labels,
    (SELECT COUNT(*) FROM labels WHERE status = 0) AS used_labels,
    (SELECT COUNT(*) FROM suppliers WHERE status = 1) AS suppliers,
    (SELECT COUNT(*) FROM requests WHERE status = 1) AS open_requests;
