-- add_shelf.sql
-- Aggiunge campo shelf (ripiano) alla tabella packages
-- Esegui con: .read add_shelf.sql

ALTER TABLE packages ADD COLUMN shelf VARCHAR(20);

-- Verifica
SELECT sql FROM sqlite_master WHERE name = 'packages';
