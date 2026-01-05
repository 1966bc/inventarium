-- Add memos table for informal notes ("foglio sul frigo")
-- Run: sqlite3 inventarium.db ".read sql/ddl/add_memos.sql"

CREATE TABLE IF NOT EXISTS memos (
    memo_id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    status INTEGER DEFAULT 1  -- 1=active, 0=done
);

-- Index for quick lookup of active memos
CREATE INDEX IF NOT EXISTS idx_memos_status ON memos(status);
