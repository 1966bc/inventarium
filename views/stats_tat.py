#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics TAT - Turn Around Time analysis for Inventarium.

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
    """TAT (Turn Around Time) analysis window."""

    def __init__(self, parent):
        super().__init__(parent, name="stats_tat")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(850, 550)

        self.init_ui()
        self.engine.center_window(self)
        self.show()


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=10)
        f0.pack(fill=tk.BOTH, expand=1)

        # Filters frame
        filters = ttk.LabelFrame(f0, text=_("Periodo di Analisi"), style="App.TLabelframe")
        filters.pack(fill=tk.X, pady=(0, 10))

        r1 = ttk.Frame(filters)
        r1.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(r1, text=_("Da:")).pack(side=tk.LEFT)
        self.cal_from = Calendarium(r1, "")
        self.cal_from.pack(side=tk.LEFT, padx=(5, 20))

        ttk.Label(r1, text=_("A:")).pack(side=tk.LEFT)
        self.cal_to = Calendarium(r1, "")
        self.cal_to.pack(side=tk.LEFT, padx=5)

        self.engine.create_button(r1, _("Calcola"), self.load_data).pack(side=tk.LEFT, padx=20)

        # Quick period buttons
        r2 = ttk.Frame(filters)
        r2.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(r2, text=_("Periodo rapido:")).pack(side=tk.LEFT)
        for text, days in [(_("30 gg"), 30), (_("90 gg"), 90), (_("6 mesi"), 180), (_("Anno"), 365)]:
            self.engine.create_button(r2, text, lambda d=days: self.set_quick_period(d), width=8).pack(side=tk.LEFT, padx=2)

        # Summary metrics
        metrics = ttk.LabelFrame(f0, text=_("Metriche TAT"), style="App.TLabelframe")
        metrics.pack(fill=tk.X, pady=(0, 10))

        self.frm_metrics = ttk.Frame(metrics)
        self.frm_metrics.pack(fill=tk.X, padx=10, pady=10)

        # Results treeview - Order TAT
        ttk.Label(f0, text=_("Tempo Richiesta → Consegna (per fornitore)"),
                 font=("", 10, "bold")).pack(anchor=tk.W)

        columns = ("supplier", "orders", "avg_days", "min_days", "max_days")
        self.tree_order = ttk.Treeview(f0, columns=columns, show="headings", height=8)

        self.tree_order.heading("supplier", text=_("Fornitore"))
        self.tree_order.heading("orders", text=_("Ordini"))
        self.tree_order.heading("avg_days", text=_("Media (gg)"))
        self.tree_order.heading("min_days", text=_("Min (gg)"))
        self.tree_order.heading("max_days", text=_("Max (gg)"))

        self.tree_order.column("supplier", width=250)
        self.tree_order.column("orders", width=100, anchor=tk.E)
        self.tree_order.column("avg_days", width=100, anchor=tk.E)
        self.tree_order.column("min_days", width=100, anchor=tk.E)
        self.tree_order.column("max_days", width=100, anchor=tk.E)

        self.tree_order.pack(fill=tk.X, pady=5)

        # Results treeview - Stock TAT
        ttk.Label(f0, text=_("Tempo in Magazzino (Carico → Scarico)"),
                 font=("", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))

        columns2 = ("product", "labels", "avg_days", "min_days", "max_days")
        self.tree_stock = ttk.Treeview(f0, columns=columns2, show="headings", height=8)

        self.tree_stock.heading("product", text=_("Prodotto"))
        self.tree_stock.heading("labels", text=_("Etichette"))
        self.tree_stock.heading("avg_days", text=_("Media (gg)"))
        self.tree_stock.heading("min_days", text=_("Min (gg)"))
        self.tree_stock.heading("max_days", text=_("Max (gg)"))

        self.tree_stock.column("product", width=250)
        self.tree_stock.column("labels", width=100, anchor=tk.E)
        self.tree_stock.column("avg_days", width=100, anchor=tk.E)
        self.tree_stock.column("min_days", width=100, anchor=tk.E)
        self.tree_stock.column("max_days", width=100, anchor=tk.E)

        self.tree_stock.pack(fill=tk.BOTH, expand=1, pady=5)

        # Buttons
        bf = ttk.Frame(f0)
        bf.pack(fill=tk.X, pady=(10, 0))

        self.engine.create_button(bf, _("Esporta CSV"), self.export_csv, width=12).pack(side=tk.LEFT, padx=5)

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel, width=12).pack(side=tk.RIGHT, padx=5)
        self.bind("<Escape>", lambda e: self.on_cancel())

    def on_open(self):
        """Initialize and show the window."""
        self.title("Analisi Tempi (TAT)")
        self.engine.dict_instances["stats_tat"] = self
        self.set_quick_period(90)  # Default: last 90 days

    def set_quick_period(self, days):
        """Set date range for quick period selection."""
        today = datetime.date.today()
        from_date = today - datetime.timedelta(days=days)

        self.cal_from.set_date(from_date)
        self.cal_to.set_date(today)
        self.load_data()

    def load_data(self):
        """Load TAT data."""
        # Clear trees
        for item in self.tree_order.get_children():
            self.tree_order.delete(item)
        for item in self.tree_stock.get_children():
            self.tree_stock.delete(item)

        # Clear metrics
        for w in self.frm_metrics.winfo_children():
            w.destroy()

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

        self.load_order_tat(date_from_str, date_to_str)
        self.load_stock_tat(date_from_str, date_to_str)
        self.load_summary_metrics(date_from_str, date_to_str)

    def load_order_tat(self, date_from, date_to):
        """Load order-to-delivery TAT by supplier."""
        sql = """
            SELECT
                s.description AS supplier,
                COUNT(DISTINCT d.delivery_id) AS orders,
                AVG(julianday(d.delivered) - julianday(r.issued)) AS avg_days,
                MIN(julianday(d.delivered) - julianday(r.issued)) AS min_days,
                MAX(julianday(d.delivered) - julianday(r.issued)) AS max_days
            FROM deliveries d
            JOIN items i ON i.item_id = d.item_id
            JOIN requests r ON r.request_id = i.request_id
            JOIN packages pk ON pk.package_id = i.package_id
            LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
            WHERE d.delivered >= ? AND d.delivered <= ? AND d.status = 1
            GROUP BY pk.supplier_id
            ORDER BY avg_days DESC
        """

        rs = self.engine.read(True, sql, (date_from, date_to))

        if rs:
            for row in rs:
                avg_days = round(row["avg_days"], 1) if row["avg_days"] else 0
                min_days = int(row["min_days"]) if row["min_days"] else 0
                max_days = int(row["max_days"]) if row["max_days"] else 0

                self.tree_order.insert("", tk.END, values=(
                    row["supplier"] or "N/D",
                    row["orders"],
                    avg_days,
                    min_days,
                    max_days
                ))

    def load_stock_tat(self, date_from, date_to):
        """Load stock residence time (loaded to unloaded)."""
        sql = """
            SELECT
                p.description AS product,
                COUNT(lb.label_id) AS labels,
                AVG(julianday(lb.unloaded) - julianday(lb.loaded)) AS avg_days,
                MIN(julianday(lb.unloaded) - julianday(lb.loaded)) AS min_days,
                MAX(julianday(lb.unloaded) - julianday(lb.loaded)) AS max_days
            FROM labels lb
            JOIN batches b ON b.batch_id = lb.batch_id
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            WHERE lb.unloaded >= ? AND lb.unloaded <= ?
            AND lb.status = 0 AND lb.loaded IS NOT NULL
            GROUP BY pk.package_id
            ORDER BY avg_days DESC
        """

        rs = self.engine.read(True, sql, (date_from, date_to))

        if rs:
            for row in rs:
                avg_days = round(row["avg_days"], 1) if row["avg_days"] else 0
                min_days = int(row["min_days"]) if row["min_days"] else 0
                max_days = int(row["max_days"]) if row["max_days"] else 0

                self.tree_stock.insert("", tk.END, values=(
                    row["product"],
                    row["labels"],
                    avg_days,
                    min_days,
                    max_days
                ))

    def load_summary_metrics(self, date_from, date_to):
        """Load overall summary metrics."""
        # Overall order TAT
        sql = """
            SELECT
                AVG(julianday(d.delivered) - julianday(r.issued)) AS avg_order_tat
            FROM deliveries d
            JOIN items i ON i.item_id = d.item_id
            JOIN requests r ON r.request_id = i.request_id
            WHERE d.delivered >= ? AND d.delivered <= ? AND d.status = 1
        """
        row = self.engine.read(False, sql, (date_from, date_to))
        avg_order_tat = round(row["avg_order_tat"], 1) if row and row["avg_order_tat"] else "N/D"

        # Overall stock TAT
        sql = """
            SELECT
                AVG(julianday(lb.unloaded) - julianday(lb.loaded)) AS avg_stock_tat
            FROM labels lb
            WHERE lb.unloaded >= ? AND lb.unloaded <= ?
            AND lb.status = 0 AND lb.loaded IS NOT NULL
        """
        row = self.engine.read(False, sql, (date_from, date_to))
        avg_stock_tat = round(row["avg_stock_tat"], 1) if row and row["avg_stock_tat"] else "N/D"

        # Display metrics
        self._add_metric(_("TAT medio ordini:"), f"{avg_order_tat} giorni")
        self._add_metric(_("TAT medio magazzino:"), f"{avg_stock_tat} giorni")

    def _add_metric(self, label, value):
        """Add a metric to the metrics frame."""
        frm = ttk.Frame(self.frm_metrics)
        frm.pack(side=tk.LEFT, padx=20)

        ttk.Label(frm, text=label).pack(side=tk.LEFT)
        ttk.Label(frm, text=value, font=("", 11, "bold")).pack(side=tk.LEFT, padx=5)

    def export_csv(self):
        """Export data to CSV file."""
        from tkinter import filedialog
        import csv

        filename = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Esporta TAT"
        )

        if filename:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")

                # Order TAT
                writer.writerow(["=== TAT Ordini ==="])
                writer.writerow(["Fornitore", "Ordini", "Media (gg)", "Min (gg)", "Max (gg)"])
                for item in self.tree_order.get_children():
                    values = self.tree_order.item(item)["values"]
                    writer.writerow(values)

                writer.writerow([])

                # Stock TAT
                writer.writerow(["=== TAT Magazzino ==="])
                writer.writerow(["Prodotto", "Etichette", "Media (gg)", "Min (gg)", "Max (gg)"])
                for item in self.tree_stock.get_children():
                    values = self.tree_stock.item(item)["values"]
                    writer.writerow(values)

    def on_cancel(self, evt=None):
        """Close the window."""
        if "stats_tat" in self.engine.dict_instances:
            del self.engine.dict_instances["stats_tat"]
        super().on_cancel()
