-- ============================================
-- Fix pending items in closed requests
-- Closes items that are still active in already closed requests
-- Usage: sqlite3 inventarium.db ".read dml/fix_pending.sql"
-- ============================================

.headers on
.mode column

-- 1. Show what will be modified
SELECT '=== ITEMS TO CLOSE ===' AS info;

SELECT
    i.item_id,
    r.reference AS request,
    p.description AS product
FROM items i
JOIN requests r ON r.request_id = i.request_id
JOIN packages pk ON pk.package_id = i.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE r.status = 0 AND i.status = 1;

-- 2. Count how many
SELECT '=== TOTAL ===' AS info;
SELECT COUNT(*) AS items_to_close
FROM items i
JOIN requests r ON r.request_id = i.request_id
WHERE r.status = 0 AND i.status = 1;

-- 3. Execute the UPDATE
UPDATE items SET status = 0
WHERE status = 1
AND request_id IN (SELECT request_id FROM requests WHERE status = 0);

SELECT changes() AS rows_modified;
