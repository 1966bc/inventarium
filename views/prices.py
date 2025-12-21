#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prices List - View and manage price list for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView
from views import price


class UI(ParentView):
    """Prices list window with add/edit functionality."""

    def __init__(self, parent):
        super().__init__(parent, name="prices")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(900, 450)

        self.table = "prices"
        self.primary_key = "price_id"
        self.obj = None
        self.status = tk.IntVar(value=1)
        self.supplier_id = tk.IntVar(value=0)

        self.init_ui()
        self.engine.center_window(self)
        self.show()

    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Prices treeview
        f1 = ttk.Frame(f0)

        # Prices treeview with count in LabelFrame title
        self.lbf = ttk.LabelFrame(f1, text=f"{_('Totale')}: 0", style="App.TLabelframe")
        w = self.lbf

        cols = ("price_id", "product", "package", "supplier", "price", "vat", "valid_from")
        self.treeview = ttk.Treeview(w, columns=cols, show="headings", height=15)

        # Hidden ID column
        self.treeview.column("price_id", width=0, stretch=False)
        self.treeview.heading("price_id", text="")

        # Visible columns
        self.treeview.column("product", width=180, anchor=tk.W)
        self.treeview.heading("product", text=_("Prodotto"), command=lambda: self.sort_column("product"))

        self.treeview.column("package", width=120, anchor=tk.W)
        self.treeview.heading("package", text=_("Confezionamento"), command=lambda: self.sort_column("package"))

        self.treeview.column("supplier", width=150, anchor=tk.W)
        self.treeview.heading("supplier", text=_("Fornitore"), command=lambda: self.sort_column("supplier"))

        self.treeview.column("price", width=100, anchor=tk.E)
        self.treeview.heading("price", text=_("Prezzo"), command=lambda: self.sort_column("price"))

        self.treeview.column("vat", width=60, anchor=tk.E)
        self.treeview.heading("vat", text=_("IVA %"), command=lambda: self.sort_column("vat"))

        self.treeview.column("valid_from", width=100, anchor=tk.CENTER)
        self.treeview.heading("valid_from", text=_("Valido dal"), command=lambda: self.sort_column("valid_from"))

        # Scrollbar
        scrollbar = ttk.Scrollbar(w, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bindings
        self.treeview.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.treeview.bind("<Double-1>", self.on_item_activated)

        # Tag for inactive items
        self.treeview.tag_configure("inactive", background="light gray")

        w.pack(fill=tk.BOTH, expand=1)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Right panel - Buttons and filters
        f2 = ttk.Frame(f0)

        # Action buttons
        buttons = [
            (_("Nuovo"), self.on_add, "<Alt-n>", 0),
            (_("Modifica"), self.on_edit, "<Alt-m>", 0),
            (_("Aggiorna"), self.on_reset, "<Alt-a>", 0),
            (_("Chiudi"), self.on_cancel, "<Alt-c>", 0),
        ]

        for text, cmd, key, ul in buttons:
            self.engine.create_button(f2, text, cmd, underline=ul).pack(fill=tk.X, padx=5, pady=3)
            self.bind(key, lambda e, c=cmd: c())

        # Supplier filter
        w = ttk.LabelFrame(f2, text=_("Fornitore"), style="App.TLabelframe")
        self.cbSupplierFilter = ttk.Combobox(w, width=18, state="readonly")
        self.cbSupplierFilter.pack(padx=5, pady=5)
        self.cbSupplierFilter.bind("<<ComboboxSelected>>", self.on_reset)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Status filter
        w = ttk.LabelFrame(f2, text=_("Stato"), style="App.TLabelframe")
        for text, value in ((_("Attivi"), 1), (_("Non Attivi"), 0), (_("Tutti"), -1)):
            ttk.Radiobutton(
                w, text=text, variable=self.status,
                value=value,
                command=self.on_reset,
                style="App.TRadiobutton"
            ).pack(anchor=tk.W, padx=5, pady=2)
        w.pack(fill=tk.X, padx=5, pady=5)

        f2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    def load_suppliers_filter(self):
        """Load suppliers into filter combobox."""
        sql = "SELECT supplier_id, description FROM suppliers WHERE status = 1 ORDER BY description"
        rs = self.engine.read(True, sql)

        self.suppliers_filter = {_("Tutti"): 0}
        values = [_("Tutti")]

        if rs:
            for row in rs:
                self.suppliers_filter[row["description"]] = row["supplier_id"]
                values.append(row["description"])

        self.cbSupplierFilter["values"] = values
        self.cbSupplierFilter.set(_("Tutti"))

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Listino Prezzi"))
        self.engine.dict_instances["prices"] = self
        self.load_suppliers_filter()
        self.on_reset()

    def on_reset(self, evt=None):
        """Reload prices list."""
        self.load_prices()

    def load_prices(self):
        """Load prices list with current filters."""
        # Clear treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        sql = """SELECT pr.price_id, p.description AS product, pk.packaging,
                        s.description AS supplier, pr.price, pr.vat, pr.valid_from, pr.status
                 FROM prices pr
                 JOIN packages pk ON pk.package_id = pr.package_id
                 JOIN products p ON p.product_id = pk.product_id
                 JOIN suppliers s ON s.supplier_id = pr.supplier_id
                 WHERE 1=1"""

        args = []
        status_val = self.status.get()

        if status_val in (0, 1):
            sql += " AND pr.status = ?"
            args.append(status_val)

        # Supplier filter
        supplier_name = self.cbSupplierFilter.get()
        supplier_id = self.suppliers_filter.get(supplier_name, 0)
        if supplier_id:
            sql += " AND pr.supplier_id = ?"
            args.append(supplier_id)

        sql += " ORDER BY p.description, pk.packaging, s.description"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for row in rs:
                tag = "inactive" if row["status"] != 1 else ""
                price_str = f"€ {row['price']:,.2f}" if row["price"] else ""
                vat_str = f"{row['vat']:.0f}" if row["vat"] else ""
                self.treeview.insert("", tk.END, values=(
                    row["price_id"],
                    row["product"] or "",
                    row["packaging"] or "",
                    row["supplier"] or "",
                    price_str,
                    vat_str,
                    row["valid_from"] or ""
                ), tags=(tag,) if tag else ())

        self.lbf.config(text=f"{_('Totale')}: {len(self.treeview.get_children())}")

    def sort_column(self, col):
        """Sort treeview by column."""
        items = [(self.treeview.set(k, col), k) for k in self.treeview.get_children("")]
        items.sort()

        for index, (val, k) in enumerate(items):
            self.treeview.move(k, "", index)

    def get_selected_id(self):
        """Get the price_id of the selected item."""
        selection = self.treeview.selection()
        if selection:
            item = selection[0]
            values = self.treeview.item(item, "values")
            return values[0]  # price_id
        return None

    def on_item_selected(self, evt=None):
        """Handle item selection."""
        pk = self.get_selected_id()
        if pk:
            self.selected_item = self.engine.get_selected(
                self.table, self.primary_key, pk
            )

    def on_item_activated(self, evt=None):
        """Handle double-click - open edit dialog."""
        self.on_edit()

    def on_add(self, evt=None):
        """Add new price."""
        self.engine.close_instance("price")
        self.obj = price.UI(self)
        self.obj.on_open()

    def on_edit(self, evt=None):
        """Edit selected price."""
        pk = self.get_selected_id()
        if pk:
            self.engine.close_instance("price")
            self.selected_item = self.engine.get_selected(
                self.table, self.primary_key, pk
            )
            self.obj = price.UI(self, index=pk)
            self.obj.on_open(self.selected_item)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )

    def refresh_and_select(self, price_id):
        """Refresh list and select price by ID."""
        self.load_prices()

        # Find and select the price by ID
        for item in self.treeview.get_children():
            values = self.treeview.item(item, "values")
            if str(values[0]) == str(price_id):
                self.treeview.selection_set(item)
                self.treeview.see(item)
                self.on_item_selected()
                break

    def on_cancel(self, evt=None):
        """Close the window."""
        if self.obj is not None:
            try:
                self.obj.destroy()
            except Exception:
                pass
        if "prices" in self.engine.dict_instances:
            del self.engine.dict_instances["prices"]
        super().on_cancel()
