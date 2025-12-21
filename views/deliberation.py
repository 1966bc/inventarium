#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deliberation Dialog - Create/Edit deliberation for Inventarium.

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
    """Dialog for creating or editing a deliberation."""

    def __init__(self, parent, index=None):
        super().__init__(parent, name="deliberation")

        self.index = index
        self.resizable(0, 0)

        self.reference = tk.StringVar()
        self.description = tk.StringVar()
        self.supplier_id = tk.IntVar()
        self.amount = tk.StringVar()
        self.cig = tk.StringVar()
        self.status = tk.BooleanVar()

        self.init_ui()
        self.engine.center_window(self)
        self.show()

    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        entry_width = 30

        r = 0
        ttk.Label(w, text=_("Numero:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtReference = ttk.Entry(w, textvariable=self.reference, width=entry_width)
        self.txtReference.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Data:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.calIssued = Calendarium(w, "")
        self.calIssued.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Fornitore:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.cbSupplier = ttk.Combobox(w, width=entry_width-2, state="readonly")
        self.cbSupplier.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Importo:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        vcmd = self.engine.get_validate_float(self)
        self.txtAmount = ttk.Entry(w, textvariable=self.amount, width=entry_width,
                                    validate="key", validatecommand=vcmd)
        self.txtAmount.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("CIG:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtCig = ttk.Entry(w, textvariable=self.cig, width=entry_width)
        self.txtCig.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Descrizione:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtDescription = ttk.Entry(w, textvariable=self.description, width=entry_width)
        self.txtDescription.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Attiva:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        chk = ttk.Checkbutton(w, onvalue=1, offvalue=0, variable=self.status, style="App.TCheckbutton")
        chk.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Buttons
        r += 1
        bf = ttk.Frame(w)
        bf.grid(row=r, column=0, columnspan=3, pady=10)

        self.engine.create_button(bf, _("Salva"), self.on_save).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-s>", self.on_save)
        self.bind("<Return>", self.on_save)

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

    def load_suppliers(self):
        """Load suppliers into combobox."""
        sql = "SELECT supplier_id, description FROM suppliers WHERE status = 1 ORDER BY description"
        rs = self.engine.read(True, sql)

        self.suppliers = {}
        values = []

        if rs:
            for row in rs:
                self.suppliers[row["description"]] = row["supplier_id"]
                values.append(row["description"])

        self.cbSupplier["values"] = values

    def on_open(self, selected_item=None):
        """
        Open dialog for new or edit deliberation.

        Args:
            selected_item: Dict with deliberation data (for edit) or None (for new)
        """
        self.load_suppliers()

        if self.index is not None and selected_item:
            # Edit mode
            self.selected_item = selected_item
            self.title(_("Modifica Delibera"))
            self.set_values()
        else:
            # New deliberation mode
            self.title(_("Nuova Delibera"))
            self.status.set(1)
            self.calIssued.set_today()

        self.txtReference.focus()

    def set_values(self):
        """Set form values from selected deliberation."""
        self.reference.set(self.selected_item.get("reference", "") or "")
        self.description.set(self.selected_item.get("description", "") or "")

        # Set date in Calendarium
        issued_str = self.selected_item.get("issued", "") or ""
        if issued_str:
            try:
                date_obj = datetime.datetime.strptime(issued_str, "%Y-%m-%d").date()
                self.calIssued.set_date(date_obj)
            except ValueError:
                self.calIssued.set_today()
        else:
            self.calIssued.set_today()
        self.cig.set(self.selected_item.get("cig", "") or "")
        self.status.set(self.selected_item.get("status", 1))

        # Set amount
        amount = self.selected_item.get("amount", 0) or 0
        self.amount.set(str(amount) if amount else "")

        # Set supplier in combobox
        supplier_id = self.selected_item.get("supplier_id")
        if supplier_id:
            sql = "SELECT description FROM suppliers WHERE supplier_id = ?"
            rs = self.engine.read(False, sql, (supplier_id,))
            if rs:
                self.cbSupplier.set(rs["description"])

    def get_values(self):
        """Get form values as list (order matches table columns excluding PK)."""
        # Get supplier_id from selection
        supplier_name = self.cbSupplier.get()
        supplier_id = self.suppliers.get(supplier_name) if supplier_name else None

        # Parse amount
        amount_str = self.amount.get().replace(",", ".")
        try:
            amount = float(amount_str) if amount_str else 0
        except ValueError:
            amount = 0

        # Get date from Calendarium
        date_obj = self.calIssued.get_date()
        issued_str = date_obj.strftime("%Y-%m-%d") if date_obj else None

        return [
            self.reference.get().strip(),
            issued_str,
            self.description.get().strip(),
            1 if self.status.get() else 0,
            supplier_id,
            amount,
            self.cig.get().strip() or None
        ]

    def on_save(self, evt=None):
        """Save the deliberation."""
        # Validate required fields
        if not self.reference.get().strip():
            messagebox.showwarning(
                self.engine.app_title,
                _("Il campo Numero è obbligatorio!"),
                parent=self
            )
            self.txtReference.focus()
            return

        if not self.cbSupplier.get():
            messagebox.showwarning(
                self.engine.app_title,
                _("Selezionare un Fornitore!"),
                parent=self
            )
            self.cbSupplier.focus()
            return

        # Check for duplicate reference
        if not self.check_reference():
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

    def check_reference(self):
        """Check if reference is unique."""
        sql = "SELECT deliberation_id FROM deliberations WHERE reference = ?"
        rs = self.engine.read(False, sql, (self.reference.get().strip(),))

        if rs:
            # If editing, allow same reference for same deliberation
            if self.index is not None:
                if rs["deliberation_id"] != self.selected_item["deliberation_id"]:
                    msg = f"La delibera '{self.reference.get()}' esiste già!"
                    messagebox.showwarning(self.engine.app_title, msg, parent=self)
                    return False
            else:
                msg = f"La delibera '{self.reference.get()}' esiste già!"
                messagebox.showwarning(self.engine.app_title, msg, parent=self)
                return False

        return True

    def on_cancel(self, evt=None):
        """Close the dialog."""
        super().on_cancel()
