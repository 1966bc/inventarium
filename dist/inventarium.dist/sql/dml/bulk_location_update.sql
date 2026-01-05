-- ============================================
-- Bulk location update example
-- Move all packages from one location to another
-- Usage: sqlite3 inventarium.db ".read dml/bulk_location_update.sql"
-- ============================================

.headers on
.mode column

-- Example: Move all packages from location 1 to location 2

-- 1. Preview affected packages
SELECT '=== PACKAGES TO MOVE ===' AS info;
SELECT
    pk.package_id,
    p.description AS product,
    l.description AS current_location
FROM packages pk
JOIN products p ON p.product_id = pk.product_id
JOIN locations l ON l.location_id = pk.location_id
WHERE pk.location_id = 1;

-- 2. Execute the move (uncomment to run)
-- UPDATE packages SET location_id = 2 WHERE location_id = 1;
-- SELECT changes() AS packages_moved;

SELECT '=== NOTE: UPDATE is commented out for safety ===' AS info;
