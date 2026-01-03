#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package Funding Dialog - Create/Edit package funding for Inventarium.

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
    """Dialog for creating or editing a package funding."""

    def __init__(self, parent, index=None):
        super().__init__(parent, name="package_funding")

        self.index = index
        self.resizable(0, 0)

        # Table info (used for SQL generation)
        self.table = "package_fundings"
        self.primary_key = "package_funding_id"

        self.package_id = tk.IntVar()
        self.funding_id = tk.IntVar()
        self.deliberation_id = tk.IntVar()
        self.status = tk.BooleanVar()
        self.search_text = tk.StringVar()

        # Selected package info
        self.selected_package_id = None
        self.packages = {}

        self.init_ui()
        self.show()

    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        entry_width = 40

        # Search section
        r = 0
        ttk.Label(w, text=_("Search Package:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        search_frame = ttk.Frame(w)
        search_frame.grid(row=r, column=1, columnspan=2, sticky=tk.W, padx=5, pady=2)

        self.txtSearch = ttk.Entry(search_frame, textvariable=self.search_text, width=entry_width-10)
        self.txtSearch.pack(side=tk.LEFT)
        self.txtSearch.bind("<Return>", self.on_search)
        self.txtSearch.bind("<KeyRelease>", self.on_search_keyrelease)

        self.engine.create_button(search_frame, _("Search"), self.on_search).pack(side=tk.LEFT, padx=5)

        # Search hint
        r += 1
        ttk.Label(w, text=_("(description or code)"), style="App.TLabel").grid(
            row=r, column=1, sticky=tk.W, padx=5)

        # Results listbox
        r += 1
        ttk.Label(w, text=_("Results:")).grid(row=r, column=0, sticky=tk.NW, pady=2)
        list_frame = ttk.Frame(w)
        list_frame.grid(row=r, column=1, columnspan=2, sticky=tk.W, padx=5, pady=2)

        self.lstResults = tk.Listbox(list_frame, width=entry_width, height=5, exportselection=False)
        self.lstResults.pack(side=tk.LEFT, fill=tk.BOTH)
        self.lstResults.bind("<<ListboxSelect>>", self.on_result_selected)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.lstResults.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lstResults.config(yscrollcommand=scrollbar.set)

        # Selected package display
        r += 1
        ttk.Label(w, text=_("Selected:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.lblSelected = ttk.Label(w, text="-", style="App.TLabel", width=entry_width)
        self.lblSelected.grid(row=r, column=1, columnspan=2, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Separator(w, orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=3, sticky="ew", pady=10)

        r += 1
        ttk.Label(w, text=_("Funding Source:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbFunding = ttk.Combobox(w, width=entry_width-2, state="readonly")
        self.cbFunding.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Resolution:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbDeliberation = ttk.Combobox(w, width=entry_width-2, state="readonly")
        self.cbDeliberation.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(w, text=_("(optional - if in tender)"), style="App.TLabel").grid(row=r, column=2, sticky=tk.W)

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

        self.engine.create_button(bf, _("Close"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

    def on_search_keyrelease(self, evt=None):
        """Auto-search after typing (with delay)."""
        # Cancel previous scheduled search
        if hasattr(self, '_search_after_id'):
            self.after_cancel(self._search_after_id)
        # Schedule new search after 300ms
        self._search_after_id = self.after(300, self.on_search)

    def on_search(self, evt=None):
        """Search for packages matching the search text."""
        self.lstResults.delete(0, tk.END)
        self.packages = {}

        search = self.search_text.get().strip()
        if len(search) < 2:
            return

        # Search by product description or reference (warehouse code)
        sql = """SELECT pk.package_id, pk.packaging, p.description AS product,
                        p.reference, s.description AS supplier
                 FROM packages pk
                 JOIN products p ON p.product_id = pk.product_id
                 JOIN suppliers s ON s.supplier_id = pk.supplier_id
                 WHERE pk.status = 1
                   AND (p.description LIKE ? OR p.reference LIKE ? OR pk.packaging LIKE ?)
                 ORDER BY p.description, pk.packaging
                 LIMIT 50"""
        pattern = f"%{search}%"
        rs = self.engine.read(True, sql, (pattern, pattern, pattern))

        if rs:
            for row in rs:
                # Format: Product - Packaging (Supplier) [Code]
                ref = f" [{row['reference']}]" if row['reference'] else ""
                label = f"{row['product']} - {row['packaging']} ({row['supplier']}){ref}"
                self.lstResults.insert(tk.END, label)
                self.packages[label] = row["package_id"]

    def on_result_selected(self, evt=None):
        """Handle selection from results list."""
        selection = self.lstResults.curselection()
        if selection:
            idx = selection[0]
            label = self.lstResults.get(idx)
            self.selected_package_id = self.packages.get(label)
            # Show shortened version in label
            self.lblSelected.config(text=label[:50] + "..." if len(label) > 50 else label)

    def load_funding_sources(self):
        """Load funding sources into combobox."""
        sql = "SELECT funding_id, description FROM funding_sources WHERE status = 1 ORDER BY description"
        rs = self.engine.read(True, sql)

        self.fundings = {}
        values = []

        if rs:
            for row in rs:
                self.fundings[row["description"]] = row["funding_id"]
                values.append(row["description"])

        self.cbFunding["values"] = values

    def load_deliberations(self):
        """Load deliberations into combobox."""
        sql = """SELECT d.deliberation_id, d.reference, s.description AS supplier
                 FROM deliberations d
                 LEFT JOIN suppliers s ON s.supplier_id = d.supplier_id
                 WHERE d.status = 1
                 ORDER BY d.reference DESC"""
        rs = self.engine.read(True, sql)

        self.deliberations = {"": None}  # Empty option for no deliberation
        values = [""]

        if rs:
            for row in rs:
                label = f"{row['reference']} ({row['supplier']})" if row['supplier'] else row['reference']
                self.deliberations[label] = row["deliberation_id"]
                values.append(label)

        self.cbDeliberation["values"] = values

    def on_open(self, selected_item=None):
        """
        Open dialog for new or edit package funding.

        Args:
            selected_item: Dict with package funding data (for edit) or None (for new)
        """
        self.load_funding_sources()
        self.load_deliberations()

        if self.index is not None and selected_item:
            # Edit mode
            self.selected_item = selected_item
            self.title(_("Edit Funding Source"))
            self.set_values()
        else:
            # New package funding mode
            self.title(_("New Funding Source"))
            self.status.set(1)
            self.calValidFrom.set_today()

        self.txtSearch.focus()

    def on_open_for_package(self, package_id, product_name, packaging):
        """
        Open dialog for new package funding with pre-selected package.

        Args:
            package_id: The package ID to create funding for
            product_name: Product description (for display)
            packaging: Package description (for display)
        """
        self.load_funding_sources()
        self.load_deliberations()

        # Get supplier for display
        sql = """SELECT s.description AS supplier, p.reference
                 FROM packages pk
                 JOIN suppliers s ON s.supplier_id = pk.supplier_id
                 JOIN products p ON p.product_id = pk.product_id
                 WHERE pk.package_id = ?"""
        rs = self.engine.read(False, sql, (package_id,))
        supplier = rs["supplier"] if rs else ""
        ref = f" [{rs['reference']}]" if rs and rs['reference'] else ""

        # Set package as selected
        self.selected_package_id = package_id
        label = f"{product_name} - {packaging} ({supplier}){ref}"
        self.lblSelected.config(text=label[:50] + "..." if len(label) > 50 else label)

        # Disable search (package already selected)
        self.txtSearch.config(state=tk.DISABLED)
        self.lstResults.config(state=tk.DISABLED)

        self.title(f"{_('New Funding Source')} - {product_name}")
        self.status.set(1)
        self.calValidFrom.set_today()

        self.cbFunding.focus()

    def set_values(self):
        """Set form values from selected package funding."""
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

        # Set package info
        package_id = self.selected_item.get("package_id")
        if package_id:
            self.selected_package_id = package_id
            sql = """SELECT p.description AS product, pk.packaging, s.description AS supplier, p.reference
                     FROM packages pk
                     JOIN products p ON p.product_id = pk.product_id
                     JOIN suppliers s ON s.supplier_id = pk.supplier_id
                     WHERE pk.package_id = ?"""
            rs = self.engine.read(False, sql, (package_id,))
            if rs:
                ref = f" [{rs['reference']}]" if rs['reference'] else ""
                label = f"{rs['product']} - {rs['packaging']} ({rs['supplier']}){ref}"
                self.lblSelected.config(text=label[:50] + "..." if len(label) > 50 else label)

        # Set funding source
        funding_id = self.selected_item.get("funding_id")
        if funding_id:
            sql = "SELECT description FROM funding_sources WHERE funding_id = ?"
            rs = self.engine.read(False, sql, (funding_id,))
            if rs:
                self.cbFunding.set(rs["description"])

        # Set deliberation
        deliberation_id = self.selected_item.get("deliberation_id")
        if deliberation_id:
            sql = """SELECT d.reference, s.description AS supplier
                     FROM deliberations d
                     LEFT JOIN suppliers s ON s.supplier_id = d.supplier_id
                     WHERE d.deliberation_id = ?"""
            rs = self.engine.read(False, sql, (deliberation_id,))
            if rs:
                label = f"{rs['reference']} ({rs['supplier']})" if rs['supplier'] else rs['reference']
                self.cbDeliberation.set(label)

    def get_values(self):
        """Get form values as list (order matches table columns excluding PK)."""
        # Get funding_id from selection
        funding_name = self.cbFunding.get()
        funding_id = self.fundings.get(funding_name) if funding_name else None

        # Get deliberation_id from selection (optional)
        deliberation_label = self.cbDeliberation.get()
        deliberation_id = self.deliberations.get(deliberation_label) if deliberation_label else None

        # Get date from Calendarium
        date_obj = self.calValidFrom.get_date()
        valid_from_str = date_obj.strftime("%Y-%m-%d") if date_obj else None

        return [
            self.selected_package_id,
            funding_id,
            deliberation_id,
            valid_from_str,
            1 if self.status.get() else 0
        ]

    def on_save(self, evt=None):
        """Save the package funding."""
        # Validate required fields
        if not self.selected_package_id:
            messagebox.showwarning(
                self.engine.app_title,
                _("Please select a Package!"),
                parent=self
            )
            self.txtSearch.focus()
            return

        if not self.cbFunding.get():
            messagebox.showwarning(
                self.engine.app_title,
                _("Please select a Funding Source!"),
                parent=self
            )
            self.cbFunding.focus()
            return

        if messagebox.askyesno(
            self.engine.app_title,
            self.engine.ask_to_save,
            parent=self
        ):
            args = self.get_values()

            if self.index is not None:
                # Update existing
                sql = self.engine.build_sql(self.table, op="update")
                args.append(self.selected_item[self.primary_key])
                self.engine.write(sql, tuple(args))
                pk = self.selected_item[self.primary_key]
            else:
                # Insert new
                sql = self.engine.build_sql(self.table, op="insert")
                pk = self.engine.write(sql, tuple(args))

            # Refresh parent list if it has the method (package_fundings list view)
            if hasattr(self.parent, 'refresh_and_select'):
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
