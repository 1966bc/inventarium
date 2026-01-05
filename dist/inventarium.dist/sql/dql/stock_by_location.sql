-- ============================================
-- Stock grouped by location
-- Shows inventory organized by physical location
-- Usage: sqlite3 inventarium.db ".read dql/stock_by_location.sql"
-- ============================================

.headers on
.mode column
.width 20 30 10 8

SELECT
    l.description AS location,
    p.description AS product,
    pk.packaging,
    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock
FROM locations l
JOIN packages pk ON pk.location_id = l.location_id
JOIN products p ON p.product_id = pk.product_id
LEFT JOIN batches b ON b.package_id = pk.package_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
WHERE l.status = 1
GROUP BY l.location_id, pk.package_id
HAVING in_stock > 0
ORDER BY l.description, p.description;
