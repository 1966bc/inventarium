#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Products List - View and manage products for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView
from views import product
from views import packages


class UI(ParentView):
    """Products list window with add/edit functionality."""

    def __init__(self, parent):
        """
        Initialize products list view.

        Args:
            parent: Parent widget
        """
        super().__init__(parent, name="products")

        # Reusing existing window, skip initialization
        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(600, 400)

        self.table = "products"
        self.primary_key = "product_id"
        self.obj = None
        self.status = tk.IntVar(value=1)
        self.search_text = tk.StringVar()

        self.init_ui()
        self.engine.center_window(self)
        self.show()


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Products treeview
        f1 = ttk.Frame(f0)

        # Products treeview with count in LabelFrame title
        self.lbf = ttk.LabelFrame(f1, text=f"{_('Totale')}: 0", style="App.TLabelframe")
        w = self.lbf

        cols = ("product_id", "reference", "description")
        self.treeview = ttk.Treeview(w, columns=cols, show="headings", height=15)

        # Hidden ID column
        self.treeview.column("product_id", width=0, stretch=False)
        self.treeview.heading("product_id", text="")

        # Visible columns
        self.treeview.column("reference", width=120, anchor=tk.W)
        self.treeview.heading("reference", text=_("Codice"), command=lambda: self.sort_column("reference"))

        self.treeview.column("description", width=350, anchor=tk.W)
        self.treeview.heading("description", text=_("Descrizione"), command=lambda: self.sort_column("description"))

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

        # Right panel - Search, Buttons and filters
        f2 = ttk.Frame(f0)

        # Search box
        w = ttk.LabelFrame(f2, text=_("Ricerca"), style="App.TLabelframe")
        self.txtSearch = ttk.Entry(w, textvariable=self.search_text, width=15)
        self.txtSearch.pack(fill=tk.X, padx=5, pady=5)
        self.txtSearch.bind("<Return>", self.on_search)
        self.txtSearch.bind("<KeyRelease>", self.on_search)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Action buttons
        buttons = [
            (_("Nuovo"), self.on_add, "<Alt-n>", 0),
            (_("Modifica"), self.on_edit, "<Alt-m>", 0),
            (_("Confezioni"), self.on_packages, "<Alt-p>", 4),
            (_("Aggiorna"), self.on_reset, "<Alt-a>", 0),
            (_("Chiudi"), self.on_cancel, "<Alt-c>", 0),
        ]

        for text, cmd, key, ul in buttons:
            self.engine.create_button(f2, text, cmd, underline=ul).pack(fill=tk.X, padx=5, pady=3)
            self.bind(key, lambda e, c=cmd: c())

        # Status filter: Attivi=1, Non Attivi=0, Tutti=-1
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

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Prodotti"))
        self.engine.dict_instances["products"] = self
        self.on_reset()
        self.txtSearch.focus()

    def on_reset(self, evt=None):
        """Reload products list."""
        self.search_text.set("")
        self.load_products()

    def on_search(self, evt=None):
        """Filter products by search text."""
        self.load_products()

    def load_products(self):
        """Load products list with current filters."""
        # Clear treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        sql = """SELECT product_id, reference, description, status
                 FROM products WHERE 1=1"""

        args = []
        status_val = self.status.get()

        if status_val in (0, 1):
            sql += " AND status = ?"
            args.append(status_val)

        # Search filter
        search = self.search_text.get().strip()
        if search:
            sql += " AND (reference LIKE ? OR description LIKE ?)"
            args.append(f"%{search}%")
            args.append(f"%{search}%")

        sql += " ORDER BY description"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for row in rs:
                tag = "inactive" if row["status"] != 1 else ""
                self.treeview.insert("", tk.END, values=(
                    row["product_id"],
                    row["reference"] or "",
                    row["description"] or ""
                ), tags=(tag,) if tag else ())

        self.lbf.config(text=f"{_('Totale')}: {len(self.treeview.get_children())}")

    def sort_column(self, col):
        """Sort treeview by column."""
        items = [(self.treeview.set(k, col), k) for k in self.treeview.get_children("")]
        items.sort()

        for index, (val, k) in enumerate(items):
            self.treeview.move(k, "", index)

    def get_selected_id(self):
        """Get the product_id of the selected item."""
        selection = self.treeview.selection()
        if selection:
            item = selection[0]
            values = self.treeview.item(item, "values")
            return values[0]  # product_id
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
        """Add new product."""
        self.engine.close_instance("product")
        self.obj = product.UI(self)
        self.obj.on_open()

    def on_edit(self, evt=None):
        """Edit selected product."""
        pk = self.get_selected_id()
        if pk:
            self.engine.close_instance("product")
            self.selected_item = self.engine.get_selected(
                self.table, self.primary_key, pk
            )
            self.obj = product.UI(self, index=pk)
            self.obj.on_open(self.selected_item)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )

    def on_packages(self, evt=None):
        """Open packages for selected product."""
        self.engine.close_instance("packages")
        pk = self.get_selected_id()
        if pk:
            self.selected_item = self.engine.get_selected(
                self.table, self.primary_key, pk
            )
            self.obj = packages.UI(self)
            self.obj.on_open(self.selected_item)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )

    def refresh_and_select(self, product_id):
        """Refresh list and select product by ID."""
        self.load_products()

        # Find and select the product by ID
        for item in self.treeview.get_children():
            values = self.treeview.item(item, "values")
            if str(values[0]) == str(product_id):
                self.treeview.selection_set(item)
                self.treeview.see(item)
                self.on_item_selected()
                break

    def on_cancel(self, evt=None):
        """Close the window and clean up."""
        if self.obj is not None:
            try:
                self.obj.destroy()
            except Exception:
                pass
        if "products" in self.engine.dict_instances:
            del self.engine.dict_instances["products"]
        super().on_cancel()
