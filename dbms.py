#!/usr/bin/env python3
"""
Database Management System (DBMS) layer for Inventarium.

This module provides the DBMS class, which handles SQLite database connections,
query execution, and connection management.

Architecture:
    - DBMS: Base database layer (this module)
    - Controller: Extends DBMS with SQL builders and domain logic
    - Engine: Main orchestrator combining all mixins including Controller

Key Features:
    - SQLite connection management
    - Dictionary-based result sets (no positional indexing)
    - Parameterized query support (SQL injection prevention)
    - Comprehensive error logging
    - Transaction support with rollback

Security:
    - All table/column names validated against SQL identifier regex
    - Mandatory use of parameterized queries (no string concatenation)

Classes:
    DBMS: Database connection and query execution layer

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import sys
import inspect
import re
import sqlite3
from typing import Optional, Union, List, Dict, Tuple, Any


class DBMS:
    """
    Database Management System base layer for SQLite operations.

    Provides connection management, query execution, and database operations
    with error handling and comprehensive logging.

    This is the foundation layer of Inventarium's data access architecture.
    Controller extends this class with SQL builders and domain logic.

    Attributes:
        database (str): Path to SQLite database file
        autocommit (bool): Enable autocommit mode (default: True)
        con: SQLite connection object (managed internally)

    Connection Management:
        - Automatic connection on initialization
        - Row factory for dictionary-like access
        - Proper cleanup and cursor management

    Query Execution:
        - read(): Execute SELECT queries, return dict results
        - write(): Execute INSERT/UPDATE/DELETE with auto-commit or rollback
        - Parameterized queries only (SQL injection prevention)
        - Dictionary cursor for named-key access (no positional indexing)

    Error Handling:
        - All database errors logged via on_log()
        - Graceful degradation (returns None on failure)
        - Automatic rollback on write failures

    Security:
        - SQL identifier validation (table/column names)
        - Mandatory parameterized queries

    Example:
        >>> dbms = DBMS("/path/to/inventarium.db")
        >>> rows = dbms.read(True, "SELECT * FROM products WHERE status = ?", (1,))
        >>> for row in rows:
        ...     print(row["description"])  # Named-key access
    """
    def __init__(
        self,
        database: str,
        autocommit: bool = True
    ) -> None:

        self.database = database
        self.autocommit = autocommit
        self.con = self._set_connection()

    def __str__(self) -> str:
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__,
                                             [x.__name__ for x in DBMS.__mro__],)

    def _dict_factory(self, cursor: sqlite3.Cursor, row: tuple) -> Dict[str, Any]:
        """Convert SQLite row to dictionary."""
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    def _set_connection(self) -> Optional[sqlite3.Connection]:
        try:
            con = sqlite3.connect(self.database)
            con.row_factory = self._dict_factory
            # Enable foreign keys
            con.execute("PRAGMA foreign_keys = ON")
            if self.autocommit:
                con.isolation_level = None  # autocommit mode
            return con
        except Exception as e:
            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return None

    def _ensure_connection(self) -> None:
        """
        Ensure there is an active DB connection.
        If no connection, open a new one.
        """
        if self.con is None:
            self.con = self._set_connection()

    def read(
        self,
        fetch: bool,
        sql: str,
        args: Tuple = ()
    ) -> Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]:
        """
        Execute a SELECT query and return results as dictionaries.

        Args:
            fetch (bool):
                - True  → return a list of dictionaries (possibly empty)
                - False → return a single dictionary or None when no rows
            sql (str): SQL query string
            args (tuple): parameters for the query (default: ())

        Returns:
            list[dict] | dict | None
                Example (fetch=True):
                    [{'id': 1, 'description': 'Chemistry'},
                     {'id': 2, 'description': 'Hematology'}]
                Example (fetch=False):
                    {'id': 1, 'description': 'Chemistry'}
                Returns None on error.
        """
        cursor = None
        try:
            self._ensure_connection()
            if self.con is None:
                raise RuntimeError("No active DB connection")

            cursor = self.con.cursor()
            cursor.execute(sql, args)

            if fetch:
                return cursor.fetchall()  # → list of dicts (possibly empty)
            else:
                return cursor.fetchone()  # → single dict or None

        except Exception as e:
            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return None

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as e:
                    f = inspect.currentframe()
                    function = f.f_code.co_name + ".close"
                    caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
                    self.on_log(function, e, type(e), sys.modules[__name__], caller)

    def write(self, sql: str, args: Tuple = ()) -> Optional[int]:
        """
        Execute a DML statement (INSERT/UPDATE/DELETE).
        Returns:
          - lastrowid when available and non-zero,
          - otherwise the affected rowcount,
          - None on error.
        Commits only if autocommit is disabled.
        """
        cursor = None
        try:

            self._ensure_connection()

            if self.con is None:
                raise RuntimeError("No active DB connection")

            cursor = self.con.cursor()
            cursor.execute(sql, args)

            # Commit only when autocommit is disabled
            if not self.autocommit:
                self.con.commit()

            # Prefer lastrowid; fallback to rowcount if not meaningful
            last_id = cursor.lastrowid
            return last_id if last_id not in (None, 0) else cursor.rowcount

        except Exception as e:
            # Rollback only if autocommit is disabled
            try:
                if self.con and not self.autocommit:
                    self.con.rollback()
            except Exception:
                pass

            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return None

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as e:
                    f = inspect.currentframe()
                    function = f.f_code.co_name + ".close"
                    caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
                    self.on_log(function, e, type(e), sys.modules[__name__], caller)

    def on_log(self, function: str, exception: Exception, exc_type: type,
               module: Any, caller: str) -> None:
        """
        Log database errors. Override this method for custom logging.

        Args:
            function: Name of the function where error occurred
            exception: The exception that was raised
            exc_type: Type of the exception
            module: Module where error occurred
            caller: Name of the calling function
        """
        print(f"[ERROR] {function} called by {caller}: {exc_type.__name__}: {exception}")

    def close(self) -> None:
        """Close the database connection."""
        if self.con:
            try:
                self.con.close()
                self.con = None
            except Exception as e:
                f = inspect.currentframe()
                function = f.f_code.co_name
                caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
                self.on_log(function, e, type(e), sys.modules[__name__], caller)

    @staticmethod
    def test_connection(db_path: str) -> Tuple[bool, str, int]:
        """
        Test if db_path is a valid Inventarium database.

        Used by ConfigDialog before Engine exists.

        Args:
            db_path: Path to the SQLite database file

        Returns:
            Tuple of (success, message, product_count)
            - success: True if connection successful and DB is valid
            - message: Status message (error or success info)
            - product_count: Number of products found (0 if failed)
        """
        import os

        if not os.path.exists(db_path):
            return False, "file_not_found", 0

        try:
            con = sqlite3.connect(db_path)
            cursor = con.cursor()

            # Check if it's a valid Inventarium database
            cursor.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='products'"
            )
            if cursor.fetchone() is None:
                con.close()
                return False, "invalid_database", 0

            # Count products as a simple test
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            con.close()

            return True, "ok", count

        except sqlite3.Error as e:
            return False, str(e), 0
        except Exception as e:
            return False, str(e), 0

    def _validate_sql_identifier(self, identifier: str, identifier_type: str = "identifier") -> None:
        """
        Validate SQL identifier (table/column name) to prevent SQL injection.

        Args:
            identifier: Table or column name to validate
            identifier_type: Type description for error message (e.g., "table", "column")

        Raises:
            ValueError: If identifier contains invalid characters

        Note:
            Valid SQL identifiers must match: ^[a-zA-Z_][a-zA-Z0-9_]*$
            This prevents SQL injection via table/column name manipulation.
        """
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
            raise ValueError(
                f"Invalid SQL {identifier_type} name: '{identifier}'. "
                f"Must match pattern: ^[a-zA-Z_][a-zA-Z0-9_]*$"
            )

    def _get_columns(self, table: str) -> Tuple[str, ...]:
        """
        Return all column names in declaration order (PK as first column).

        Uses PRAGMA table_info to fetch column metadata from SQLite.

        Args:
            table: Table name to get columns for

        Returns:
            Tuple of column names in declaration order
        """
        cursor = None
        try:
            self._validate_sql_identifier(table, "table")
            self._ensure_connection()

            if self.con is None:
                raise RuntimeError("No active DB connection")

            cursor = self.con.cursor()
            cursor.execute(f"PRAGMA table_info({table})")
            # table_info returns: cid, name, type, notnull, dflt_value, pk
            # Sort by cid to maintain declaration order
            rows = cursor.fetchall()
            return tuple(row["name"] for row in sorted(rows, key=lambda r: r["cid"]))

        except Exception as e:
            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return tuple()

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as e:
                    f = inspect.currentframe()
                    function = f.f_code.co_name + ".close"
                    caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
                    self.on_log(function, e, type(e), sys.modules[__name__], caller)

    def build_sql(self, table: str, op: str) -> Optional[str]:
        """
        Generate SQL for INSERT or UPDATE using project conventions.

        Conventions:
            - PK is the first column (excluded from INSERT, used in WHERE for UPDATE)
            - Placeholders use '?' (SQLite style)

        Args:
            table: Table name
            op: Operation type - "insert" or "update"

        Returns:
            SQL string or None on error

        Example:
            >>> engine.build_sql("products", "insert")
            'INSERT INTO products(reference,description,status) VALUES(?,?,?)'

            >>> engine.build_sql("products", "update")
            'UPDATE products SET reference = ?, description = ?, status = ? WHERE product_id = ?'
        """
        try:
            self._validate_sql_identifier(table, "table")
            all_cols = list(self._get_columns(table))

            if not all_cols:
                raise ValueError(f"No columns found for table '{table}'")

            if op == "insert":
                fields = all_cols[1:]  # skip PK
                cols_list = ",".join(fields)
                placeholders = ",".join(["?"] * len(fields))
                return f"INSERT INTO {table}({cols_list}) VALUES({placeholders})"

            elif op == "update":
                primary_key = all_cols[0]
                set_cols = [c for c in all_cols if c != primary_key]
                set_clause = ", ".join(f"{c} = ?" for c in set_cols)
                return f"UPDATE {table} SET {set_clause} WHERE {primary_key} = ?"

            else:
                raise ValueError("op must be 'insert' or 'update'")

        except Exception as e:
            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return None
