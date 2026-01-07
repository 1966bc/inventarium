#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Labels Dialog - Load labels into stock for Inventarium.

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
    """Dialog for loading labels (packages) into stock."""

    def __init__(self, parent):
        super().__init__(parent, name="labels")

        self.attributes("-topmost", True)

        self.labels_count = tk.IntVar(value=1)
        self.product = tk.StringVar()
        self.lot = tk.StringVar()
        self.expiration = tk.StringVar()

        self.init_ui()
        self.show()


    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        r = 0
        ttk.Label(w, text=_("Product:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtProduct = ttk.Entry(w, textvariable=self.product, state="readonly", width=30)
        self.txtProduct.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Batch:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtLot = ttk.Entry(w, textvariable=self.lot, state="readonly", width=20)
        self.txtLot.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Expiration:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtExpiration = ttk.Entry(w, textvariable=self.expiration, state="readonly", width=12)
        self.txtExpiration.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Separator(w, orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=2, sticky="ew", pady=10)

        r += 1
        ttk.Label(w, text=_("Number of labels:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.spnLabels = ttk.Spinbox(
            w,
            from_=1,
            to=100,
            textvariable=self.labels_count,
            width=5,
            validate="key",
            validatecommand=self.engine.get_validate_integer(self)
        )
        self.spnLabels.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Buttons
        r += 1
        bf = ttk.Frame(w)
        bf.grid(row=r, column=0, columnspan=2, pady=10)

        self.engine.create_button(bf, _("Load"), self.on_save).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-s>", self.on_save)
        self.bind("<Return>", self.on_save)

        self.engine.create_button(bf, _("Close"), self.on_cancel).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", self.on_cancel)

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

        self.title(_("Load Labels"))
        self.labels_count.set(1)
        self.spnLabels.focus()

    def on_save(self, evt=None):
        """Load labels into stock."""
        count = self.labels_count.get()

        if count < 1:
            messagebox.showwarning(
                self.engine.app_title,
                _("Enter a valid number of labels!"),
                parent=self
            )
            return

        msg = _("Load {} label?").format(count) if count == 1 else _("Load {} labels?").format(count)
        if messagebox.askyesno(self.engine.app_title, msg, parent=self):
            # Load labels
            for i in range(count):
                self.engine.load_label(self.batch_id)

            # Refresh labels list and stock count
            self.parent.load_labels(self.batch_id)
            self.parent.update_product_stock()
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
