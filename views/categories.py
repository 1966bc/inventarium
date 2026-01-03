#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Categories List - View and manage categories for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView
from views import category


class UI(ParentView):
    """Categories list window with add/edit functionality."""

    def __init__(self, parent):
        super().__init__(parent, name="categories")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(500, 400)

        self.table = "categories"
        self.primary_key = "category_id"
        self.obj = None

        # reference_id: 1=Prodotti, 2=Ubicazioni
        self.reference_types = {
            1: _("Products"),
            2: _("Locations")
        }
        self.reference_id = tk.IntVar(value=1)
        self.status = tk.IntVar(value=1)
        self.dict_items = {}

        self.init_ui()
        self.engine.center_window(self)
        self.show()


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Categories list
        f1 = ttk.Frame(f0)

        # Categories listbox with count in LabelFrame title
        self.lbf = ttk.LabelFrame(f1, text=f"{_('Total')}: 0", style="App.TLabelframe")
        w = self.lbf

        # Header
        header = ttk.Label(
            w,
            text=f"{'Descrizione':<40}",
            font=("Courier", 9, "bold")
        )
        header.pack(fill=tk.X, padx=2)

        scrollbar = ttk.Scrollbar(w, orient=tk.VERTICAL)
        self.lstItems = tk.Listbox(
            w,
            height=15,
            font=("Courier", 9),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.lstItems.yview)
        self.lstItems.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-1>", self.on_item_activated)
        w.pack(fill=tk.BOTH, expand=1)

        f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Right panel - Buttons and Filters
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

        # Reference type filter
        w = ttk.LabelFrame(f2, text=_("Type"), style="App.TLabelframe")
        for ref_id, text in self.reference_types.items():
            ttk.Radiobutton(
                w, text=text, variable=self.reference_id,
                value=ref_id,
                command=self.on_reset,
                style="App.TRadiobutton"
            ).pack(anchor=tk.W, padx=5, pady=2)
        w.pack(fill=tk.X, padx=5, pady=5)

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
        self.title(_("Categories"))
        self.engine.dict_instances["categories"] = self
        self.on_reset()

    def on_reset(self, evt=None):
        """Reload categories list."""
        self.lstItems.delete(0, tk.END)
        self.dict_items = {}

        sql = """SELECT category_id, description, status
                 FROM categories
                 WHERE reference_id = ?"""

        args = [self.reference_id.get()]
        status_val = self.status.get()

        if status_val in (0, 1):
            sql += " AND status = ?"
            args.append(status_val)

        sql += " ORDER BY description"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for idx, row in enumerate(rs):
                self.dict_items[idx] = row["category_id"]

                # Format line
                desc = (row["description"] or "")[:40].ljust(40)

                self.lstItems.insert(tk.END, desc)

                # Color inactive
                if row["status"] != 1:
                    self.lstItems.itemconfig(idx, bg="light gray")

        type_name = self.reference_types.get(self.reference_id.get(), "")
        self.lbf.config(text=f"{_('Categories')} {type_name}: {self.lstItems.size()}")

    def on_item_selected(self, evt=None):
        """Handle item selection."""
        if self.lstItems.curselection():
            idx = self.lstItems.curselection()[0]
            pk = self.dict_items.get(idx)
            if pk:
                self.selected_item = self.engine.get_selected(
                    self.table, self.primary_key, pk
                )

    def on_item_activated(self, evt=None):
        """Handle double-click - open edit dialog."""
        self.on_edit()

    def on_add(self, evt=None):
        """Add new category."""
        self.engine.close_instance("category")
        self.obj = category.UI(self)
        self.obj.on_open(self.reference_id.get())

    def on_edit(self, evt=None):
        """Edit selected category."""
        if self.lstItems.curselection():
            self.engine.close_instance("category")
            idx = self.lstItems.curselection()[0]
            pk = self.dict_items.get(idx)
            if pk:
                self.selected_item = self.engine.get_selected(
                    self.table, self.primary_key, pk
                )
                self.obj = category.UI(self, index=idx)
                self.obj.on_open(self.reference_id.get(), self.selected_item)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )

    def refresh_and_select(self, category_id):
        """Refresh list and select category by ID."""
        self.on_reset()

        # Find and select the category by ID
        for idx, pk in self.dict_items.items():
            if pk == category_id:
                self.lstItems.selection_set(idx)
                self.lstItems.see(idx)
                self.on_item_selected()
                break

    def on_cancel(self, evt=None):
        """Close the window."""
        if self.obj is not None:
            try:
                self.obj.destroy()
            except Exception:
                pass
        if "categories" in self.engine.dict_instances:
            del self.engine.dict_instances["categories"]
        super().on_cancel()
