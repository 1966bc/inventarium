#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics Consumption - Product consumption analysis for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
import datetime

from i18n import _
from calendarium import Calendarium
from views.parent_view import ParentView


class UI(ParentView):
    """Consumption analysis window."""

    def __init__(self, parent):
        super().__init__(parent, name="stats_consumption")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(800, 550)

        self.dict_categories = {}

        self.init_ui()
        self.engine.center_window(self)
        self.show()


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=10)
        f0.pack(fill=tk.BOTH, expand=1)

        # Filters frame
        filters = ttk.LabelFrame(f0, text=_("Filtri"), style="App.TLabelframe")
        filters.pack(fill=tk.X, pady=(0, 10))

        # Row 1: dates
        r1 = ttk.Frame(filters)
        r1.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(r1, text=_("Da:")).pack(side=tk.LEFT)
        self.cal_from = Calendarium(r1, "")
        self.cal_from.pack(side=tk.LEFT, padx=(5, 20))

        ttk.Label(r1, text=_("A:")).pack(side=tk.LEFT)
        self.cal_to = Calendarium(r1, "")
        self.cal_to.pack(side=tk.LEFT, padx=5)

        # Row 2: category filter
        r2 = ttk.Frame(filters)
        r2.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(r2, text=_("Categoria:")).pack(side=tk.LEFT)
        self.cbCategories = ttk.Combobox(r2, state="readonly", width=25, style="App.TCombobox")
        self.cbCategories.pack(side=tk.LEFT, padx=5)

        self.engine.create_button(r2, _("Calcola"), self.load_data).pack(side=tk.LEFT, padx=20)

        # Quick period buttons
        r3 = ttk.Frame(filters)
        r3.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(r3, text=_("Periodo rapido:")).pack(side=tk.LEFT)
        for text, days in [(_("30 gg"), 30), (_("60 gg"), 60), (_("90 gg"), 90), (_("Anno"), 365)]:
            self.engine.create_button(r3, text, lambda d=days: self.set_quick_period(d), width=8).pack(side=tk.LEFT, padx=2)

        # Results treeview
        tree_frame = ttk.Frame(f0)
        tree_frame.pack(fill=tk.BOTH, expand=1)

        columns = ("product", "supplier", "consumed", "avg_month")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading("product", text=_("Prodotto"))
        self.tree.heading("supplier", text=_("Fornitore"))
        self.tree.heading("consumed", text=_("Consumato"))
        self.tree.heading("avg_month", text=_("Media/Mese"))

        self.tree.column("product", width=250)
        self.tree.column("supplier", width=200)
        self.tree.column("consumed", width=100, anchor=tk.E)
        self.tree.column("avg_month", width=100, anchor=tk.E)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Summary label
        self.lbl_summary = ttk.Label(f0, text="")
        self.lbl_summary.pack(anchor=tk.W, pady=(10, 5))

        # Buttons
        bf = ttk.Frame(f0)
        bf.pack(fill=tk.X, pady=(5, 0))

        self.engine.create_button(bf, _("Esporta CSV"), self.export_csv, width=12).pack(side=tk.LEFT, padx=5)

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel, width=12).pack(side=tk.RIGHT, padx=5)
        self.bind("<Escape>", lambda e: self.on_cancel())

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Analisi Consumi"))
        self.engine.dict_instances["stats_consumption"] = self
        self.set_categories()
        self.set_quick_period(30)  # Default: last 30 days

    def set_categories(self):
        """Load categories into combobox."""
        self.dict_categories = {}
        voices = [_("-- Tutte --")]
        self.dict_categories[0] = None

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
        self.cbCategories.current(0)

    def set_quick_period(self, days):
        """Set date range for quick period selection."""
        today = datetime.date.today()
        from_date = today - datetime.timedelta(days=days)

        self.cal_from.set_date(from_date)
        self.cal_to.set_date(today)
        self.load_data()

    def load_data(self):
        """Load consumption data."""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get date range
        if not self.cal_from.is_valid or not self.cal_to.is_valid:
            messagebox.showwarning(
                self.engine.app_title,
                _("Le date non sono valide!"),
                parent=self
            )
            return

        date_from = self.cal_from.get_date()
        date_to = self.cal_to.get_date()

        date_from_str = date_from.isoformat()
        date_to_str = date_to.isoformat()

        # Calculate months for average
        days = (date_to - date_from).days
        months = max(1, days / 30)

        # Get category filter
        cat_idx = self.cbCategories.current()
        category_id = self.dict_categories.get(cat_idx)

        # Build query
        sql = """
            SELECT
                p.description AS product,
                s.description AS supplier,
                COUNT(lb.label_id) AS consumed
            FROM labels lb
            JOIN batches b ON b.batch_id = lb.batch_id
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
            WHERE lb.unloaded >= ? AND lb.unloaded <= ? AND lb.status = 0
        """
        args = [date_from_str, date_to_str]

        if category_id:
            sql += " AND pk.category_id = ?"
            args.append(category_id)

        sql += """
            GROUP BY pk.package_id
            ORDER BY consumed DESC
        """

        rs = self.engine.read(True, sql, tuple(args))

        total_consumed = 0
        if rs:
            for row in rs:
                consumed = row["consumed"]
                avg_month = round(consumed / months, 1)
                total_consumed += consumed

                self.tree.insert("", tk.END, values=(
                    row["product"],
                    row["supplier"] or "",
                    consumed,
                    avg_month
                ))

        # Update summary
        self.lbl_summary.config(
            text=f"{_('Totale prodotti')}: {len(rs) if rs else 0} | "
                 f"{_('Totale consumato')}: {total_consumed} | "
                 f"{_('Periodo')}: {days} {_('giorni')}"
        )

    def export_csv(self):
        """Export data to CSV file."""
        from tkinter import filedialog
        import csv

        filename = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title=_("Esporta Consumi")
        )

        if filename:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([_("Prodotto"), _("Fornitore"), _("Consumato"), _("Media/Mese")])

                for item in self.tree.get_children():
                    values = self.tree.item(item)["values"]
                    writer.writerow(values)

    def on_cancel(self, evt=None):
        """Close the window."""
        if "stats_consumption" in self.engine.dict_instances:
            del self.engine.dict_instances["stats_consumption"]
        super().on_cancel()
