-- ============================================
-- Check pending items in closed requests
-- Usage: sqlite3 inventarium.db ".read dql/check_pending.sql"
-- ============================================

.headers on
.mode column
.width 15 30 8 8 12

SELECT
    r.reference AS request,
    p.description AS product,
    i.quantity AS ordered,
    COALESCE((SELECT SUM(d.quantity) FROM deliveries d WHERE d.item_id = i.item_id AND d.status = 1), 0) AS delivered,
    CASE i.status
        WHEN 0 THEN 'Closed'
        WHEN 1 THEN 'Active'
        WHEN 2 THEN 'Cancelled'
    END AS item_status
FROM items i
JOIN requests r ON r.request_id = i.request_id
JOIN packages pk ON pk.package_id = i.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE r.status = 0          -- closed requests
  AND i.status = 1          -- still active items
ORDER BY r.reference, p.description;
