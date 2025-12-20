#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conservations List - View and manage conservations for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk

from i18n import _
from tkinter import ttk
from tkinter import messagebox

from views import conservation


class UI(tk.Toplevel):
    """Conservations list window with add/edit functionality."""

    def __init__(self, parent):
        super().__init__(name="conservations")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.minsize(400, 300)

        self.table = "conservations"
        self.primary_key = "conservation_id"
        self.obj = None
        self.status = tk.IntVar(value=1)
        self.dict_items = {}

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Conservations list
        f1 = ttk.Frame(f0)

        # Conservations listbox with count in LabelFrame title
        self.lbf = ttk.LabelFrame(f1, text=f"{_('Totale')}: 0", style="App.TLabelframe")
        w = self.lbf

        # Header
        header = ttk.Label(
            w,
            text=f"{'Descrizione':<30}",
            font=("Courier", 9, "bold")
        )
        header.pack(fill=tk.X, padx=2)

        scrollbar = ttk.Scrollbar(w, orient=tk.VERTICAL)
        self.lstItems = tk.Listbox(
            w,
            height=12,
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

        # Right panel - Buttons and filters
        f2 = ttk.Frame(f0)

        # Action buttons
        buttons = [
            (_("Nuovo"), self.on_add, "<Alt-n>", 0),
            (_("Modifica"), self.on_edit, "<Alt-m>", 0),
            (_("Aggiorna"), self.on_reset, "<Alt-a>", 0),
            (_("Chiudi"), self.on_cancel, "<Alt-c>", 0),
        ]

        for text, cmd, key, ul in buttons:
            self.engine.create_button(f2, text, cmd, underline=ul).pack(fill=tk.X, padx=5, pady=3)
            self.bind(key, lambda e, c=cmd: c())

        # Status filter
        w = ttk.LabelFrame(f2, text=_("Stato"), style="App.TLabelframe")
        for text, value in ((_("Attivi"), 1), (_("Non Attivi"), 0), (_("Tutti"), -1)):
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
        self.title(_("Conservazioni"))
        self.engine.dict_instances["conservations"] = self
        self.on_reset()

    def on_reset(self, evt=None):
        """Reload conservations list."""
        self.lstItems.delete(0, tk.END)
        self.dict_items = {}

        sql = """SELECT conservation_id, description, status
                 FROM conservations"""

        args = []
        status_val = self.status.get()

        if status_val in (0, 1):
            sql += " WHERE status = ?"
            args.append(status_val)

        sql += " ORDER BY description"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for idx, row in enumerate(rs):
                self.dict_items[idx] = row["conservation_id"]

                # Format line
                desc = (row["description"] or "")[:30].ljust(30)

                self.lstItems.insert(tk.END, desc)

                # Color inactive
                if row["status"] != 1:
                    self.lstItems.itemconfig(idx, bg="light gray")

        self.lbf.config(text=f"{_('Totale')}: {self.lstItems.size()}")

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
        """Add new conservation."""
        self.obj = conservation.UI(self)
        self.obj.on_open()

    def on_edit(self, evt=None):
        """Edit selected conservation."""
        if self.lstItems.curselection():
            idx = self.lstItems.curselection()[0]
            pk = self.dict_items.get(idx)
            if pk:
                self.selected_item = self.engine.get_selected(
                    self.table, self.primary_key, pk
                )
                self.obj = conservation.UI(self, index=idx)
                self.obj.on_open(self.selected_item)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )

    def refresh_and_select(self, conservation_id):
        """Refresh list and select conservation by ID."""
        self.on_reset()

        for idx, pk in self.dict_items.items():
            if pk == conservation_id:
                self.lstItems.selection_set(idx)
                self.lstItems.see(idx)
                self.on_item_selected()
                break

    def on_cancel(self, evt=None):
        """Close the window."""
        if self.obj is not None:
            try:
                self.obj.destroy()
            except:
                pass
        if "conservations" in self.engine.dict_instances:
            del self.engine.dict_instances["conservations"]
        self.destroy()
