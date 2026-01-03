#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stocks Report - Print stock reports for Inventarium.

This module provides a dialog for selecting report options and generating
stock reports in PDF format.

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
    """Stocks report dialog."""

    def __init__(self, parent):
        super().__init__(parent, name="stocks")

        if self._reusing:
            return

        self.resizable(0, 0)

        self.report_type = tk.IntVar(value=0)
        self.dict_categories = {}
        self.dict_locations = {}

        self.init_ui()
        self.show()


    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        # Left side - Category and report type
        left = ttk.Frame(w)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5)

        # Category selection
        ttk.Label(left, text=_("Category:")).pack(anchor=tk.W)
        self.cbCategories = ttk.Combobox(left, state="readonly", width=25, style="App.TCombobox")
        self.cbCategories.pack(fill=tk.X, pady=5)

        # Report type
        lf = ttk.LabelFrame(left, text=_("Print Type"), style="App.TLabelframe")
        lf.pack(fill=tk.X, pady=5)

        reports = [
            (_("Detailed (with batches)"), 0),
            (_("Compact (stock only)"), 1),
            (_("By location (with stock)"), 2),
            (_("By location (without stock)"), 3),
        ]
        for text, value in reports:
            ttk.Radiobutton(
                lf, text=text,
                variable=self.report_type,
                value=value,
                command=self.on_report_type_changed,
                style="App.TRadiobutton"
            ).pack(anchor=tk.W, padx=5, pady=2)

        # Location selection (for location reports)
        self.lfLocation = ttk.LabelFrame(left, text=_("Location"), style="App.TLabelframe")
        ttk.Label(self.lfLocation, text=_("Select location:")).pack(anchor=tk.W, padx=5)
        self.cbLocations = ttk.Combobox(self.lfLocation, state="readonly", width=25, style="App.TCombobox")
        self.cbLocations.pack(fill=tk.X, padx=5, pady=5)
        # Initially hidden
        self.lfLocation.pack_forget()

        # Right side - Buttons
        right = ttk.Frame(w)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        self.engine.create_button(right, _("Print"), self.on_print, width=12).pack(pady=3)
        self.bind("<Alt-s>", lambda e: self.on_print())

        self.engine.create_button(right, _("Close"), self.on_cancel, width=12).pack(pady=3)
        self.bind("<Alt-c>", lambda e: self.on_cancel())

    def on_open(self):
        """Initialize and show the dialog."""
        self.title(_("Print Stock"))
        self.set_categories()
        self.set_locations()

    def on_report_type_changed(self):
        """Show/hide location selector based on report type."""
        if self.report_type.get() in (2, 3):
            # Location reports - show location selector
            self.lfLocation.pack(fill=tk.X, pady=5)
        else:
            # Other reports - hide location selector
            self.lfLocation.pack_forget()

    def set_locations(self):
        """Load locations into combobox."""
        self.dict_locations = {}
        voices = []

        sql = """SELECT location_id, description, room
                 FROM locations
                 WHERE status = 1
                 ORDER BY room, description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs):
                self.dict_locations[idx] = row["location_id"]
                room = row["room"] or ""
                desc = row["description"] or ""
                display = f"{room} - {desc}" if room else desc
                voices.append(display)

        self.cbLocations["values"] = voices
        if voices:
            self.cbLocations.current(0)

    def set_categories(self):
        """Load categories into combobox."""
        self.dict_categories = {}
        voices = []

        # Add "All" option first
        self.dict_categories[0] = None
        voices.append(_("-- All categories --"))

        sql = """SELECT category_id, description
                 FROM categories
                 WHERE reference_id = 1 AND status = 1
                 ORDER BY description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs, start=1):
                self.dict_categories[idx] = row["category_id"]
                voices.append(row["description"])

        self.cbCategories["values"] = voices
        if voices:
            self.cbCategories.current(0)

    def on_print(self, evt=None):
        """Generate and print the report."""
        if self.cbCategories.current() == -1:
            messagebox.showwarning(
                self.engine.app_title,
                _("Please select a category!"),
                parent=self
            )
            return

        category_idx = self.cbCategories.current()
        category_id = self.dict_categories.get(category_idx)
        category_name = self.cbCategories.get()
        report_type = self.report_type.get()

        # Build query based on report type
        if report_type == 0:
            # Detailed report with batches
            self.print_detailed_report(category_id, category_name)
        elif report_type == 1:
            # Compact report - just product and stock
            self.print_compact_report(category_id, category_name)
        elif report_type == 2:
            # Location report with stock
            if self.cbLocations.current() == -1:
                messagebox.showwarning(
                    self.engine.app_title,
                    _("Please select a location!"),
                    parent=self
                )
                return
            location_id = self.dict_locations.get(self.cbLocations.current())
            location_name = self.cbLocations.get()
            self.print_location_report(location_id, location_name, show_stock=True)
        else:
            # Location report without stock (for posting)
            if self.cbLocations.current() == -1:
                messagebox.showwarning(
                    self.engine.app_title,
                    _("Please select a location!"),
                    parent=self
                )
                return
            location_id = self.dict_locations.get(self.cbLocations.current())
            location_name = self.cbLocations.get()
            self.print_location_report(location_id, location_name, show_stock=False)

    def print_detailed_report(self, category_id, category_name):
        """Print detailed report with batches and labels."""
        try:
            self.config(cursor="watch")
            self.update()

            from reports import rpt_stocks

            # Get products with stock info
            sql = """
                SELECT
                    pk.package_id,
                    p.description AS product_name,
                    pk.reference AS supplier_code,
                    s.description AS supplier,
                    pk.packaging,
                    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock
                FROM packages pk
                JOIN products p ON p.product_id = pk.product_id
                LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
                LEFT JOIN batches b ON b.package_id = pk.package_id AND b.status = 1
                LEFT JOIN labels lb ON lb.batch_id = b.batch_id
                WHERE pk.status = 1 AND p.status = 1
            """
            args = []

            if category_id:
                sql += " AND pk.category_id = ?"
                args.append(category_id)

            sql += " GROUP BY pk.package_id ORDER BY p.description"

            rs = self.engine.read(True, sql, tuple(args))

            if rs:
                report = rpt_stocks.Report(self)
                report.init_report(rs, category_name)
                report.create_doc()
            else:
                messagebox.showinfo(
                    self.engine.app_title,
                    _("No products found for the selected category."),
                    parent=self
                )

        except Exception as e:
            messagebox.showerror(
                self.engine.app_title,
                _("Error generating report:") + f"\n{e}",
                parent=self
            )
        finally:
            self.config(cursor="")
            self.update()

    def print_compact_report(self, category_id, category_name):
        """Print compact report with just product and stock count."""
        try:
            self.config(cursor="watch")
            self.update()

            from reports import rpt_stocks_list

            sql = """
                SELECT
                    p.description AS product_name,
                    pk.reference AS supplier_code,
                    s.description AS supplier,
                    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock
                FROM packages pk
                JOIN products p ON p.product_id = pk.product_id
                LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
                LEFT JOIN batches b ON b.package_id = pk.package_id AND b.status = 1
                LEFT JOIN labels lb ON lb.batch_id = b.batch_id
                WHERE pk.status = 1 AND p.status = 1
            """
            args = []

            if category_id:
                sql += " AND pk.category_id = ?"
                args.append(category_id)

            sql += " GROUP BY pk.package_id ORDER BY p.description"

            rs = self.engine.read(True, sql, tuple(args))

            if rs:
                report = rpt_stocks_list.Report(self)
                report.init_report(rs, category_name)
                report.create_doc()
            else:
                messagebox.showinfo(
                    self.engine.app_title,
                    _("No products found for the selected category."),
                    parent=self
                )

        except Exception as e:
            messagebox.showerror(
                self.engine.app_title,
                _("Error generating report:") + f"\n{e}",
                parent=self
            )
        finally:
            self.config(cursor="")
            self.update()

    def print_location_report(self, location_id, location_name, show_stock=True):
        """Print report for a single location."""
        try:
            self.config(cursor="watch")
            self.update()

            from reports import rpt_locations

            sql = """
                SELECT
                    l.description AS location_name,
                    l.room,
                    p.description AS product_name,
                    pk.reference AS supplier_code,
                    pk.packaging,
                    pk.shelf,
                    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock
                FROM packages pk
                JOIN products p ON p.product_id = pk.product_id
                LEFT JOIN locations l ON l.location_id = pk.location_id
                LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
                LEFT JOIN batches b ON b.package_id = pk.package_id AND b.status = 1
                LEFT JOIN labels lb ON lb.batch_id = b.batch_id
                WHERE pk.status = 1 AND p.status = 1
                AND pk.location_id = ?
                GROUP BY pk.package_id
                ORDER BY pk.shelf, p.description
            """

            rs = self.engine.read(True, sql, (location_id,))

            if rs:
                report = rpt_locations.Report(self)
                report.init_report(rs, location_name, show_stock=show_stock)
                report.create_doc()
            else:
                messagebox.showinfo(
                    self.engine.app_title,
                    _("No products found for the selected location."),
                    parent=self
                )

        except Exception as e:
            messagebox.showerror(
                self.engine.app_title,
                _("Error generating report:") + f"\n{e}",
                parent=self
            )
        finally:
            self.config(cursor="")
            self.update()

    def on_cancel(self, evt=None):
        """Close the dialog."""
        super().on_cancel()
