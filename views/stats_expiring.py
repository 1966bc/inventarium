#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics Expiring - Expiration analysis and losses for Inventarium.

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
    """Expiration analysis window."""

    def __init__(self, parent):
        super().__init__(name="stats_expiring")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.minsize(850, 550)

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=10)
        f0.pack(fill=tk.BOTH, expand=1)

        # Period filter
        filters = ttk.LabelFrame(f0, text=_("Analisi Storica Scaduti"), style="App.TLabelframe")
        filters.pack(fill=tk.X, pady=(0, 10))

        r1 = ttk.Frame(filters)
        r1.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(r1, text=_("Periodo scadenza - Da:")).pack(side=tk.LEFT)
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
        for text, days in [(_("Anno scorso"), -365), (_("6 mesi fa"), -180), (_("Oggi"), 0),
                          (_("+30 gg"), 30), (_("+90 gg"), 90)]:
            self.engine.create_button(r2, text, lambda d=days: self.set_quick_period(d)).pack(side=tk.LEFT, padx=2)

        # Summary metrics
        metrics = ttk.LabelFrame(f0, text=_("Riepilogo"), style="App.TLabelframe")
        metrics.pack(fill=tk.X, pady=(0, 10))

        self.frm_metrics = ttk.Frame(metrics)
        self.frm_metrics.pack(fill=tk.X, padx=10, pady=10)

        # Expired batches tree
        ttk.Label(f0, text=_("Lotti Scaduti (con giacenza residua)"),
                 font=("", 10, "bold")).pack(anchor=tk.W)

        columns = ("product", "supplier", "lot", "expiration", "in_stock", "used", "loss_pct")
        self.tree_expired = ttk.Treeview(f0, columns=columns, show="headings", height=8)

        self.tree_expired.heading("product", text=_("Prodotto"))
        self.tree_expired.heading("supplier", text=_("Fornitore"))
        self.tree_expired.heading("lot", text=_("Lotto"))
        self.tree_expired.heading("expiration", text=_("Scadenza"))
        self.tree_expired.heading("in_stock", text=_("Residuo"))
        self.tree_expired.heading("used", text=_("Usato"))
        self.tree_expired.heading("loss_pct", text="Perdita %")

        self.tree_expired.column("product", width=180)
        self.tree_expired.column("supplier", width=150)
        self.tree_expired.column("lot", width=100)
        self.tree_expired.column("expiration", width=100)
        self.tree_expired.column("in_stock", width=80, anchor=tk.E)
        self.tree_expired.column("used", width=80, anchor=tk.E)
        self.tree_expired.column("loss_pct", width=80, anchor=tk.E)

        self.tree_expired.tag_configure("high_loss", foreground="red")
        self.tree_expired.tag_configure("medium_loss", foreground="orange")

        self.tree_expired.pack(fill=tk.X, pady=5)

        # FEFO efficiency
        ttk.Label(f0, text=_("Efficienza FEFO (First Expired First Out)"),
                 font=("", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))

        columns2 = ("product", "total_labels", "fefo_correct", "fefo_pct")
        self.tree_fefo = ttk.Treeview(f0, columns=columns2, show="headings", height=8)

        self.tree_fefo.heading("product", text=_("Prodotto"))
        self.tree_fefo.heading("total_labels", text=_("Etichette Scaricate"))
        self.tree_fefo.heading("fefo_correct", text=_("FEFO Corrette"))
        self.tree_fefo.heading("fefo_pct", text="Efficienza %")

        self.tree_fefo.column("product", width=250)
        self.tree_fefo.column("total_labels", width=150, anchor=tk.E)
        self.tree_fefo.column("fefo_correct", width=150, anchor=tk.E)
        self.tree_fefo.column("fefo_pct", width=100, anchor=tk.E)

        self.tree_fefo.tag_configure("good", foreground="green")
        self.tree_fefo.tag_configure("warning", foreground="orange")
        self.tree_fefo.tag_configure("bad", foreground="red")

        self.tree_fefo.pack(fill=tk.BOTH, expand=1, pady=5)

        # Buttons
        bf = ttk.Frame(f0)
        bf.pack(fill=tk.X, pady=(10, 0))

        self.engine.create_button(bf, _("Esporta CSV"), self.export_csv, width=12).pack(side=tk.LEFT, padx=5)

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel, width=12).pack(side=tk.RIGHT, padx=5)
        self.bind("<Escape>", lambda e: self.on_cancel())

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Analisi Scadenze"))
        self.engine.dict_instances["stats_expiring"] = self
        self.set_quick_period(0)  # Default: around today

    def set_quick_period(self, days):
        """Set date range for quick period selection."""
        today = datetime.date.today()

        if days <= 0:
            # Past period
            from_date = today + datetime.timedelta(days=days)
            to_date = today
        else:
            # Future period
            from_date = today
            to_date = today + datetime.timedelta(days=days)

        self.cal_from.set_date(from_date)
        self.cal_to.set_date(to_date)
        self.load_data()

    def load_data(self):
        """Load expiration data."""
        # Clear trees
        for item in self.tree_expired.get_children():
            self.tree_expired.delete(item)
        for item in self.tree_fefo.get_children():
            self.tree_fefo.delete(item)

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

        self.load_expired_batches(date_from_str, date_to_str)
        self.load_fefo_analysis()
        self.load_summary_metrics(date_from_str, date_to_str)

    def load_expired_batches(self, date_from, date_to):
        """Load batches that expired with remaining stock."""
        sql = """
            SELECT
                p.description AS product,
                s.description AS supplier,
                b.description AS lot,
                b.expiration,
                SUM(CASE WHEN lb.status = 1 THEN 1 ELSE 0 END) AS in_stock,
                SUM(CASE WHEN lb.status = 0 THEN 1 ELSE 0 END) AS used,
                COUNT(lb.label_id) AS total
            FROM batches b
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
            LEFT JOIN labels lb ON lb.batch_id = b.batch_id
            WHERE b.expiration >= ? AND b.expiration <= ?
            GROUP BY b.batch_id
            HAVING in_stock > 0
            ORDER BY b.expiration ASC
        """

        rs = self.engine.read(True, sql, (date_from, date_to))

        if rs:
            for row in rs:
                in_stock = row["in_stock"] or 0
                used = row["used"] or 0
                total = row["total"] or 0
                loss_pct = round((in_stock / total * 100), 1) if total > 0 else 0

                # Determine tag based on loss percentage
                if loss_pct >= 50:
                    tag = "high_loss"
                elif loss_pct >= 25:
                    tag = "medium_loss"
                else:
                    tag = ""

                # Format expiration date
                exp = row["expiration"] or ""
                if exp and "-" in exp:
                    parts = exp.split("-")
                    if len(parts) == 3:
                        exp = f"{parts[2]}-{parts[1]}-{parts[0]}"

                self.tree_expired.insert("", tk.END, values=(
                    row["product"],
                    row["supplier"] or "",
                    row["lot"],
                    exp,
                    in_stock,
                    used,
                    f"{loss_pct}%"
                ), tags=(tag,) if tag else ())

    def load_fefo_analysis(self):
        """Load FEFO efficiency analysis."""
        # This analyzes if labels were unloaded in order of expiration
        sql = """
            SELECT
                p.description AS product,
                pk.package_id,
                COUNT(lb.label_id) AS total_labels
            FROM labels lb
            JOIN batches b ON b.batch_id = lb.batch_id
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            WHERE lb.status = 0 AND lb.unloaded IS NOT NULL
            GROUP BY pk.package_id
            HAVING total_labels > 1
            ORDER BY total_labels DESC
            LIMIT 20
        """

        rs = self.engine.read(True, sql)

        if rs:
            for row in rs:
                package_id = row["package_id"]

                # Check FEFO compliance: for each unloaded label,
                # was there a label with earlier expiration still in stock at that moment?
                # Simplified: count labels unloaded when older stock existed
                sql2 = """
                    SELECT COUNT(*) AS fefo_violations
                    FROM labels lb1
                    JOIN batches b1 ON b1.batch_id = lb1.batch_id
                    WHERE b1.package_id = ?
                    AND lb1.status = 0
                    AND EXISTS (
                        SELECT 1 FROM labels lb2
                        JOIN batches b2 ON b2.batch_id = lb2.batch_id
                        WHERE b2.package_id = ?
                        AND b2.expiration < b1.expiration
                        AND (lb2.status = 1 OR (lb2.status = 0 AND lb2.unloaded > lb1.unloaded))
                    )
                """
                r2 = self.engine.read(False, sql2, (package_id, package_id))
                violations = r2["fefo_violations"] if r2 else 0

                total = row["total_labels"]
                correct = total - violations
                fefo_pct = round((correct / total * 100), 1) if total > 0 else 100

                # Determine tag
                if fefo_pct >= 90:
                    tag = "good"
                elif fefo_pct >= 70:
                    tag = "warning"
                else:
                    tag = "bad"

                self.tree_fefo.insert("", tk.END, values=(
                    row["product"],
                    total,
                    correct,
                    f"{fefo_pct}%"
                ), tags=(tag,))

    def load_summary_metrics(self, date_from, date_to):
        """Load summary metrics."""
        today = datetime.date.today().isoformat()

        # Total expired batches with stock
        sql = """
            SELECT COUNT(DISTINCT b.batch_id) AS cnt
            FROM batches b
            JOIN labels lb ON lb.batch_id = b.batch_id AND lb.status = 1
            WHERE b.expiration < ?
        """
        row = self.engine.read(False, sql, (today,))
        expired_with_stock = row["cnt"] if row else 0

        # Total expired labels (losses)
        sql = """
            SELECT COUNT(*) AS cnt
            FROM labels lb
            JOIN batches b ON b.batch_id = lb.batch_id
            WHERE lb.status = 1 AND b.expiration < ?
        """
        row = self.engine.read(False, sql, (today,))
        expired_labels = row["cnt"] if row else 0

        # Batches expiring in next 30 days
        in_30 = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
        sql = """
            SELECT COUNT(DISTINCT b.batch_id) AS cnt
            FROM batches b
            JOIN labels lb ON lb.batch_id = b.batch_id AND lb.status = 1
            WHERE b.expiration >= ? AND b.expiration <= ?
        """
        row = self.engine.read(False, sql, (today, in_30))
        expiring_30 = row["cnt"] if row else 0

        # Display metrics
        self._add_metric(_("Lotti scaduti con giacenza:"), expired_with_stock,
                        color="red" if expired_with_stock > 0 else None)
        self._add_metric(_("Etichette scadute (perdite):"), expired_labels,
                        color="red" if expired_labels > 0 else None)
        self._add_metric(_("In scadenza (30 gg):"), expiring_30,
                        color="orange" if expiring_30 > 0 else None)

    def _add_metric(self, label, value, color=None):
        """Add a metric to the metrics frame."""
        frm = ttk.Frame(self.frm_metrics)
        frm.pack(side=tk.LEFT, padx=20)

        ttk.Label(frm, text=label).pack(side=tk.LEFT)
        lbl = ttk.Label(frm, text=str(value), font=("", 11, "bold"))
        if color:
            lbl.configure(foreground=color)
        lbl.pack(side=tk.LEFT, padx=5)

    def export_csv(self):
        """Export data to CSV file."""
        from tkinter import filedialog
        import csv

        filename = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Esporta Scadenze"
        )

        if filename:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")

                # Expired batches
                writer.writerow(["=== Lotti Scaduti ==="])
                writer.writerow(["Prodotto", "Fornitore", "Lotto", "Scadenza",
                               "Residuo", "Usato", "Perdita %"])
                for item in self.tree_expired.get_children():
                    values = self.tree_expired.item(item)["values"]
                    writer.writerow(values)

                writer.writerow([])

                # FEFO analysis
                writer.writerow(["=== Efficienza FEFO ==="])
                writer.writerow(["Prodotto", "Etichette Scaricate", "FEFO Corrette", "Efficienza %"])
                for item in self.tree_fefo.get_children():
                    values = self.tree_fefo.item(item)["values"]
                    writer.writerow(values)

    def on_cancel(self, evt=None):
        """Close the window."""
        if "stats_expiring" in self.engine.dict_instances:
            del self.engine.dict_instances["stats_expiring"]
        self.destroy()
