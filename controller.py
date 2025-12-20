#!/usr/bin/env python3
"""
Controller layer for Inventarium - SQL builders and domain logic.

This module provides the Controller class, which extends DBMS with SQL query builders
and domain-specific business logic for inventory management.

Architecture:
    - DBMS: Base database layer (connection + basic read/write)
    - Controller: This layer (SQL builders + domain logic)
    - Engine: Main orchestrator (combines Controller + Tools)

Responsibilities:
    - Build SQL queries for INSERT/UPDATE/DELETE operations
    - Implement domain-specific data retrieval methods
    - Window instance management and refresh coordination

Classes:
    Controller: SQL builder and domain logic layer

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import sys
import inspect
import re
from typing import Optional, List, Dict, Any, Union


class Controller:
    """
    Controller layer - SQL builders and domain logic for Inventarium.

    Extends DBMS with application-specific database operations and SQL query builders.
    """

    def __str__(self) -> str:
        return "class: %s\nMRO: %s" % (self.__class__.__name__,
                                        [x.__name__ for x in Controller.__mro__])

    def get_selected(self, table: str, field: str, pk: Any) -> Optional[Dict[Union[int, str], Any]]:
        """
        Return a single row from the given table.

        Backward compatible behavior:
          - numeric keys:    record[0], record[1], ...  (old style)
          - named keys:      record['column_name']      (new style)

        Args:
            table: table name
            field: column name used in WHERE clause (usually PK)
            pk: value to match in the WHERE clause

        Returns:
            Hybrid dictionary (both int and str keys) or None if no row is found

        Raises:
            ValueError: If table or field name contains invalid characters
        """
        # Validate table and field names to prevent SQL injection
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table):
            raise ValueError(
                f"Invalid SQL table name: '{table}'. "
                f"Must match pattern: ^[a-zA-Z_][a-zA-Z0-9_]*$"
            )
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', field):
            raise ValueError(
                f"Invalid SQL column name: '{field}'. "
                f"Must match pattern: ^[a-zA-Z_][a-zA-Z0-9_]*$"
            )

        sql = f"SELECT * FROM {table} WHERE {field} = ?;"
        row = self.read(False, sql, (pk,))

        if row is None:
            return None

        hybrid = {}

        # Preserve order from read: Python 3.7+ dicts are ordered.
        for idx, (col, value) in enumerate(row.items()):
            # Old style: record[0], record[1], ...
            hybrid[idx] = value
            # New style: record['column_name']
            hybrid[col] = value

        return hybrid

    def refresh_windows_for_table(self, table_name: str) -> None:
        """
        Central dispatcher for cross-window GUI refreshes after editing lookup tables.
        """
        registry = getattr(self, "dict_instances", None)
        if not registry:
            return

        # Mapping of table changes to windows that need refresh
        mapping = {
            "products": ("packages", "batches", "main"),
            "packages": ("batches", "items", "main"),
            "batches": ("labels", "main"),
            "suppliers": ("packages",),
            "categories": ("packages", "locations"),
            "conservations": ("packages", "locations"),
            "locations": ("packages",),
            "requests": ("items", "deliveries"),
            "items": ("deliveries",),
        }

        # Default refresh methods for each window type
        refresh_methods = {
            "main": "refresh",
            "packages": "refresh",
            "batches": "refresh",
            "labels": "refresh",
            "items": "refresh",
            "deliveries": "refresh",
        }

        targets = mapping.get(table_name, ())
        if not targets:
            return

        for name in targets:
            win = registry.get(name)
            if not win:
                continue

            try:
                if callable(getattr(win, "winfo_exists", None)) and not win.winfo_exists():
                    continue

                method_name = refresh_methods.get(name, "refresh")
                if method_name and hasattr(win, method_name):
                    getattr(win, method_name)()

            except Exception as e:
                print(f"Error refreshing {name}: {e}")

    # -------------------------------------------------------------------------
    # Domain-specific queries for Inventarium
    # -------------------------------------------------------------------------

    def get_stock(self, package_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get stock levels (labels in stock) for packages.

        Args:
            package_id: Optional filter by package

        Returns:
            List of stock records
        """
        sql = """
            SELECT
                p.product_id,
                p.reference AS product_code,
                p.description AS product_name,
                pk.package_id,
                pk.reference AS supplier_code,
                pk.packaging,
                s.description AS supplier,
                c.description AS category,
                l.description AS location,
                COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock,
                COUNT(CASE WHEN lb.status = 0 THEN 1 END) AS used,
                COUNT(CASE WHEN lb.status = -1 THEN 1 END) AS cancelled
            FROM products p
            JOIN packages pk ON pk.product_id = p.product_id
            LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
            LEFT JOIN categories c ON c.category_id = pk.category_id
            LEFT JOIN locations l ON l.location_id = pk.location_id
            LEFT JOIN batches b ON b.package_id = pk.package_id
            LEFT JOIN labels lb ON lb.batch_id = b.batch_id
            WHERE p.status = 1 AND pk.status = 1
        """

        args = ()
        if package_id:
            sql += " AND pk.package_id = ?"
            args = (package_id,)

        sql += " GROUP BY pk.package_id ORDER BY p.description"

        return self.read(True, sql, args) or []

    def get_expiring_batches(self, days: int = 90) -> List[Dict[str, Any]]:
        """
        Get batches expiring within specified days.

        Args:
            days: Number of days to look ahead (default 90)

        Returns:
            List of expiring batch records
        """
        sql = """
            SELECT
                p.description AS product_name,
                pk.packaging,
                b.batch_id,
                b.description AS lot,
                b.expiration,
                CAST(julianday(b.expiration) - julianday('now') AS INTEGER) AS days_left,
                COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS labels_in_stock
            FROM batches b
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            LEFT JOIN labels lb ON lb.batch_id = b.batch_id
            WHERE b.expiration IS NOT NULL
              AND b.expiration >= date('now')
              AND b.expiration <= date('now', '+' || ? || ' days')
              AND b.status = 1
            GROUP BY b.batch_id
            ORDER BY b.expiration
        """
        return self.read(True, sql, (days,)) or []

    def get_expired_batches(self) -> List[Dict[str, Any]]:
        """
        Get expired batches that are still active.

        Returns:
            List of expired batch records
        """
        sql = """
            SELECT
                p.description AS product_name,
                pk.packaging,
                b.batch_id,
                b.description AS lot,
                b.expiration,
                CAST(julianday('now') - julianday(b.expiration) AS INTEGER) AS days_expired,
                COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS labels_in_stock
            FROM batches b
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            LEFT JOIN labels lb ON lb.batch_id = b.batch_id
            WHERE b.expiration < date('now')
              AND b.status = 1
            GROUP BY b.batch_id
            ORDER BY b.expiration DESC
        """
        return self.read(True, sql) or []

    def get_open_requests(self) -> List[Dict[str, Any]]:
        """
        Get open requests with delivery status.

        Returns:
            List of open request records
        """
        sql = """
            SELECT
                r.request_id,
                r.reference,
                r.issued,
                COUNT(i.item_id) AS total_items,
                SUM(i.quantity) AS qty_ordered,
                COALESCE(SUM(d.quantity), 0) AS qty_delivered
            FROM requests r
            JOIN items i ON i.request_id = r.request_id
            LEFT JOIN deliveries d ON d.item_id = i.item_id
            WHERE r.status = 1
            GROUP BY r.request_id
            ORDER BY r.issued DESC
        """
        return self.read(True, sql) or []

    def load_label(self, batch_id: int) -> Optional[int]:
        """
        Create a new label (load into stock).

        Args:
            batch_id: Batch to create label for

        Returns:
            New label_id or None on error
        """
        tick = self.get_tick()
        sql = "INSERT INTO labels (batch_id, tick, loaded, status) VALUES (?, ?, date('now'), 1)"
        return self.write(sql, (batch_id, tick))

    def unload_label(self, label_id: int) -> Optional[int]:
        """
        Unload a label (mark as used).

        Args:
            label_id: Label to unload

        Returns:
            Rows affected or None on error
        """
        sql = "UPDATE labels SET unloaded = date('now'), status = 0 WHERE label_id = ?"
        return self.write(sql, (label_id,))

    def cancel_label(self, label_id: int) -> Optional[int]:
        """
        Cancel a label (mark as error).

        Args:
            label_id: Label to cancel

        Returns:
            Rows affected or None on error
        """
        sql = "UPDATE labels SET status = -1 WHERE label_id = ?"
        return self.write(sql, (label_id,))

    def restore_label(self, label_id: int) -> Optional[int]:
        """
        Restore a cancelled or used label back to stock.

        Args:
            label_id: Label to restore

        Returns:
            Rows affected or None on error
        """
        sql = "UPDATE labels SET unloaded = NULL, status = 1 WHERE label_id = ?"
        return self.write(sql, (label_id,))

    # -------------------------------------------------------------------------
    # Settings management
    # -------------------------------------------------------------------------

    def get_setting(self, key: str, default: str = "") -> str:
        """
        Get a setting value by key.

        Args:
            key: Setting key name
            default: Default value if not found

        Returns:
            Setting value or default
        """
        sql = "SELECT value FROM settings WHERE key = ?"
        row = self.read(False, sql, (key,))
        if row:
            return row["value"] or default
        return default

    def set_setting(self, key: str, value: str) -> Optional[int]:
        """
        Set a setting value (inserts if not exists).

        Args:
            key: Setting key name
            value: Value to set

        Returns:
            Rows affected or None on error
        """
        sql = "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)"
        return self.write(sql, (key, value))
