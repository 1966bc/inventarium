-- ============================================
-- Supplier summary with product count and stock value
-- Overview of supplier relationships and inventory exposure
-- Usage: sqlite3 inventarium.db ".read dql/supplier_summary.sql"
-- ============================================

.headers on
.mode column
.width 25 8 10 12

SELECT
    s.description AS supplier,
    COUNT(DISTINCT pk.package_id) AS products,
    SUM(CASE WHEN lb.status = 1 THEN 1 ELSE 0 END) AS labels_in_stock,
    ROUND(SUM(CASE WHEN lb.status = 1 THEN COALESCE(pr.price, 0) ELSE 0 END), 2) AS stock_value
FROM suppliers s
LEFT JOIN packages pk ON pk.supplier_id = s.supplier_id AND pk.status = 1
LEFT JOIN batches b ON b.package_id = pk.package_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
LEFT JOIN prices pr ON pr.package_id = pk.package_id AND pr.status = 1
WHERE s.status = 1
GROUP BY s.supplier_id
ORDER BY stock_value DESC;
