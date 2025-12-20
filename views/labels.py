#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Labels Dialog - Load labels into stock for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk

from i18n import _
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    """Dialog for loading labels (packages) into stock."""

    def __init__(self, parent):
        super().__init__(name="labels")

        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.attributes("-topmost", True)
        self.transient(parent)
        self.resizable(0, 0)

        self.labels_count = tk.IntVar(value=1)
        self.product = tk.StringVar()
        self.lot = tk.StringVar()
        self.expiration = tk.StringVar()

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        r = 0
        ttk.Label(w, text="Prodotto:").grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtProduct = ttk.Entry(w, textvariable=self.product, state="readonly", width=30)
        self.txtProduct.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Lotto:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtLot = ttk.Entry(w, textvariable=self.lot, state="readonly", width=20)
        self.txtLot.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Scadenza:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtExpiration = ttk.Entry(w, textvariable=self.expiration, state="readonly", width=12)
        self.txtExpiration.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Separator(w, orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=2, sticky="ew", pady=10)

        r += 1
        ttk.Label(w, text="Numero etichette:").grid(row=r, column=0, sticky=tk.W, pady=2)
        self.spnLabels = ttk.Spinbox(w, from_=1, to=100, textvariable=self.labels_count, width=5)
        self.spnLabels.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Buttons
        r += 1
        bf = ttk.Frame(w)
        bf.grid(row=r, column=0, columnspan=2, pady=10)

        self.engine.create_button(bf, _("Carica"), self.on_save).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-s>", self.on_save)
        self.bind("<Return>", self.on_save)

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

    def on_open(self, selected_package, selected_batch):
        """
        Open dialog for loading labels.

        Args:
            selected_package: Tuple (package_id, product_name, ...)
            selected_batch: Dict with batch data
        """
        self.selected_package = selected_package
        self.selected_batch = selected_batch

        self.package_id = selected_package[0]
        self.batch_id = selected_batch["batch_id"]

        # Set display values
        product_name = selected_package[1] if len(selected_package) > 1 else ""
        self.product.set(product_name)
        self.lot.set(selected_batch.get("description", ""))
        self.expiration.set(selected_batch.get("expiration", ""))

        self.title("Carica Etichette")
        self.labels_count.set(1)
        self.spnLabels.focus()

    def on_save(self, evt=None):
        """Load labels into stock."""
        count = self.labels_count.get()

        if count < 1:
            messagebox.showwarning(
                self.engine.app_title,
                "Inserire un numero di etichette valido!",
                parent=self
            )
            return

        msg = f"Caricare {count} etichett{'a' if count == 1 else 'e'}?"
        if messagebox.askyesno(self.engine.app_title, msg, parent=self):
            # Load labels
            for _ in range(count):
                self.engine.load_label(self.batch_id)

            # Refresh only labels list
            self.parent.load_labels(self.batch_id)
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
