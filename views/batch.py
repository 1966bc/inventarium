#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Dialog - Create/Edit batch for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk

from i18n import _
from tkinter import ttk
from tkinter import messagebox
import datetime

from calendarium import Calendarium


class UI(tk.Toplevel):
    """Dialog for creating or editing a batch."""

    def __init__(self, parent, index=None):
        super().__init__(name="batch")

        self.parent = parent
        self.index = index
        self.engine = self.nametowidget(".").engine
        self.attributes('-topmost', True)
        self.transient(parent)
        self.resizable(0, 0)

        self.lot = tk.StringVar()
        self.status = tk.BooleanVar()

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the dialog UI."""
        # Main container
        main = ttk.Frame(self, padding=10)
        main.pack(fill=tk.BOTH, expand=1)

        # Left frame - form fields
        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        r = 0
        ttk.Label(left, text=_("Lotto:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtLot = ttk.Entry(left, textvariable=self.lot, width=25)
        self.txtLot.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(left, text=_("Scadenza:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.calExpiration = Calendarium(left, "")
        self.calExpiration.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(left, text=_("Attivo:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        chk = ttk.Checkbutton(left, onvalue=1, offvalue=0, variable=self.status, style="App.TCheckbutton")
        chk.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Right frame - buttons
        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        self.engine.create_button(right, _("Salva"), self.on_save).pack(fill=tk.X, pady=2)
        self.bind("<Alt-s>", self.on_save)

        self.engine.create_button(right, _("Chiudi"), self.on_cancel).pack(fill=tk.X, pady=2)
        self.bind("<Alt-c>", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

    def on_open(self, selected_package, selected_batch=None):
        """
        Open dialog for new or edit batch.

        Args:
            selected_package: Tuple (package_id, product_name, ...)
            selected_batch: Dict with batch data (for edit) or None (for new)
        """
        self.selected_package = selected_package
        self.package_id = selected_package[0]

        # Get product description for title
        product_name = selected_package[1] if len(selected_package) > 1 else f"Package {self.package_id}"

        if self.index is not None and selected_batch:
            # Edit mode
            self.selected_batch = selected_batch
            self.title(f"{_('Modifica Lotto')} - {product_name}")
            self.set_values()
        else:
            # New batch mode
            self.title(f"{_('Nuovo Lotto')} - {product_name}")
            self.calExpiration.set_today()
            self.status.set(1)

        self.txtLot.focus()

    def on_save(self, evt=None):
        """Save the batch."""
        # Validate
        if not self.lot.get().strip():
            messagebox.showwarning(
                self.engine.app_title,
                _("Il campo Lotto è obbligatorio!"),
                parent=self
            )
            self.txtLot.focus()
            return

        if not self.calExpiration.is_valid:
            messagebox.showwarning(
                self.engine.app_title,
                _("La data Scadenza non è valida!"),
                parent=self
            )
            return

        # Check expiration date (only for new batches)
        if self.index is None:
            exp_date = self.calExpiration.get_date()
            today = datetime.date.today()
            days_left = (exp_date - today).days

            # Check duplicate lot
            lot_name = self.lot.get().strip()
            exp_str = exp_date.isoformat()

            # Check exact duplicate (same lot + same expiration)
            sql = """SELECT batch_id FROM batches
                     WHERE package_id = ? AND description = ? AND expiration = ? AND status = 1"""
            existing = self.engine.read(False, sql, (self.package_id, lot_name, exp_str))
            if existing:
                messagebox.showerror(
                    self.engine.app_title,
                    _("Il lotto '{}' con scadenza {} esiste già!").format(lot_name, exp_date.strftime('%d-%m-%Y')),
                    parent=self
                )
                return

            # Check same lot with different expiration
            sql = """SELECT batch_id, expiration FROM batches
                     WHERE package_id = ? AND description = ? AND status = 1"""
            existing = self.engine.read(False, sql, (self.package_id, lot_name))
            if existing:
                existing_exp = existing.get("expiration", "")
                if existing_exp:
                    try:
                        existing_date = datetime.datetime.strptime(existing_exp, "%Y-%m-%d").date()
                        existing_fmt = existing_date.strftime('%d-%m-%Y')
                    except ValueError:
                        existing_fmt = existing_exp
                else:
                    existing_fmt = "N/D"

                if not messagebox.askyesno(
                    self.engine.app_title,
                    _("Il lotto '{}' esiste già con scadenza {}.\nVuoi inserirlo comunque con scadenza {}?").format(
                        lot_name, existing_fmt, exp_date.strftime('%d-%m-%Y')),
                    parent=self
                ):
                    return

            if days_left < 0:
                # Expired - don't allow
                messagebox.showerror(
                    self.engine.app_title,
                    _("Il lotto è già scaduto!\nImpossibile inserire."),
                    parent=self
                )
                return

            if days_left <= 30:
                # Expiring soon - ask confirmation
                if not messagebox.askyesno(
                    self.engine.app_title,
                    _("Attenzione: il lotto scade tra {} giorni.\nProcedere comunque?").format(days_left),
                    parent=self
                ):
                    return

        if messagebox.askyesno(
            self.engine.app_title,
            self.engine.ask_to_save,
            parent=self
        ):
            args = self.get_values()

            if self.index is not None:
                # Update existing
                sql = self.engine.build_sql("batches", op="update")
                args.append(self.selected_batch["batch_id"])
                self.engine.write(sql, tuple(args))
            else:
                # Insert new
                sql = self.engine.build_sql("batches", op="insert")
                self.engine.write(sql, tuple(args))

            # Refresh parent
            self.parent.load_batches(self.package_id)
            self.on_cancel()

        else:
            messagebox.showinfo(
                self.engine.app_title,
                self.engine.abort,
                parent=self
            )

    def get_values(self):
        """Get form values as list."""
        exp_date = self.calExpiration.get_date()
        expiration = exp_date.isoformat() if exp_date else ""
        return [
            self.package_id,
            self.lot.get().strip(),
            expiration,
            1 if self.status.get() else 0
        ]

    def set_values(self):
        """Set form values from selected batch."""
        self.lot.set(self.selected_batch.get("description", ""))

        # Set expiration date in Calendarium
        exp_str = self.selected_batch.get("expiration", "")
        if exp_str:
            try:
                exp_date = datetime.datetime.strptime(exp_str, "%Y-%m-%d").date()
                self.calExpiration.set_date(exp_date)
            except ValueError:
                pass

        self.status.set(self.selected_batch.get("status", 1))

    def on_cancel(self, evt=None):
        """Close the dialog."""
        self.destroy()
