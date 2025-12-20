-- verify_data.sql
-- Query di verifica integrità dati dopo migrazione
-- Eseguire con: sqlite3 sql/inventarium.db ".read sql/dql/verify_data.sql"

.headers on
.mode column

-- =============================================
-- 1. CONTEGGI GENERALI
-- =============================================
SELECT '=== CONTEGGI GENERALI ===' as info;
SELECT
    (SELECT COUNT(*) FROM products) as products,
    (SELECT COUNT(*) FROM packages) as packages,
    (SELECT COUNT(*) FROM batches) as batches,
    (SELECT COUNT(*) FROM labels) as labels,
    (SELECT COUNT(*) FROM suppliers) as suppliers,
    (SELECT COUNT(*) FROM categories) as categories,
    (SELECT COUNT(*) FROM locations) as locations,
    (SELECT COUNT(*) FROM requests) as requests,
    (SELECT COUNT(*) FROM items) as items,
    (SELECT COUNT(*) FROM deliveries) as deliveries;

-- =============================================
-- 2. DUPLICATI (dovrebbero essere 0)
-- =============================================
SELECT '';
SELECT '=== VERIFICA DUPLICATI ===' as info;

SELECT 'Categories duplicati (ref_id + description):' as check_type,
       COUNT(*) as duplicates
FROM (
    SELECT reference_id, description, COUNT(*) as cnt
    FROM categories
    GROUP BY reference_id, description
    HAVING cnt > 1
);

SELECT 'Products duplicati (reference):' as check_type,
       COUNT(*) as duplicates
FROM (
    SELECT reference, COUNT(*) as cnt
    FROM products
    GROUP BY reference
    HAVING cnt > 1
);

SELECT 'Suppliers duplicati (description):' as check_type,
       COUNT(*) as duplicates
FROM (
    SELECT description, COUNT(*) as cnt
    FROM suppliers
    GROUP BY description
    HAVING cnt > 1
);

-- =============================================
-- 3. ORFANI (record senza parent - errori FK)
-- =============================================
SELECT '';
SELECT '=== VERIFICA ORFANI ===' as info;

SELECT 'Packages senza product valido:' as check_type,
       COUNT(*) as orphans
FROM packages pk
WHERE NOT EXISTS (SELECT 1 FROM products p WHERE p.product_id = pk.product_id);

SELECT 'Packages senza supplier valido:' as check_type,
       COUNT(*) as orphans
FROM packages pk
WHERE pk.supplier_id > 0
  AND NOT EXISTS (SELECT 1 FROM suppliers s WHERE s.supplier_id = pk.supplier_id);

SELECT 'Packages senza category valida:' as check_type,
       COUNT(*) as orphans
FROM packages pk
WHERE pk.category_id > 0
  AND NOT EXISTS (SELECT 1 FROM categories c WHERE c.category_id = pk.category_id);

SELECT 'Batches senza package valido:' as check_type,
       COUNT(*) as orphans
FROM batches b
WHERE NOT EXISTS (SELECT 1 FROM packages pk WHERE pk.package_id = b.package_id);

SELECT 'Labels senza batch valido:' as check_type,
       COUNT(*) as orphans
FROM labels l
WHERE NOT EXISTS (SELECT 1 FROM batches b WHERE b.batch_id = l.batch_id);

SELECT 'Items senza request valida:' as check_type,
       COUNT(*) as orphans
FROM items i
WHERE NOT EXISTS (SELECT 1 FROM requests r WHERE r.request_id = i.request_id);

SELECT 'Items senza package valido:' as check_type,
       COUNT(*) as orphans
FROM items i
WHERE NOT EXISTS (SELECT 1 FROM packages pk WHERE pk.package_id = i.package_id);

SELECT 'Deliveries senza item valido:' as check_type,
       COUNT(*) as orphans
FROM deliveries d
WHERE NOT EXISTS (SELECT 1 FROM items i WHERE i.item_id = d.item_id);

-- =============================================
-- 4. STATISTICHE STOCK
-- =============================================
SELECT '';
SELECT '=== STATISTICHE STOCK ===' as info;

SELECT 'Labels in stock (status=1):' as metric, COUNT(*) as count FROM labels WHERE status = 1
UNION ALL
SELECT 'Labels usate (status=0):', COUNT(*) FROM labels WHERE status = 0
UNION ALL
SELECT 'Labels annullate (status=-1):', COUNT(*) FROM labels WHERE status = -1;

SELECT '';
SELECT 'Products con packages:' as metric, COUNT(DISTINCT p.product_id) as count
FROM products p
WHERE EXISTS (SELECT 1 FROM packages pk WHERE pk.product_id = p.product_id);

SELECT 'Products senza packages:' as metric, COUNT(*) as count
FROM products p
WHERE NOT EXISTS (SELECT 1 FROM packages pk WHERE pk.product_id = p.product_id);

SELECT 'Packages con batches:' as metric, COUNT(DISTINCT pk.package_id) as count
FROM packages pk
WHERE EXISTS (SELECT 1 FROM batches b WHERE b.package_id = pk.package_id);

SELECT 'Packages senza batches:' as metric, COUNT(*) as count
FROM packages pk
WHERE NOT EXISTS (SELECT 1 FROM batches b WHERE b.package_id = pk.package_id);

-- =============================================
-- 5. RICHIESTE APERTE
-- =============================================
SELECT '';
SELECT '=== RICHIESTE ===' as info;

SELECT 'Richieste totali:' as metric, COUNT(*) as count FROM requests
UNION ALL
SELECT 'Richieste aperte (status=1):', COUNT(*) FROM requests WHERE status = 1
UNION ALL
SELECT 'Richieste chiuse (status=0):', COUNT(*) FROM requests WHERE status = 0;

-- =============================================
-- 6. VINCOLI UNIQUE ATTIVI
-- =============================================
SELECT '';
SELECT '=== VINCOLI UNIQUE ===' as info;
SELECT name, tbl_name
FROM sqlite_master
WHERE type='index' AND sql LIKE '%UNIQUE%';
