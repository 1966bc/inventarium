-- Demo data for Inventarium
-- This creates sample data for testing and demonstration purposes

-- Clear existing data (if any)
DELETE FROM deliveries;
DELETE FROM items;
DELETE FROM requests;
DELETE FROM labels;
DELETE FROM batches;
DELETE FROM package_fundings;
DELETE FROM prices;
DELETE FROM packages;
DELETE FROM products;
DELETE FROM deliberations;
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
(1, 1, 'Chemical Reagents', 1),
(2, 1, 'Reference Standards', 1),
(3, 1, 'Solvents', 1),
(4, 1, 'Technical Gases', 1),
(5, 1, 'Consumables', 1),
(6, 2, 'Reagent Cabinet', 1),
(7, 2, 'Refrigerator', 1),
(8, 2, 'Freezer', 1);

-- =============================================================================
-- Conservations (Storage conditions)
-- =============================================================================
INSERT INTO conservations (conservation_id, description, status) VALUES
(1, 'Room temperature (15-25°C)', 1),
(2, 'Refrigerated (2-8°C)', 1),
(3, 'Frozen (-20°C)', 1),
(4, 'Deep frozen (-80°C)', 1),
(5, 'Under nitrogen', 1);

-- =============================================================================
-- Locations
-- =============================================================================
INSERT INTO locations (location_id, code, room, description, category_id, conservation_id, status) VALUES
(1, 'CAB-01', 'Spectrometry Lab', 'Main reagent cabinet', 6, 1, 1),
(2, 'FRG-01', 'Spectrometry Lab', 'Liebherr refrigerator', 7, 2, 1),
(3, 'FRZ-01', 'Spectrometry Lab', 'Freezer -20', 8, 3, 1),
(4, 'CAB-02', 'Spectrometry Lab', 'Solvent cabinet', 6, 1, 1),
(5, 'FRZ-02', 'Spectrometry Lab', 'Thermo -80 freezer', 8, 4, 1);

-- =============================================================================
-- Funding Sources
-- =============================================================================
INSERT INTO funding_sources (funding_id, code, description, status) VALUES
(1, 'ORD', 'Regular Budget', 1),
(2, 'PRJ-001', 'Research Project Alpha', 1),
(3, 'PRJ-002', 'EU Horizon Project', 1),
(4, 'CONTO', 'Conto Capitale', 1);

-- =============================================================================
-- Suppliers
-- =============================================================================
INSERT INTO suppliers (supplier_id, description, reference, status) VALUES
(1, 'Sigma-Aldrich', 'SIGMA', 1),
(2, 'Thermo Fisher Scientific', 'THERMO', 1),
(3, 'VWR International', 'VWR', 1),
(4, 'Merck KGaA', 'MERCK', 1),
(5, 'Agilent Technologies', 'AGILENT', 1),
(6, 'Waters Corporation', 'WATERS', 1),
(7, 'ChromSystems', 'CHROMSYS', 1),
(8, 'Abbott Diagnostics', 'ABBOTT', 1);

-- =============================================================================
-- Deliberations (Tender awards and direct purchases authorization)
-- =============================================================================
INSERT INTO deliberations (deliberation_id, reference, issued, description, supplier_id, amount, cig, status) VALUES
-- Tender awards (with CIG)
(1, 'DEL-2024-0125', '2024-01-15', 'Gara solventi e reagenti chimici 2024-2026', 1, 85000.00, 'Z4F3A2B1C0D9', 1),
(2, 'DEL-2024-0126', '2024-01-20', 'Gara materiale di consumo laboratorio', 3, 45000.00, 'Z5G4B3C2D1E0', 1),
(3, 'DEL-2024-0340', '2024-03-10', 'Gara colonne cromatografiche e accessori', 5, 120000.00, 'Z6H5C4D3E2F1', 1),
(4, 'DEL-2024-0455', '2024-04-25', 'Gara standard certificati IVD', 7, 65000.00, 'Z7I6D5E4F3G2', 1),
(5, 'DEL-2024-0670', '2024-06-15', 'Gara diagnostici Abbott 2024-2027', 8, 250000.00, 'Z8J7E6F5G4H3', 1),
-- Direct purchases (no CIG - economia)
(6, 'DEL-2024-0890', '2024-09-01', 'Acquisto diretto materiali urgenti', NULL, 5000.00, NULL, 1),
(7, 'DEL-2024-1010', '2024-10-15', 'Acquisto economato piccole forniture', NULL, 3500.00, NULL, 1);

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
(11, 'COL-C18', 'C18 Column 150x2.1mm 1.8um', 1),
(12, 'COL-HILIC', 'HILIC Column 100x2.1mm 1.7um', 1),
(13, 'VIAL-2ML', 'Vials 2mL amber with cap', 1),
(14, 'FILT-02', 'Syringe filters 0.2um PVDF', 1),
(15, 'TIP-1000', 'Pipette tips 1000uL filtered', 1),
(16, 'MMA-KIT', 'MassChrom Amino Acids Kit', 1),
(17, 'VIT-D', 'Vitamin D Calibrator Set', 1),
(18, 'CTRL-ABB', 'Abbott Multichem Control', 1);

-- =============================================================================
-- Packages (SKUs linking products to suppliers)
-- =============================================================================
INSERT INTO packages (package_id, product_id, supplier_id, reference, labels, packaging, conservation_id, in_the_dark, category_id, location_id, order_by_piece, pieces_per_label, labels_per_unit, reorder, funding_id, status) VALUES
-- Solvents (Sigma)
(1, 1, 1, '34851-2.5L', 1, '2.5L', 1, 0, 3, 4, 1, 1, 1, 2, 1, 1),
(2, 2, 1, '34860-2.5L', 1, '2.5L', 1, 0, 3, 4, 1, 1, 1, 2, 1, 1),
(3, 3, 2, 'W6-4', 1, '4L', 1, 0, 3, 4, 1, 1, 1, 2, 1, 1),
(4, 4, 1, '56302-50ML', 1, '50mL', 1, 0, 1, 1, 1, 1, 1, 1, 1, 1),
(5, 5, 1, '45754-100ML', 1, '100mL', 1, 0, 1, 1, 1, 1, 1, 1, 1, 1),
-- Salts
(6, 6, 4, '1.01116.0500', 1, '500g', 1, 0, 1, 1, 1, 1, 1, 1, 1, 1),
(7, 7, 1, '09830-500G', 1, '500g', 1, 0, 1, 1, 1, 1, 1, 1, 1, 1),
-- Standards (Sigma)
(8, 8, 1, 'C0750-1ML', 1, '1mL', 2, 1, 2, 2, 1, 1, 1, 2, 2, 1),
(9, 9, 1, 'PHR1005-1ML', 1, '1mL', 2, 1, 2, 2, 1, 1, 1, 2, 2, 1),
(10, 10, 1, 'PHR1004-1ML', 1, '1mL', 2, 1, 2, 2, 1, 1, 1, 2, 2, 1),
-- Columns (Agilent, Waters)
(11, 11, 5, '959758-902', 1, '1 pc', 1, 0, 5, 1, 1, 1, 1, 1, 1, 1),
(12, 12, 6, '186003462', 1, '1 pc', 1, 0, 5, 1, 1, 1, 1, 1, 1, 1),
-- Consumables (VWR)
(13, 13, 3, '548-0053', 100, 'Box 100', 1, 0, 5, 1, 0, 100, 1, 1, 1, 1),
(14, 14, 3, '514-0061', 100, 'Box 100', 1, 0, 5, 1, 0, 100, 1, 1, 1, 1),
(15, 15, 3, '613-2697', 96, 'Rack 96', 1, 0, 5, 1, 0, 96, 1, 2, 1, 1),
-- ChromSystems products
(16, 16, 7, '55000', 1, 'Kit 100 tests', 2, 1, 2, 2, 1, 1, 1, 1, 4, 1),
(17, 17, 7, '62000', 1, 'Set 6x1mL', 2, 1, 2, 2, 1, 1, 1, 2, 4, 1),
-- Abbott products
(18, 18, 8, '09P2301', 1, 'Kit 4x5mL', 2, 0, 2, 2, 1, 1, 1, 2, 1, 1);

-- =============================================================================
-- Prices (Price list with history)
-- =============================================================================
INSERT INTO prices (price_id, package_id, supplier_id, price, vat, valid_from, status) VALUES
-- Solvents
(1, 1, 1, 125.50, 22, '2024-01-01', 1),
(2, 2, 1, 98.00, 22, '2024-01-01', 1),
(3, 3, 2, 85.00, 22, '2024-01-01', 1),
(4, 4, 1, 45.00, 22, '2024-01-01', 1),
(5, 5, 1, 52.00, 22, '2024-01-01', 1),
-- Salts
(6, 6, 4, 65.00, 22, '2024-01-01', 1),
(7, 7, 1, 42.00, 22, '2024-01-01', 1),
-- Standards
(8, 8, 1, 180.00, 22, '2024-01-01', 1),
(9, 9, 1, 175.00, 22, '2024-01-01', 1),
(10, 10, 1, 175.00, 22, '2024-01-01', 1),
-- Columns (high value)
(11, 11, 5, 850.00, 22, '2024-01-01', 1),
(12, 12, 6, 920.00, 22, '2024-01-01', 1),
-- Consumables
(13, 13, 3, 45.00, 22, '2024-01-01', 1),
(14, 14, 3, 85.00, 22, '2024-01-01', 1),
(15, 15, 3, 32.00, 22, '2024-01-01', 1),
-- ChromSystems
(16, 16, 7, 1250.00, 22, '2024-01-01', 1),
(17, 17, 7, 485.00, 22, '2024-01-01', 1),
-- Abbott
(18, 18, 8, 320.00, 22, '2024-01-01', 1),
-- Historical prices (old, inactive)
(19, 1, 1, 115.00, 22, '2023-01-01', 0),  -- Old ACN price
(20, 11, 5, 780.00, 22, '2023-01-01', 0); -- Old column price

-- =============================================================================
-- Package Fundings (Funding source assignments with deliberations)
-- =============================================================================
INSERT INTO package_fundings (package_funding_id, package_id, funding_id, deliberation_id, valid_from, status) VALUES
-- Solvents via tender DEL-2024-0125 (Sigma)
(1, 1, 1, 1, '2024-01-15', 1),   -- ACN
(2, 2, 1, 1, '2024-01-15', 1),   -- MeOH
(3, 4, 1, 1, '2024-01-15', 1),   -- Formic acid
(4, 5, 1, 1, '2024-01-15', 1),   -- Acetic acid
(5, 7, 1, 1, '2024-01-15', 1),   -- NH4HCO3
-- Water from Thermo (economia - no deliberation)
(6, 3, 1, NULL, '2024-01-01', 1),
-- Salts from Merck (economia)
(7, 6, 1, NULL, '2024-01-01', 1),
-- Standards via Research Project
(8, 8, 2, NULL, '2024-01-01', 1),   -- Caffeine
(9, 9, 2, NULL, '2024-01-01', 1),   -- Paracetamol
(10, 10, 2, NULL, '2024-01-01', 1), -- Ibuprofen
-- Consumables via tender DEL-2024-0126 (VWR)
(11, 13, 1, 2, '2024-01-20', 1),  -- Vials
(12, 14, 1, 2, '2024-01-20', 1),  -- Filters
(13, 15, 1, 2, '2024-01-20', 1),  -- Tips
-- Columns via tender DEL-2024-0340 (Agilent)
(14, 11, 1, 3, '2024-03-10', 1),  -- C18 column
(15, 12, 1, 3, '2024-03-10', 1),  -- HILIC column
-- ChromSystems via tender DEL-2024-0455
(16, 16, 4, 4, '2024-04-25', 1),  -- MMA Kit
(17, 17, 4, 4, '2024-04-25', 1),  -- Vit D Calibrator
-- Abbott via tender DEL-2024-0670
(18, 18, 1, 5, '2024-06-15', 1);  -- Multichem Control

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
-- Columns
(10, 11, 'USGH12345', '2028-12-31', 1),
(11, 12, '0234567890', '2028-12-31', 1),
-- Vials
(12, 13, 'VL2024001', '2030-12-31', 1),
-- Filters
(13, 14, 'FLT2024A', '2026-12-31', 1),
-- Tips
(14, 15, 'TIP2024X', '2027-06-30', 1),
-- ChromSystems
(15, 16, 'CS240501', '2025-05-31', 1),
(16, 17, 'CS240612', '2025-12-31', 1),
-- Abbott
(17, 18, 'ABT2024A', '2025-08-31', 1);

-- =============================================================================
-- Labels (Stock units with barcode tick)
-- =============================================================================
-- ACN Lot 1 - 3 bottles, 1 used
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(1, '2024-01-15', NULL, 1, 3785862192),
(1, '2024-01-15', NULL, 1, 1372098375),
(1, '2024-01-15', '2024-06-20', 0, 6272729586);

-- ACN Lot 2 - 2 bottles in stock
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(2, '2024-03-10', NULL, 1, 2655089979),
(2, '2024-03-10', NULL, 1, 3994891528);

-- MeOH - 2 bottles, 1 used
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(3, '2024-02-01', NULL, 1, 5244360272),
(3, '2024-02-01', '2024-05-15', 0, 9306733371);

-- H2O - expiring soon, 1 bottle
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(4, '2024-06-01', NULL, 1, 8590618074);

-- Formic acid - 2 bottles
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(5, '2024-04-01', NULL, 1, 5451473070),
(5, '2024-04-01', NULL, 1, 9351316536);

-- Caffeine std - expired lot + valid lot
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(6, '2024-01-10', NULL, 1, 4127859634),  -- expired
(7, '2024-09-01', NULL, 1, 7523648190),
(7, '2024-09-01', NULL, 1, 2846173950);

-- Paracetamol std
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(8, '2024-03-15', NULL, 1, 6391527408);

-- Ibuprofen std
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(9, '2024-05-20', NULL, 1, 1947362850),
(9, '2024-05-20', NULL, 1, 8062419375);

-- C18 column - 1 unit
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(10, '2024-02-01', NULL, 1, 5738294016);

-- HILIC column - 1 unit
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(11, '2024-04-15', NULL, 1, 3095186742);

-- Vials - 3 boxes
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(12, '2024-01-01', NULL, 1, 7284619503),
(12, '2024-01-01', NULL, 1, 4916285037),
(12, '2024-01-01', '2024-08-01', 0, 2073958146);

-- Filters - 2 boxes
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(13, '2024-03-01', NULL, 1, 8502746391),
(13, '2024-03-01', NULL, 1, 1638529470);

-- Tips - 4 racks, 1 used
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(14, '2024-02-15', NULL, 1, 9471630285),
(14, '2024-02-15', NULL, 1, 3820516974),
(14, '2024-02-15', NULL, 1, 6159382740),
(14, '2024-02-15', '2024-07-01', 0, 2748163095);

-- ChromSystems MMA Kit - 2 units
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(15, '2024-05-10', NULL, 1, 5093847261),
(15, '2024-05-10', NULL, 1, 8371629405);

-- ChromSystems Vit D - 1 unit
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(16, '2024-06-20', NULL, 1, 4628051937);

-- Abbott Control - 2 units
INSERT INTO labels (batch_id, loaded, unloaded, status, tick) VALUES
(17, '2024-07-01', NULL, 1, 7150493826),
(17, '2024-07-01', NULL, 1, 2936481570);

-- =============================================================================
-- Requests (Purchase orders)
-- Status: 0=Closed, 1=Draft, 2=Sent
-- =============================================================================
INSERT INTO requests (request_id, reference, issued, status) VALUES
(1, 'REQ-2024-001', '2024-01-10', 0),  -- Closed
(2, 'REQ-2024-002', '2024-03-15', 0),  -- Closed
(3, 'REQ-2024-003', '2024-06-01', 2),  -- Sent (partial delivery)
(4, 'REQ-2024-004', '2024-09-20', 2);  -- Sent (pending)

-- =============================================================================
-- Items (Request line items)
-- Status: 1=Active, 2=Cancelled
-- =============================================================================
INSERT INTO items (item_id, request_id, package_id, quantity, status, note) VALUES
-- REQ-001 (closed)
(1, 1, 1, 3, 1, NULL),   -- ACN x3
(2, 1, 2, 2, 1, NULL),   -- MeOH x2
-- REQ-002 (closed)
(3, 2, 8, 2, 1, NULL),   -- Caffeine std x2
(4, 2, 13, 3, 1, NULL),  -- Vials x3
-- REQ-003 (sent - partial delivery)
(5, 3, 3, 2, 1, NULL),   -- H2O x2
(6, 3, 15, 4, 1, NULL),  -- Tips x4
(9, 3, 6, 1, 2, 'Product discontinued by supplier'),  -- NH4AC cancelled
-- REQ-004 (sent - pending)
(7, 4, 11, 1, 1, NULL),  -- C18 column x1
(8, 4, 4, 2, 1, NULL);   -- Formic acid x2

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
('lab_name', 'Spectrometry Laboratory'),
('manager', 'Dr. Demo User'),
('room', 'Building A - Room 101'),
('phone', '+1 555 000 0000'),
('language', 'en'),
('idle_timeout', '30'),
('default_vat', '22');
