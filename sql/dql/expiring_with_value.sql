-- ============================================
-- Expiring batches with estimated value
-- Combines expiration data with pricing for financial planning
-- Usage: sqlite3 inventarium.db ".read dql/expiring_with_value.sql"
-- ============================================

.headers on
.mode column
.width 25 12 10 8 10

SELECT
    p.description AS product,
    b.description AS lot,
    b.expiration,
    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS qty,
    COALESCE(pr.price, 0) AS unit_price,
    ROUND(COUNT(CASE WHEN lb.status = 1 THEN 1 END) * COALESCE(pr.price, 0), 2) AS total_value
FROM batches b
JOIN packages pk ON pk.package_id = b.package_id
JOIN products p ON p.product_id = pk.product_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
LEFT JOIN prices pr ON pr.package_id = pk.package_id AND pr.status = 1
WHERE b.expiration <= date('now', '+90 days')
  AND b.status = 1
GROUP BY b.batch_id
HAVING qty > 0
ORDER BY b.expiration;
