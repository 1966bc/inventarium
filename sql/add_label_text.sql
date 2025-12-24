-- add_label_text.sql
-- Aggiunge campi label_text e label_font_size alla tabella packages
-- Esegui con: .read add_label_text.sql

ALTER TABLE packages ADD COLUMN label_text VARCHAR(40);
ALTER TABLE packages ADD COLUMN label_font_size INTEGER DEFAULT 36;

-- Verifica
.schema packages
