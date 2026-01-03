#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deliberations List - View and manage deliberations for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView
from views import deliberation


class UI(ParentView):
    """Deliberations list window with add/edit functionality."""

    def __init__(self, parent):
        super().__init__(parent, name="deliberations")

        if self._reusing:
            return

        self.minsize(800, 400)

        self.table = "deliberations"
        self.primary_key = "deliberation_id"
        self.obj = None
        self.status = tk.IntVar(value=1)

        self.init_ui()
        self.show()

    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Deliberations treeview
        f1 = ttk.Frame(f0)

        # Deliberations treeview with count in LabelFrame title
        self.lbf = ttk.LabelFrame(f1, text=f"{_('Total')}: 0", style="App.TLabelframe")
        w = self.lbf

        cols = ("deliberation_id", "reference", "issued", "supplier", "amount", "cig", "description")
        self.treeview = ttk.Treeview(w, columns=cols, show="headings", height=15)

        # Hidden ID column
        self.treeview.column("deliberation_id", width=0, stretch=False)
        self.treeview.heading("deliberation_id", text="")

        # Visible columns
        self.treeview.column("reference", width=100, anchor=tk.W)
        self.treeview.heading("reference", text=_("Number"), command=lambda: self.sort_column("reference"))

        self.treeview.column("issued", width=100, anchor=tk.CENTER)
        self.treeview.heading("issued", text=_("Date"), command=lambda: self.sort_column("issued"))

        self.treeview.column("supplier", width=150, anchor=tk.W)
        self.treeview.heading("supplier", text=_("Supplier"), command=lambda: self.sort_column("supplier"))

        self.treeview.column("amount", width=100, anchor=tk.E)
        self.treeview.heading("amount", text=_("Amount"), command=lambda: self.sort_column("amount"))

        self.treeview.column("cig", width=100, anchor=tk.W)
        self.treeview.heading("cig", text=_("CIG"), command=lambda: self.sort_column("cig"))

        self.treeview.column("description", width=250, anchor=tk.W)
        self.treeview.heading("description", text=_("Description"), command=lambda: self.sort_column("description"))

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
        for text, value in ((_("Active"), 1), (_("Closed"), 0), (_("All"), -1)):
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
        self.title(_("Resolutions"))
        self.engine.dict_instances["deliberations"] = self
        self.on_reset()

    def on_reset(self, evt=None):
        """Reload deliberations list."""
        self.load_deliberations()

    def load_deliberations(self):
        """Load deliberations list with current filters."""
        # Clear treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        sql = """SELECT d.deliberation_id, d.reference, d.issued,
                        s.description AS supplier, d.amount, d.cig, d.description, d.status
                 FROM deliberations d
                 LEFT JOIN suppliers s ON s.supplier_id = d.supplier_id
                 WHERE 1=1"""

        args = []
        status_val = self.status.get()

        if status_val in (0, 1):
            sql += " AND d.status = ?"
            args.append(status_val)

        sql += " ORDER BY d.issued DESC, d.reference DESC"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for row in rs:
                tag = "inactive" if row["status"] != 1 else ""
                amount_str = f"€ {row['amount']:,.2f}" if row["amount"] else ""
                self.treeview.insert("", tk.END, values=(
                    row["deliberation_id"],
                    row["reference"] or "",
                    row["issued"] or "",
                    row["supplier"] or "",
                    amount_str,
                    row["cig"] or "",
                    row["description"] or ""
                ), tags=(tag,) if tag else ())

        self.lbf.config(text=f"{_('Total')}: {len(self.treeview.get_children())}")

    def sort_column(self, col):
        """Sort treeview by column."""
        items = [(self.treeview.set(k, col), k) for k in self.treeview.get_children("")]
        items.sort()

        for index, (val, k) in enumerate(items):
            self.treeview.move(k, "", index)

    def get_selected_id(self):
        """Get the deliberation_id of the selected item."""
        selection = self.treeview.selection()
        if selection:
            item = selection[0]
            values = self.treeview.item(item, "values")
            return values[0]  # deliberation_id
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
        """Add new deliberation."""
        self.engine.close_instance("deliberation")
        self.obj = deliberation.UI(self)
        self.obj.on_open()

    def on_edit(self, evt=None):
        """Edit selected deliberation."""
        pk = self.get_selected_id()
        if pk:
            self.engine.close_instance("deliberation")
            self.selected_item = self.engine.get_selected(
                self.table, self.primary_key, pk
            )
            self.obj = deliberation.UI(self, index=pk)
            self.obj.on_open(self.selected_item)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )

    def refresh_and_select(self, deliberation_id):
        """Refresh list and select deliberation by ID."""
        self.load_deliberations()

        # Find and select the deliberation by ID
        for item in self.treeview.get_children():
            values = self.treeview.item(item, "values")
            if str(values[0]) == str(deliberation_id):
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
        if "deliberations" in self.engine.dict_instances:
            del self.engine.dict_instances["deliberations"]
        super().on_cancel()
