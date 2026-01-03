#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics Dashboard - Overview of inventory status for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
import datetime

from i18n import _
from views.parent_view import ParentView


class UI(ParentView):
    """Dashboard with key inventory metrics."""

    def __init__(self, parent):
        super().__init__(parent, name="stats_dashboard")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(700, 500)

        self.init_ui()
        self.engine.center_window(self)
        self.show()


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=10)
        f0.pack(fill=tk.BOTH, expand=1)

        # Title
        title = ttk.Label(f0, text=_("Warehouse Dashboard"), font=("", 14, "bold"))
        title.pack(pady=(0, 15))

        # Metrics frame - 2 columns
        metrics_frame = ttk.Frame(f0)
        metrics_frame.pack(fill=tk.BOTH, expand=1)

        # Left column
        left = ttk.Frame(metrics_frame)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5)

        # Giacenze
        self.frm_stock = ttk.LabelFrame(left, text=_("Stock"), style="App.TLabelframe")
        self.frm_stock.pack(fill=tk.X, pady=5)

        # Sotto soglia
        self.frm_reorder = ttk.LabelFrame(left, text=_("Below Reorder Threshold"), style="App.TLabelframe")
        self.frm_reorder.pack(fill=tk.X, pady=5)

        # Scadenze
        self.frm_expiring = ttk.LabelFrame(left, text=_("Expirations"), style="App.TLabelframe")
        self.frm_expiring.pack(fill=tk.X, pady=5)

        # Right column
        right = ttk.Frame(metrics_frame)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5)

        # Movimenti periodo
        self.frm_movements = ttk.LabelFrame(right, text=_("Movements (last 30 days)"), style="App.TLabelframe")
        self.frm_movements.pack(fill=tk.X, pady=5)

        # Richieste aperte
        self.frm_requests = ttk.LabelFrame(right, text=_("Requests"), style="App.TLabelframe")
        self.frm_requests.pack(fill=tk.X, pady=5)

        # Top prodotti
        self.frm_top = ttk.LabelFrame(right, text=_("Top 5 Consumption (30 days)"), style="App.TLabelframe")
        self.frm_top.pack(fill=tk.BOTH, expand=1, pady=5)

        # Buttons
        bf = ttk.Frame(f0)
        bf.pack(fill=tk.X, pady=(15, 0))

        self.engine.create_button(bf, _("Refresh"), self.load_data, width=12).pack(side=tk.LEFT, padx=5)

        self.engine.create_button(bf, _("Close"), self.on_cancel, width=12).pack(side=tk.RIGHT, padx=5)
        self.bind("<Escape>", lambda e: self.on_cancel())

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Statistics Dashboard"))
        self.engine.dict_instances["stats_dashboard"] = self
        self.load_data()

    def load_data(self):
        """Load all dashboard metrics."""
        self.load_stock_metrics()
        self.load_reorder_metrics()
        self.load_expiring_metrics()
        self.load_movement_metrics()
        self.load_request_metrics()
        self.load_top_consumption()

    def load_stock_metrics(self):
        """Load stock overview metrics."""
        # Clear frame
        for w in self.frm_stock.winfo_children():
            w.destroy()

        # Total products
        sql = "SELECT COUNT(DISTINCT pk.package_id) AS cnt FROM packages pk WHERE pk.status = 1"
        row = self.engine.read(False, sql)
        total_products = row["cnt"] if row else 0

        # Total labels in stock
        sql = "SELECT COUNT(*) AS cnt FROM labels WHERE status = 1"
        row = self.engine.read(False, sql)
        labels_in_stock = row["cnt"] if row else 0

        # Active batches
        sql = "SELECT COUNT(*) AS cnt FROM batches WHERE status = 1"
        row = self.engine.read(False, sql)
        active_batches = row["cnt"] if row else 0

        self._add_metric(self.frm_stock, _("Active products:"), total_products)
        self._add_metric(self.frm_stock, _("Labels in stock:"), labels_in_stock)
        self._add_metric(self.frm_stock, _("Active batches:"), active_batches)

    def load_reorder_metrics(self):
        """Load reorder threshold metrics."""
        for w in self.frm_reorder.winfo_children():
            w.destroy()

        # Products below reorder threshold
        sql = """
            SELECT COUNT(*) AS cnt
            FROM packages pk
            WHERE pk.status = 1 AND pk.reorder > 0
            AND (
                SELECT COUNT(*) FROM labels lb
                JOIN batches b ON b.batch_id = lb.batch_id
                WHERE b.package_id = pk.package_id AND lb.status = 1
            ) <= pk.reorder
        """
        row = self.engine.read(False, sql)
        below_reorder = row["cnt"] if row else 0

        # Products with zero stock
        sql = """
            SELECT COUNT(*) AS cnt
            FROM packages pk
            WHERE pk.status = 1 AND pk.reorder > 0
            AND (
                SELECT COUNT(*) FROM labels lb
                JOIN batches b ON b.batch_id = lb.batch_id
                WHERE b.package_id = pk.package_id AND lb.status = 1
            ) = 0
        """
        row = self.engine.read(False, sql)
        zero_stock = row["cnt"] if row else 0

        self._add_metric(self.frm_reorder, _("Products below threshold:"), below_reorder,
                        color="orange" if below_reorder > 0 else None)
        self._add_metric(self.frm_reorder, _("Out of stock products:"), zero_stock,
                        color="red" if zero_stock > 0 else None)

    def load_expiring_metrics(self):
        """Load expiration metrics."""
        for w in self.frm_expiring.winfo_children():
            w.destroy()

        today = datetime.date.today().isoformat()
        in_30 = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
        in_60 = (datetime.date.today() + datetime.timedelta(days=60)).isoformat()
        in_90 = (datetime.date.today() + datetime.timedelta(days=90)).isoformat()

        # Already expired
        sql = """
            SELECT COUNT(DISTINCT b.batch_id) AS cnt
            FROM batches b
            JOIN labels lb ON lb.batch_id = b.batch_id AND lb.status = 1
            WHERE b.status = 1 AND b.expiration < ?
        """
        row = self.engine.read(False, sql, (today,))
        expired = row["cnt"] if row else 0

        # Expiring in 30 days
        sql = """
            SELECT COUNT(DISTINCT b.batch_id) AS cnt
            FROM batches b
            JOIN labels lb ON lb.batch_id = b.batch_id AND lb.status = 1
            WHERE b.status = 1 AND b.expiration >= ? AND b.expiration <= ?
        """
        row = self.engine.read(False, sql, (today, in_30))
        exp_30 = row["cnt"] if row else 0

        # Expiring in 60 days
        row = self.engine.read(False, sql, (today, in_60))
        exp_60 = row["cnt"] if row else 0

        # Expiring in 90 days
        row = self.engine.read(False, sql, (today, in_90))
        exp_90 = row["cnt"] if row else 0

        self._add_metric(self.frm_expiring, _("Expired batches:"), expired,
                        color="red" if expired > 0 else None)
        self._add_metric(self.frm_expiring, _("Expiring (30 days):"), exp_30,
                        color="orange" if exp_30 > 0 else None)
        self._add_metric(self.frm_expiring, _("Expiring (60 days):"), exp_60)
        self._add_metric(self.frm_expiring, _("Expiring (90 days):"), exp_90)

    def load_movement_metrics(self):
        """Load movement metrics for last 30 days."""
        for w in self.frm_movements.winfo_children():
            w.destroy()

        date_30_ago = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()

        # Labels loaded
        sql = "SELECT COUNT(*) AS cnt FROM labels WHERE loaded >= ?"
        row = self.engine.read(False, sql, (date_30_ago,))
        loaded = row["cnt"] if row else 0

        # Labels unloaded
        sql = "SELECT COUNT(*) AS cnt FROM labels WHERE unloaded >= ? AND status = 0"
        row = self.engine.read(False, sql, (date_30_ago,))
        unloaded = row["cnt"] if row else 0

        # Labels cancelled
        sql = "SELECT COUNT(*) AS cnt FROM labels WHERE status = -1"
        row = self.engine.read(False, sql)
        cancelled = row["cnt"] if row else 0

        self._add_metric(self.frm_movements, _("Labels loaded:"), loaded)
        self._add_metric(self.frm_movements, _("Labels unloaded:"), unloaded)
        self._add_metric(self.frm_movements, _("Labels cancelled:"), cancelled)

    def load_request_metrics(self):
        """Load request metrics."""
        for w in self.frm_requests.winfo_children():
            w.destroy()

        # Open requests
        sql = "SELECT COUNT(*) AS cnt FROM requests WHERE status = 1"
        row = self.engine.read(False, sql)
        open_req = row["cnt"] if row else 0

        # Pending items
        sql = """
            SELECT COUNT(*) AS cnt
            FROM items i
            JOIN requests r ON r.request_id = i.request_id AND r.status = 1
            WHERE i.status = 1
            AND i.quantity > COALESCE(
                (SELECT SUM(d.quantity) FROM deliveries d WHERE d.item_id = i.item_id AND d.status = 1), 0
            )
        """
        row = self.engine.read(False, sql)
        pending_items = row["cnt"] if row else 0

        self._add_metric(self.frm_requests, _("Open requests:"), open_req)
        self._add_metric(self.frm_requests, _("Pending items:"), pending_items)

    def load_top_consumption(self):
        """Load top 5 consumed products in last 30 days."""
        for w in self.frm_top.winfo_children():
            w.destroy()

        date_30_ago = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()

        sql = """
            SELECT p.description AS product, COUNT(lb.label_id) AS consumed
            FROM labels lb
            JOIN batches b ON b.batch_id = lb.batch_id
            JOIN packages pk ON pk.package_id = b.package_id
            JOIN products p ON p.product_id = pk.product_id
            WHERE lb.unloaded >= ? AND lb.status = 0
            GROUP BY pk.package_id
            ORDER BY consumed DESC
            LIMIT 5
        """
        rs = self.engine.read(True, sql, (date_30_ago,))

        if rs:
            for row in rs:
                product = row["product"][:30]
                consumed = row["consumed"]
                self._add_metric(self.frm_top, f"{product}:", consumed)
        else:
            ttk.Label(self.frm_top, text=_("No data available")).pack(anchor=tk.W, padx=10, pady=2)

    def _add_metric(self, parent, label, value, color=None):
        """Add a metric row to the frame."""
        frm = ttk.Frame(parent)
        frm.pack(fill=tk.X, padx=10, pady=2)

        ttk.Label(frm, text=label).pack(side=tk.LEFT)

        lbl_value = ttk.Label(frm, text=str(value), font=("", 10, "bold"))
        if color:
            lbl_value.configure(foreground=color)
        lbl_value.pack(side=tk.RIGHT)

    def on_cancel(self, evt=None):
        """Close the window."""
        if "stats_dashboard" in self.engine.dict_instances:
            del self.engine.dict_instances["stats_dashboard"]
        super().on_cancel()
