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

from i18n import _
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    """Expiring batches monitoring window."""

    def __init__(self, parent):
        super().__init__(name="expiring")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.transient(parent)

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the UI."""
        self.minsize(700, 500)

        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Expired batches section
        f1 = ttk.LabelFrame(main_frame, text=_("Lotti Scaduti"), style="App.TLabelframe")
        f1.pack(fill=tk.BOTH, expand=1, pady=(0, 10))

        # Expired treeview
        cols = ("batch_id", "product", "lot", "expiration", "days", "stock")
        self.treeExpired = ttk.Treeview(f1, columns=cols, show="headings", height=8)
        self.treeExpired.column("batch_id", width=0, stretch=False)  # Hidden column
        self.treeExpired.heading("product", text=_("Prodotto"))
        self.treeExpired.heading("lot", text=_("Lotto"))
        self.treeExpired.heading("expiration", text=_("Scadenza"))
        self.treeExpired.heading("days", text=_("GG Scad."))
        self.treeExpired.heading("stock", text=_("Giac."))

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
        f2 = ttk.LabelFrame(main_frame, text=_("Lotti in Scadenza (30 giorni)"), style="App.TLabelframe")
        f2.pack(fill=tk.BOTH, expand=1)

        # Expiring treeview
        self.treeExpiring = ttk.Treeview(f2, columns=cols, show="headings", height=8)
        self.treeExpiring.heading("product", text=_("Prodotto"))
        self.treeExpiring.heading("lot", text=_("Lotto"))
        self.treeExpiring.heading("expiration", text=_("Scadenza"))
        self.treeExpiring.heading("days", text=_("GG Rim."))
        self.treeExpiring.heading("stock", text=_("Giac."))

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

        self.engine.create_button(bf, _("Aggiorna"), self.refresh, width=12).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-a>", lambda e: self.refresh())

        self.btnAnnulla = self.engine.create_button(bf, _("Annulla Lotto"), self.on_cancel_batch, width=14, underline=1)
        self.btnAnnulla.pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-n>", lambda e: self.on_cancel_batch())

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel, width=12).pack(side=tk.RIGHT, padx=5)
        self.bind("<Alt-c>", lambda e: self.on_cancel())
        self.bind("<Escape>", lambda e: self.on_cancel())

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Scadenze"))
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
                _("Seleziona un lotto scaduto da annullare!"),
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
        msg = _("Annullare il lotto '{}' di '{}'?\n\nVerranno annullate {} etichette in giacenza.\n\nQuesta operazione non è reversibile.").format(lot, product_name, labels_count)

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
            _("Lotto '{}' annullato con successo.").format(lot),
            parent=self
        )

        # Refresh this window
        self.refresh()

        # Refresh warehouse if open
        warehouse = self.engine.dict_instances.get("warehouse")
        if warehouse and warehouse.winfo_exists():
            warehouse.refresh()

    def on_cancel(self, evt=None):
        """Close the window."""
        if "expiring" in self.engine.dict_instances:
            del self.engine.dict_instances["expiring"]
        self.destroy()
