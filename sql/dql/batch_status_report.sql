-- ============================================
-- Batch status report with label breakdown
-- Shows batch lifecycle: active, used, cancelled labels
-- Usage: sqlite3 inventarium.db ".read dql/batch_status_report.sql"
-- ============================================

.headers on
.mode column
.width 25 15 10 8 8 8

SELECT
    p.description AS product,
    b.description AS lot,
    b.expiration,
    SUM(CASE WHEN lb.status = 1 THEN 1 ELSE 0 END) AS active,
    SUM(CASE WHEN lb.status = 0 THEN 1 ELSE 0 END) AS used,
    SUM(CASE WHEN lb.status = -1 THEN 1 ELSE 0 END) AS cancelled
FROM batches b
JOIN packages pk ON pk.package_id = b.package_id
JOIN products p ON p.product_id = pk.product_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
WHERE b.status = 1
GROUP BY b.batch_id
ORDER BY b.expiration;
