#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Item Cancel Dialog - Cancel a request item with a note in Inventarium.

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
    """Dialog for cancelling a request item with a note."""

    def __init__(self, parent):
        super().__init__(parent, name="item_cancel")

        self.minsize(400, 200)

        self.note = tk.StringVar()

        self.init_ui()
        self.show()

    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        # Info label
        self.lblInfo = ttk.Label(w, text="", wraplength=380)
        self.lblInfo.pack(fill=tk.X, pady=(0, 10))

        # Note field
        ttk.Label(w, text=_("Cancellation reason:")).pack(anchor=tk.W, pady=(5, 2))

        self.txtNote = ttk.Entry(w, textvariable=self.note, width=50)
        self.txtNote.pack(fill=tk.X, pady=(0, 10))

        # Buttons
        bf = ttk.Frame(w)
        bf.pack(pady=10)

        self.engine.create_button(bf, _("Cancel Item"), self.on_save).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-a>", self.on_save)

        self.engine.create_button(bf, _("Close"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)

    def on_open(self, selected_item, product_name):
        """
        Open dialog for cancelling an item.

        Args:
            selected_item: Dict with item data
            product_name: Product name for display
        """
        self.selected_item = selected_item
        self.title(_("Cancel Item"))

        # Show item info
        qty = selected_item.get("quantity", 0)
        info = f"{_('Product')}: {product_name}\n{_('Quantity')}: {qty}"
        self.lblInfo.config(text=info)

        self.txtNote.focus()

    def on_save(self, evt=None):
        """Save the cancellation."""
        note = self.note.get().strip()

        if not note:
            messagebox.showwarning(
                self.engine.app_title,
                _("Please enter the cancellation reason!"),
                parent=self
            )
            self.txtNote.focus()
            return

        if messagebox.askyesno(
            self.engine.app_title,
            _("Confirm item cancellation?"),
            parent=self
        ):
            # Set status = 2 (cancelled) and save note
            sql = """UPDATE items
                     SET status = 2, note = ?
                     WHERE item_id = ?"""

            self.engine.write(sql, (note, self.selected_item["item_id"]))

            # Check if there are remaining active items
            request_id = self.selected_item.get("request_id")
            if request_id:
                sql = "SELECT COUNT(*) as cnt FROM items WHERE request_id = ? AND status = 1"
                result = self.engine.read(False, sql, (request_id,))
                if result and result["cnt"] == 0:
                    # No more active items, ask to close
                    if messagebox.askyesno(
                        self.engine.app_title,
                        _("No more active items.") + "\n" + _("Close the request?"),
                        parent=self
                    ):
                        sql = "UPDATE requests SET status = 0 WHERE request_id = ?"
                        self.engine.write(sql, (request_id,))

            # Refresh parent list
            self.parent.refresh_request_list()

            self.on_cancel()

    def on_cancel(self, evt=None):
        """Close the dialog."""
        super().on_cancel()
