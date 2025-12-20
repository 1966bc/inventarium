#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics Suppliers - Supplier performance analysis for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk

from i18n import _
from tkinter import ttk
import datetime

from calendarium import Calendarium


class UI(tk.Toplevel):
    """Supplier performance analysis window."""

    def __init__(self, parent):
        super().__init__(name="stats_suppliers")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.minsize(900, 550)

        self.init_ui()
        self.engine.center_window(self)


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

        # Results treeview
        tree_frame = ttk.Frame(f0)
        tree_frame.pack(fill=tk.BOTH, expand=1)

        columns = ("supplier", "orders", "items_ordered", "items_delivered",
                  "completion", "avg_tat", "products")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading("supplier", text=_("Fornitore"))
        self.tree.heading("orders", text=_("Ordini"))
        self.tree.heading("items_ordered", text=_("Ordinato"))
        self.tree.heading("items_delivered", text=_("Consegnato"))
        self.tree.heading("completion", text="Completamento %")
        self.tree.heading("avg_tat", text="TAT medio (gg)")
        self.tree.heading("products", text=_("Prodotti"))

        self.tree.column("supplier", width=200)
        self.tree.column("orders", width=80, anchor=tk.E)
        self.tree.column("items_ordered", width=80, anchor=tk.E)
        self.tree.column("items_delivered", width=90, anchor=tk.E)
        self.tree.column("completion", width=110, anchor=tk.E)
        self.tree.column("avg_tat", width=100, anchor=tk.E)
        self.tree.column("products", width=80, anchor=tk.E)

        # Tags for completion rate colors
        self.tree.tag_configure("good", foreground="green")
        self.tree.tag_configure("warning", foreground="orange")
        self.tree.tag_configure("bad", foreground="red")

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
        self.title(_("Analisi Fornitori"))
        self.engine.dict_instances["stats_suppliers"] = self
        self.set_quick_period(365)  # Default: last year

    def set_quick_period(self, days):
        """Set date range for quick period selection."""
        today = datetime.date.today()
        from_date = today - datetime.timedelta(days=days)

        self.cal_from.set_date(from_date)
        self.cal_to.set_date(today)
        self.load_data()

    def load_data(self):
        """Load supplier performance data."""
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

        # Query supplier performance
        sql = """
            SELECT
                s.supplier_id,
                s.description AS supplier,
                COUNT(DISTINCT r.request_id) AS orders,
                SUM(i.quantity) AS items_ordered,
                SUM(COALESCE(
                    (SELECT SUM(d.quantity) FROM deliveries d
                     WHERE d.item_id = i.item_id AND d.status = 1
                     AND d.delivered >= ? AND d.delivered <= ?), 0
                )) AS items_delivered,
                AVG(
                    SELECT AVG(julianday(d2.delivered) - julianday(r2.issued))
                    FROM deliveries d2
                    JOIN items i2 ON i2.item_id = d2.item_id
                    JOIN requests r2 ON r2.request_id = i2.request_id
                    JOIN packages pk2 ON pk2.package_id = i2.package_id
                    WHERE pk2.supplier_id = s.supplier_id
                    AND d2.delivered >= ? AND d2.delivered <= ?
                    AND d2.status = 1
                ) AS avg_tat,
                COUNT(DISTINCT pk.package_id) AS products
            FROM suppliers s
            JOIN packages pk ON pk.supplier_id = s.supplier_id
            JOIN items i ON i.package_id = pk.package_id
            JOIN requests r ON r.request_id = i.request_id
            WHERE r.issued >= ? AND r.issued <= ?
            AND s.status = 1
            GROUP BY s.supplier_id
            ORDER BY items_ordered DESC
        """

        # Simplified query - the above is complex, let's break it down
        sql = """
            SELECT
                s.supplier_id,
                s.description AS supplier,
                COUNT(DISTINCT r.request_id) AS orders,
                SUM(i.quantity) AS items_ordered,
                COUNT(DISTINCT pk.package_id) AS products
            FROM suppliers s
            JOIN packages pk ON pk.supplier_id = s.supplier_id
            JOIN items i ON i.package_id = pk.package_id
            JOIN requests r ON r.request_id = i.request_id
            WHERE r.issued >= ? AND r.issued <= ?
            AND s.status = 1
            GROUP BY s.supplier_id
            ORDER BY items_ordered DESC
        """

        rs = self.engine.read(True, sql, (date_from_str, date_to_str))

        if not rs:
            self.lbl_summary.config(text=_("Nessun dato nel periodo selezionato"))
            return

        # For each supplier, get delivery stats
        data = []
        for row in rs:
            supplier_id = row["supplier_id"]

            # Get delivered items
            sql2 = """
                SELECT SUM(d.quantity) AS delivered
                FROM deliveries d
                JOIN items i ON i.item_id = d.item_id
                JOIN packages pk ON pk.package_id = i.package_id
                WHERE pk.supplier_id = ? AND d.status = 1
                AND d.delivered >= ? AND d.delivered <= ?
            """
            r2 = self.engine.read(False, sql2, (supplier_id, date_from_str, date_to_str))
            items_delivered = r2["delivered"] if r2 and r2["delivered"] else 0

            # Get average TAT
            sql3 = """
                SELECT AVG(julianday(d.delivered) - julianday(r.issued)) AS avg_tat
                FROM deliveries d
                JOIN items i ON i.item_id = d.item_id
                JOIN requests r ON r.request_id = i.request_id
                JOIN packages pk ON pk.package_id = i.package_id
                WHERE pk.supplier_id = ? AND d.status = 1
                AND d.delivered >= ? AND d.delivered <= ?
            """
            r3 = self.engine.read(False, sql3, (supplier_id, date_from_str, date_to_str))
            avg_tat = round(r3["avg_tat"], 1) if r3 and r3["avg_tat"] else 0

            items_ordered = row["items_ordered"] or 0
            completion = round((items_delivered / items_ordered * 100), 1) if items_ordered > 0 else 0

            data.append({
                "supplier": row["supplier"],
                "orders": row["orders"],
                "items_ordered": items_ordered,
                "items_delivered": items_delivered,
                "completion": completion,
                "avg_tat": avg_tat,
                "products": row["products"]
            })

        # Insert into tree
        total_ordered = 0
        total_delivered = 0

        for d in data:
            # Determine tag based on completion rate
            if d["completion"] >= 90:
                tag = "good"
            elif d["completion"] >= 70:
                tag = "warning"
            else:
                tag = "bad"

            self.tree.insert("", tk.END, values=(
                d["supplier"],
                d["orders"],
                d["items_ordered"],
                d["items_delivered"],
                f"{d['completion']}%",
                d["avg_tat"],
                d["products"]
            ), tags=(tag,))

            total_ordered += d["items_ordered"]
            total_delivered += d["items_delivered"]

        # Update summary
        overall_completion = round((total_delivered / total_ordered * 100), 1) if total_ordered > 0 else 0
        self.lbl_summary.config(
            text=f"Fornitori: {len(data)} | "
                 f"Totale ordinato: {total_ordered} | "
                 f"Totale consegnato: {total_delivered} | "
                 f"Completamento: {overall_completion}%"
        )

    def export_csv(self):
        """Export data to CSV file."""
        from tkinter import filedialog
        import csv

        filename = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Esporta Fornitori"
        )

        if filename:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["Fornitore", "Ordini", "Ordinato", "Consegnato",
                               "Completamento %", "TAT medio (gg)", _("Prodotti")])

                for item in self.tree.get_children():
                    values = self.tree.item(item)["values"]
                    writer.writerow(values)

    def on_cancel(self, evt=None):
        """Close the window."""
        if "stats_suppliers" in self.engine.dict_instances:
            del self.engine.dict_instances["stats_suppliers"]
        self.destroy()
