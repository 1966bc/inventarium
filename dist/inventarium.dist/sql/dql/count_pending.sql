-- ============================================
-- Count pending items in closed requests
-- Usage: sqlite3 inventarium.db ".read dql/count_pending.sql"
-- ============================================

SELECT COUNT(*) AS pending_items
FROM items i
JOIN requests r ON r.request_id = i.request_id
WHERE r.status = 0 AND i.status = 1;
