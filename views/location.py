#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Location Dialog - Create/Edit location for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk

from i18n import _
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    """Dialog for creating or editing a location."""

    def __init__(self, parent, index=None):
        super().__init__(name="location")

        self.parent = parent
        self.index = index
        self.engine = self.nametowidget(".").engine
        self.transient(parent)
        self.resizable(0, 0)

        self.code = tk.StringVar()
        self.room = tk.StringVar()
        self.description = tk.StringVar()
        self.status = tk.BooleanVar()

        # Dictionaries for combobox mappings
        self.dict_categories = {}
        self.dict_conservations = {}

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        entry_width = self.engine.get_entry_width()

        r = 0
        ttk.Label(w, text=_("Codice:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtCode = ttk.Entry(w, textvariable=self.code, width=entry_width)
        self.txtCode.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Stanza:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtRoom = ttk.Entry(w, textvariable=self.room, width=entry_width)
        self.txtRoom.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Descrizione:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtDescription = ttk.Entry(w, textvariable=self.description, width=entry_width)
        self.txtDescription.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Tipo:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbCategories = ttk.Combobox(w, state="readonly", width=entry_width - 3, style="App.TCombobox")
        self.cbCategories.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Conservazione:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbConservations = ttk.Combobox(w, state="readonly", width=entry_width - 3, style="App.TCombobox")
        self.cbConservations.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

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
        self.bind("<Return>", self.on_save)

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

    def on_open(self, selected_item=None):
        """
        Open dialog for new or edit location.

        Args:
            selected_item: Dict with location data (for edit) or None (for new)
        """
        # Load combobox data
        self.set_categories()
        self.set_conservations()

        if self.index is not None and selected_item:
            # Edit mode
            self.selected_item = selected_item
            self.title(_("Modifica Ubicazione"))
            self.set_values()
        else:
            # New location mode
            self.title(_("Nuova Ubicazione"))
            self.status.set(1)

        self.txtCode.focus()

    def set_categories(self):
        """Load location categories (reference_id=2) into combobox."""
        self.dict_categories = {}
        voices = []

        # Add "Not assigned" option
        self.dict_categories[0] = None
        voices.append(_("-- Non assegnato --"))

        sql = """SELECT category_id, description
                 FROM categories
                 WHERE reference_id = 2 AND status = 1
                 ORDER BY description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs, start=1):
                self.dict_categories[idx] = row["category_id"]
                voices.append(row["description"])

        self.cbCategories["values"] = voices

    def set_conservations(self):
        """Load conservations into combobox."""
        self.dict_conservations = {}
        voices = []

        # Add "Not assigned" option
        self.dict_conservations[0] = None
        voices.append(_("-- Non assegnata --"))

        sql = """SELECT conservation_id, description
                 FROM conservations
                 WHERE status = 1
                 ORDER BY description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs, start=1):
                self.dict_conservations[idx] = row["conservation_id"]
                voices.append(row["description"])

        self.cbConservations["values"] = voices

    def set_values(self):
        """Set form values from selected location."""
        self.code.set(self.selected_item.get("code", "") or "")
        self.room.set(self.selected_item.get("room", "") or "")
        self.description.set(self.selected_item.get("description", "") or "")
        self.status.set(self.selected_item.get("status", 1))

        # Set category
        try:
            key = next(
                key for key, value in self.dict_categories.items()
                if value == self.selected_item.get("category_id")
            )
            self.cbCategories.current(key)
        except StopIteration:
            self.cbCategories.current(0)

        # Set conservation
        try:
            key = next(
                key for key, value in self.dict_conservations.items()
                if value == self.selected_item.get("conservation_id")
            )
            self.cbConservations.current(key)
        except StopIteration:
            self.cbConservations.current(0)

    def get_values(self):
        """Get form values as list."""
        category_idx = self.cbCategories.current()
        conservation_idx = self.cbConservations.current()

        return [
            self.dict_categories.get(category_idx),
            self.code.get().strip(),
            self.room.get().strip(),
            self.description.get().strip(),
            self.dict_conservations.get(conservation_idx),
            1 if self.status.get() else 0
        ]

    def on_save(self, evt=None):
        """Save the location."""
        # Validate required fields
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

            self.on_cancel()

        else:
            messagebox.showinfo(
                self.engine.app_title,
                self.engine.abort,
                parent=self
            )

    def on_cancel(self, evt=None):
        """Close the dialog."""
        self.destroy()
