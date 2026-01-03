#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Request Dialog - Edit request date and reference in Inventarium.

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
    """Dialog for editing a request."""

    def __init__(self, parent):
        super().__init__(parent, name="request")

        self.minsize(350, 150)

        self.reference = tk.StringVar()

        self.init_ui()
        self.show()

    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        r = 0
        ttk.Label(w, text=_("Reference:")).grid(row=r, column=0, sticky=tk.W, pady=5)
        self.txtReference = ttk.Entry(w, textvariable=self.reference, width=30)
        self.txtReference.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text=_("Date:")).grid(row=r, column=0, sticky=tk.W, pady=5)
        self.cal_issued = Calendarium(w, "")
        self.cal_issued.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)

        # Buttons
        r += 1
        bf = ttk.Frame(w)
        bf.grid(row=r, column=0, columnspan=2, pady=15)

        self.engine.create_button(bf, _("Save"), self.on_save).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-s>", self.on_save)

        self.engine.create_button(bf, _("Close"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)

    def on_open(self, selected_request):
        """
        Open dialog for editing request.

        Args:
            selected_request: Dict with request data
        """
        self.selected_request = selected_request
        self.title(_("Edit Request"))
        self.set_values()
        self.txtReference.focus()

    def set_values(self):
        """Set form values from selected request."""
        self.reference.set(self.selected_request.get("reference", ""))

        # Set date (convert string to date object)
        issued = self.selected_request.get("issued", "")
        if issued:
            date_obj = datetime.datetime.strptime(issued, "%Y-%m-%d").date()
            self.cal_issued.set_date(date_obj)

    def on_save(self, evt=None):
        """Save the request."""
        if messagebox.askyesno(
            self.engine.app_title,
            self.engine.ask_to_save,
            parent=self
        ):
            reference = self.reference.get().strip()
            issued = self.cal_issued.get_date()

            sql = """UPDATE requests
                     SET reference = ?, issued = ?
                     WHERE request_id = ?"""

            self.engine.write(sql, (reference, issued, self.selected_request["request_id"]))

            # Refresh parent list
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
