#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Barcode Scanner - Unload labels or get info by scanning barcode.

This module provides a simple interface for unloading labels from stock
or viewing label details by scanning a barcode or manually entering the label ID.

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
    """Barcode scanner for unloading labels or viewing info."""

    def __init__(self, parent):
        super().__init__(parent, name="barcode")

        if self._reusing:
            return

        self.resizable(0, 0)
        self.attributes("-topmost", True)

        self.barcode = tk.StringVar()
        self.action = tk.IntVar(value=0)  # 0=Unload, 1=Info

        self.init_ui()
        self.show()

    def init_ui(self):
        """Build the UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        # Instructions
        ttk.Label(
            w,
            text=_("Scan barcode or enter label code:")
        ).pack(anchor=tk.W, pady=(0, 10))

        # Barcode entry
        self.txtBarcode = ttk.Entry(w, textvariable=self.barcode, width=30)
        self.txtBarcode.pack(fill=tk.X, pady=5)
        self.txtBarcode.bind("<Return>", self.on_scan)

        # Action radio buttons
        rf = ttk.LabelFrame(w, text=_("Action"), padding=5)
        rf.pack(fill=tk.X, pady=10)

        ttk.Radiobutton(
            rf, text=_("Unload"), variable=self.action, value=0
        ).pack(side=tk.LEFT, padx=10)

        ttk.Radiobutton(
            rf, text=_("Info"), variable=self.action, value=1
        ).pack(side=tk.LEFT, padx=10)

        # Result label
        self.lblResult = ttk.Label(w, text="", foreground="gray")
        self.lblResult.pack(fill=tk.X, pady=10)

        # Buttons
        bf = ttk.Frame(w)
        bf.pack(fill=tk.X, pady=(10, 0))

        self.engine.create_button(bf, _("Execute"), self.on_scan).pack(side=tk.LEFT, padx=5)

        self.engine.create_button(bf, _("Close"), self.on_cancel).pack(side=tk.RIGHT, padx=5)

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Barcode Scanner"))
        self.engine.dict_instances["barcode"] = self
        self.txtBarcode.focus()

    def on_scan(self, evt=None):
        """Process scanned barcode."""
        code = self.barcode.get().strip()

        if not code:
            return

        # Try to parse as label tick or label_id
        try:
            code_int = int(code)
        except ValueError:
            self.show_result(_("Invalid code!"), "red")
            self.clear_entry()
            return

        # Route to appropriate action
        if self.action.get() == 0:
            self.do_unload(code_int)
        else:
            self.do_info(code_int)

    def do_unload(self, code_int):
        """Unload (scarica) a label."""
        # Check if label exists by tick (barcode) or label_id
        sql = """
            SELECT
                lb.label_id,
                lb.tick,
                lb.status,
                p.description AS product_name,
                b.description AS lot
            FROM labels lb
            JOIN batches b ON b.batch_id = lb.batch_id
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            WHERE lb.tick = ? OR lb.label_id = ?
        """
        row = self.engine.read(False, sql, (code_int, code_int))

        if not row:
            self.show_result(_("Label") + f" {code_int} " + _("not found!"), "red")
            self.clear_entry()
            return

        # Get the actual label_id for unloading
        label_id = row["label_id"]

        if row["status"] == 0:
            self.show_result(_("Label") + f" {label_id} " + _("already unloaded!"), "orange")
            self.clear_entry()
            return

        if row["status"] == -1:
            self.show_result(_("Label") + f" {label_id} " + _("cancelled!"), "orange")
            self.clear_entry()
            return

        # Unload the label
        result = self.engine.unload_label(label_id)

        if result:
            product = row.get("product_name", "")
            lot = row.get("lot", "")
            self.show_result(
                _("Unloaded:") + f" {product}\n" + _("Batch:") + f" {lot}",
                "green"
            )
            # Notify subscribers that a label was unloaded
            self.engine.notify("label_unloaded")
        else:
            self.show_result(_("Error unloading!"), "red")

        self.clear_entry()

    def do_info(self, code_int):
        """Show full label information."""
        row = self.engine.get_label_info(code_int)

        if not row:
            self.show_result(_("Label") + f" {code_int} " + _("not found!"), "red")
            self.clear_entry()
            return

        # Show info dialog
        self.show_label_info(row)
        self.clear_entry()

    def show_label_info(self, data):
        """Display label information in a dialog."""
        # Status text
        status_map = {
            1: (_("In stock"), "green"),
            0: (_("Used"), "gray"),
            -1: (_("Cancelled"), "red")
        }
        status_text, status_color = status_map.get(data["status"], (_("Unknown"), "black"))

        # Days left text
        days_left = data.get("days_left")
        if days_left is not None:
            if days_left < 0:
                exp_text = _("EXPIRED by") + f" {abs(days_left)} " + _("days")
                exp_color = "red"
            elif days_left <= 30:
                exp_text = _("Expires in") + f" {days_left} " + _("days")
                exp_color = "orange"
            else:
                exp_text = _("Expires in") + f" {days_left} " + _("days")
                exp_color = "green"
        else:
            exp_text = _("No expiration")
            exp_color = "gray"

        # Build info window
        info_win = tk.Toplevel(self)
        info_win.title(_("Label Detail"))
        info_win.transient(self)
        info_win.resizable(0, 0)
        info_win.attributes("-topmost", True)

        f = ttk.Frame(info_win, padding=15)
        f.pack(fill=tk.BOTH, expand=1)

        # Header with status
        hf = ttk.Frame(f)
        hf.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            hf,
            text=data.get("product_name", ""),
            font=("TkDefaultFont", 11, "bold")
        ).pack(side=tk.LEFT)

        status_lbl = ttk.Label(hf, text=status_text, foreground=status_color)
        status_lbl.pack(side=tk.RIGHT)

        ttk.Separator(f, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Info grid
        info_frame = ttk.Frame(f)
        info_frame.pack(fill=tk.BOTH, expand=1)

        fields = [
            (_("Barcode:"), data.get("tick") or data.get("label_id")),
            (_("Product code:"), data.get("product_code", "")),
            (_("Packaging:"), data.get("packaging", "")),
            (_("Batch:"), data.get("lot", "")),
            (_("Expiration:"), data.get("expiration", "")),
            (_("Expiration status:"), exp_text),
            (_("Supplier:"), data.get("supplier", "")),
            (_("Supplier code:"), data.get("supplier_code", "")),
            (_("Category:"), data.get("category", "")),
            (_("Location:"), data.get("location", "")),
            (_("Storage:"), data.get("conservation", "")),
            (_("Loaded on:"), data.get("loaded", "")),
            (_("Unloaded on:"), data.get("unloaded", "") or "-"),
        ]

        for r, (label, value) in enumerate(fields):
            ttk.Label(info_frame, text=label).grid(row=r, column=0, sticky=tk.W, pady=2)
            val_lbl = ttk.Label(info_frame, text=str(value) if value else "-")
            val_lbl.grid(row=r, column=1, sticky=tk.W, padx=(10, 0), pady=2)

            # Color the expiration status
            if label == _("Expiration status:"):
                val_lbl.config(foreground=exp_color)

        # Close button
        ttk.Separator(f, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        self.engine.create_button(f, _("Close"), info_win.destroy).pack()

        info_win.bind("<Escape>", lambda e: info_win.destroy())
        info_win.bind("<Return>", lambda e: info_win.destroy())

        # Center on parent
        info_win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - info_win.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - info_win.winfo_height()) // 2
        info_win.geometry(f"+{x}+{y}")

        info_win.focus_set()

    def show_result(self, text, color):
        """Display result message."""
        self.lblResult.config(text=text, foreground=color)

    def clear_entry(self):
        """Clear entry and refocus."""
        self.barcode.set("")
        self.txtBarcode.focus()

    def on_cancel(self, evt=None):
        """Close the window."""
        if "barcode" in self.engine.dict_instances:
            del self.engine.dict_instances["barcode"]
        super().on_cancel()
