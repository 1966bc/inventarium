#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Locations List - View and manage locations for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView
from views import location


class UI(ParentView):
    """Locations list window with add/edit functionality."""

    def __init__(self, parent):
        super().__init__(parent, name="locations")

        if self._reusing:
            return

        self.minsize(700, 400)

        self.table = "locations"
        self.primary_key = "location_id"
        self.obj = None
        self.status = tk.IntVar(value=1)

        self.init_ui()
        self.show()


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Locations treeview
        f1 = ttk.Frame(f0)

        # Locations treeview with count in LabelFrame title
        self.lbf = ttk.LabelFrame(f1, text=f"{_('Total')}: 0", style="App.TLabelframe")
        w = self.lbf

        cols = ("location_id", "code", "room", "description", "category", "conservation")
        self.treeview = ttk.Treeview(w, columns=cols, show="headings", height=15)

        # Hidden ID column
        self.treeview.column("location_id", width=0, stretch=False)
        self.treeview.heading("location_id", text="")

        # Visible columns
        self.treeview.column("code", width=80, anchor=tk.W)
        self.treeview.heading("code", text=_("Code"), command=lambda: self.sort_column("code"))

        self.treeview.column("room", width=100, anchor=tk.W)
        self.treeview.heading("room", text=_("Room"), command=lambda: self.sort_column("room"))

        self.treeview.column("description", width=200, anchor=tk.W)
        self.treeview.heading("description", text=_("Description"), command=lambda: self.sort_column("description"))

        self.treeview.column("category", width=120, anchor=tk.W)
        self.treeview.heading("category", text=_("Type"), command=lambda: self.sort_column("category"))

        self.treeview.column("conservation", width=120, anchor=tk.W)
        self.treeview.heading("conservation", text=_("Storage"), command=lambda: self.sort_column("conservation"))

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
        for text, value in ((_("Active"), 1), (_("Inactive"), 0), (_("All"), -1)):
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
        self.title(_("Locations"))
        self.engine.dict_instances["locations"] = self
        self.on_reset()

    def on_reset(self, evt=None):
        """Reload locations list."""
        self.load_locations()

    def load_locations(self):
        """Load locations list with current filters."""
        # Clear treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        sql = """
            SELECT
                l.location_id,
                l.code,
                l.room,
                l.description,
                c.description AS category,
                co.description AS conservation,
                l.status
            FROM locations l
            LEFT JOIN categories c ON c.category_id = l.category_id
            LEFT JOIN conservations co ON co.conservation_id = l.conservation_id
            WHERE 1=1
        """

        args = []
        status_val = self.status.get()

        if status_val in (0, 1):
            sql += " AND l.status = ?"
            args.append(status_val)

        sql += " ORDER BY l.room, l.description"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for row in rs:
                tag = "inactive" if row["status"] != 1 else ""
                self.treeview.insert("", tk.END, values=(
                    row["location_id"],
                    row["code"] or "",
                    row["room"] or "",
                    row["description"] or "",
                    row["category"] or "",
                    row["conservation"] or ""
                ), tags=(tag,) if tag else ())

        self.lbf.config(text=f"{_('Total')}: {len(self.treeview.get_children())}")

    def sort_column(self, col):
        """Sort treeview by column."""
        items = [(self.treeview.set(k, col), k) for k in self.treeview.get_children("")]
        items.sort()

        for index, (val, k) in enumerate(items):
            self.treeview.move(k, "", index)

    def get_selected_id(self):
        """Get the location_id of the selected item."""
        selection = self.treeview.selection()
        if selection:
            item = selection[0]
            values = self.treeview.item(item, "values")
            return values[0]  # location_id
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
        """Add new location."""
        self.engine.close_instance("location")
        self.obj = location.UI(self)
        self.obj.on_open()

    def on_edit(self, evt=None):
        """Edit selected location."""
        pk = self.get_selected_id()
        if pk:
            self.engine.close_instance("location")
            self.selected_item = self.engine.get_selected(
                self.table, self.primary_key, pk
            )
            self.obj = location.UI(self, index=pk)
            self.obj.on_open(self.selected_item)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )

    def refresh_and_select(self, location_id):
        """Refresh list and select location by ID."""
        self.load_locations()

        # Find and select the location by ID
        for item in self.treeview.get_children():
            values = self.treeview.item(item, "values")
            if str(values[0]) == str(location_id):
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
        if "locations" in self.engine.dict_instances:
            del self.engine.dict_instances["locations"]
        super().on_cancel()
