# SQLite CLI - Quick Reference

A guide to using the SQLite command line interface for Inventarium database maintenance.

## Setup

1. Download `sqlite3.exe` from [sqlite.org/download.html](https://sqlite.org/download.html)
   - Section: **Precompiled Binaries for Windows**
   - File: `sqlite-tools-win-x64-*.zip`
2. Extract `sqlite3.exe` to the `sql/` folder

## Opening the Database

### Read database path from config.ini

```cmd
cd path\to\inventarium
type config.ini
```

### Open local database

```cmd
cd sql
.\sqlite3 -init setconsole inventarium.db
```

### Open network database

```cmd
cd sql
.\sqlite3 -init setconsole "\\server\share\inventarium.db"
```

### Linux

```bash
cd sql
sqlite3 -init setconsole inventarium.db
```

The `setconsole` file automatically configures:
- `.headers on` - show column headers
- `.mode column` - formatted column output
- `.timer on` - show execution time
- `.nullvalue NULL` - display NULL instead of empty

## Main Commands

| Command | Description |
|---------|-------------|
| `.tables` | List all tables |
| `.schema` | Show full database schema |
| `.schema tablename` | Show schema for specific table |
| `.indexes` | List all indexes |
| `.read file.sql` | Execute SQL script |
| `.backup file.db` | Create database backup |
| `.quit` or `.exit` | Exit SQLite |

## Useful Queries

### Quick counts

```sql
SELECT COUNT(*) FROM products WHERE status = 1;
SELECT COUNT(*) FROM labels WHERE status = 1;
SELECT COUNT(*) FROM requests WHERE status = 2;  -- sent
```

### Stock by product

```sql
SELECT 
    p.description,
    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock
FROM products p
JOIN packages pk ON pk.product_id = p.product_id
LEFT JOIN batches b ON b.package_id = pk.package_id
LEFT JOIN labels lb ON lb.batch_id = b.batch_id
WHERE p.status = 1
GROUP BY p.product_id
ORDER BY p.description;
```

### Expiring products (next 30 days)

```sql
SELECT * FROM v_expiring WHERE days_left BETWEEN 0 AND 30;
```

### Open requests

```sql
SELECT * FROM v_open_requests;
```

## Maintenance Scripts

### Check orphan items

```sql
.read check_pending.sql
```

Shows items still active in closed requests.

### Fix orphan items

```sql
.read fix_pending.sql
```

Shows preview, then uncomment the UPDATE statement to fix.

## Backup and Restore

### Create backup

```sql
.backup backup_2025-12-24.db
```

### Restore (close all Inventarium instances first)

Windows:
```cmd
copy backup_2025-12-24.db inventarium.db
```

Linux:
```bash
cp backup_2025-12-24.db inventarium.db
```

## Troubleshooting

### Database locked

If you see "database is locked", close all Inventarium instances and retry.

### Special characters in path

Always use quotes for network paths or paths with spaces:
```cmd
.\sqlite3 "\\server\share\path with spaces\file.db"
```

### Verify integrity

```sql
PRAGMA integrity_check;
```

---

*Reference: [SQLite Documentation](https://sqlite.org/docs.html)*
