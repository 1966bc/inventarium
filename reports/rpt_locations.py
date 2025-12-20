#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Location Report - Stock report organized by location.

This module generates text reports organized by location (room/shelf),
useful for inventory checks and for posting on location (required by law).

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
from reports.rpt_format import Format


class Report(Format):
    """Location-based stock report."""

    def __init__(self, caller):
        super().__init__(caller)

    def init_report(self, rs, location_name, show_stock=True):
        """
        Initialize report data.

        Args:
            rs: List of product records for the location
            location_name: Name of the location
            show_stock: If True, show stock quantities; if False, just product list
        """
        self.rs = rs
        self.location_name = location_name
        self.show_stock = show_stock

    def create_doc(self):
        """Build the text document."""
        # Location header
        self.add_separator("*")
        self.add_line(f"UBICAZIONE: {self.location_name}")
        self.add_separator("*")
        self.add_line()

        if self.show_stock:
            self.add_line("INVENTARIO")
        else:
            self.add_line("ELENCO PRODOTTI")
            self.add_line("(Da affiggere in loco)")
        self.add_separator("-")
        self.add_line()

        # Table header
        if self.show_stock:
            self.add_table_row(
                ["Prodotto", "Cod.Fornitore", "Confez.", "Giac."],
                [35, 15, 18, -5]
            )
        else:
            self.add_table_row(
                ["Prodotto", "Cod.Fornitore", "Confezionamento"],
                [35, 15, 25]
            )
        self.add_line("-" * 75)

        # Product rows
        for row in self.rs:
            if self.show_stock:
                self.add_table_row(
                    [
                        row['product_name'] or '-',
                        row['supplier_code'] or '-',
                        row['packaging'] or '-',
                        row['in_stock'] or 0
                    ],
                    [35, 15, 18, -5]
                )
            else:
                self.add_table_row(
                    [
                        row['product_name'] or '-',
                        row['supplier_code'] or '-',
                        row['packaging'] or '-'
                    ],
                    [35, 15, 25]
                )

        # Footer
        self.add_line()
        self.add_separator("=")

        manager = self.engine.get_setting("lab_manager", "")

        if self.show_stock:
            total_stock = sum(row['in_stock'] or 0 for row in self.rs)
            self.add_line(f"Totale prodotti: {len(self.rs)}")
            self.add_line(f"Totale giacenza: {total_stock}")
            self.add_line()
            self.add_line("Firma verifica: _______________________")
        else:
            self.add_line(f"Totale prodotti: {len(self.rs)}")
            self.add_line()
            self.add_line(f"Data aggiornamento: {self.today.strftime('%d-%m-%Y')}")
            self.add_line()
            if manager:
                self.add_line(f"Il Responsabile: {manager}")
            else:
                self.add_line("Il Responsabile: _______________________")

        self.build_document()
