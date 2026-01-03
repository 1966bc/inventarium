#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expiring Batches View - Shows expired and expiring batches.

This module provides a view for monitoring batches that are expired
or approaching expiration date.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView


class UI(ParentView):
    """Expiring batches monitoring window."""

    def __init__(self, parent):
        super().__init__(parent, name="expiring")

        if self._reusing:
            return


        self.init_ui()
        self.show()


    def init_ui(self):
        """Build the UI."""
        self.minsize(700, 500)

        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Expired batches section
        f1 = ttk.LabelFrame(main_frame, text=_("Expired Batches"), style="App.TLabelframe")
        f1.pack(fill=tk.BOTH, expand=1, pady=(0, 10))

        # Expired treeview
        cols = ("batch_id", "product", "lot", "expiration", "days", "stock")
        self.treeExpired = ttk.Treeview(f1, columns=cols, show="headings", height=8)
        self.treeExpired.column("batch_id", width=0, stretch=False)  # Hidden column
        self.treeExpired.heading("product", text=_("Product"))
        self.treeExpired.heading("lot", text=_("Batch"))
        self.treeExpired.heading("expiration", text=_("Expiration"))
        self.treeExpired.heading("days", text=_("Days Exp."))
        self.treeExpired.heading("stock", text=_("Stock"))

        self.treeExpired.column("product", width=250)
        self.treeExpired.column("lot", width=120)
        self.treeExpired.column("expiration", width=100, anchor=tk.CENTER)
        self.treeExpired.column("days", width=70, anchor=tk.CENTER)
        self.treeExpired.column("stock", width=60, anchor=tk.CENTER)

        # Scrollbar for expired
        sb1 = ttk.Scrollbar(f1, orient=tk.VERTICAL, command=self.treeExpired.yview)
        self.treeExpired.configure(yscrollcommand=sb1.set)

        self.treeExpired.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(5, 0), pady=5)
        sb1.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)

        # Expiring batches section
        f2 = ttk.LabelFrame(main_frame, text=_("Expiring Batches (30 days)"), style="App.TLabelframe")
        f2.pack(fill=tk.BOTH, expand=1)

        # Expiring treeview
        self.treeExpiring = ttk.Treeview(f2, columns=cols, show="headings", height=8)
        self.treeExpiring.heading("product", text=_("Product"))
        self.treeExpiring.heading("lot", text=_("Batch"))
        self.treeExpiring.heading("expiration", text=_("Expiration"))
        self.treeExpiring.heading("days", text=_("Days Left"))
        self.treeExpiring.heading("stock", text=_("Stock"))

        self.treeExpiring.column("product", width=250)
        self.treeExpiring.column("lot", width=120)
        self.treeExpiring.column("expiration", width=100, anchor=tk.CENTER)
        self.treeExpiring.column("days", width=70, anchor=tk.CENTER)
        self.treeExpiring.column("stock", width=60, anchor=tk.CENTER)

        # Scrollbar for expiring
        sb2 = ttk.Scrollbar(f2, orient=tk.VERTICAL, command=self.treeExpiring.yview)
        self.treeExpiring.configure(yscrollcommand=sb2.set)

        self.treeExpiring.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(5, 0), pady=5)
        sb2.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)

        # Tags for coloring
        self.treeExpired.tag_configure("expired", background="coral")
        self.treeExpiring.tag_configure("critical", background="coral")
        self.treeExpiring.tag_configure("warning", background="khaki")

        # Buttons
        bf = ttk.Frame(main_frame)
        bf.pack(fill=tk.X, pady=(10, 0))

        self.engine.create_button(bf, _("Refresh"), self.refresh, width=12).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-a>", lambda e: self.refresh())

        self.btnAnnulla = self.engine.create_button(bf, _("Cancel Batch"), self.on_cancel_batch, width=14, underline=0)
        self.btnAnnulla.pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-n>", lambda e: self.on_cancel_batch())

        self.engine.create_button(bf, _("Close"), self.on_cancel, width=12).pack(side=tk.RIGHT, padx=5)
        self.bind("<Alt-c>", lambda e: self.on_cancel())

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Expiring"))
        self.engine.dict_instances["expiring"] = self
        self.refresh()

    def format_date(self, date_str):
        """Convert yyyy-mm-dd to dd-mm-yyyy."""
        if date_str and '-' in date_str:
            parts = date_str.split('-')
            if len(parts) == 3:
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
        return date_str or ""

    def refresh(self):
        """Reload data."""
        # Clear trees
        for item in self.treeExpired.get_children():
            self.treeExpired.delete(item)
        for item in self.treeExpiring.get_children():
            self.treeExpiring.delete(item)

        # Load expired batches
        expired = self.engine.get_expired_batches()
        for row in expired:
            self.treeExpired.insert("", tk.END, values=(
                row.get("batch_id", 0),
                row.get("product_name", ""),
                row.get("lot", ""),
                self.format_date(row.get("expiration", "")),
                row.get("days_expired", 0),
                row.get("labels_in_stock", 0)
            ), tags=("expired",))

        # Load expiring batches (30 days)
        expiring = self.engine.get_expiring_batches(30)
        for row in expiring:
            days_left = row.get("days_left", 0)
            if days_left <= 7:
                tag = "critical"
            elif days_left <= 14:
                tag = "warning"
            else:
                tag = ""

            self.treeExpiring.insert("", tk.END, values=(
                row.get("product_name", ""),
                row.get("lot", ""),
                self.format_date(row.get("expiration", "")),
                days_left,
                row.get("labels_in_stock", 0)
            ), tags=(tag,) if tag else ())

    def on_cancel_batch(self, evt=None):
        """Cancel selected expired batch and its labels."""
        # Get selected item from expired tree
        selection = self.treeExpired.selection()
        if not selection:
            messagebox.showwarning(
                self.engine.app_title,
                _("Select an expired batch to cancel!"),
                parent=self
            )
            return

        item = selection[0]
        values = self.treeExpired.item(item, "values")
        batch_id = values[0]
        product_name = values[1]
        lot = values[2]
        labels_count = values[5]

        # Confirm
        msg = _("Cancel batch '{}' of '{}'?\n\n{} labels in stock will be cancelled.\n\nThis operation is not reversible.").format(lot, product_name, labels_count)

        if not messagebox.askyesno(self.engine.app_title, msg, parent=self):
            return

        # Cancel labels (status = -1)
        sql_labels = "UPDATE labels SET status = -1 WHERE batch_id = ? AND status = 1"
        self.engine.write(sql_labels, (batch_id,))

        # Close batch (status = 0)
        sql_batch = "UPDATE batches SET status = 0 WHERE batch_id = ?"
        self.engine.write(sql_batch, (batch_id,))

        messagebox.showinfo(
            self.engine.app_title,
            _("Batch '{}' cancelled successfully.").format(lot),
            parent=self
        )

        # Refresh this window
        self.refresh()

        # Notify subscribers that a batch was cancelled
        self.engine.notify("batch_cancelled")

    def on_cancel(self, evt=None):
        """Close the window."""
        if "expiring" in self.engine.dict_instances:
            del self.engine.dict_instances["expiring"]
        super().on_cancel()
