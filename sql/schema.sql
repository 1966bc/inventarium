--
-- File generated with SQLiteStudio v3.4.3 on mer dic 24 06:09:01 2025
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: batches
CREATE TABLE IF NOT EXISTS "batches" (
    batch_id INTEGER NOT NULL PRIMARY KEY,
    package_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    expiration DATE,
    status INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (package_id) REFERENCES packages(package_id)
);

-- Table: categories
CREATE TABLE IF NOT EXISTS categories (
 category_id INTEGER NOT NULL ,
 reference_id INTEGER NOT NULL,
 description TEXT NOT NULL,
 status INTEGER NOT NULL DEFAULT 1,
 PRIMARY KEY (category_id)
);

-- Table: conservations
CREATE TABLE IF NOT EXISTS conservations (
 conservation_id INTEGER NOT NULL ,
 description TEXT NOT NULL,
 status INTEGER NOT NULL DEFAULT 1,
 PRIMARY KEY (conservation_id)
);

-- Table: deliberations
CREATE TABLE IF NOT EXISTS deliberations (
    deliberation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference VARCHAR(50) NOT NULL,
    issued DATE,
    description VARCHAR(200),
    status INTEGER DEFAULT 1
, supplier_id INTEGER REFERENCES suppliers(supplier_id), amount REAL DEFAULT 0, cig VARCHAR(20));

-- Table: deliveries
CREATE TABLE IF NOT EXISTS "deliveries" (
    delivery_id INTEGER NOT NULL PRIMARY KEY,
    item_id INTEGER NOT NULL,
    package_id INTEGER NOT NULL,
    ddt TEXT NOT NULL DEFAULT 'N/D',
    delivered TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity INTEGER NOT NULL,
    status INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (package_id) REFERENCES packages(package_id)
);

-- Table: funding_sources
CREATE TABLE IF NOT EXISTS funding_sources (
    funding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(10) NOT NULL,
    description VARCHAR(100) NOT NULL,
    status INTEGER DEFAULT 1
);

-- Table: items
CREATE TABLE IF NOT EXISTS "items" (
    item_id INTEGER NOT NULL PRIMARY KEY,
    request_id INTEGER NOT NULL,
    package_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    status INTEGER NOT NULL DEFAULT 1, note TEXT DEFAULT NULL,
    FOREIGN KEY (request_id) REFERENCES requests(request_id),
    FOREIGN KEY (package_id) REFERENCES packages(package_id)
);

-- Table: labels
CREATE TABLE IF NOT EXISTS "labels" (
    label_id INTEGER NOT NULL PRIMARY KEY,
    batch_id INTEGER NOT NULL,
    loaded DATE DEFAULT CURRENT_DATE,
    unloaded DATE,
    status INTEGER NOT NULL DEFAULT 1, tick INTEGER,
    FOREIGN KEY (batch_id) REFERENCES batches(batch_id)
);

-- Table: locations
CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER NOT NULL PRIMARY KEY,
    category_id INTEGER,
    code TEXT,
    room TEXT,
    description TEXT NOT NULL,
    conservation_id INTEGER,
    status INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (conservation_id) REFERENCES conservations(conservation_id)
);

-- Table: package_fundings
CREATE TABLE IF NOT EXISTS package_fundings (
    package_funding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    funding_id INTEGER NOT NULL,
    deliberation_id INTEGER,
    valid_from DATE,
    status INTEGER DEFAULT 1,
    FOREIGN KEY (package_id) REFERENCES packages(package_id),
    FOREIGN KEY (funding_id) REFERENCES funding_sources(funding_id),
    FOREIGN KEY (deliberation_id) REFERENCES deliberations(deliberation_id)
);

-- Table: packages
CREATE TABLE IF NOT EXISTS "packages" (
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
    status INTEGER NOT NULL DEFAULT 1, order_by_piece INTEGER NOT NULL DEFAULT 1, pieces_per_label INTEGER NOT NULL DEFAULT 1, reorder INTEGER NOT NULL DEFAULT 0, funding_id INTEGER REFERENCES funding_sources(funding_id), labels_per_unit INTEGER DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (conservation_id) REFERENCES conservations(conservation_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Table: prices
CREATE TABLE IF NOT EXISTS prices (
    price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    price REAL NOT NULL,
    vat REAL DEFAULT 10,
    valid_from DATE NOT NULL,
    status INTEGER DEFAULT 1,
    FOREIGN KEY (package_id) REFERENCES packages(package_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- Table: products
CREATE TABLE IF NOT EXISTS "products" (
    product_id INTEGER NOT NULL PRIMARY KEY,
    reference TEXT NOT NULL,
    description TEXT NOT NULL,
    status INTEGER NOT NULL DEFAULT 1
);

-- Table: requests
CREATE TABLE IF NOT EXISTS "requests" (
    request_id INTEGER NOT NULL PRIMARY KEY,
    reference TEXT NOT NULL,
    issued DATE DEFAULT NULL,
    status INTEGER NOT NULL DEFAULT 1
);

-- Table: settings
CREATE TABLE IF NOT EXISTS settings (
    setting_id INTEGER PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    description TEXT
);

-- Table: suppliers
CREATE TABLE IF NOT EXISTS suppliers (
 supplier_id INTEGER NOT NULL ,
 description TEXT DEFAULT NULL,
 reference TEXT DEFAULT NULL,
 status INTEGER NOT NULL DEFAULT 1,
 PRIMARY KEY (supplier_id)
);

-- Index: idx_batches_expiration
CREATE INDEX IF NOT EXISTS idx_batches_expiration ON batches(expiration);

-- Index: idx_batches_package
CREATE INDEX IF NOT EXISTS idx_batches_package ON batches(package_id);

-- Index: idx_categories_unique
CREATE UNIQUE INDEX IF NOT EXISTS idx_categories_unique 
ON categories(reference_id, description);

-- Index: idx_deliveries_item
CREATE INDEX IF NOT EXISTS idx_deliveries_item ON deliveries(item_id);

-- Index: idx_items_package
CREATE INDEX IF NOT EXISTS idx_items_package ON items(package_id);

-- Index: idx_items_request
CREATE INDEX IF NOT EXISTS idx_items_request ON items(request_id);

-- Index: idx_labels_batch
CREATE INDEX IF NOT EXISTS idx_labels_batch ON labels(batch_id);

-- Index: idx_labels_status
CREATE INDEX IF NOT EXISTS idx_labels_status ON labels(status);

-- Index: idx_packages_category
CREATE INDEX IF NOT EXISTS idx_packages_category ON packages(category_id);

-- Index: idx_packages_location
CREATE INDEX IF NOT EXISTS idx_packages_location ON packages(location_id);

-- Index: idx_packages_product
CREATE INDEX IF NOT EXISTS idx_packages_product ON packages(product_id);

-- Index: idx_packages_supplier
CREATE INDEX IF NOT EXISTS idx_packages_supplier ON packages(supplier_id);

-- Index: idx_prices_package
CREATE INDEX IF NOT EXISTS idx_prices_package ON prices(package_id);

-- Index: idx_prices_supplier
CREATE INDEX IF NOT EXISTS idx_prices_supplier ON prices(supplier_id);

-- Index: idx_products_description_unique
CREATE UNIQUE INDEX IF NOT EXISTS idx_products_description_unique ON products(description);

-- Index: idx_products_reference_unique
CREATE UNIQUE INDEX IF NOT EXISTS idx_products_reference_unique 
ON products(reference);

-- Index: idx_suppliers_description_unique
CREATE UNIQUE INDEX IF NOT EXISTS idx_suppliers_description_unique 
ON suppliers(description);

-- View: v_expiring
CREATE VIEW IF NOT EXISTS v_expiring AS
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

-- View: v_open_requests
CREATE VIEW IF NOT EXISTS v_open_requests AS
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

-- View: v_stock
CREATE VIEW IF NOT EXISTS v_stock AS
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

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
