#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package Fundings List - View and manage package funding sources for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView
from views import package_funding


class UI(ParentView):
    """Package Fundings list window with add/edit functionality."""

    def __init__(self, parent):
        super().__init__(parent, name="package_fundings")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(950, 450)

        self.table = "package_fundings"
        self.primary_key = "package_funding_id"
        self.obj = None
        self.status = tk.IntVar(value=1)

        self.init_ui()
        self.show()

    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Package fundings treeview
        f1 = ttk.Frame(f0)

        # Package fundings treeview with count in LabelFrame title
        self.lbf = ttk.LabelFrame(f1, text=f"{_('Total')}: 0", style="App.TLabelframe")
        w = self.lbf

        cols = ("package_funding_id", "product", "package", "supplier", "funding", "deliberation", "valid_from")
        self.treeview = ttk.Treeview(w, columns=cols, show="headings", height=15)

        # Hidden ID column
        self.treeview.column("package_funding_id", width=0, stretch=False)
        self.treeview.heading("package_funding_id", text="")

        # Visible columns
        self.treeview.column("product", width=180, anchor=tk.W)
        self.treeview.heading("product", text=_("Product"), command=lambda: self.sort_column("product"))

        self.treeview.column("package", width=120, anchor=tk.W)
        self.treeview.heading("package", text=_("Packaging"), command=lambda: self.sort_column("package"))

        self.treeview.column("supplier", width=130, anchor=tk.W)
        self.treeview.heading("supplier", text=_("Supplier"), command=lambda: self.sort_column("supplier"))

        self.treeview.column("funding", width=120, anchor=tk.W)
        self.treeview.heading("funding", text=_("Source"), command=lambda: self.sort_column("funding"))

        self.treeview.column("deliberation", width=150, anchor=tk.W)
        self.treeview.heading("deliberation", text=_("Resolution"), command=lambda: self.sort_column("deliberation"))

        self.treeview.column("valid_from", width=100, anchor=tk.CENTER)
        self.treeview.heading("valid_from", text=_("Valid from"), command=lambda: self.sort_column("valid_from"))

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
        # Tag for items with deliberation (in gara)
        self.treeview.tag_configure("in_gara", background="#e6ffe6")

        w.pack(fill=tk.BOTH, expand=1)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Right panel - Buttons and filters
        f2 = ttk.Frame(f0)

        # Action buttons
        buttons = [
            (_("New"), self.on_add, "<Alt-n>", 0),
            (_("Edit"), self.on_edit, "<Alt-m>", 0),
            (_("Refresh"), self.on_reset, "<Alt-a>", 0),
            (_("Close"), self.on_cancel, "<Alt-c>", 0),
        ]

        for text, cmd, key, ul in buttons:
            self.engine.create_button(f2, text, cmd, underline=ul).pack(fill=tk.X, padx=5, pady=3)
            self.bind(key, lambda e, c=cmd: c())

        # Status filter
        w = ttk.LabelFrame(f2, text=_("Status"), style="App.TLabelframe")
        for text, value in ((_("Active"), 1), (_("Inactive"), 0), (_("All"), -1)):
            ttk.Radiobutton(
                w, text=text, variable=self.status,
                value=value,
                command=self.on_reset,
                style="App.TRadiobutton"
            ).pack(anchor=tk.W, padx=5, pady=2)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Legend
        w = ttk.LabelFrame(f2, text=_("Legend"), style="App.TLabelframe")
        f_leg = tk.Frame(w, bg="#e6ffe6", height=15, width=15)
        f_leg.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Label(w, text=_("In Tender"), style="App.TLabel").pack(side=tk.LEFT, padx=2)
        w.pack(fill=tk.X, padx=5, pady=5)

        f2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Package Funding Sources"))
        self.engine.dict_instances["package_fundings"] = self
        self.on_reset()

    def on_reset(self, evt=None):
        """Reload package fundings list."""
        self.load_package_fundings()

    def load_package_fundings(self):
        """Load package fundings list with current filters."""
        # Clear treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        sql = """SELECT pf.package_funding_id,
                        p.description AS product,
                        pk.packaging,
                        s.description AS supplier,
                        fs.description AS funding,
                        d.reference AS deliberation,
                        pf.valid_from,
                        pf.status,
                        pf.deliberation_id
                 FROM package_fundings pf
                 JOIN packages pk ON pk.package_id = pf.package_id
                 JOIN products p ON p.product_id = pk.product_id
                 JOIN suppliers s ON s.supplier_id = pk.supplier_id
                 JOIN funding_sources fs ON fs.funding_id = pf.funding_id
                 LEFT JOIN deliberations d ON d.deliberation_id = pf.deliberation_id
                 WHERE 1=1"""

        args = []
        status_val = self.status.get()

        if status_val in (0, 1):
            sql += " AND pf.status = ?"
            args.append(status_val)

        sql += " ORDER BY p.description, pk.packaging"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for row in rs:
                tags = []
                if row["status"] != 1:
                    tags.append("inactive")
                elif row["deliberation_id"]:
                    tags.append("in_gara")

                self.treeview.insert("", tk.END, values=(
                    row["package_funding_id"],
                    row["product"] or "",
                    row["packaging"] or "",
                    row["supplier"] or "",
                    row["funding"] or "",
                    row["deliberation"] or _("Economy"),
                    row["valid_from"] or ""
                ), tags=tuple(tags) if tags else ())

        self.lbf.config(text=f"{_('Total')}: {len(self.treeview.get_children())}")

    def sort_column(self, col):
        """Sort treeview by column."""
        items = [(self.treeview.set(k, col), k) for k in self.treeview.get_children("")]
        items.sort()

        for index, (val, k) in enumerate(items):
            self.treeview.move(k, "", index)

    def get_selected_id(self):
        """Get the package_funding_id of the selected item."""
        selection = self.treeview.selection()
        if selection:
            item = selection[0]
            values = self.treeview.item(item, "values")
            return values[0]  # package_funding_id
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
        """Add new package funding."""
        self.engine.close_instance("package_funding")
        self.obj = package_funding.UI(self)
        self.obj.on_open()

    def on_edit(self, evt=None):
        """Edit selected package funding."""
        pk = self.get_selected_id()
        if pk:
            self.engine.close_instance("package_funding")
            self.selected_item = self.engine.get_selected(
                self.table, self.primary_key, pk
            )
            self.obj = package_funding.UI(self, index=pk)
            self.obj.on_open(self.selected_item)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )

    def refresh_and_select(self, package_funding_id):
        """Refresh list and select package funding by ID."""
        self.load_package_fundings()

        # Find and select the package funding by ID
        for item in self.treeview.get_children():
            values = self.treeview.item(item, "values")
            if str(values[0]) == str(package_funding_id):
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
        if "package_fundings" in self.engine.dict_instances:
            del self.engine.dict_instances["package_fundings"]
        super().on_cancel()
