#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package Dialog - Create/Edit package for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views import package_funding
from views.child_view import ChildView


class UI(ChildView):
    """Dialog for creating or editing a package."""

    def __init__(self, parent, index=None):
        super().__init__(parent, name="package")

        self.index = index
        self.resizable(0, 0)

        # Form variables
        self.reference = tk.StringVar()
        self.packaging = tk.StringVar()
        self.order_by_piece = tk.IntVar(value=1)  # 1=al pezzo, 0=a confezione
        self.pieces_per_label = tk.IntVar(value=1)
        self.labels_per_unit = tk.IntVar(value=1)
        self.reorder = tk.IntVar(value=0)
        self.in_the_dark = tk.BooleanVar()
        self.status = tk.BooleanVar()

        # Dictionaries for combobox mappings
        self.dict_suppliers = {}
        self.dict_conservations = {}
        self.dict_categories = {}
        self.dict_locations = {}

        self.init_ui()
        self.engine.center_window(self)
        self.show()


    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        field_width = 30

        r = 0
        ttk.Label(w, text=_("Fornitore:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbSuppliers = ttk.Combobox(w, state="readonly", width=field_width, style="App.TCombobox")
        self.cbSuppliers.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Cod. Fornitore:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtReference = ttk.Entry(w, textvariable=self.reference, width=field_width)
        self.txtReference.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Confezionamento:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtPackaging = ttk.Entry(w, textvariable=self.packaging, width=field_width)
        self.txtPackaging.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Conservazione:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbConservations = ttk.Combobox(w, state="readonly", width=field_width, style="App.TCombobox")
        self.cbConservations.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Categoria:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbCategories = ttk.Combobox(w, state="readonly", width=field_width, style="App.TCombobox")
        self.cbCategories.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Ubicazione:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbLocations = ttk.Combobox(w, state="readonly", width=field_width, style="App.TCombobox")
        self.cbLocations.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Ordinazione
        r += 1
        ttk.Label(w, text=_("Ordinazione:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        order_frame = ttk.Frame(w)
        order_frame.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Radiobutton(
            order_frame, text=_("Al pezzo"), variable=self.order_by_piece, value=1,
            style="App.TRadiobutton"
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            order_frame, text=_("A confezione"), variable=self.order_by_piece, value=0,
            style="App.TRadiobutton"
        ).pack(side=tk.LEFT, padx=10)

        r += 1
        ttk.Label(w, text=_("Pezzi per etichetta:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.spnPiecesPerLabel = ttk.Spinbox(
            w, from_=1, to=10000, textvariable=self.pieces_per_label, width=8
        )
        self.spnPiecesPerLabel.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Etichette per unità:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.spnLabelsPerUnit = ttk.Spinbox(
            w, from_=1, to=100, textvariable=self.labels_per_unit, width=8
        )
        self.spnLabelsPerUnit.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Soglia riordino:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.spnReorder = ttk.Spinbox(
            w, from_=0, to=1000, textvariable=self.reorder, width=8
        )
        self.spnReorder.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Al buio:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.in_the_dark, style="App.TCheckbutton")
        chk.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Attivo:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.status, style="App.TCheckbutton")
        chk.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Buttons
        r += 1
        bf = ttk.Frame(w)
        bf.grid(row=r, column=0, columnspan=2, pady=10)

        self.engine.create_button(bf, _("Salva"), self.on_save).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-s>", self.on_save)

        self.btnFunding = self.engine.create_button(bf, _("Fonti/Delibere"), self.on_funding)
        self.btnFunding.pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-f>", self.on_funding)

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

    def on_open(self, selected_product, selected_package=None):
        """
        Open dialog for new or edit package.

        Args:
            selected_product: Dict with product data
            selected_package: Dict with package data (for edit) or None (for new)
        """
        self.selected_product = selected_product

        # Load combobox data
        self.set_suppliers()
        self.set_conservations()
        self.set_categories()
        self.set_locations()

        product_name = selected_product.get("description", "")

        if self.index is not None and selected_package:
            # Edit mode
            self.selected_package = selected_package
            self.title(f"Modifica Confezione - {product_name}")
            self.set_values()
            self.btnFunding.config(state=tk.NORMAL)
        else:
            # New package mode
            self.title(f"Nuova Confezione - {product_name}")
            self.order_by_piece.set(1)
            self.pieces_per_label.set(1)
            self.labels_per_unit.set(1)
            self.reorder.set(0)
            self.status.set(1)
            self.btnFunding.config(state=tk.DISABLED)  # No package_id yet

        self.cbSuppliers.focus()

    def set_suppliers(self):
        """Load suppliers into combobox."""
        self.dict_suppliers = {}
        voices = []

        sql = """SELECT supplier_id, description
                 FROM suppliers
                 WHERE status = 1
                 ORDER BY description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs):
                self.dict_suppliers[idx] = row["supplier_id"]
                voices.append(row["description"])

        self.cbSuppliers["values"] = voices

    def set_conservations(self):
        """Load conservations into combobox."""
        self.dict_conservations = {}
        voices = []

        sql = """SELECT conservation_id, description
                 FROM conservations
                 WHERE status = 1
                 ORDER BY description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs):
                self.dict_conservations[idx] = row["conservation_id"]
                voices.append(row["description"])

        self.cbConservations["values"] = voices

    def set_categories(self):
        """Load categories into combobox (product categories, reference_id=1)."""
        self.dict_categories = {}
        voices = []

        # Add "Not assigned" option
        self.dict_categories[0] = 0
        voices.append(_("-- Non assegnata --"))

        sql = """SELECT category_id, description
                 FROM categories
                 WHERE reference_id = 1 AND status = 1
                 ORDER BY description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs, start=1):
                self.dict_categories[idx] = row["category_id"]
                voices.append(row["description"])

        self.cbCategories["values"] = voices

    def set_locations(self):
        """Load locations into combobox."""
        self.dict_locations = {}
        voices = []

        # Add "Not assigned" option
        self.dict_locations[0] = None
        voices.append(_("-- Non assegnata --"))

        sql = """SELECT location_id, description, room
                 FROM locations
                 WHERE status = 1
                 ORDER BY room, description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs, start=1):
                self.dict_locations[idx] = row["location_id"]
                room = row["room"] or ""
                desc = row["description"] or ""
                display = f"{room} - {desc}" if room else desc
                voices.append(display)

        self.cbLocations["values"] = voices

    def set_values(self):
        """Set form values from selected package."""
        # Set supplier
        try:
            key = next(
                key for key, value in self.dict_suppliers.items()
                if value == self.selected_package.get("supplier_id")
            )
            self.cbSuppliers.current(key)
        except StopIteration:
            pass

        # Set conservation
        try:
            key = next(
                key for key, value in self.dict_conservations.items()
                if value == self.selected_package.get("conservation_id")
            )
            self.cbConservations.current(key)
        except StopIteration:
            pass

        # Set category
        try:
            key = next(
                key for key, value in self.dict_categories.items()
                if value == self.selected_package.get("category_id")
            )
            self.cbCategories.current(key)
        except StopIteration:
            self.cbCategories.current(0)

        # Set location
        try:
            key = next(
                key for key, value in self.dict_locations.items()
                if value == self.selected_package.get("location_id")
            )
            self.cbLocations.current(key)
        except StopIteration:
            self.cbLocations.current(0)

        self.reference.set(self.selected_package.get("reference", ""))
        self.packaging.set(self.selected_package.get("packaging", ""))
        self.order_by_piece.set(self.selected_package.get("order_by_piece", 1))
        self.pieces_per_label.set(self.selected_package.get("pieces_per_label", 1) or 1)
        self.labels_per_unit.set(self.selected_package.get("labels_per_unit", 1) or 1)
        self.reorder.set(self.selected_package.get("reorder", 0) or 0)
        self.in_the_dark.set(self.selected_package.get("in_the_dark", 0))
        self.status.set(self.selected_package.get("status", 1))

    def get_values(self):
        """Get form values as list (order matches table columns excluding PK)."""
        supplier_idx = self.cbSuppliers.current()
        conservation_idx = self.cbConservations.current()
        category_idx = self.cbCategories.current()
        location_idx = self.cbLocations.current()

        # Get current labels count (preserve on edit, 0 on new)
        labels = 0
        if self.index is not None:
            labels = self.selected_package.get("labels", 0) or 0

        return [
            self.selected_product["product_id"],      # product_id
            self.dict_suppliers.get(supplier_idx, 0), # supplier_id
            self.reference.get().strip(),             # reference
            labels,                                   # labels (preserved)
            self.packaging.get().strip(),             # packaging
            self.dict_conservations.get(conservation_idx, 0),  # conservation_id
            1 if self.in_the_dark.get() else 0,       # in_the_dark
            self.dict_categories.get(category_idx, 0),  # category_id
            self.dict_locations.get(location_idx),    # location_id
            1 if self.status.get() else 0,            # status
            1 if self.order_by_piece.get() else 0,    # order_by_piece
            self.pieces_per_label.get(),              # pieces_per_label
            self.reorder.get(),                       # reorder
            None,                                     # funding_id
            self.labels_per_unit.get(),               # labels_per_unit
        ]

    def on_save(self, evt=None):
        """Save the package."""
        # Validate required fields
        if self.cbSuppliers.current() == -1:
            messagebox.showwarning(
                self.engine.app_title,
                _("Selezionare un fornitore!"),
                parent=self
            )
            self.cbSuppliers.focus()
            return

        if not self.reference.get().strip():
            messagebox.showwarning(
                self.engine.app_title,
                _("Il campo Codice Fornitore è obbligatorio!"),
                parent=self
            )
            self.txtReference.focus()
            return

        if not self.packaging.get().strip():
            messagebox.showwarning(
                self.engine.app_title,
                _("Il campo Confezionamento è obbligatorio!"),
                parent=self
            )
            self.txtPackaging.focus()
            return

        if self.cbConservations.current() == -1:
            messagebox.showwarning(
                self.engine.app_title,
                _("Selezionare una modalità di conservazione!"),
                parent=self
            )
            self.cbConservations.focus()
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
                args.append(self.selected_package[self.parent.primary_key])
                self.engine.write(sql, tuple(args))
                pk = self.selected_package[self.parent.primary_key]
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

    def on_funding(self, evt=None):
        """Open funding sources dialog for this package."""
        if self.index is None:
            return  # Can't manage funding for unsaved package

        package_id = self.selected_package.get("package_id")
        product_name = self.selected_product.get("description", "")
        packaging = self.selected_package.get("packaging", "")

        # Open package_funding dialog pre-filled with this package
        obj = package_funding.UI(self, index=None)
        obj.on_open_for_package(package_id, product_name, packaging)

    def on_cancel(self, evt=None):
        """Close the dialog."""
        super().on_cancel()
