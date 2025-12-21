#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package History - View order history for a package in Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk

from i18n import _
from tkinter import ttk


class UI(tk.Toplevel):
    """Package order history window."""

    def __init__(self, parent):
        super().__init__(name="package_history")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.transient(parent)
        self.minsize(500, 300)

        self.count = tk.StringVar()

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # History listbox
        w = ttk.LabelFrame(f0, text=_("Storico Ordini"), style="App.TLabelframe")

        # Header
        header = ttk.Label(
            w,
            text=f"{_('Data'):<12} {_('Rif. Richiesta'):<20} {_('Ord.'):>5} {_('Evaso'):>5}",
            font=("Courier", 9, "bold")
        )
        header.pack(fill=tk.X, padx=2)

        scrollbar = ttk.Scrollbar(w, orient=tk.VERTICAL)
        self.lstHistory = tk.Listbox(
            w,
            height=12,
            font=("Courier", 9),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.lstHistory.yview)
        self.lstHistory.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        w.pack(fill=tk.BOTH, expand=1, pady=(0, 5))

        # Bottom frame - count and button
        bf = ttk.Frame(f0)

        ttk.Label(bf, textvariable=self.count, anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel).pack(side=tk.RIGHT, padx=5)
        self.bind("<Escape>", self.on_cancel)
        self.bind("<Alt-c>", self.on_cancel)

        bf.pack(fill=tk.X, pady=5)

    def on_open(self, package_id, product_name):
        """
        Initialize and show the window.

        Args:
            package_id: ID of the package
            product_name: Name of the product for title
        """
        self.package_id = package_id
        self.title(f"{_('Storico')} - {product_name}")
        self.load_history()

    def load_history(self):
        """Load order history for the package."""
        self.lstHistory.delete(0, tk.END)

        # Query to get order history from items/requests/deliveries
        sql = """
            SELECT
                r.issued,
                r.reference,
                i.quantity AS ordered,
                COALESCE(SUM(d.quantity), 0) AS delivered
            FROM items i
            INNER JOIN requests r ON r.request_id = i.request_id
            LEFT JOIN deliveries d ON d.item_id = i.item_id
            WHERE i.package_id = ?
            GROUP BY i.item_id
            ORDER BY r.issued DESC, r.request_id DESC
        """

        rs = self.engine.read(True, sql, (self.package_id,))

        total_ordered = 0
        total_delivered = 0

        if rs:
            for idx, row in enumerate(rs):
                ordered = row["ordered"] or 0
                delivered = row["delivered"] or 0

                total_ordered += ordered
                total_delivered += delivered

                # Format date
                issued = row["issued"] or ""
                if issued and "-" in issued:
                    parts = issued.split("-")
                    if len(parts) == 3:
                        issued = f"{parts[2]}-{parts[1]}-{parts[0]}"

                # Format line
                date_str = issued[:12].ljust(12)
                ref = (row["reference"] or "")[:20].ljust(20)
                ord_str = str(ordered).rjust(5)
                del_str = str(delivered).rjust(5)

                line = f"{date_str} {ref} {ord_str} {del_str}"
                self.lstHistory.insert(tk.END, line)

                # Color fully delivered
                if delivered >= ordered and ordered > 0:
                    self.lstHistory.itemconfig(idx, fg="gray")

        self.count.set(f"{_('Righe')}: {self.lstHistory.size()} | {_('Tot. Ord')}: {total_ordered} | {_('Tot. Evaso')}: {total_delivered}")

    def on_cancel(self, evt=None):
        """Close the window."""
        self.destroy()
