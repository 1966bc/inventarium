-- Migration 001: Add note column to items table
-- Date: 2025-12-23
-- Description: Add note field for cancelled items (status=2)

ALTER TABLE items ADD COLUMN note TEXT DEFAULT NULL;
