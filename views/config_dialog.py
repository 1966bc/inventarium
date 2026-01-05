#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ConfigDialog - Database configuration dialog for Inventarium.

Shown at first startup or when database path is invalid.
Offers options to find existing database or create a new one.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import os
import sqlite3
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from app_config import DEFAULT_DB_PATH, USER_CONFIG_DIR
from i18n import _


class ConfigDialog(tk.Toplevel):
    """Dialog for configuring database path."""

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.result = None

        self.title(_("Database Configuration"))
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self.db_path = tk.StringVar(value=DEFAULT_DB_PATH)

        self.init_ui()
        self.center_on_screen()

    def center_on_screen(self):
        """Center dialog on screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"+{x}+{y}")

    def init_ui(self):
        """Build dialog UI."""
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Message
        msg = ttk.Label(
            frame,
            text=_("Database not found.") + "\n\n" +
                 _("What do you want to do?"),
            justify=tk.LEFT,
            font=('', 10)
        )
        msg.pack(fill=tk.X, pady=(0, 20))

        # Buttons frame
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)

        # Find existing database button
        btn_find = ttk.Button(
            btn_frame,
            text=_("Find existing database..."),
            command=self.on_find_database,
            width=30
        )
        btn_find.pack(pady=5)

        # Create new database button
        btn_create = ttk.Button(
            btn_frame,
            text=_("Create new database"),
            command=self.on_create_database,
            width=30
        )
        btn_create.pack(pady=5)

        # Cancel button
        btn_cancel = ttk.Button(
            btn_frame,
            text=_("Cancel"),
            command=self.on_cancel,
            width=30
        )
        btn_cancel.pack(pady=5)

        self.bind("<Escape>", self.on_cancel)

    def on_find_database(self):
        """Browse for existing database file."""
        # Prefer user config directory, fallback to app directory
        if os.path.exists(USER_CONFIG_DIR):
            initial_dir = USER_CONFIG_DIR
        else:
            initial_dir = os.path.dirname(os.path.dirname(__file__))

        filename = filedialog.askopenfilename(
            parent=self,
            title=_("Select Database"),
            initialdir=initial_dir,
            filetypes=[
                ("SQLite Database", "*.db"),
                (_("All files"), "*.*")
            ]
        )

        if filename:
            # Verify it's a valid database
            if self._verify_database(filename):
                self.result = filename
                self.destroy()
            else:
                messagebox.showerror(
                    _("Error"),
                    _("The selected file is not a valid Inventarium database."),
                    parent=self
                )

    def on_create_database(self):
        """Create a new database with demo data."""
        # Prefer user config directory, fallback to app directory
        if os.path.exists(USER_CONFIG_DIR):
            initial_dir = USER_CONFIG_DIR
        else:
            initial_dir = os.path.dirname(os.path.dirname(__file__))
            # Create user config dir if we're in system install
            if "/usr/share" in initial_dir:
                os.makedirs(USER_CONFIG_DIR, exist_ok=True)
                initial_dir = USER_CONFIG_DIR

        filename = filedialog.asksaveasfilename(
            parent=self,
            title=_("Create New Database"),
            initialdir=initial_dir,
            initialfile="inventarium.db",
            defaultextension=".db",
            filetypes=[
                ("SQLite Database", "*.db"),
                (_("All files"), "*.*")
            ]
        )

        if filename:
            # Create the database
            if self._create_database(filename):
                messagebox.showinfo(
                    _("Database Created"),
                    _("Database created successfully!") + f"\n\n{filename}",
                    parent=self
                )
                self.result = filename
                self.destroy()
            else:
                messagebox.showerror(
                    _("Error"),
                    _("Unable to create the database."),
                    parent=self
                )

    def _verify_database(self, path):
        """
        Verify that a file is a valid Inventarium database.
        
        Args:
            path: Path to database file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            
            # Check for required tables
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('products', 'packages', 'batches', 'labels')
            """)
            tables = cursor.fetchall()
            conn.close()
            
            # Must have at least these core tables
            return len(tables) >= 4
            
        except Exception:
            return False

    def _create_database(self, path):
        """
        Create a new database with schema and demo data.

        Args:
            path: Path for new database file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Find init.sql
            app_dir = os.path.dirname(os.path.dirname(__file__))
            sql_paths = [
                os.path.join(app_dir, "sql", "init.sql"),
                os.path.join(app_dir, "init.sql"),
                "/usr/share/inventarium/sql/init.sql",  # System install
            ]

            sql_file = None
            for p in sql_paths:
                if os.path.exists(p):
                    sql_file = p
                    break

            if not sql_file:
                messagebox.showerror(
                    _("Error"),
                    _("File init.sql not found!"),
                    parent=self
                )
                return False

            # Remove existing file to ensure clean creation
            if os.path.exists(path):
                os.remove(path)

            # Read SQL script
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()

            # Create database and execute script
            t0 = time.perf_counter()
            conn = sqlite3.connect(path)
            conn.executescript(sql_script)
            conn.commit()
            conn.close()
            print(f"[INFO] Database created in {time.perf_counter() - t0:.3f}s")

            return True
            
        except Exception as e:
            messagebox.showerror(
                _("Error"),
                f"{_('Error during database creation:')}\n{e}",
                parent=self
            )
            return False

    def on_cancel(self, evt=None):
        """Cancel dialog."""
        self.result = None
        self.destroy()
