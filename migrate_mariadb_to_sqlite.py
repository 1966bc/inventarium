#!/usr/bin/env python3
"""
Migration script: MariaDB (inventarium) → SQLite (inventarium.db)

Migrates data from the production MariaDB database to the new SQLite schema.

Usage:
    python3 migrate_mariadb_to_sqlite.py

Author: Claude Code
"""
import sqlite3
import sys

try:
    import mysql.connector
except ImportError:
    print("ERROR: mysql-connector-python not installed")
    print("Run: pip install mysql-connector-python")
    sys.exit(1)

# Configuration
MARIADB_CONFIG = {
    'host': 'localhost',
    'user': 'claude',
    'password': 'inv2025',
    'database': 'inventarium',
    'charset': 'utf8mb4'
}

SQLITE_PATH = '/opt/inventarium/sql/inventarium.db'


def connect_mariadb():
    """Connect to MariaDB."""
    return mysql.connector.connect(**MARIADB_CONFIG)


def connect_sqlite():
    """Connect to SQLite."""
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def clear_sqlite(sqlite_conn):
    """Clear all data from SQLite tables (in correct order for FK constraints)."""
    print("\n=== Clearing SQLite database ===")

    # Disable foreign keys temporarily
    sqlite_conn.execute("PRAGMA foreign_keys = OFF")

    tables = [
        'deliveries',
        'items',
        'requests',
        'labels',
        'batches',
        'packages',
        'products',
        'locations',
        'conservations',
        'categories',
        'suppliers',
    ]

    for table in tables:
        try:
            sqlite_conn.execute(f"DELETE FROM {table}")
            print(f"  Cleared: {table}")
        except Exception as e:
            print(f"  Warning: {table} - {e}")

    sqlite_conn.commit()
    sqlite_conn.execute("PRAGMA foreign_keys = ON")
    print("  Done clearing tables")


def migrate_suppliers(maria_conn, sqlite_conn):
    """Migrate suppliers table."""
    print("\n=== Migrating suppliers ===")

    cursor = maria_conn.cursor(dictionary=True)
    cursor.execute("SELECT supplier_id, description, reference, status FROM suppliers")
    rows = cursor.fetchall()

    for row in rows:
        sqlite_conn.execute(
            "INSERT INTO suppliers (supplier_id, description, reference, status) VALUES (?, ?, ?, ?)",
            (row['supplier_id'], row['description'], row['reference'], row['status'])
        )

    sqlite_conn.commit()
    print(f"  Migrated {len(rows)} suppliers")


def migrate_conservations(maria_conn, sqlite_conn):
    """Migrate conservations table."""
    print("\n=== Migrating conservations ===")

    cursor = maria_conn.cursor(dictionary=True)
    cursor.execute("SELECT conservation_id, description, status FROM conservations")
    rows = cursor.fetchall()

    for row in rows:
        sqlite_conn.execute(
            "INSERT INTO conservations (conservation_id, description, status) VALUES (?, ?, ?)",
            (row['conservation_id'], row['description'], row['status'])
        )

    sqlite_conn.commit()
    print(f"  Migrated {len(rows)} conservations")


def migrate_categories(maria_conn, sqlite_conn):
    """Migrate section_product_categories → categories (skip duplicates)."""
    print("\n=== Migrating section_product_categories → categories ===")

    cursor = maria_conn.cursor(dictionary=True)
    cursor.execute("SELECT category_id, category, status FROM section_product_categories ORDER BY category_id")
    rows = cursor.fetchall()

    migrated = 0
    skipped = 0
    seen_descriptions = set()

    for row in rows:
        desc = row['category'].strip()
        if desc in seen_descriptions:
            skipped += 1
            continue

        seen_descriptions.add(desc)
        sqlite_conn.execute(
            "INSERT INTO categories (category_id, reference_id, description, status) VALUES (?, ?, ?, ?)",
            (row['category_id'], 1, desc, row['status'])  # reference_id always 1
        )
        migrated += 1

    sqlite_conn.commit()
    print(f"  Migrated {migrated} categories (skipped {skipped} duplicates)")


def migrate_locations(maria_conn, sqlite_conn):
    """Migrate locations table."""
    print("\n=== Migrating locations ===")

    cursor = maria_conn.cursor(dictionary=True)
    cursor.execute("SELECT location_id, section_id, code, description, status FROM locations")
    rows = cursor.fetchall()

    for row in rows:
        # Map section_id to category_id in SQLite (simplified mapping)
        sqlite_conn.execute(
            "INSERT INTO locations (location_id, category_id, code, description, status) VALUES (?, ?, ?, ?, ?)",
            (row['location_id'], row['section_id'], row['code'], row['description'], row['status'])
        )

    sqlite_conn.commit()
    print(f"  Migrated {len(rows)} locations")


def migrate_products(maria_conn, sqlite_conn):
    """Migrate products table (skip duplicates, keep first by product_id)."""
    print("\n=== Migrating products ===")

    cursor = maria_conn.cursor(dictionary=True)
    cursor.execute("SELECT product_id, code, description, status FROM products ORDER BY product_id")
    rows = cursor.fetchall()

    migrated = 0
    skipped = 0
    seen_references = set()

    for row in rows:
        ref = row['code'].strip() if row['code'] else ''
        if ref in seen_references:
            skipped += 1
            continue

        seen_references.add(ref)
        sqlite_conn.execute(
            "INSERT INTO products (product_id, reference, description, status) VALUES (?, ?, ?, ?)",
            (row['product_id'], ref, row['description'], row['status'])
        )
        migrated += 1

    sqlite_conn.commit()
    print(f"  Migrated {migrated} products (skipped {skipped} duplicates)")


def migrate_packages(maria_conn, sqlite_conn):
    """Migrate packages table with dict_products data merged."""
    print("\n=== Migrating packages (with dict_products merge) ===")

    cursor = maria_conn.cursor(dictionary=True)

    # Join packages with dict_products to get category_id and other fields
    query = """
        SELECT
            pk.package_id,
            pk.product_id,
            pk.supplier_id,
            pk.reference,
            pk.labels,
            pk.description as packaging,
            pk.conservation_id,
            pk.in_the_dark,
            pk.status,
            dp.category_id,
            dp.section_id,
            dp.understock as reorder
        FROM packages pk
        LEFT JOIN dict_products dp ON dp.package_id = pk.package_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    migrated = 0
    skipped = 0

    for row in rows:
        # Skip packages without a valid product_id
        if not row['product_id']:
            skipped += 1
            continue

        # Map section_id to location_id (use section_id as location reference)
        location_id = row['section_id'] if row['section_id'] else None
        category_id = row['category_id'] if row['category_id'] else 0
        reorder = row['reorder'] if row['reorder'] else 0

        try:
            sqlite_conn.execute(
                """INSERT INTO packages
                   (package_id, product_id, supplier_id, reference, labels, packaging,
                    conservation_id, in_the_dark, category_id, location_id, status, reorder)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (row['package_id'], row['product_id'], row['supplier_id'],
                 row['reference'], row['labels'], row['packaging'],
                 row['conservation_id'], row['in_the_dark'],
                 category_id, location_id, row['status'], reorder)
            )
            migrated += 1
        except Exception as e:
            print(f"  Warning: package {row['package_id']} - {e}")
            skipped += 1

    sqlite_conn.commit()
    print(f"  Migrated {migrated} packages (skipped {skipped})")


def migrate_batches(maria_conn, sqlite_conn):
    """Migrate batches table, mapping dict_product_id to package_id."""
    print("\n=== Migrating batches ===")

    cursor = maria_conn.cursor(dictionary=True)

    # Get mapping from dict_product_id to package_id
    cursor.execute("SELECT dict_product_id, package_id FROM dict_products")
    dp_mapping = {row['dict_product_id']: row['package_id'] for row in cursor.fetchall()}

    # Get batches
    cursor.execute("SELECT batch_id, dict_product_id, lot, expiration, status FROM batches")
    rows = cursor.fetchall()

    migrated = 0
    skipped = 0

    for row in rows:
        # Map dict_product_id to package_id
        package_id = dp_mapping.get(row['dict_product_id'])

        if not package_id:
            skipped += 1
            continue

        try:
            sqlite_conn.execute(
                "INSERT INTO batches (batch_id, package_id, description, expiration, status) VALUES (?, ?, ?, ?, ?)",
                (row['batch_id'], package_id, row['lot'], row['expiration'], row['status'])
            )
            migrated += 1
        except Exception as e:
            print(f"  Warning: batch {row['batch_id']} - {e}")
            skipped += 1

    sqlite_conn.commit()
    print(f"  Migrated {migrated} batches (skipped {skipped})")


def migrate_labels(maria_conn, sqlite_conn):
    """Migrate labels table."""
    print("\n=== Migrating labels ===")

    cursor = maria_conn.cursor(dictionary=True)
    cursor.execute("SELECT label_id, batch_id, barcode, status, enable FROM labels")
    rows = cursor.fetchall()

    migrated = 0
    skipped = 0

    for row in rows:
        # Map MariaDB status/enable to SQLite status:
        # MariaDB: status=1 means in stock, enable=1 means active
        # SQLite: status 1=in stock, 0=used, -1=cancelled

        if row['enable'] == 0:
            status = -1  # Cancelled
        elif row['status'] == 0:
            status = 0   # Used
        else:
            status = 1   # In stock

        # Use barcode as tick (unique identifier)
        tick = hash(row['barcode']) % 10000000000

        try:
            sqlite_conn.execute(
                "INSERT INTO labels (label_id, batch_id, tick, status) VALUES (?, ?, ?, ?)",
                (row['label_id'], row['batch_id'], tick, status)
            )
            migrated += 1
        except Exception as e:
            print(f"  Warning: label {row['label_id']} - {e}")
            skipped += 1

    sqlite_conn.commit()
    print(f"  Migrated {migrated} labels (skipped {skipped})")


def migrate_requests(maria_conn, sqlite_conn):
    """Migrate orders → requests."""
    print("\n=== Migrating orders → requests ===")

    cursor = maria_conn.cursor(dictionary=True)
    cursor.execute("SELECT order_id, reference, issued, status FROM orders")
    rows = cursor.fetchall()

    for row in rows:
        sqlite_conn.execute(
            "INSERT INTO requests (request_id, reference, issued, status) VALUES (?, ?, ?, ?)",
            (row['order_id'], row['reference'], row['issued'], row['status'])
        )

    sqlite_conn.commit()
    print(f"  Migrated {len(rows)} requests (from orders)")


def migrate_items(maria_conn, sqlite_conn):
    """Migrate order_items → items."""
    print("\n=== Migrating order_items → items ===")

    cursor = maria_conn.cursor(dictionary=True)

    # Get mapping from dict_product_id to package_id
    cursor.execute("SELECT dict_product_id, package_id FROM dict_products")
    dp_mapping = {row['dict_product_id']: row['package_id'] for row in cursor.fetchall()}

    # Get order_items
    cursor.execute("SELECT order_item_id, order_id, dict_product_id, quantity, status FROM order_items")
    rows = cursor.fetchall()

    migrated = 0
    skipped = 0

    for row in rows:
        package_id = dp_mapping.get(row['dict_product_id'])

        if not package_id:
            skipped += 1
            continue

        try:
            sqlite_conn.execute(
                "INSERT INTO items (item_id, request_id, package_id, quantity, status) VALUES (?, ?, ?, ?, ?)",
                (row['order_item_id'], row['order_id'], package_id, row['quantity'], row['status'])
            )
            migrated += 1
        except Exception as e:
            print(f"  Warning: item {row['order_item_id']} - {e}")
            skipped += 1

    sqlite_conn.commit()
    print(f"  Migrated {migrated} items (skipped {skipped})")


def migrate_deliveries(maria_conn, sqlite_conn):
    """Migrate deliveries table."""
    print("\n=== Migrating deliveries ===")

    cursor = maria_conn.cursor(dictionary=True)

    # Get mapping from dict_product_id to package_id
    cursor.execute("SELECT dict_product_id, package_id FROM dict_products")
    dp_mapping = {row['dict_product_id']: row['package_id'] for row in cursor.fetchall()}

    # Note: MariaDB has typo "dict_ptoduct_id" instead of "dict_product_id"
    cursor.execute("""
        SELECT delivery_id, order_item_id, dict_ptoduct_id, delivery, delivered, quantity, status
        FROM deliveries
    """)
    rows = cursor.fetchall()

    migrated = 0
    skipped = 0

    for row in rows:
        package_id = dp_mapping.get(row['dict_ptoduct_id'])

        if not package_id:
            skipped += 1
            continue

        try:
            sqlite_conn.execute(
                """INSERT INTO deliveries
                   (delivery_id, item_id, package_id, ddt, delivered, quantity, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (row['delivery_id'], row['order_item_id'], package_id,
                 row['delivery'], row['delivered'], row['quantity'], row['status'])
            )
            migrated += 1
        except Exception as e:
            print(f"  Warning: delivery {row['delivery_id']} - {e}")
            skipped += 1

    sqlite_conn.commit()
    print(f"  Migrated {migrated} deliveries (skipped {skipped})")


def validate_migration(sqlite_conn):
    """Validate migrated data counts."""
    print("\n=== Validation ===")

    tables = ['suppliers', 'conservations', 'categories', 'locations',
              'products', 'packages', 'batches', 'labels',
              'requests', 'items', 'deliveries']

    for table in tables:
        cursor = sqlite_conn.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} rows")


def main():
    print("=" * 60)
    print("MariaDB → SQLite Migration")
    print("=" * 60)

    # Connect to databases
    print("\nConnecting to databases...")
    maria_conn = connect_mariadb()
    sqlite_conn = connect_sqlite()
    print("  Connected!")

    try:
        # Clear SQLite
        clear_sqlite(sqlite_conn)

        # Migrate in correct order (respecting foreign keys)
        migrate_suppliers(maria_conn, sqlite_conn)
        migrate_conservations(maria_conn, sqlite_conn)
        migrate_categories(maria_conn, sqlite_conn)
        migrate_locations(maria_conn, sqlite_conn)
        migrate_products(maria_conn, sqlite_conn)
        migrate_packages(maria_conn, sqlite_conn)
        migrate_batches(maria_conn, sqlite_conn)
        migrate_labels(maria_conn, sqlite_conn)
        migrate_requests(maria_conn, sqlite_conn)
        migrate_items(maria_conn, sqlite_conn)
        migrate_deliveries(maria_conn, sqlite_conn)

        # Validate
        validate_migration(sqlite_conn)

        print("\n" + "=" * 60)
        print("Migration completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        maria_conn.close()
        sqlite_conn.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
