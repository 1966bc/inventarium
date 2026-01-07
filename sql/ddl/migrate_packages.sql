-- Migration script: Add commercial_name to packages table
-- Reorders columns so status is always last (project convention)
--
-- Author: 1966bc (Giuseppe Costanzi)
-- Date: 2026-01-07
--
-- BACKUP YOUR DATABASE BEFORE RUNNING THIS SCRIPT!

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

-- Step 1: Drop views that depend on packages
DROP VIEW IF EXISTS v_expiring;
DROP VIEW IF EXISTS v_open_requests;
DROP VIEW IF EXISTS v_stock;

-- Step 2: Create new table with correct column order
CREATE TABLE packages_new (
    package_id INTEGER NOT NULL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    reference TEXT NOT NULL,
    labels INTEGER,
    packaging TEXT NOT NULL,
    conservation_id INTEGER NOT NULL DEFAULT 4,
    in_the_dark INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER NOT NULL DEFAULT 0,
    location_id INTEGER,
    order_by_piece INTEGER NOT NULL DEFAULT 1,
    pieces_per_label INTEGER NOT NULL DEFAULT 1,
    reorder INTEGER NOT NULL DEFAULT 0,
    funding_id INTEGER REFERENCES funding_sources(funding_id),
    labels_per_unit INTEGER DEFAULT 1,
    label_text VARCHAR(40),
    label_font_size INTEGER DEFAULT 36,
    shelf VARCHAR(20),
    commercial_name TEXT,
    status INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (conservation_id) REFERENCES conservations(conservation_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Step 3: Copy data from old table
INSERT INTO packages_new (
    package_id,
    product_id,
    supplier_id,
    reference,
    labels,
    packaging,
    conservation_id,
    in_the_dark,
    category_id,
    location_id,
    order_by_piece,
    pieces_per_label,
    reorder,
    funding_id,
    labels_per_unit,
    label_text,
    label_font_size,
    shelf,
    commercial_name,
    status
)
SELECT
    package_id,
    product_id,
    supplier_id,
    reference,
    labels,
    packaging,
    conservation_id,
    in_the_dark,
    category_id,
    location_id,
    order_by_piece,
    pieces_per_label,
    reorder,
    funding_id,
    labels_per_unit,
    label_text,
    label_font_size,
    shelf,
    NULL,
    status
FROM packages;

-- Step 4: Drop old table
DROP TABLE packages;

-- Step 5: Rename new table
ALTER TABLE packages_new RENAME TO packages;

-- Step 6: Recreate indexes
CREATE INDEX idx_packages_product ON packages(product_id);
CREATE INDEX idx_packages_supplier ON packages(supplier_id);
CREATE INDEX idx_packages_category ON packages(category_id);
CREATE INDEX idx_packages_location ON packages(location_id);

-- Step 7: Recreate views
CREATE VIEW v_expiring AS
SELECT 
    p.description AS product_name,
    pk.packaging,
    b.batch_id,
    b.description AS lot,
    b.expiration,
    CAST(julianday(b.expiration) - julianday('now') AS INTEGER) AS days_left,
    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS labels_in_stock
FROM batches b
JOIN packages pk ON pk.package_id = b.package_id
JOIN products p ON p.product_id = pk.product_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
WHERE b.expiration IS NOT NULL
GROUP BY b.batch_id
ORDER BY b.expiration;

CREATE VIEW v_open_requests AS
SELECT 
    r.request_id,
    r.reference,
    r.issued,
    COUNT(i.item_id) AS total_items,
    SUM(i.quantity) AS total_qty,
    COALESCE(SUM(d.quantity), 0) AS delivered_qty
FROM requests r
JOIN items i ON i.request_id = r.request_id
LEFT JOIN deliveries d ON d.item_id = i.item_id
WHERE r.status = 1
GROUP BY r.request_id;

CREATE VIEW v_stock AS
SELECT 
    p.product_id,
    p.reference AS product_code,
    p.description AS product_name,
    pk.package_id,
    pk.reference AS supplier_code,
    pk.packaging,
    s.description AS supplier,
    c.description AS category,
    l.description AS location,
    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock,
    COUNT(CASE WHEN lb.status = 0 THEN 1 END) AS used,
    COUNT(CASE WHEN lb.status = -1 THEN 1 END) AS cancelled
FROM products p
JOIN packages pk ON pk.product_id = p.product_id
LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
LEFT JOIN categories c ON c.category_id = pk.category_id
LEFT JOIN locations l ON l.location_id = pk.location_id
LEFT JOIN batches b ON b.package_id = pk.package_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
GROUP BY pk.package_id;

COMMIT;
PRAGMA foreign_keys = ON;

-- Verify
SELECT 'Migration completed. Packages table now has ' || COUNT(*) || ' rows.' FROM packages;