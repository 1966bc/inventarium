-- =============================================================================
-- Inventarium - Demo Database
-- This file creates the complete database schema and populates it with demo data
-- Execute this file to create a new empty database with sample data
-- =============================================================================

-- Speed up initial creation (safe for new database)
PRAGMA synchronous = OFF;
PRAGMA journal_mode = MEMORY;

PRAGMA foreign_keys = OFF;

-- =============================================================================
-- SCHEMA: Tables
-- =============================================================================

CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER NOT NULL PRIMARY KEY,
    reference_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    status INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS conservations (
    conservation_id INTEGER NOT NULL PRIMARY KEY,
    description TEXT NOT NULL,
    status INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER NOT NULL PRIMARY KEY,
    description TEXT DEFAULT NULL,
    reference TEXT DEFAULT NULL,
    status INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER NOT NULL PRIMARY KEY,
    reference TEXT NOT NULL,
    description TEXT NOT NULL,
    status INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS requests (
    request_id INTEGER NOT NULL PRIMARY KEY,
    reference TEXT NOT NULL,
    issued DATE DEFAULT NULL,
    status INTEGER NOT NULL DEFAULT 1
);

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

CREATE TABLE IF NOT EXISTS funding_sources (
    funding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(10) NOT NULL,
    description VARCHAR(100) NOT NULL,
    status INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS deliberations (
    deliberation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference VARCHAR(50) NOT NULL,
    issued DATE,
    description VARCHAR(200),
    supplier_id INTEGER REFERENCES suppliers(supplier_id),
    amount REAL DEFAULT 0,
    cig VARCHAR(20),
    status INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS packages (
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

CREATE TABLE IF NOT EXISTS batches (
    batch_id INTEGER NOT NULL PRIMARY KEY,
    package_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    expiration DATE,
    status INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (package_id) REFERENCES packages(package_id)
);

CREATE TABLE IF NOT EXISTS labels (
    label_id INTEGER NOT NULL PRIMARY KEY,
    batch_id INTEGER NOT NULL,
    loaded DATE DEFAULT CURRENT_DATE,
    unloaded DATE,
    tick INTEGER,
    status INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (batch_id) REFERENCES batches(batch_id)
);

CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER NOT NULL PRIMARY KEY,
    request_id INTEGER NOT NULL,
    package_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    note TEXT DEFAULT NULL,
    status INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (request_id) REFERENCES requests(request_id),
    FOREIGN KEY (package_id) REFERENCES packages(package_id)
);

CREATE TABLE IF NOT EXISTS deliveries (
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

CREATE TABLE IF NOT EXISTS settings (
    setting_id INTEGER PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    description TEXT
);

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

CREATE TABLE IF NOT EXISTS memos (
    memo_id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    status INTEGER DEFAULT 1  -- 1=active, 0=done
);

-- =============================================================================
-- SCHEMA: Indexes
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_packages_product ON packages(product_id);
CREATE INDEX IF NOT EXISTS idx_packages_supplier ON packages(supplier_id);
CREATE INDEX IF NOT EXISTS idx_packages_category ON packages(category_id);
CREATE INDEX IF NOT EXISTS idx_packages_location ON packages(location_id);
CREATE INDEX IF NOT EXISTS idx_batches_package ON batches(package_id);
CREATE INDEX IF NOT EXISTS idx_batches_expiration ON batches(expiration);
CREATE INDEX IF NOT EXISTS idx_labels_batch ON labels(batch_id);
CREATE INDEX IF NOT EXISTS idx_labels_status ON labels(status);
CREATE INDEX IF NOT EXISTS idx_items_request ON items(request_id);
CREATE INDEX IF NOT EXISTS idx_items_package ON items(package_id);
CREATE INDEX IF NOT EXISTS idx_deliveries_item ON deliveries(item_id);
CREATE INDEX IF NOT EXISTS idx_prices_package ON prices(package_id);
CREATE INDEX IF NOT EXISTS idx_prices_supplier ON prices(supplier_id);
CREATE INDEX IF NOT EXISTS idx_memos_status ON memos(status);

CREATE UNIQUE INDEX IF NOT EXISTS idx_categories_unique ON categories(reference_id, description);
CREATE UNIQUE INDEX IF NOT EXISTS idx_products_reference_unique ON products(reference);
CREATE UNIQUE INDEX IF NOT EXISTS idx_products_description_unique ON products(description);
CREATE UNIQUE INDEX IF NOT EXISTS idx_suppliers_description_unique ON suppliers(description);

-- =============================================================================
-- SCHEMA: Views
-- =============================================================================

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

-- =============================================================================
-- DEMO DATA
-- =============================================================================

BEGIN TRANSACTION;

-- Categories (reference_id groups categories)
INSERT INTO categories (category_id, reference_id, description, status) VALUES
(1, 1, 'Reagents', 1),
(2, 1, 'Standards & Controls', 1),
(3, 1, 'Solvents', 1),
(4, 2, 'Equipment', 1),
(5, 2, 'Consumables', 1),
(6, 3, 'Archived', 0);

-- Conservations (storage conditions)
INSERT INTO conservations (conservation_id, description, status) VALUES
(1, 'Room temperature (15-25°C)', 1),
(2, 'Refrigerated (2-8°C)', 1),
(3, 'Frozen (-20°C)', 1),
(4, 'Deep frozen (-80°C)', 1);

-- Suppliers
INSERT INTO suppliers (supplier_id, description, reference, status) VALUES
(1, 'Sigma-Aldrich', 'SA', 1),
(2, 'Honeywell', 'HW', 1),
(3, 'VWR International', 'VWR', 1),
(4, 'Merck', 'MRK', 1),
(5, 'Agilent Technologies', 'AGI', 1),
(6, 'Waters Corporation', 'WAT', 1),
(7, 'Chromsystems', 'CHR', 1),
(8, 'Abbott Diagnostics', 'ABT', 1);

-- Locations
INSERT INTO locations (location_id, category_id, code, room, description, conservation_id, status) VALUES
(1, 1, 'A1-01', 'Lab 101', 'Main reagent cabinet', 1, 1),
(2, 2, 'B2-01', 'Lab 101', 'Standards refrigerator', 2, 1),
(3, 3, 'C1-01', 'Lab 102', 'Solvent cabinet', 1, 1),
(4, 3, 'C2-01', 'Lab 102', 'Flammables cabinet', 1, 1),
(5, 5, 'D1-01', 'Storage', 'Consumables shelf', 1, 1);

-- Funding sources
INSERT INTO funding_sources (funding_id, code, description, status) VALUES
(1, 'ORD', 'Ordinary Budget', 1),
(2, 'RES', 'Research Funds', 1),
(3, 'EXT', 'External Funding', 1),
(4, 'IVD', 'IVD Diagnostics', 1);

-- Deliberations (procurement acts)
INSERT INTO deliberations (deliberation_id, reference, issued, description, supplier_id, amount, cig, status) VALUES
(1, 'DEL-2024-0045', '2024-01-15', 'Gara reagenti e solventi per laboratorio', 1, 85000.00, 'Z4F3A2B1C0D9', 1),
(2, 'DEL-2024-0126', '2024-01-20', 'Gara materiale di consumo laboratorio', 3, 45000.00, 'Z5G4B3C2D1E0', 1),
(3, 'DEL-2024-0340', '2024-03-10', 'Gara colonne cromatografiche e accessori', 5, 120000.00, 'Z6H5C4D3E2F1', 1),
(4, 'DEL-2024-0455', '2024-04-25', 'Gara standard certificati IVD', 7, 65000.00, 'Z7I6D5E4F3G2', 1),
(5, 'DEL-2024-0670', '2024-06-15', 'Gara diagnostici Abbott 2024-2027', 8, 250000.00, 'Z8J7E6F5G4H3', 1),
(6, 'DEL-2024-0890', '2024-09-01', 'Acquisto diretto materiali urgenti', NULL, 5000.00, NULL, 1),
(7, 'DEL-2024-1010', '2024-10-15', 'Acquisto economato piccole forniture', NULL, 3500.00, NULL, 1);

-- Products
INSERT INTO products (product_id, reference, description, status) VALUES
(1, 'ACN-HPLC', 'Acetonitrile HPLC Grade', 1),
(2, 'MEOH-HPLC', 'Methanol HPLC Grade', 1),
(3, 'H2O-LCMS', 'Water LC-MS Grade', 1),
(4, 'FA-LCMS', 'Formic Acid LC-MS Grade', 1),
(5, 'AA-LCMS', 'Acetic Acid LC-MS Grade', 1),
(6, 'NH4AC', 'Ammonium Acetate', 1),
(7, 'NH4HCO3', 'Ammonium Bicarbonate', 1),
(8, 'STD-CAF', 'Caffeine Standard 1mg/mL', 1),
(9, 'STD-PAR', 'Paracetamol Standard 1mg/mL', 1),
(10, 'STD-IBU', 'Ibuprofen Standard 1mg/mL', 1),
(11, 'COL-C18', 'C18 Column 150x2.1mm 1.8um', 1),
(12, 'COL-HILIC', 'HILIC Column 100x2.1mm 1.7um', 1),
(13, 'VIAL-2ML', 'Vials 2mL amber with cap', 1),
(14, 'FILT-02', 'Syringe filters 0.2um PVDF', 1),
(15, 'TIP-1000', 'Pipette tips 1000uL filtered', 1),
(16, 'MMA-KIT', 'MassChrom Amino Acids Kit', 1),
(17, 'VIT-D', 'Vitamin D Calibrator Set', 1),
(18, 'CTRL-ABB', 'Abbott Multichem Control', 1);

-- Packages (with commercial_name and status as last field)
INSERT INTO packages (package_id, product_id, supplier_id, reference, labels, packaging, conservation_id, in_the_dark, category_id, location_id, order_by_piece, pieces_per_label, labels_per_unit, reorder, funding_id, label_text, label_font_size, shelf, commercial_name, status) VALUES
(1, 1, 1, '34851-2.5L', 1, '2.5L', 1, 0, 3, 4, 1, 1, 1, 2, 1, 'ACETONITRILE HPLC', 44, '1', 'Chromasolv Plus for HPLC', 1),
(2, 2, 1, '34860-2.5L', 1, '2.5L', 1, 0, 3, 4, 1, 1, 1, 2, 1, 'METHANOL HPLC', 44, '1', 'Chromasolv for HPLC', 1),
(3, 3, 2, 'W6-4', 1, '4L', 1, 0, 3, 4, 1, 1, 1, 2, 1, 'WATER LC-MS', 44, '2', 'LC-MS Chromasolv', 1),
(4, 4, 1, '56302-50ML', 1, '50mL', 1, 0, 1, 1, 1, 1, 1, 1, 1, 'FORMIC ACID', 44, '1', NULL, 1),
(5, 5, 1, '45754-100ML', 1, '100mL', 1, 0, 1, 1, 1, 1, 1, 1, 1, 'ACETIC ACID', 44, '1', NULL, 1),
(6, 6, 4, '1.01116.0500', 1, '500g', 1, 0, 1, 1, 1, 1, 1, 1, 1, NULL, 36, '2', NULL, 1),
(7, 7, 1, '09830-500G', 1, '500g', 1, 0, 1, 1, 1, 1, 1, 1, 1, NULL, 36, '2', NULL, 1),
(8, 8, 1, 'C0750-1ML', 1, '1mL', 2, 1, 2, 2, 1, 1, 1, 2, 2, 'CAFFEINE STD', 40, '1', 'Caffeine analytical standard', 1),
(9, 9, 1, 'PHR1005-1ML', 1, '1mL', 2, 1, 2, 2, 1, 1, 1, 2, 2, 'PARACETAMOL STD', 40, '1', 'Paracetamol pharmaceutical secondary standard', 1),
(10, 10, 1, 'PHR1004-1ML', 1, '1mL', 2, 1, 2, 2, 1, 1, 1, 2, 2, 'IBUPROFEN STD', 40, '1', 'Ibuprofen pharmaceutical secondary standard', 1),
(11, 11, 5, '959758-902', 1, '1 pc', 1, 0, 5, 1, 1, 1, 1, 1, 1, 'COLONNA C18', 44, '3', 'ZORBAX Eclipse Plus C18 RRHD', 1),
(12, 12, 6, '186003462', 1, '1 pc', 1, 0, 5, 1, 1, 1, 1, 1, 1, 'COLONNA HILIC', 44, '3', 'ACQUITY UPLC BEH HILIC', 1),
(13, 13, 3, '548-0053', 100, 'Box 100', 1, 0, 5, 1, 0, 100, 1, 1, 1, 'VIALS 2ML', 44, '4', NULL, 1),
(14, 14, 3, '514-0061', 100, 'Box 100', 1, 0, 5, 1, 0, 100, 1, 1, 1, 'FILTRI 0.2um', 44, '4', NULL, 1),
(15, 15, 3, '613-2697', 96, 'Rack 96', 1, 0, 5, 1, 0, 96, 1, 2, 1, 'TIPS 1000uL', 44, '4', NULL, 1),
(16, 16, 7, '55000', 1, 'Kit 100 tests', 2, 1, 2, 2, 1, 1, 1, 1, 4, 'KIT AMINOACIDI', 40, '2', 'MassChrom Amino Acids and Acylcarnitines', 1),
(17, 17, 7, '62000', 1, 'Set 6x1mL', 2, 1, 2, 2, 1, 1, 1, 2, 4, 'CALIBRATORI VIT D', 36, '2', 'MassChrom 25-OH-Vitamin D3/D2 Calibrator Set', 1),
(18, 18, 8, '09P2301', 1, 'Kit 4x5mL', 2, 0, 2, 2, 1, 1, 1, 2, 1, 'CONTROLLI ABBOTT', 40, '3', 'Multichem S Plus', 1);

-- Prices
INSERT INTO prices (price_id, package_id, supplier_id, price, vat, valid_from, status) VALUES
(1, 1, 1, 125.50, 22, '2024-01-01', 1),
(2, 2, 1, 98.00, 22, '2024-01-01', 1),
(3, 3, 2, 85.00, 22, '2024-01-01', 1),
(4, 4, 1, 45.00, 22, '2024-01-01', 1),
(5, 5, 1, 52.00, 22, '2024-01-01', 1),
(6, 6, 4, 65.00, 22, '2024-01-01', 1),
(7, 7, 1, 42.00, 22, '2024-01-01', 1),
(8, 8, 1, 180.00, 22, '2024-01-01', 1),
(9, 9, 1, 175.00, 22, '2024-01-01', 1),
(10, 10, 1, 175.00, 22, '2024-01-01', 1),
(11, 11, 5, 850.00, 22, '2024-01-01', 1),
(12, 12, 6, 920.00, 22, '2024-01-01', 1),
(13, 13, 3, 45.00, 22, '2024-01-01', 1),
(14, 14, 3, 85.00, 22, '2024-01-01', 1),
(15, 15, 3, 32.00, 22, '2024-01-01', 1),
(16, 16, 7, 1250.00, 22, '2024-01-01', 1),
(17, 17, 7, 485.00, 22, '2024-01-01', 1),
(18, 18, 8, 320.00, 22, '2024-01-01', 1),
(19, 1, 1, 115.00, 22, '2023-01-01', 0),
(20, 11, 5, 780.00, 22, '2023-01-01', 0);

-- Package Fundings
INSERT INTO package_fundings (package_funding_id, package_id, funding_id, deliberation_id, valid_from, status) VALUES
(1, 1, 1, 1, '2024-01-15', 1),
(2, 2, 1, 1, '2024-01-15', 1),
(3, 3, 1, 1, '2024-01-15', 1),
(4, 4, 1, 1, '2024-01-15', 1),
(5, 5, 1, 1, '2024-01-15', 1),
(6, 6, 1, 1, '2024-01-15', 1),
(7, 7, 1, 1, '2024-01-15', 1),
(8, 8, 2, 1, '2024-01-15', 1),
(9, 9, 2, 1, '2024-01-15', 1),
(10, 10, 2, 1, '2024-01-15', 1),
(11, 13, 1, 2, '2024-01-20', 1),
(12, 14, 1, 2, '2024-01-20', 1),
(13, 15, 1, 2, '2024-01-20', 1),
(14, 11, 1, 3, '2024-03-10', 1),
(15, 12, 1, 3, '2024-03-10', 1),
(16, 16, 4, 4, '2024-04-25', 1),
(17, 17, 4, 4, '2024-04-25', 1),
(18, 18, 1, 5, '2024-06-15', 1);

-- Batches (Lots)
INSERT INTO batches (batch_id, package_id, description, expiration, status) VALUES
(1, 1, 'SHBM1234', '2026-06-30', 1),
(2, 1, 'SHBN5678', '2026-08-31', 1),
(3, 2, 'SHBK9012', '2026-05-31', 1),
(4, 3, 'W6789012', '2025-12-31', 1),
(5, 4, 'BCCD1234', '2027-01-31', 1),
(6, 8, 'LRAC1234', '2025-06-30', 1),
(7, 8, 'LRAC5678', '2026-03-31', 1),
(8, 9, 'PHR20234', '2025-09-30', 1),
(9, 10, 'PHR10456', '2026-01-31', 1),
(10, 11, 'USGH12345', '2028-12-31', 1),
(11, 12, '0234567890', '2028-12-31', 1),
(12, 13, 'VL2024001', '2030-12-31', 1),
(13, 14, 'FLT2024A', '2026-12-31', 1),
(14, 15, 'TIP2024X', '2027-06-30', 1),
(15, 16, 'CS240501', '2025-05-31', 1),
(16, 17, 'CS240612', '2025-12-31', 1),
(17, 18, 'ABT2024A', '2025-08-31', 1);

-- Labels (Stock units with barcode tick - timestamp in microseconds)
INSERT INTO labels (batch_id, loaded, unloaded, tick, status) VALUES
(1, '2024-01-15', NULL, 1705312800123456, 1),
(1, '2024-01-15', NULL, 1705312801234567, 1),
(1, '2024-01-15', '2024-06-20', 1705312802345678, 0),
(2, '2024-03-10', NULL, 1710028800456789, 1),
(2, '2024-03-10', NULL, 1710028801567890, 1),
(3, '2024-02-01', NULL, 1706745600678901, 1),
(3, '2024-02-01', '2024-05-15', 1706745601789012, 0),
(4, '2024-06-01', NULL, 1717200000890123, 1),
(5, '2024-04-01', NULL, 1711929600901234, 1),
(5, '2024-04-01', NULL, 1711929601012345, 1),
(6, '2024-01-10', NULL, 1704844800123456, 1),
(7, '2024-09-01', NULL, 1725148800234567, 1),
(7, '2024-09-01', NULL, 1725148801345678, 1),
(8, '2024-03-15', NULL, 1710460800456789, 1),
(9, '2024-05-20', NULL, 1716163200567890, 1),
(9, '2024-05-20', NULL, 1716163201678901, 1),
(10, '2024-02-01', NULL, 1706745602789012, 1),
(11, '2024-04-15', NULL, 1713139200890123, 1),
(12, '2024-01-01', NULL, 1704067200901234, 1),
(12, '2024-01-01', NULL, 1704067201012345, 1),
(12, '2024-01-01', '2024-08-01', 1704067202123456, 0),
(13, '2024-03-01', NULL, 1709251200234567, 1),
(13, '2024-03-01', NULL, 1709251201345678, 1),
(14, '2024-02-15', NULL, 1707955200456789, 1),
(14, '2024-02-15', NULL, 1707955201567890, 1),
(14, '2024-02-15', NULL, 1707955202678901, 1),
(14, '2024-02-15', '2024-07-01', 1707955203789012, 0),
(15, '2024-05-10', NULL, 1715299200890123, 1),
(15, '2024-05-10', NULL, 1715299201901234, 1),
(16, '2024-06-20', NULL, 1718841600012345, 1),
(17, '2024-07-01', NULL, 1719792000123456, 1),
(17, '2024-07-01', NULL, 1719792001234567, 1);

-- Requests (Purchase orders)
INSERT INTO requests (request_id, reference, issued, status) VALUES
(1, 'REQ-2024-001', '2024-01-10', 0),
(2, 'REQ-2024-002', '2024-03-15', 0),
(3, 'REQ-2024-003', '2024-06-01', 2),
(4, 'REQ-2024-004', '2024-09-20', 2);

-- Items (Request line items)
INSERT INTO items (item_id, request_id, package_id, quantity, note, status) VALUES
(1, 1, 1, 3, NULL, 1),
(2, 1, 2, 2, NULL, 1),
(3, 2, 8, 2, NULL, 1),
(4, 2, 13, 3, NULL, 1),
(5, 3, 3, 2, NULL, 1),
(6, 3, 15, 4, NULL, 1),
(9, 3, 6, 1, 'Product discontinued by supplier', 2),
(7, 4, 11, 1, NULL, 1),
(8, 4, 4, 2, NULL, 1);

-- Deliveries
INSERT INTO deliveries (delivery_id, item_id, package_id, ddt, delivered, quantity, status) VALUES
(1, 1, 1, 'DDT-2024-0123', '2024-01-20', 3, 1),
(2, 2, 2, 'DDT-2024-0124', '2024-01-22', 2, 1),
(3, 3, 8, 'DDT-2024-0456', '2024-03-25', 2, 1),
(4, 4, 13, 'DDT-2024-0457', '2024-03-25', 3, 1),
(5, 5, 3, 'DDT-2024-0789', '2024-06-15', 1, 1);

-- Settings
INSERT INTO settings (key, value) VALUES
('company', 'Demo Hospital'),
('lab_name', 'Spectrometry Laboratory'),
('manager', 'Dr. Demo User'),
('room', 'Building A - Room 101'),
('phone', '+1 555 000 0000'),
('language', 'en'),
('idle_timeout', '30'),
('default_vat', '22');

-- Memos (demo data with different ages)
INSERT INTO memos (text, created_at, status) VALUES
('Order nitrile gloves size M', datetime('now'), 1),
('Check acetonitrile stock level', datetime('now', '-2 days'), 1),
('Request quote for new HPLC column', datetime('now', '-5 days'), 1),
('Call supplier about delayed delivery', datetime('now', '-10 days'), 1),
('Update safety data sheets', datetime('now', '-15 days'), 0);

COMMIT;
