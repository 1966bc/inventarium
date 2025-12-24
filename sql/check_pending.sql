-- check_pending.sql
-- Verifica articoli ancora attivi in richieste chiuse
-- Esegui con: .read check_pending.sql

.headers on
.mode column
.width 15 30 8 8 12

SELECT 
    r.reference AS richiesta,
    p.description AS prodotto,
    i.quantity AS ordinato,
    COALESCE((SELECT SUM(d.quantity) FROM deliveries d WHERE d.item_id = i.item_id AND d.status = 1), 0) AS evaso,
    CASE i.status 
        WHEN 0 THEN 'Chiuso'
        WHEN 1 THEN 'Attivo'
        WHEN 2 THEN 'Annullato'
    END AS stato_item
FROM items i
JOIN requests r ON r.request_id = i.request_id
JOIN packages pk ON pk.package_id = i.package_id
JOIN products p ON p.product_id = pk.product_id
WHERE r.status = 0          -- richieste chiuse
  AND i.status = 1          -- articoli ancora attivi
ORDER BY r.reference, p.description;
