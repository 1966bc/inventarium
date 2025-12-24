-- fix_pending.sql
-- Chiude articoli ancora attivi in richieste già chiuse
-- Esegui con: .read fix_pending.sql

.headers on
.mode column

-- 1. Prima mostra cosa verrà modificato
SELECT '=== ARTICOLI DA CHIUDERE ===' AS info;

SELECT 
    i.item_id,
    r.reference AS richiesta,
    p.description AS prodotto
FROM items i
JOIN requests r ON r.request_id = i.request_id
JOIN packages pk ON pk.package_id = i.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE r.status = 0 AND i.status = 1;

-- 2. Conta quanti sono
SELECT '=== TOTALE ===' AS info;
SELECT COUNT(*) AS articoli_da_chiudere
FROM items i
JOIN requests r ON r.request_id = i.request_id
WHERE r.status = 0 AND i.status = 1;

-- 3. ESEGUI L'UPDATE (decommentare per eseguire)
UPDATE items SET status = 0
WHERE status = 1
AND request_id IN (SELECT request_id FROM requests WHERE status = 0);

SELECT changes() AS righe_modificate;
