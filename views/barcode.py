#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Barcode Scanner - Unload labels by scanning barcode or entering label ID.

This module provides a simple interface for unloading labels from stock
by scanning a barcode or manually entering the label ID.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk

from i18n import _
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    """Barcode scanner for unloading labels."""

    def __init__(self, parent):
        super().__init__(name="barcode")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.transient(parent)
        self.resizable(0, 0)
        self.attributes("-topmost", True)

        self.barcode = tk.StringVar()

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        # Instructions
        ttk.Label(
            w,
            text="Scansiona il barcode o inserisci il codice etichetta:"
        ).pack(anchor=tk.W, pady=(0, 10))

        # Barcode entry
        self.txtBarcode = ttk.Entry(w, textvariable=self.barcode, width=30)
        self.txtBarcode.pack(fill=tk.X, pady=5)
        self.txtBarcode.bind("<Return>", self.on_scan)

        # Result label
        self.lblResult = ttk.Label(w, text="", foreground="gray")
        self.lblResult.pack(fill=tk.X, pady=10)

        # Buttons
        bf = ttk.Frame(w)
        bf.pack(fill=tk.X, pady=(10, 0))

        self.engine.create_button(bf, _("Scarica"), self.on_scan).pack(side=tk.LEFT, padx=5)

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel).pack(side=tk.RIGHT, padx=5)
        self.bind("<Escape>", lambda e: self.on_cancel())

    def on_open(self):
        """Initialize and show the window."""
        self.title("Scarico Etichetta")
        self.engine.dict_instances["barcode"] = self
        self.txtBarcode.focus()

    def on_scan(self, evt=None):
        """Process scanned barcode."""
        code = self.barcode.get().strip()

        if not code:
            return

        # Try to parse as label_id
        try:
            label_id = int(code)
        except ValueError:
            self.show_result("Codice non valido!", "red")
            self.clear_entry()
            return

        # Check if label exists and is in stock
        sql = """
            SELECT
                lb.label_id,
                lb.status,
                p.description AS product_name,
                b.description AS lot
            FROM labels lb
            JOIN batches b ON b.batch_id = lb.batch_id
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            WHERE lb.label_id = ?
        """
        row = self.engine.read(False, sql, (label_id,))

        if not row:
            self.show_result(f"Etichetta {label_id} non trovata!", "red")
            self.clear_entry()
            return

        if row["status"] == 0:
            self.show_result(f"Etichetta {label_id} già scaricata!", "orange")
            self.clear_entry()
            return

        if row["status"] == -1:
            self.show_result(f"Etichetta {label_id} annullata!", "orange")
            self.clear_entry()
            return

        # Unload the label
        result = self.engine.unload_label(label_id)

        if result:
            product = row.get("product_name", "")
            lot = row.get("lot", "")
            self.show_result(
                f"Scaricata: {product}\nLotto: {lot}",
                "green"
            )
            # Refresh warehouse labels list if open
            if "warehouse" in self.engine.dict_instances:
                try:
                    wh = self.engine.dict_instances["warehouse"]
                    if wh.selected_batch_id:
                        wh.load_labels(wh.selected_batch_id)
                except:
                    pass
        else:
            self.show_result("Errore nello scarico!", "red")

        self.clear_entry()

    def show_result(self, text, color):
        """Display result message."""
        self.lblResult.config(text=text, foreground=color)

    def clear_entry(self):
        """Clear entry and refocus."""
        self.barcode.set("")
        self.txtBarcode.focus()

    def on_cancel(self, evt=None):
        """Close the window."""
        if "barcode" in self.engine.dict_instances:
            del self.engine.dict_instances["barcode"]
        self.destroy()
