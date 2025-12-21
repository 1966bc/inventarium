#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funding Source Dialog - Create/Edit funding source for Inventarium.

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
    """Dialog for creating or editing a funding source."""

    def __init__(self, parent, index=None):
        super().__init__(parent, name="funding_source")

        self.index = index
        self.resizable(0, 0)

        self.code = tk.StringVar()
        self.description = tk.StringVar()
        self.status = tk.BooleanVar()

        self.init_ui()
        self.engine.center_window(self)
        self.show()

    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        r = 0
        ttk.Label(w, text=_("Codice:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtCode = ttk.Entry(w, textvariable=self.code, width=12)
        self.txtCode.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Descrizione:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtDescription = ttk.Entry(w, textvariable=self.description, width=35)
        self.txtDescription.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

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

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

    def on_open(self, selected_item=None):
        """Open dialog for new or edit."""
        if self.index is not None and selected_item:
            self.selected_item = selected_item
            self.title("Modifica Fonte Finanziamento")
            self.set_values()
        else:
            self.title("Nuova Fonte Finanziamento")
            self.status.set(1)

        self.txtCode.focus()

    def set_values(self):
        """Set form values from selected item."""
        self.code.set(self.selected_item.get("code", ""))
        self.description.set(self.selected_item.get("description", ""))
        self.status.set(self.selected_item.get("status", 1))

    def get_values(self):
        """Get form values as list."""
        return [
            self.code.get().strip().upper(),
            self.engine.clean_text(self.description.get()),
            1 if self.status.get() else 0
        ]

    def on_save(self, evt=None):
        """Save the funding source."""
        if not self.code.get().strip():
            messagebox.showwarning(
                self.engine.app_title,
                _("Il campo Codice è obbligatorio!"),
                parent=self
            )
            self.txtCode.focus()
            return

        if not self.description.get().strip():
            messagebox.showwarning(
                self.engine.app_title,
                _("Il campo Descrizione è obbligatorio!"),
                parent=self
            )
            self.txtDescription.focus()
            return

        if messagebox.askyesno(
            self.engine.app_title,
            self.engine.ask_to_save,
            parent=self
        ):
            args = self.get_values()

            if self.index is not None:
                sql = self.engine.build_sql(self.parent.table, op="update")
                args.append(self.selected_item[self.parent.primary_key])
                self.engine.write(sql, tuple(args))
                pk = self.selected_item[self.parent.primary_key]
            else:
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

    def on_cancel(self, evt=None):
        """Close the dialog."""
        super().on_cancel()
