#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Category Dialog - Create/Edit category for Inventarium.

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
    """Dialog for creating or editing a category."""

    def __init__(self, parent, index=None):
        super().__init__(parent, name="category")

        self.index = index
        self.resizable(0, 0)

        self.description = tk.StringVar()
        self.status = tk.BooleanVar()

        self.init_ui()
        self.show()


    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        entry_width = self.engine.get_entry_width()

        r = 0
        ttk.Label(w, text=_("Description:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtDescription = ttk.Entry(w, textvariable=self.description, width=entry_width)
        self.txtDescription.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Active:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.status, style="App.TCheckbutton")
        chk.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Buttons
        r += 1
        bf = ttk.Frame(w)
        bf.grid(row=r, column=0, columnspan=2, pady=10)

        self.engine.create_button(bf, _("Save"), self.on_save).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-s>", self.on_save)
        self.bind("<Return>", self.on_save)

        self.engine.create_button(bf, _("Close"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

    def on_open(self, reference_id, selected_item=None):
        """
        Open dialog for new or edit category.

        Args:
            reference_id: Type of category (1=Prodotti, 2=Documenti, 3=Ubicazioni)
            selected_item: Dict with category data (for edit) or None (for new)
        """
        self.reference_id = reference_id

        if self.index is not None and selected_item:
            # Edit mode
            self.selected_item = selected_item
            self.title(_("Edit Category"))
            self.set_values()
        else:
            # New category mode
            self.title(_("New Category"))
            self.status.set(1)

        self.txtDescription.focus()

    def set_values(self):
        """Set form values from selected category."""
        self.description.set(self.selected_item.get("description", ""))
        self.status.set(self.selected_item.get("status", 1))

    def get_values(self):
        """Get form values as list."""
        return [
            self.reference_id,
            self.description.get().strip(),
            1 if self.status.get() else 0
        ]

    def on_save(self, evt=None):
        """Save the category."""
        # Validate required fields
        if not self.description.get().strip():
            messagebox.showwarning(
                self.engine.app_title,
                _("The Description field is required!"),
                parent=self
            )
            self.txtDescription.focus()
            return

        # Check for duplicate description
        if not self.check_description():
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

            # Notify subscribers that a category changed (only for product categories)
            if self.reference_id == 1:
                self.engine.notify("category_changed")

            self.on_cancel()

        else:
            messagebox.showinfo(
                self.engine.app_title,
                self.engine.abort,
                parent=self
            )

    def check_description(self):
        """Check if description is unique within same reference_id."""
        sql = """SELECT category_id FROM categories
                 WHERE description = ? AND reference_id = ?"""
        rs = self.engine.read(False, sql, (self.description.get().strip(), self.reference_id))

        if rs:
            # If editing, allow same description for same category
            if self.index is not None:
                if rs["category_id"] != self.selected_item["category_id"]:
                    msg = _("The category '{}' already exists!").format(self.description.get())
                    messagebox.showwarning(self.engine.app_title, msg, parent=self)
                    return False
            else:
                msg = _("The category '{}' already exists!").format(self.description.get())
                messagebox.showwarning(self.engine.app_title, msg, parent=self)
                return False

        return True

    def on_cancel(self, evt=None):
        """Close the dialog."""
        super().on_cancel()
