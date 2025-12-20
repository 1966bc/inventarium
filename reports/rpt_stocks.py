#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Report (Detailed) - Detailed stock report with batches and labels.

This module generates a detailed text report showing products with their
batches, expiration dates, and labels. Expired/expiring items are marked.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
from reports.rpt_format import Format


# Query to get batches for a package
SQL_BATCHES = """
    SELECT
        b.description AS lot,
        CAST(julianday(b.expiration) - julianday('now') AS INTEGER) AS days_left,
        b.expiration,
        lb.label_id
    FROM batches b
    INNER JOIN labels lb ON lb.batch_id = b.batch_id
    WHERE b.package_id = ?
    AND b.status = 1
    AND lb.status = 1
    ORDER BY days_left ASC
"""


class Report(Format):
    """Detailed stock report with batches."""

    def __init__(self, caller):
        super().__init__(caller)

    def init_report(self, rs, category):
        """
        Initialize report data.

        Args:
            rs: List of product records (dict with package_id, product_name, etc.)
            category: Category name for the report header
        """
        self.rs = rs
        self.category = category

    def format_expiration(self, exp):
        """Convert yyyy-mm-dd to dd-mm-yyyy."""
        if exp and '-' in exp:
            parts = exp.split('-')
            if len(parts) == 3:
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
        return exp or ""

    def get_status_marker(self, days):
        """Get status marker based on days to expiration."""
        if days is None:
            return " "
        if days < 0:
            return "!"  # Expired
        if days <= 30:
            return "*"  # Expiring soon
        return " "

    def create_doc(self):
        """Build the text document."""
        # Category header
        self.add_line(f"Categoria: {self.category}")
        self.add_separator("=")
        self.add_line()

        # Legend
        self.add_line("Legenda: ! = SCADUTO   * = In scadenza (< 30 gg)")
        self.add_separator("-")
        self.add_line()

        # Products with batches
        for row in self.rs:
            # Product info
            self.add_line(f"Prodotto:       {row['product_name'] or '-'}")
            self.add_line(f"Cod.Fornitore:  {row['supplier_code'] or '-'}")
            self.add_line(f"Fornitore:      {row['supplier'] or '-'}")
            self.add_line(f"Confezionamento:{row['packaging'] or '-'}")
            self.add_line(f"Giacenza:       {row['in_stock'] or 0}")
            self.add_line()

            # Get batches for this package
            batches = self.engine.read(True, SQL_BATCHES, (row['package_id'],))

            if batches:
                # Batch table header
                self.add_table_row(
                    ["", "Lotto", "Giorni", "Scadenza", "Etichetta"],
                    [1, 20, -6, 12, -10]
                )
                self.add_line("-" * 52)

                for batch in batches:
                    marker = self.get_status_marker(batch['days_left'])
                    exp = self.format_expiration(batch['expiration'])
                    days = batch['days_left'] if batch['days_left'] is not None else ""

                    self.add_table_row(
                        [marker, batch['lot'] or "", days, exp, batch['label_id'] or ""],
                        [1, 20, -6, 12, -10]
                    )

            self.add_line()
            self.add_separator("-")
            self.add_line()

        # Footer
        self.add_line()
        self.add_line(f"Totale prodotti: {len(self.rs)}")

        self.build_document()
