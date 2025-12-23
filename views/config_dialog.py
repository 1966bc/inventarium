#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ConfigDialog - Database configuration dialog for Inventarium.

Shown at first startup or when database path is invalid.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from app_config import DEFAULT_DB_PATH
from dbms import DBMS
from i18n import _


class ConfigDialog(tk.Toplevel):
    """Dialog for configuring database path."""

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.result = None

        self.title(_("Configurazione Database"))
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
            text=_("Configurazione del percorso database.") + "\n\n" +
                 _("Selezionare il file database SQLite (.db)") + "\n" +
                 _("o inserire manualmente il percorso."),
            justify=tk.LEFT
        )
        msg.pack(fill=tk.X, pady=(0, 15))

        # Path entry with browse button
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill=tk.X, pady=5)

        ttk.Label(path_frame, text=_("Percorso:")).pack(side=tk.LEFT)

        self.entry = ttk.Entry(path_frame, textvariable=self.db_path, width=50)
        self.entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Button(
            path_frame,
            text=_("Sfoglia..."),
            command=self.on_browse
        ).pack(side=tk.LEFT)

        # Test connection button and status
        test_frame = ttk.Frame(frame)
        test_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            test_frame,
            text=_("Test Connessione"),
            command=self.on_test_connection
        ).pack(side=tk.LEFT)

        self.test_status = tk.StringVar()
        self.lbl_status = ttk.Label(test_frame, textvariable=self.test_status)
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(
            btn_frame,
            text=_("OK"),
            command=self.on_ok,
            width=10
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            btn_frame,
            text=_("Annulla"),
            command=self.on_cancel,
            width=10
        ).pack(side=tk.RIGHT)

        self.bind("<Return>", self.on_ok)
        self.bind("<Escape>", self.on_cancel)

    def on_test_connection(self):
        """Test database connection."""
        path = self.db_path.get().strip()
        if not path:
            self.test_status.set(_("Inserire un percorso"))
            self.lbl_status.configure(foreground="red")
            return

        # Make path absolute if relative
        check_path = path
        if not os.path.isabs(check_path):
            check_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), check_path)

        # Test connection using DBMS
        success, message, count = DBMS.test_connection(check_path)

        if success:
            self.test_status.set(f"OK - {count} " + _("prodotti trovati"))
            self.lbl_status.configure(foreground="green")
        elif message == "file_not_found":
            self.test_status.set(_("File non trovato"))
            self.lbl_status.configure(foreground="red")
        elif message == "invalid_database":
            self.test_status.set(_("Database non valido"))
            self.lbl_status.configure(foreground="orange")
        else:
            self.test_status.set(_("Errore") + f": {message}")
            self.lbl_status.configure(foreground="red")

    def on_browse(self):
        """Browse for database file."""
        initial_dir = os.path.dirname(self.db_path.get()) or os.path.dirname(os.path.dirname(__file__))

        filename = filedialog.askopenfilename(
            parent=self,
            title=_("Seleziona Database"),
            initialdir=initial_dir,
            filetypes=[
                ("SQLite Database", "*.db"),
                (_("Tutti i file"), "*.*")
            ]
        )

        if filename:
            self.db_path.set(filename)

    def on_ok(self, evt=None):
        """Validate and accept."""
        path = self.db_path.get().strip()

        if not path:
            messagebox.showwarning(
                _("Configurazione"),
                _("Inserire un percorso valido."),
                parent=self
            )
            return

        # Check if file exists
        check_path = path
        if not os.path.isabs(check_path):
            check_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), check_path)

        if not os.path.exists(check_path):
            if not messagebox.askyesno(
                _("Configurazione"),
                _("Il file non esiste:") + f"\n{check_path}\n\n" + _("Continuare comunque?"),
                parent=self
            ):
                return

        self.result = path
        self.destroy()

    def on_cancel(self, evt=None):
        """Cancel dialog."""
        self.result = None
        self.destroy()
