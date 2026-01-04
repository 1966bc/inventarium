-- ============================================
-- Archive expired batches
-- Sets status=0 for batches past expiration date
-- Usage: sqlite3 inventarium.db ".read dml/archive_expired.sql"
-- ============================================

.headers on
.mode column

-- 1. Preview what will be archived
SELECT '=== BATCHES TO ARCHIVE ===' AS info;

SELECT
    b.batch_id,
    p.description AS product,
    b.description AS lot,
    b.expiration
FROM batches b
JOIN packages pk ON pk.package_id = b.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE b.expiration < date('now')
  AND b.status = 1;

SELECT '=== COUNT ===' AS info;
SELECT COUNT(*) AS batches_to_archive
FROM batches
WHERE expiration < date('now') AND status = 1;

-- 2. Execute the update
UPDATE batches SET status = 0
WHERE expiration < date('now') AND status = 1;

SELECT changes() AS rows_modified;
