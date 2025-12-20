-- Demo data for Inventarium
-- This creates sample data for testing and demonstration purposes

-- Clear existing data (if any)
DELETE FROM deliveries;
DELETE FROM items;
DELETE FROM requests;
DELETE FROM labels;
DELETE FROM batches;
DELETE FROM packages;
DELETE FROM products;
DELETE FROM suppliers;
DELETE FROM categories;
DELETE FROM conservations;
DELETE FROM locations;
DELETE FROM funding_sources;

-- Reset sequences
DELETE FROM sqlite_sequence;

-- =============================================================================
-- Categories (reference_id: 1=Products, 2=Locations)
-- =============================================================================
INSERT INTO categories (category_id, reference_id, description, status) VALUES
(1, 1, 'Reagenti Chimici', 1),
(2, 1, 'Standard di Riferimento', 1),
(3, 1, 'Solventi', 1),
(4, 1, 'Gas Tecnici', 1),
(5, 1, 'Consumabili', 1),
(6, 2, 'Armadio Reagenti', 1),
(7, 2, 'Frigorifero', 1),
(8, 2, 'Congelatore', 1);

-- =============================================================================
-- Conservations (Storage conditions)
-- =============================================================================
INSERT INTO conservations (conservation_id, description, status) VALUES
(1, 'Temperatura ambiente (15-25°C)', 1),
(2, 'Refrigerato (2-8°C)', 1),
(3, 'Congelato (-20°C)', 1),
(4, 'Congelato (-80°C)', 1),
(5, 'Sotto azoto', 1);

-- =============================================================================
-- Locations
-- =============================================================================
INSERT INTO locations (location_id, code, room, description, category_id, conservation_id, status) VALUES
(1, 'ARM-01', 'Lab Spettrometria', 'Armadio reagenti principale', 6, 1, 1),
(2, 'FRG-01', 'Lab Spettrometria', 'Frigorifero Liebherr', 7, 2, 1),
(3, 'FRZ-01', 'Lab Spettrometria', 'Congelatore -20', 8, 3, 1),
(4, 'ARM-02', 'Lab Spettrometria', 'Armadio solventi', 6, 1, 1),
(5, 'FRZ-02', 'Lab Spettrometria', 'Congelatore -80 Thermo', 8, 4, 1);

-- =============================================================================
-- Funding Sources
-- =============================================================================
INSERT INTO funding_sources (funding_id, code, description, status) VALUES
(1, 'ORD', 'Budget Ordinario', 1),
(2, 'PRJ-001', 'Progetto Ricerca Alpha', 1),
(3, 'PRJ-002', 'Progetto EU Horizon', 1);

-- =============================================================================
-- Suppliers
-- =============================================================================
INSERT INTO suppliers (supplier_id, description, reference, status) VALUES
(1, 'Sigma-Aldrich', 'SIGMA', 1),
(2, 'Thermo Fisher Scientific', 'THERMO', 1),
(3, 'VWR International', 'VWR', 1),
(4, 'Merck KGaA', 'MERCK', 1),
(5, 'Agilent Technologies', 'AGILENT', 1),
(6, 'Waters Corporation', 'WATERS', 1);

-- =============================================================================
-- Products
-- =============================================================================
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
(11, 'COL-C18', 'Colonna C18 150x2.1mm 1.8um', 1),
(12, 'COL-HILIC', 'Colonna HILIC 100x2.1mm 1.7um', 1),
(13, 'VIAL-2ML', 'Vials 2mL amber with cap', 1),
(14, 'FILT-02', 'Filtri siringa 0.2um PVDF', 1),
(15, 'TIP-1000', 'Puntali 1000uL filter tips', 1);

-- =============================================================================
-- Packages (SKUs linking products to suppliers)
-- =============================================================================
INSERT INTO packages (package_id, product_id, supplier_id, reference, labels, packaging, conservation_id, in_the_dark, category_id, location_id, order_by_piece, pieces_per_label, reorder, funding_id, status) VALUES
-- Solventi
(1, 1, 1, '34851-2.5L', 1, '2.5L', 1, 0, 3, 4, 1, 1, 2, 1, 1),
(2, 2, 1, '34860-2.5L', 1, '2.5L', 1, 0, 3, 4, 1, 1, 2, 1, 1),
(3, 3, 2, 'W6-4', 1, '4L', 1, 0, 3, 4, 1, 1, 2, 1, 1),
(4, 4, 1, '56302-50ML', 1, '50mL', 1, 0, 1, 1, 1, 1, 1, 1, 1),
(5, 5, 1, '45754-100ML', 1, '100mL', 1, 0, 1, 1, 1, 1, 1, 1, 1),
-- Sali
(6, 6, 4, '1.01116.0500', 1, '500g', 1, 0, 1, 1, 1, 1, 1, 1, 1),
(7, 7, 1, '09830-500G', 1, '500g', 1, 0, 1, 1, 1, 1, 1, 1, 1),
-- Standards
(8, 8, 1, 'C0750-1ML', 1, '1mL', 2, 1, 2, 2, 1, 1, 2, 2, 1),
(9, 9, 1, 'PHR1005-1ML', 1, '1mL', 2, 1, 2, 2, 1, 1, 2, 2, 1),
(10, 10, 1, 'PHR1004-1ML', 1, '1mL', 2, 1, 2, 2, 1, 1, 2, 2, 1),
-- Colonne
(11, 11, 5, '959758-902', 1, '1 pz', 1, 0, 5, 1, 1, 1, 1, 1, 1),
(12, 12, 6, '186003462', 1, '1 pz', 1, 0, 5, 1, 1, 1, 1, 1, 1),
-- Consumabili
(13, 13, 3, '548-0053', 100, 'Box 100', 1, 0, 5, 1, 0, 100, 1, 1, 1),
(14, 14, 3, '514-0061', 100, 'Box 100', 1, 0, 5, 1, 0, 100, 1, 1, 1),
(15, 15, 3, '613-2697', 96, 'Rack 96', 1, 0, 5, 1, 0, 96, 2, 1, 1);

-- =============================================================================
-- Batches (Lots)
-- =============================================================================
INSERT INTO batches (batch_id, package_id, description, expiration, status) VALUES
-- ACN
(1, 1, 'SHBM1234', '2026-06-30', 1),
(2, 1, 'SHBN5678', '2026-08-31', 1),
-- MeOH
(3, 2, 'SHBK9012', '2026-05-31', 1),
-- H2O
(4, 3, 'W6789012', '2025-12-31', 1),
-- Formic Acid
(5, 4, 'BCCD1234', '2027-01-31', 1),
-- Standards
(6, 8, 'LRAC1234', '2025-06-30', 1),
(7, 8, 'LRAC5678', '2026-03-31', 1),
(8, 9, 'PHR20234', '2025-09-30', 1),
(9, 10, 'PHR10456', '2026-01-31', 1),
-- Colonne
(10, 11, 'USGH12345', '2028-12-31', 1),
(11, 12, '0234567890', '2028-12-31', 1),
-- Vials
(12, 13, 'VL2024001', '2030-12-31', 1),
-- Filtri
(13, 14, 'FLT2024A', '2026-12-31', 1),
-- Tips
(14, 15, 'TIP2024X', '2027-06-30', 1);

-- =============================================================================
-- Labels (Stock units)
-- =============================================================================
-- ACN Lot 1 - 3 bottles, 1 used
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(1, '2024-01-15', NULL, 1),
(1, '2024-01-15', NULL, 1),
(1, '2024-01-15', '2024-06-20', 0);

-- ACN Lot 2 - 2 bottles in stock
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(2, '2024-03-10', NULL, 1),
(2, '2024-03-10', NULL, 1);

-- MeOH - 2 bottles, 1 used
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(3, '2024-02-01', NULL, 1),
(3, '2024-02-01', '2024-05-15', 0);

-- H2O - expiring soon, 1 bottle
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(4, '2024-06-01', NULL, 1);

-- Formic acid - 2 bottles
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(5, '2024-04-01', NULL, 1),
(5, '2024-04-01', NULL, 1);

-- Caffeine std - expired lot + valid lot
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(6, '2024-01-10', NULL, 1),  -- expired
(7, '2024-09-01', NULL, 1),
(7, '2024-09-01', NULL, 1);

-- Paracetamol std
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(8, '2024-03-15', NULL, 1);

-- Ibuprofen std
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(9, '2024-05-20', NULL, 1),
(9, '2024-05-20', NULL, 1);

-- C18 column - 1 unit
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(10, '2024-02-01', NULL, 1);

-- HILIC column - 1 unit
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(11, '2024-04-15', NULL, 1);

-- Vials - 3 boxes
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(12, '2024-01-01', NULL, 1),
(12, '2024-01-01', NULL, 1),
(12, '2024-01-01', '2024-08-01', 0);

-- Filtri - 2 boxes
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(13, '2024-03-01', NULL, 1),
(13, '2024-03-01', NULL, 1);

-- Tips - 4 racks, 1 used
INSERT INTO labels (batch_id, loaded, unloaded, status) VALUES
(14, '2024-02-15', NULL, 1),
(14, '2024-02-15', NULL, 1),
(14, '2024-02-15', NULL, 1),
(14, '2024-02-15', '2024-07-01', 0);

-- =============================================================================
-- Requests (Purchase orders)
-- =============================================================================
INSERT INTO requests (request_id, reference, issued, status) VALUES
(1, 'REQ-2024-001', '2024-01-10', 0),  -- Closed
(2, 'REQ-2024-002', '2024-03-15', 0),  -- Closed
(3, 'REQ-2024-003', '2024-06-01', 1),  -- Open
(4, 'REQ-2024-004', '2024-09-20', 1);  -- Open

-- =============================================================================
-- Items (Request line items)
-- =============================================================================
INSERT INTO items (item_id, request_id, package_id, quantity, status) VALUES
-- REQ-001
(1, 1, 1, 3, 1),   -- ACN x3
(2, 1, 2, 2, 1),   -- MeOH x2
-- REQ-002
(3, 2, 8, 2, 1),   -- Caffeine std x2
(4, 2, 13, 3, 1),  -- Vials x3
-- REQ-003 (open)
(5, 3, 3, 2, 1),   -- H2O x2
(6, 3, 15, 4, 1),  -- Tips x4
-- REQ-004 (open)
(7, 4, 11, 1, 1),  -- C18 column x1
(8, 4, 4, 2, 1);   -- Formic acid x2

-- =============================================================================
-- Deliveries
-- =============================================================================
INSERT INTO deliveries (delivery_id, item_id, package_id, ddt, delivered, quantity, status) VALUES
-- REQ-001 fully delivered
(1, 1, 1, 'DDT-2024-0123', '2024-01-20', 3, 1),
(2, 2, 2, 'DDT-2024-0124', '2024-01-22', 2, 1),
-- REQ-002 fully delivered
(3, 3, 8, 'DDT-2024-0456', '2024-03-25', 2, 1),
(4, 4, 13, 'DDT-2024-0457', '2024-03-25', 3, 1),
-- REQ-003 partially delivered
(5, 5, 3, 'DDT-2024-0789', '2024-06-15', 1, 1);  -- Only 1 of 2 H2O delivered

-- =============================================================================
-- Settings
-- =============================================================================
INSERT OR REPLACE INTO settings (key, value) VALUES
('company', 'Demo Hospital'),
('lab', 'Spectrometry Laboratory'),
('manager', 'Dr. Demo User'),
('room', 'Building A - Room 101'),
('phone', '+39 000 000 0000'),
('language', 'it'),
('idle_timeout', '30'),
('default_vat', '22');
