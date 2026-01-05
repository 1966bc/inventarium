-- ============================================
-- Reorder alert - products below threshold
-- Identifies products that need to be reordered
-- Usage: sqlite3 inventarium.db ".read dql/reorder_alert.sql"
-- ============================================

.headers on
.mode column
.width 25 15 8 8 10

SELECT
    p.description AS product,
    s.description AS supplier,
    pk.reorder AS threshold,
    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock,
    CASE
        WHEN COUNT(CASE WHEN lb.status = 1 THEN 1 END) = 0 THEN 'OUT OF STOCK'
        WHEN COUNT(CASE WHEN lb.status = 1 THEN 1 END) <= pk.reorder THEN 'REORDER'
        ELSE 'OK'
    END AS status
FROM packages pk
JOIN products p ON p.product_id = pk.product_id
JOIN suppliers s ON s.supplier_id = pk.supplier_id
LEFT JOIN batches b ON b.package_id = pk.package_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
WHERE pk.status = 1 AND pk.reorder > 0
GROUP BY pk.package_id
HAVING status != 'OK'
ORDER BY status DESC, in_stock;
