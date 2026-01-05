-- ============================================
-- Add shelf column to packages table
-- Usage: sqlite3 inventarium.db ".read ddl/add_shelf.sql"
-- ============================================

ALTER TABLE packages ADD COLUMN shelf VARCHAR(20);

-- Verify
SELECT sql FROM sqlite_master WHERE name = 'packages';
