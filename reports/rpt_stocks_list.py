#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Report (Compact) - Compact stock list for inventory check.

This module generates a simple text report showing products with their
stock count in a compact table format, suitable for visual inventory checks.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
from reports.rpt_format import Format


class Report(Format):
    """Compact stock list report."""

    def __init__(self, caller):
        super().__init__(caller)

    def init_report(self, rs, category):
        """
        Initialize report data.

        Args:
            rs: List of product records (dict with product_name, product_code, supplier, in_stock)
            category: Category name for the report header
        """
        self.rs = rs
        self.category = category

    def create_doc(self):
        """Build the text document."""
        # Category header
        self.add_line(f"Categoria: {self.category}")
        self.add_line("Tipo: Lista compatta per inventario")
        self.add_separator("=")
        self.add_line()

        # Table header
        self.add_table_row(
            ["Prodotto", "Cod.Fornitore", "Fornitore", "Giac.", "Verif."],
            [30, 15, 18, -5, -8]
        )
        self.add_separator("-")

        # Data rows
        for row in self.rs:
            self.add_table_row(
                [
                    row['product_name'] or '-',
                    row['supplier_code'] or '-',
                    row['supplier'] or '-',
                    row['in_stock'] or 0,
                    "[   ]"
                ],
                [30, 15, 18, -5, -8]
            )

        # Summary
        self.add_separator("=")
        total_products = len(self.rs)
        total_stock = sum(row['in_stock'] or 0 for row in self.rs)

        self.add_line()
        self.add_line(f"Totale prodotti: {total_products}")
        self.add_line(f"Totale giacenza: {total_stock}")
        self.add_line()
        self.add_line("Firma verifica: _______________________")

        self.build_document()
