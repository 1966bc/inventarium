#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memos - Informal notes board ("foglio sul frigo").

A simple shared notepad for quick reminders about items to order or tasks to do.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView


class UI(ParentView):
    """Memos board - informal notes list."""

    def __init__(self, parent):
        super().__init__(parent, name="memos")

        if self._reusing:
            return

        self.minsize(450, 400)

        self.show_done = tk.BooleanVar(value=False)
        self.dict_items = {}

        self.init_ui()
        self.on_open()
        self.show()

    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Top - Add new memo
        f_add = ttk.Frame(f0)

        self.memo_text = tk.StringVar()
        self.entry = ttk.Entry(f_add, textvariable=self.memo_text, width=40)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=(0, 5))
        self.entry.bind("<Return>", self.on_add)

        btn_add = self.engine.create_button(f_add, _("Add"), self.on_add, underline=0)
        btn_add.pack(side=tk.RIGHT)
        self.bind("<Alt-a>", self.on_add)

        f_add.pack(fill=tk.X, pady=(0, 8))

        # Middle - Memos list
        self.lbf = ttk.LabelFrame(f0, text=_("Memos"), style="App.TLabelframe")

        scrollbar = ttk.Scrollbar(self.lbf, orient=tk.VERTICAL)
        self.lstItems = tk.Listbox(
            self.lbf,
            height=12,
            font=("TkFixedFont", 10),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.lstItems.yview)
        self.lstItems.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lstItems.bind("<Double-1>", self.on_complete)

        self.lbf.pack(fill=tk.BOTH, expand=1, pady=(0, 8))

        # Bottom - Buttons
        f_btn = ttk.Frame(f0)

        btn_complete = self.engine.create_button(f_btn, _("Done"), self.on_complete, underline=0)
        btn_complete.pack(side=tk.LEFT, padx=(0, 5))
        self.bind("<Alt-d>", self.on_complete)

        btn_delete = self.engine.create_button(f_btn, _("Delete"), self.on_delete, underline=0)
        btn_delete.pack(side=tk.LEFT, padx=(0, 5))

        # Show done checkbox
        ttk.Checkbutton(
            f_btn,
            text=_("Show completed"),
            variable=self.show_done,
            command=self.on_refresh,
            style="App.TCheckbutton"
        ).pack(side=tk.LEFT, padx=10)

        btn_close = self.engine.create_button(f_btn, _("Close"), self.on_cancel, underline=0)
        btn_close.pack(side=tk.RIGHT)
        self.bind("<Alt-c>", self.on_cancel)

        f_btn.pack(fill=tk.X)

    def on_open(self):
        """Initialize the window."""
        self.title(_("Memos"))
        self.entry.focus_set()
        self.on_refresh()

    def on_refresh(self, evt=None):
        """Reload memos list."""
        self.lstItems.delete(0, tk.END)
        self.dict_items = {}

        rs = self.engine.get_memos(include_done=self.show_done.get())

        if rs:
            from datetime import datetime

            today = datetime.now().date()

            for idx, row in enumerate(rs):
                self.dict_items[idx] = row["memo_id"]

                # Format date (DD/MM/YYYY) and calculate age
                date_str = ""
                days_old = 0
                if row["created_at"]:
                    parts = row["created_at"][:10].split("-")
                    if len(parts) == 3:
                        date_str = f"{parts[2]}/{parts[1]}/{parts[0]}"
                        memo_date = datetime(int(parts[0]), int(parts[1]), int(parts[2])).date()
                        days_old = (today - memo_date).days

                text = row["text"][:40]

                if row["status"] == 0:
                    line = f"✓ {date_str}  {text}"
                else:
                    line = f"  {date_str}  {text}"

                self.lstItems.insert(tk.END, line)

                # Color based on age (completed memos stay gray)
                if row["status"] == 0:
                    self.lstItems.itemconfig(idx, fg="gray")
                elif days_old > 7:
                    self.lstItems.itemconfig(idx, fg="red")
                elif days_old > 3:
                    self.lstItems.itemconfig(idx, fg="orange")

        count = self.lstItems.size()
        self.lbf.config(text=f"{_('Memos')}: {count}")

    def on_add(self, evt=None):
        """Add a new memo."""
        text = self.memo_text.get().strip()
        if not text:
            return

        self.engine.add_memo(text)
        self.memo_text.set("")
        self.on_refresh()
        self.entry.focus_set()

    def on_complete(self, evt=None):
        """Mark selected memo as done."""
        if not self.lstItems.curselection():
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )
            return

        idx = self.lstItems.curselection()[0]
        memo_id = self.dict_items.get(idx)

        if memo_id:
            self.engine.complete_memo(memo_id)
            self.on_refresh()

    def on_delete(self, evt=None):
        """Delete selected memo."""
        if not self.lstItems.curselection():
            messagebox.showwarning(
                self.engine.app_title,
                self.engine.no_selected,
                parent=self
            )
            return

        idx = self.lstItems.curselection()[0]
        memo_id = self.dict_items.get(idx)

        if memo_id:
            if messagebox.askyesno(
                self.engine.app_title,
                _("Delete this memo?"),
                parent=self
            ):
                self.engine.delete_memo(memo_id)
                self.on_refresh()

    def on_cancel(self, evt=None):
        """Close the window."""
        super().on_cancel()
