#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package History - View order history for a package in Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk

from i18n import _
from views.child_view import ChildView


class UI(ChildView):
    """Package order history window."""

    def __init__(self, parent):
        super().__init__(parent, name="package_history")

        self.minsize(450, 300)

        self.count = tk.StringVar()

        self.init_ui()
        self.show()


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # History treeview
        w = ttk.LabelFrame(f0, text=_("Order History"), style="App.TLabelframe")

        cols = ("date", "reference", "ordered", "delivered")
        self.treeHistory = ttk.Treeview(w, columns=cols, show="headings", height=10)

        self.treeHistory.column("date", width=90, minwidth=80, anchor=tk.W)
        self.treeHistory.heading("date", text=_("Date"), anchor=tk.W)

        self.treeHistory.column("reference", width=150, minwidth=100, anchor=tk.W)
        self.treeHistory.heading("reference", text=_("Request Ref."), anchor=tk.W)

        self.treeHistory.column("ordered", width=50, minwidth=40, anchor=tk.CENTER)
        self.treeHistory.heading("ordered", text=_("Ord."), anchor=tk.CENTER)

        self.treeHistory.column("delivered", width=50, minwidth=40, anchor=tk.CENTER)
        self.treeHistory.heading("delivered", text=_("Deliv."), anchor=tk.CENTER)

        sb = ttk.Scrollbar(w, orient=tk.VERTICAL, command=self.treeHistory.yview)
        self.treeHistory.configure(yscrollcommand=sb.set)
        self.treeHistory.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        # Tag for completed orders
        self.treeHistory.tag_configure("completed", foreground="gray")

        w.pack(fill=tk.BOTH, expand=1, pady=(0, 5))

        # Bottom frame - count and button
        bf = ttk.Frame(f0)

        ttk.Label(bf, textvariable=self.count, anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.engine.create_button(bf, _("Close"), self.on_cancel).pack(side=tk.RIGHT, padx=5)
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
        self.title(f"{_('History')} - {product_name}")
        self.load_history()

    def load_history(self):
        """Load order history for the package."""
        for item in self.treeHistory.get_children():
            self.treeHistory.delete(item)

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
            for row in rs:
                ordered = row["ordered"] or 0
                delivered = row["delivered"] or 0

                total_ordered += ordered
                total_delivered += delivered

                # Format date dd-mm-yyyy
                issued = row["issued"] or ""
                if issued and "-" in issued:
                    parts = issued.split("-")
                    if len(parts) == 3:
                        issued = f"{parts[2]}-{parts[1]}-{parts[0]}"

                reference = row["reference"] or ""

                # Determine tag
                tag = ("completed",) if delivered >= ordered and ordered > 0 else ()

                self.treeHistory.insert(
                    "", tk.END,
                    values=(issued, reference, ordered, delivered),
                    tags=tag
                )

        row_count = len(self.treeHistory.get_children())
        self.count.set(f"{_('Rows')}: {row_count} | {_('Tot. Ord')}: {total_ordered} | {_('Tot. Deliv')}: {total_delivered}")

    def on_cancel(self, evt=None):
        """Close the window."""
        super().on_cancel()
