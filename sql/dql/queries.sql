-- ============================================
-- INVENTARIUM - Query di controllo
-- Uso: sqlite3 inventarium.db ".read queries.sql"
-- ============================================

.headers on
.mode column

-- 1. GIACENZE (top 20)
SELECT '=== GIACENZE TOP 20 ===' AS '';
SELECT
    p.reference AS codice,
    p.description AS prodotto,
    pk.packaging AS confezione,
    s.description AS fornitore,
    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock
FROM products p
JOIN packages pk ON pk.product_id = p.product_id
LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
LEFT JOIN batches b ON b.package_id = pk.package_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
GROUP BY pk.package_id
HAVING in_stock > 0
ORDER BY in_stock DESC
LIMIT 20;

-- 2. SCADENZE PROSSIME (90 giorni)
SELECT '';
SELECT '=== SCADENZE PROSSIME 90 GG ===' AS '';
SELECT
    p.description AS prodotto,
    b.description AS lotto,
    b.expiration AS scadenza,
    CAST(julianday(b.expiration) - julianday('now') AS INTEGER) AS giorni
FROM batches b
JOIN packages pk ON pk.package_id = b.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE b.expiration IS NOT NULL
  AND b.expiration >= date('now')
  AND b.expiration <= date('now', '+90 days')
ORDER BY b.expiration
LIMIT 20;

-- 3. PRODOTTI SCADUTI
SELECT '';
SELECT '=== PRODOTTI SCADUTI ===' AS '';
SELECT
    p.description AS prodotto,
    b.description AS lotto,
    b.expiration AS scadenza,
    CAST(julianday('now') - julianday(b.expiration) AS INTEGER) AS giorni_scaduto
FROM batches b
JOIN packages pk ON pk.package_id = b.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE b.expiration < date('now')
  AND b.status = 1
ORDER BY b.expiration DESC
LIMIT 20;

-- 4. RICHIESTE APERTE
SELECT '';
SELECT '=== RICHIESTE APERTE ===' AS '';
SELECT
    r.reference AS richiesta,
    r.issued AS data,
    COUNT(i.item_id) AS righe,
    SUM(i.quantity) AS qty_ordinata,
    COALESCE(SUM(d.quantity), 0) AS qty_consegnata
FROM requests r
JOIN items i ON i.request_id = r.request_id
LEFT JOIN deliveries d ON d.item_id = i.item_id
WHERE r.status = 1
GROUP BY r.request_id
ORDER BY r.issued DESC;

-- 5. ULTIME CONSEGNE
SELECT '';
SELECT '=== ULTIME 10 CONSEGNE ===' AS '';
SELECT
    d.ddt,
    d.delivered AS data,
    p.description AS prodotto,
    d.quantity AS qty
FROM deliveries d
JOIN items i ON i.item_id = d.item_id
JOIN packages pk ON pk.package_id = i.package_id
JOIN products p ON p.product_id = pk.product_id
ORDER BY d.delivered DESC
LIMIT 10;

-- 6. FORNITORI
SELECT '';
SELECT '=== FORNITORI ===' AS '';
SELECT
    supplier_id AS id,
    description AS fornitore,
    reference AS codice
FROM suppliers
WHERE status = 1
ORDER BY description;

-- 7. CATEGORIE PRODOTTI
SELECT '';
SELECT '=== CATEGORIE PRODOTTI ===' AS '';
SELECT
    category_id AS id,
    description AS categoria
FROM categories
WHERE reference_id = 1 AND status = 1
ORDER BY description;

-- 8. CATEGORIE UBICAZIONI
SELECT '';
SELECT '=== CATEGORIE UBICAZIONI ===' AS '';
SELECT
    category_id AS id,
    description AS tipo
FROM categories
WHERE reference_id = 3 AND status = 1
ORDER BY description;

-- 9. CONSERVAZIONI
SELECT '';
SELECT '=== MODALITA CONSERVAZIONE ===' AS '';
SELECT * FROM conservations WHERE status = 1;

-- 10. STATISTICHE GENERALI
SELECT '';
SELECT '=== STATISTICHE ===' AS '';
SELECT
    (SELECT COUNT(*) FROM products WHERE status = 1) AS prodotti,
    (SELECT COUNT(*) FROM packages WHERE status = 1) AS packages,
    (SELECT COUNT(*) FROM batches WHERE status = 1) AS lotti,
    (SELECT COUNT(*) FROM labels WHERE status = 1) AS etichette_attive,
    (SELECT COUNT(*) FROM labels WHERE status = 0) AS etichette_usate,
    (SELECT COUNT(*) FROM suppliers WHERE status = 1) AS fornitori,
    (SELECT COUNT(*) FROM requests WHERE status = 1) AS richieste_aperte;
