-- ============================================
-- Update prices example
-- Shows how to deactivate old prices and insert new ones
-- Usage: sqlite3 inventarium.db ".read dml/update_prices.sql"
-- ============================================

.headers on
.mode column

-- Example: Update price for package_id = 1
-- Step 1: Deactivate current price
UPDATE prices
SET status = 0
WHERE package_id = 1 AND status = 1;

-- Step 2: Insert new price
INSERT INTO prices (package_id, supplier_id, price, vat, valid_from, status)
SELECT
    package_id,
    supplier_id,
    125.50,           -- new price
    22,               -- VAT percentage
    date('now'),      -- valid from today
    1                 -- active
FROM packages
WHERE package_id = 1;

-- Verify price history
SELECT '=== PRICE HISTORY FOR PACKAGE 1 ===' AS info;
SELECT
    price,
    vat,
    valid_from,
    CASE status WHEN 1 THEN 'Active' ELSE 'Inactive' END AS status
FROM prices
WHERE package_id = 1
ORDER BY valid_from DESC;
