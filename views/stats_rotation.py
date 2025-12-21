#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics Rotation - Inventory rotation and ABC analysis for Inventarium.

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
    """Rotation index and ABC analysis window."""

    def __init__(self, parent):
        super().__init__(parent, name="stats_rotation")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(900, 550)

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
        for text, days in [(_("90 gg"), 90), (_("6 mesi"), 180), (_("Anno"), 365)]:
            self.engine.create_button(r2, text, lambda d=days: self.set_quick_period(d), width=8).pack(side=tk.LEFT, padx=2)

        # ABC Legend
        legend = ttk.Frame(filters)
        legend.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(legend, text=_("Classificazione ABC:")).pack(side=tk.LEFT)
        ttk.Label(legend, text=_("A = Alta rotazione (80% movimenti)"),
                 foreground="green").pack(side=tk.LEFT, padx=10)
        ttk.Label(legend, text=_("B = Media rotazione"),
                 foreground="orange").pack(side=tk.LEFT, padx=10)
        ttk.Label(legend, text=_("C = Bassa rotazione"),
                 foreground="red").pack(side=tk.LEFT, padx=10)

        # Results treeview
        tree_frame = ttk.Frame(f0)
        tree_frame.pack(fill=tk.BOTH, expand=1)

        columns = ("product", "supplier", "stock", "consumed", "rotation", "coverage", "abc")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading("product", text=_("Prodotto"))
        self.tree.heading("supplier", text=_("Fornitore"))
        self.tree.heading("stock", text=_("Giacenza"))
        self.tree.heading("consumed", text=_("Consumato"))
        self.tree.heading("rotation", text=_("Rotazione"))
        self.tree.heading("coverage", text=_("Copertura (gg)"))
        self.tree.heading("abc", text=_("ABC"))

        self.tree.column("product", width=200)
        self.tree.column("supplier", width=150)
        self.tree.column("stock", width=80, anchor=tk.E)
        self.tree.column("consumed", width=80, anchor=tk.E)
        self.tree.column("rotation", width=80, anchor=tk.E)
        self.tree.column("coverage", width=100, anchor=tk.E)
        self.tree.column("abc", width=50, anchor=tk.CENTER)

        # Tags for ABC colors
        self.tree.tag_configure("A", foreground="green")
        self.tree.tag_configure("B", foreground="orange")
        self.tree.tag_configure("C", foreground="red")

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
        self.title(_("Analisi Rotazione e ABC"))
        self.engine.dict_instances["stats_rotation"] = self
        self.set_quick_period(365)  # Default: last year

    def set_quick_period(self, days):
        """Set date range for quick period selection."""
        today = datetime.date.today()
        from_date = today - datetime.timedelta(days=days)

        self.cal_from.set_date(from_date)
        self.cal_to.set_date(today)
        self.load_data()

    def load_data(self):
        """Load rotation data and calculate ABC classification."""
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

        # Calculate days for coverage
        days = max(1, (date_to - date_from).days)

        # Query: get all products with stock and consumption
        sql = """
            SELECT
                pk.package_id,
                p.description AS product,
                s.description AS supplier,
                (SELECT COUNT(*) FROM labels lb
                 JOIN batches b ON b.batch_id = lb.batch_id
                 WHERE b.package_id = pk.package_id AND lb.status = 1) AS stock,
                (SELECT COUNT(*) FROM labels lb
                 JOIN batches b ON b.batch_id = lb.batch_id
                 WHERE b.package_id = pk.package_id
                 AND lb.unloaded >= ? AND lb.unloaded <= ? AND lb.status = 0) AS consumed
            FROM packages pk
            JOIN products p ON p.product_id = pk.product_id
            LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
            WHERE pk.status = 1
            ORDER BY consumed DESC
        """

        rs = self.engine.read(True, sql, (date_from_str, date_to_str))

        if not rs:
            return

        # Calculate total consumption for ABC
        total_consumed = sum(row["consumed"] for row in rs)

        # Process data and calculate ABC
        data = []
        cumulative = 0

        for row in rs:
            stock = row["stock"]
            consumed = row["consumed"]

            # Rotation index = Consumed / Average Stock
            # Simplified: using current stock as proxy
            avg_stock = max(1, (stock + consumed) / 2)
            rotation = round(consumed / avg_stock, 2) if avg_stock > 0 else 0

            # Coverage days = Stock / Daily consumption
            daily_consumption = consumed / days if days > 0 else 0
            coverage = round(stock / daily_consumption, 0) if daily_consumption > 0 else float('inf')
            if coverage == float('inf'):
                coverage_str = "∞"
            else:
                coverage_str = str(int(coverage))

            # ABC classification based on cumulative percentage
            cumulative += consumed
            if total_consumed > 0:
                cumulative_pct = (cumulative / total_consumed) * 100
            else:
                cumulative_pct = 100

            if cumulative_pct <= 80:
                abc = "A"
            elif cumulative_pct <= 95:
                abc = "B"
            else:
                abc = "C"

            data.append({
                "product": row["product"],
                "supplier": row["supplier"] or "",
                "stock": stock,
                "consumed": consumed,
                "rotation": rotation,
                "coverage": coverage_str,
                "abc": abc
            })

        # Insert into tree
        count_a = count_b = count_c = 0
        for d in data:
            self.tree.insert("", tk.END, values=(
                d["product"],
                d["supplier"],
                d["stock"],
                d["consumed"],
                d["rotation"],
                d["coverage"],
                d["abc"]
            ), tags=(d["abc"],))

            if d["abc"] == "A":
                count_a += 1
            elif d["abc"] == "B":
                count_b += 1
            else:
                count_c += 1

        # Update summary
        self.lbl_summary.config(
            text=f"{_('Totale prodotti')}: {len(data)} | "
                 f"{_('Classe A')}: {count_a} | {_('Classe B')}: {count_b} | {_('Classe C')}: {count_c} | "
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
            title=_("Esporta Rotazione")
        )

        if filename:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([_("Prodotto"), _("Fornitore"), _("Giacenza"), _("Consumato"),
                               _("Rotazione"), _("Copertura (gg)"), _("ABC")])

                for item in self.tree.get_children():
                    values = self.tree.item(item)["values"]
                    writer.writerow(values)

    def on_cancel(self, evt=None):
        """Close the window."""
        if "stats_rotation" in self.engine.dict_instances:
            del self.engine.dict_instances["stats_rotation"]
        super().on_cancel()
