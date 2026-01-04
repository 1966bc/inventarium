-- ============================================
-- Monthly consumption analysis
-- Track usage patterns over time using strftime()
-- Usage: sqlite3 inventarium.db ".read dql/consumption_monthly.sql"
-- ============================================

.headers on
.mode column
.width 7 25 8

SELECT
    strftime('%Y-%m', lb.unloaded) AS month,
    p.description AS product,
    COUNT(*) AS consumed
FROM labels lb
JOIN batches b ON b.batch_id = lb.batch_id
JOIN packages pk ON pk.package_id = b.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE lb.status = 0
  AND lb.unloaded IS NOT NULL
  AND lb.unloaded >= date('now', '-12 months')
GROUP BY month, pk.package_id
ORDER BY month DESC, consumed DESC;
