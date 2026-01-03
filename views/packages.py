#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Packages List - View and manage packages for a product in Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView
from views import package


class UI(ParentView):
    """Packages list window for a selected product."""

    def __init__(self, parent):
        super().__init__(parent, name="packages")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(800, 350)

        self.table = "packages"
        self.primary_key = "package_id"
        self.obj = None

        self.init_ui()
        self.show()

    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Packages treeview
        f1 = ttk.Frame(f0)

        self.lbf = ttk.LabelFrame(f1, text=f"{_('Total')}: 0", style="App.TLabelframe")
        w = self.lbf

        # Treeview with columns
        columns = ("reference", "supplier", "labels", "packaging",
                   "conservation", "dark", "category", "fonte")

        self.tree = ttk.Treeview(w, columns=columns, show="headings", height=12)

        # Define headings
        self.tree.heading("reference", text=_("Supp.Code"))
        self.tree.heading("supplier", text=_("Supplier"))
        self.tree.heading("labels", text=_("Lb."))
        self.tree.heading("packaging", text=_("Packaging"))
        self.tree.heading("conservation", text=_("Storage"))
        self.tree.heading("dark", text=_("D"))
        self.tree.heading("category", text=_("Category"))
        self.tree.heading("fonte", text=_("Source"))

        # Define column widths
        self.tree.column("reference", width=80, anchor=tk.W)
        self.tree.column("supplier", width=120, anchor=tk.W)
        self.tree.column("labels", width=40, anchor=tk.E)
        self.tree.column("packaging", width=150, anchor=tk.W)
        self.tree.column("conservation", width=100, anchor=tk.W)
        self.tree.column("dark", width=30, anchor=tk.CENTER)
        self.tree.column("category", width=100, anchor=tk.W)
        self.tree.column("fonte", width=80, anchor=tk.W)

        # Scrollbar
        scrollbar = ttk.Scrollbar(w, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bindings
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.tree.bind("<Double-1>", self.on_item_activated)

        # Tag for inactive items
        self.tree.tag_configure("inactive", foreground="gray")

        w.pack(fill=tk.BOTH, expand=1)

        # Right panel - Buttons
        f2 = ttk.Frame(f0)

        buttons = [
            (_("New"), self.on_add, "<Alt-n>", 0),
            (_("Edit"), self.on_edit, "<Alt-m>", 0),
            (_("Refresh"), self.on_reset, "<Alt-a>", 0),
            (_("Close"), self.on_cancel, "<Alt-c>", 0),
        ]

        for text, cmd, key, ul in buttons:
            self.engine.create_button(f2, text, cmd, underline=ul).pack(fill=tk.X, padx=5, pady=3)
            self.bind(key, lambda e, c=cmd: c())

        f2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # Left panel (pack after buttons)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

    def on_open(self, selected_product):
        """
        Initialize and show the window.

        Args:
            selected_product: Dict with product data
        """
        self.selected_product = selected_product
        product_name = selected_product.get("description", "")
        self.title(f"{_('Packages')} - {product_name}")
        self.engine.dict_instances["packages"] = self
        self.on_reset()

    def on_reset(self, evt=None):
        """Reload packages list."""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        sql = """
            SELECT
                pk.package_id,
                pk.reference,
                s.description AS supplier,
                pk.labels,
                pk.packaging,
                c.description AS conservation,
                pk.in_the_dark,
                cat.description AS category,
                pk.status,
                fs.code AS fonte
            FROM packages pk
            LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
            LEFT JOIN conservations c ON c.conservation_id = pk.conservation_id
            LEFT JOIN categories cat ON cat.category_id = pk.category_id
            LEFT JOIN funding_sources fs ON fs.funding_id = pk.funding_id
            WHERE pk.product_id = ?
            ORDER BY s.description
        """

        rs = self.engine.read(True, sql, (self.selected_product["product_id"],))

        if rs:
            for row in rs:
                package_id = row["package_id"]
                in_the_dark = "S" if row["in_the_dark"] == 1 else "N"

                tag = ("inactive",) if row["status"] != 1 else ()

                self.tree.insert(
                    "", tk.END,
                    iid=package_id,
                    values=(
                        row["reference"] or "",
                        row["supplier"] or "",
                        row["labels"] or "",
                        row["packaging"] or "",
                        row["conservation"] or "",
                        in_the_dark,
                        row["category"] or "",
                        row["fonte"] or ""
                    ),
                    tags=tag
                )

        self.lbf.config(text=f"{_('Total')}: {len(self.tree.get_children())}")

    def on_item_selected(self, evt=None):
        """Handle item selection."""
        selection = self.tree.selection()
        if selection:
            package_id = int(selection[0])
            self.selected_package = self.engine.get_selected(
                self.table, self.primary_key, package_id
            )

    def on_item_activated(self, evt=None):
        """Handle double-click - open edit dialog."""
        self.on_edit()

    def on_add(self, evt=None):
        """Add new package."""
        self.engine.close_instance("package")
        self.obj = package.UI(self)
        self.obj.on_open(self.selected_product)

    def on_edit(self, evt=None):
        """Edit selected package."""
        selection = self.tree.selection()
        if selection:
            self.engine.close_instance("package")
            package_id = int(selection[0])
            self.selected_package = self.engine.get_selected(
                self.table, self.primary_key, package_id
            )
            self.obj = package.UI(self, index=package_id)
            self.obj.on_open(self.selected_product, self.selected_package)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )

    def refresh_and_select(self, package_id):
        """Refresh list and select package by ID."""
        self.on_reset()

        # Select the item
        try:
            self.tree.selection_set(package_id)
            self.tree.see(package_id)
            self.on_item_selected()
        except tk.TclError:
            pass

    def on_cancel(self, evt=None):
        """Close the window."""
        if self.obj is not None:
            try:
                self.obj.destroy()
            except Exception:
                pass
        if "packages" in self.engine.dict_instances:
            del self.engine.dict_instances["packages"]
        super().on_cancel()
