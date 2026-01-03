#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Request Item Dialog - Add/Edit item for a request in Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.child_view import ChildView


class UI(ChildView):
    """Dialog for adding or editing a request item."""

    def __init__(self, parent, index=None):
        super().__init__(parent, name="request_item")

        self.index = index
        self.minsize(450, 300)

        self.quantity = tk.IntVar(value=1)

        # Dictionaries for combobox mappings
        self.dict_categories = {}
        self.dict_products = {}
        self.dict_packages = {}

        self.init_ui()
        self.show()


    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        combo_width = 50  # Wider for long product names

        r = 0
        ttk.Label(w, text=_("Category:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbCategories = ttk.Combobox(w, state="readonly", width=combo_width, style="App.TCombobox")
        self.cbCategories.bind("<<ComboboxSelected>>", self.on_category_selected)
        self.cbCategories.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Product:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbProducts = ttk.Combobox(w, state="readonly", width=combo_width, style="App.TCombobox")
        self.cbProducts.bind("<<ComboboxSelected>>", self.on_product_selected)
        self.cbProducts.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Package:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbPackages = ttk.Combobox(w, state="readonly", width=combo_width, style="App.TCombobox")
        self.cbPackages.bind("<<ComboboxSelected>>", self.on_package_selected)
        self.cbPackages.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Quantity:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        vcmd = self.engine.get_validate_integer(self)
        self.txtQuantity = ttk.Entry(
            w, textvariable=self.quantity, width=8,
            validate="key", validatecommand=vcmd
        )
        self.txtQuantity.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Buttons
        r += 1
        bf = ttk.Frame(w)
        bf.grid(row=r, column=0, columnspan=2, pady=10)

        self.engine.create_button(bf, _("Save"), self.on_save).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-s>", self.on_save)

        self.engine.create_button(bf, _("Close"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)

        # History treeview
        r += 1
        self.lbfHistory = ttk.LabelFrame(w, text=_("Order History"), style="App.TLabelframe")
        self.lbfHistory.grid(row=r, column=0, columnspan=2, sticky=tk.NSEW, pady=(10, 0))

        # Treeview with columns
        columns = ("date", "reference", "ordered", "delivered")
        self.trvHistory = ttk.Treeview(
            self.lbfHistory,
            columns=columns,
            show="headings",
            height=6,
            selectmode="browse"
        )

        # Configure columns
        self.trvHistory.heading("date", text=_("Date"))
        self.trvHistory.heading("reference", text=_("Reference"))
        self.trvHistory.heading("ordered", text=_("Ord."))
        self.trvHistory.heading("delivered", text=_("Del."))

        self.trvHistory.column("date", width=90, anchor=tk.W)
        self.trvHistory.column("reference", width=120, anchor=tk.W)
        self.trvHistory.column("ordered", width=50, anchor=tk.CENTER)
        self.trvHistory.column("delivered", width=50, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.lbfHistory, orient=tk.VERTICAL, command=self.trvHistory.yview)
        self.trvHistory.configure(yscrollcommand=scrollbar.set)

        self.trvHistory.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tag for completed orders (gray)
        self.trvHistory.tag_configure("completed", foreground="gray")

        # Make the history row expandable
        w.rowconfigure(r, weight=1)

    def on_open(self, selected_request, selected_item=None, category_id=None):
        """
        Open dialog for new or edit item.

        Args:
            selected_request: Dict with request data
            selected_item: Dict with item data (for edit) or None (for new)
            category_id: Pre-selected category ID (for new items)
        """
        self.selected_request = selected_request

        # Load categories first
        self.set_categories()

        if self.index is not None and selected_item:
            # Edit mode
            self.selected_item = selected_item
            self.title(_("Edit Item"))
            self.set_values()
        else:
            # New item mode
            self.title(_("New Item"))
            self.quantity.set(1)

            # Pre-select category if provided
            if category_id:
                for key, value in self.dict_categories.items():
                    if value == category_id:
                        self.cbCategories.current(key)
                        self.set_products(category_id)
                        break

        self.cbProducts.focus()

    def set_categories(self):
        """Load categories into combobox."""
        self.dict_categories = {}
        voices = []

        # reference_id = 1 is for Products categories
        sql = """SELECT category_id, description
                 FROM categories
                 WHERE reference_id = 1 AND status = 1
                 ORDER BY description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs):
                self.dict_categories[idx] = row["category_id"]
                voices.append(row["description"])

        self.cbCategories["values"] = voices

    def on_category_selected(self, evt=None):
        """Handle category selection - load products for that category."""
        if self.cbCategories.current() != -1:
            category_id = self.dict_categories[self.cbCategories.current()]
            self.set_products(category_id)
            # Clear packages and history when category changes
            self.cbPackages["values"] = []
            self.cbPackages.set("")
            for item in self.trvHistory.get_children():
                self.trvHistory.delete(item)
            self.lbfHistory.config(text=_("Order History"))

    def set_products(self, category_id):
        """Load products into combobox filtered by category."""
        self.dict_products = {}
        voices = []

        sql = """SELECT DISTINCT p.product_id, p.description
                 FROM products p
                 INNER JOIN packages pk ON pk.product_id = p.product_id
                 WHERE p.status = 1 AND pk.status = 1
                 AND pk.category_id = ?
                 ORDER BY p.description"""

        rs = self.engine.read(True, sql, (category_id,))

        if rs:
            for idx, row in enumerate(rs):
                self.dict_products[idx] = row["product_id"]
                voices.append(row["description"])

        self.cbProducts["values"] = voices
        self.cbProducts.set("")

    def on_product_selected(self, evt=None):
        """Handle product selection - load packages."""
        if self.cbProducts.current() != -1:
            product_id = self.dict_products[self.cbProducts.current()]
            category_id = self.dict_categories.get(self.cbCategories.current())
            self.set_packages(product_id, category_id)

    def set_packages(self, product_id, category_id=None):
        """Load packages for selected product filtered by category."""
        self.dict_packages = {}
        voices = []

        sql = """SELECT pk.package_id, s.description AS supplier, pk.packaging
                 FROM packages pk
                 INNER JOIN suppliers s ON s.supplier_id = pk.supplier_id
                 WHERE pk.product_id = ? AND pk.status = 1"""

        args = [product_id]

        if category_id:
            sql += " AND pk.category_id = ?"
            args.append(category_id)

        sql += " ORDER BY s.description"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for idx, row in enumerate(rs):
                self.dict_packages[idx] = row["package_id"]
                display = f"{row['supplier']} - {row['packaging']}"
                voices.append(display)

        self.cbPackages["values"] = voices
        if voices:
            self.cbPackages.current(0)
            # Load history for first package
            self.load_history(self.dict_packages[0])

    def on_package_selected(self, evt=None):
        """Handle package selection - load order history."""
        if self.cbPackages.current() != -1:
            package_id = self.dict_packages[self.cbPackages.current()]
            self.load_history(package_id)

    def load_history(self, package_id):
        """Load order history for selected package."""
        # Clear existing items
        for item in self.trvHistory.get_children():
            self.trvHistory.delete(item)

        # Query with ordered quantity and delivered (labels generated)
        sql = """
            SELECT
                r.issued,
                r.reference,
                i.quantity AS ordered,
                (SELECT COUNT(*) FROM labels lb
                 INNER JOIN batches b ON b.batch_id = lb.batch_id
                 WHERE b.package_id = i.package_id
                 AND lb.loaded >= r.issued) AS delivered
            FROM items i
            INNER JOIN requests r ON r.request_id = i.request_id
            WHERE i.package_id = ?
            ORDER BY r.issued DESC, r.request_id DESC
            LIMIT 10
        """

        rs = self.engine.read(True, sql, (package_id,))

        if rs:
            for row in rs:
                # Format date (YYYY-MM-DD to DD-MM-YYYY)
                issued = row["issued"] or ""
                if issued and "-" in issued:
                    parts = issued.split("-")
                    if len(parts) == 3:
                        issued = f"{parts[2]}-{parts[1]}-{parts[0]}"

                ordered = row["ordered"] or 0
                delivered = row["delivered"] or 0
                reference = row["reference"] or ""

                # Determine tag for completed orders
                tags = ("completed",) if delivered >= ordered and ordered > 0 else ()

                # Insert into treeview
                self.trvHistory.insert(
                    "", tk.END,
                    values=(issued, reference, ordered, delivered),
                    tags=tags
                )

        # Update label with count
        count = len(self.trvHistory.get_children())
        self.lbfHistory.config(text=f"{_('Order History')} ({count})")

    def set_values(self):
        """Set form values from selected item."""
        # Get package info
        package = self.engine.get_selected("packages", "package_id", self.selected_item["package_id"])

        if package:
            # Set category first
            category_id = package.get("category_id")
            if category_id:
                try:
                    key = next(
                        key for key, value in self.dict_categories.items()
                        if value == category_id
                    )
                    self.cbCategories.current(key)
                    self.set_products(category_id)
                except StopIteration:
                    pass

            # Set product
            try:
                key = next(
                    key for key, value in self.dict_products.items()
                    if value == package["product_id"]
                )
                self.cbProducts.current(key)
                self.set_packages(package["product_id"], category_id)
            except StopIteration:
                pass

            # Set package
            try:
                key = next(
                    key for key, value in self.dict_packages.items()
                    if value == self.selected_item["package_id"]
                )
                self.cbPackages.current(key)
                # Load history for this package
                self.load_history(self.selected_item["package_id"])
            except StopIteration:
                pass

        self.quantity.set(self.selected_item.get("quantity", 1))

    def get_values(self):
        """Get form values as list."""
        package_idx = self.cbPackages.current()

        return [
            self.selected_request["request_id"],
            self.dict_packages.get(package_idx, 0),
            self.quantity.get(),
            1  # status
        ]

    def on_save(self, evt=None):
        """Save the item."""
        # Validate required fields
        if self.cbCategories.current() == -1:
            messagebox.showwarning(
                self.engine.app_title,
                _("Please select a category!"),
                parent=self
            )
            self.cbCategories.focus()
            return

        if self.cbProducts.current() == -1:
            messagebox.showwarning(
                self.engine.app_title,
                _("Please select a product!"),
                parent=self
            )
            self.cbProducts.focus()
            return

        if self.cbPackages.current() == -1:
            messagebox.showwarning(
                self.engine.app_title,
                _("Please select a package!"),
                parent=self
            )
            self.cbPackages.focus()
            return

        if self.quantity.get() < 1:
            messagebox.showwarning(
                self.engine.app_title,
                _("Quantity must be at least 1!"),
                parent=self
            )
            self.txtQuantity.focus()
            return

        if messagebox.askyesno(
            self.engine.app_title,
            self.engine.ask_to_save,
            parent=self
        ):
            args = self.get_values()

            if self.index is not None:
                # Update existing item
                sql = """UPDATE items
                         SET request_id = ?, package_id = ?, quantity = ?, status = ?
                         WHERE item_id = ?"""
                args.append(self.selected_item["item_id"])
                self.engine.write(sql, tuple(args))
            else:
                # Check if package already exists in this request
                check_sql = """SELECT item_id FROM items
                               WHERE request_id = ? AND package_id = ? AND status = 1"""
                existing = self.engine.read(False, check_sql,
                                           (self.selected_request["request_id"],
                                            self.dict_packages[self.cbPackages.current()]))

                if existing:
                    # Update quantity instead of adding new
                    sql = """UPDATE items SET quantity = quantity + ?
                             WHERE item_id = ?"""
                    self.engine.write(sql, (self.quantity.get(), existing["item_id"]))
                    messagebox.showinfo(
                        self.engine.app_title,
                        _("Item already exists.") + "\n" + _("Quantity has been added."),
                        parent=self
                    )
                else:
                    # Insert new item
                    sql = """INSERT INTO items (request_id, package_id, quantity, status)
                             VALUES (?, ?, ?, ?)"""
                    self.engine.write(sql, tuple(args))

            # Refresh parent list keeping selection
            self.parent.refresh_request_list()

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
