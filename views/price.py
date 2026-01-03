#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Price Dialog - Create/Edit price for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

from i18n import _
from calendarium import Calendarium
from views.child_view import ChildView


class UI(ChildView):
    """Dialog for creating or editing a price."""

    def __init__(self, parent, index=None):
        super().__init__(parent, name="price")

        self.index = index
        self.resizable(0, 0)

        self.package_id = tk.IntVar()
        self.supplier_id = tk.IntVar()
        self.price = tk.StringVar()
        self.vat = tk.StringVar(value="22")
        self.status = tk.BooleanVar()

        self.init_ui()
        self.show()

    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        entry_width = 30

        r = 0
        ttk.Label(w, text=_("Product:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbProduct = ttk.Combobox(w, width=entry_width-2, state="readonly")
        self.cbProduct.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        self.cbProduct.bind("<<ComboboxSelected>>", self.on_product_selected)

        r += 1
        ttk.Label(w, text=_("Package:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbPackage = ttk.Combobox(w, width=entry_width-2, state="readonly")
        self.cbPackage.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Supplier:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbSupplier = ttk.Combobox(w, width=entry_width-2, state="readonly")
        self.cbSupplier.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Price:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        vcmd = self.engine.get_validate_float(self)
        self.txtPrice = ttk.Entry(w, textvariable=self.price, width=entry_width,
                                   validate="key", validatecommand=vcmd)
        self.txtPrice.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("VAT %:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtVat = ttk.Entry(w, textvariable=self.vat, width=entry_width,
                                 validate="key", validatecommand=vcmd)
        self.txtVat.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Valid from:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.calValidFrom = Calendarium(w, "")
        self.calValidFrom.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Active:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.status, style="App.TCheckbutton")
        chk.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Buttons
        r += 1
        bf = ttk.Frame(w)
        bf.grid(row=r, column=0, columnspan=3, pady=10)

        self.engine.create_button(bf, _("Save"), self.on_save).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-s>", self.on_save)
        self.bind("<Return>", self.on_save)

        self.engine.create_button(bf, _("Close"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

    def load_products(self):
        """Load products into combobox."""
        sql = "SELECT product_id, description FROM products WHERE status = 1 ORDER BY description"
        rs = self.engine.read(True, sql)

        self.products = {}
        values = []

        if rs:
            for row in rs:
                self.products[row["description"]] = row["product_id"]
                values.append(row["description"])

        self.cbProduct["values"] = values

    def load_packages(self, product_id):
        """Load packages for selected product."""
        sql = """SELECT pk.package_id, pk.packaging, s.description AS supplier
                 FROM packages pk
                 JOIN suppliers s ON s.supplier_id = pk.supplier_id
                 WHERE pk.product_id = ? AND pk.status = 1
                 ORDER BY pk.packaging"""
        rs = self.engine.read(True, sql, (product_id,))

        self.packages = {}
        values = []

        if rs:
            for row in rs:
                label = f"{row['packaging']} ({row['supplier']})"
                self.packages[label] = row["package_id"]
                values.append(label)

        self.cbPackage["values"] = values
        if values:
            self.cbPackage.set(values[0])

    def load_suppliers(self):
        """Load suppliers into combobox."""
        sql = "SELECT supplier_id, description FROM suppliers WHERE status = 1 ORDER BY description"
        rs = self.engine.read(True, sql)

        self.suppliers = {}
        values = []

        if rs:
            for row in rs:
                self.suppliers[row["description"]] = row["supplier_id"]
                values.append(row["description"])

        self.cbSupplier["values"] = values

    def on_product_selected(self, evt=None):
        """Handle product selection - load packages."""
        product_name = self.cbProduct.get()
        product_id = self.products.get(product_name)
        if product_id:
            self.load_packages(product_id)

    def on_open(self, selected_item=None):
        """
        Open dialog for new or edit price.

        Args:
            selected_item: Dict with price data (for edit) or None (for new)
        """
        self.load_products()
        self.load_suppliers()

        if self.index is not None and selected_item:
            # Edit mode
            self.selected_item = selected_item
            self.title(_("Edit Price"))
            self.set_values()
        else:
            # New price mode
            self.title(_("New Price"))
            self.status.set(1)
            self.calValidFrom.set_today()

        self.cbProduct.focus()

    def set_values(self):
        """Set form values from selected price."""
        # Set price
        price_val = self.selected_item.get("price", 0) or 0
        self.price.set(str(price_val) if price_val else "")

        # Set VAT
        vat = self.selected_item.get("vat", 22) or 22
        self.vat.set(str(vat))

        # Set date in Calendarium
        valid_from_str = self.selected_item.get("valid_from", "") or ""
        if valid_from_str:
            try:
                date_obj = datetime.datetime.strptime(valid_from_str, "%Y-%m-%d").date()
                self.calValidFrom.set_date(date_obj)
            except ValueError:
                self.calValidFrom.set_today()
        else:
            self.calValidFrom.set_today()

        self.status.set(self.selected_item.get("status", 1))

        # Set product and package
        package_id = self.selected_item.get("package_id")
        if package_id:
            sql = """SELECT p.description AS product, pk.packaging, s.description AS supplier
                     FROM packages pk
                     JOIN products p ON p.product_id = pk.product_id
                     JOIN suppliers s ON s.supplier_id = pk.supplier_id
                     WHERE pk.package_id = ?"""
            rs = self.engine.read(False, sql, (package_id,))
            if rs:
                self.cbProduct.set(rs["product"])
                self.load_packages(self.products.get(rs["product"]))
                label = f"{rs['packaging']} ({rs['supplier']})"
                self.cbPackage.set(label)

        # Set supplier
        supplier_id = self.selected_item.get("supplier_id")
        if supplier_id:
            sql = "SELECT description FROM suppliers WHERE supplier_id = ?"
            rs = self.engine.read(False, sql, (supplier_id,))
            if rs:
                self.cbSupplier.set(rs["description"])

    def get_values(self):
        """Get form values as list (order matches table columns excluding PK)."""
        # Get package_id from selection
        package_label = self.cbPackage.get()
        package_id = self.packages.get(package_label) if package_label else None

        # Get supplier_id from selection
        supplier_name = self.cbSupplier.get()
        supplier_id = self.suppliers.get(supplier_name) if supplier_name else None

        # Parse price
        price_str = self.price.get().replace(",", ".")
        try:
            price_val = float(price_str) if price_str else 0
        except ValueError:
            price_val = 0

        # Parse VAT
        vat_str = self.vat.get().replace(",", ".")
        try:
            vat_val = float(vat_str) if vat_str else 22
        except ValueError:
            vat_val = 22

        # Get date from Calendarium
        date_obj = self.calValidFrom.get_date()
        valid_from_str = date_obj.strftime("%Y-%m-%d") if date_obj else None

        return [
            package_id,
            supplier_id,
            price_val,
            vat_val,
            valid_from_str,
            1 if self.status.get() else 0
        ]

    def on_save(self, evt=None):
        """Save the price."""
        # Validate required fields
        if not self.cbPackage.get():
            messagebox.showwarning(
                self.engine.app_title,
                _("Please select a Package!"),
                parent=self
            )
            self.cbPackage.focus()
            return

        if not self.cbSupplier.get():
            messagebox.showwarning(
                self.engine.app_title,
                _("Please select a Supplier!"),
                parent=self
            )
            self.cbSupplier.focus()
            return

        if not self.price.get().strip():
            messagebox.showwarning(
                self.engine.app_title,
                _("The Price field is required!"),
                parent=self
            )
            self.txtPrice.focus()
            return

        if not self.calValidFrom.is_valid:
            messagebox.showwarning(
                self.engine.app_title,
                _("The Valid from field is required!"),
                parent=self
            )
            return

        if messagebox.askyesno(
            self.engine.app_title,
            self.engine.ask_to_save,
            parent=self
        ):
            args = self.get_values()

            if self.index is not None:
                # Update existing
                sql = self.engine.build_sql(self.parent.table, op="update")
                args.append(self.selected_item[self.parent.primary_key])
                self.engine.write(sql, tuple(args))
                pk = self.selected_item[self.parent.primary_key]
            else:
                # Insert new
                sql = self.engine.build_sql(self.parent.table, op="insert")
                pk = self.engine.write(sql, tuple(args))

            self.parent.refresh_and_select(pk)

            self.on_cancel()

        else:
            messagebox.showinfo(
                self.engine.app_title,
                self.engine.abort,
                parent=self
            )

    def on_cancel(self, evt=None):
        """Close the dialog."""
        super().on_cancel()
