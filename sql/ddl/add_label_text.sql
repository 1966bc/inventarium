-- ============================================
-- Add label_text and label_font_size columns to packages table
-- Usage: sqlite3 inventarium.db ".read ddl/add_label_text.sql"
-- ============================================

ALTER TABLE packages ADD COLUMN label_text VARCHAR(40);
ALTER TABLE packages ADD COLUMN label_font_size INTEGER DEFAULT 36;

-- Verify
.schema packages
