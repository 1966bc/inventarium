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
            show_stock: If True, show stock grouped by shelf; 
                       if False, show product list with shelf column
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
            self._create_inventory_report()
        else:
            self._create_posting_report()

        self.build_document()

    def _create_inventory_report(self):
        """Create inventory report grouped by shelf."""
        self.add_line("INVENTARIO")
        self.add_separator("-")
        self.add_line()

        # Group by shelf
        shelves = {}
        for row in self.rs:
            shelf = row.get('shelf') or 'N/D'
            if shelf not in shelves:
                shelves[shelf] = []
            shelves[shelf].append(row)

        # Sort shelves (N/D last)
        shelf_keys = sorted(
            shelves.keys(),
            key=lambda x: (x == 'N/D', x)
        )

        total_stock = 0

        for shelf in shelf_keys:
            rows = shelves[shelf]
            
            # Shelf header
            self.add_line(f"--- RIPIANO {shelf} ---")
            self.add_line()
            
            # Table header
            self.add_table_row(
                ["Prodotto", "Cod.Fornitore", "Confez.", "Giac."],
                [35, 15, 18, -5]
            )
            self.add_line("-" * 75)

            # Product rows
            shelf_stock = 0
            for row in rows:
                stock = row.get('in_stock') or 0
                shelf_stock += stock
                self.add_table_row(
                    [
                        row.get('product_name') or '-',
                        row.get('supplier_code') or '-',
                        row.get('packaging') or '-',
                        stock
                    ],
                    [35, 15, 18, -5]
                )

            # Shelf subtotal
            self.add_line()
            self.add_line(f"Subtotale ripiano {shelf}: {len(rows)} prodotti, {shelf_stock} pezzi")
            self.add_line()
            total_stock += shelf_stock

        # Footer
        self.add_separator("=")
        self.add_line(f"Totale prodotti: {len(self.rs)}")
        self.add_line(f"Totale giacenza: {total_stock}")
        self.add_line()
        self.add_line("Firma verifica: _______________________")

    def _create_posting_report(self):
        """Create product list for posting on location."""
        self.add_line("ELENCO PRODOTTI")
        self.add_line("(Da affiggere in loco)")
        self.add_separator("-")
        self.add_line()

        # Table header with shelf column
        self.add_table_row(
            ["Prodotto", "Cod.Fornitore", "Confez.", "Rip."],
            [32, 15, 18, -6]
        )
        self.add_line("-" * 75)

        # Sort by shelf then product name
        sorted_rs = sorted(
            self.rs,
            key=lambda x: (
                x.get('shelf') or 'ZZZ',  # N/D last
                x.get('product_name') or ''
            )
        )

        # Product rows
        for row in sorted_rs:
            self.add_table_row(
                [
                    row.get('product_name') or '-',
                    row.get('supplier_code') or '-',
                    row.get('packaging') or '-',
                    row.get('shelf') or '-'
                ],
                [32, 15, 18, -6]
            )

        # Footer
        self.add_line()
        self.add_separator("=")
        self.add_line(f"Totale prodotti: {len(self.rs)}")
        self.add_line()
        self.add_line(f"Data aggiornamento: {self.today.strftime('%d-%m-%Y')}")
        self.add_line()

        manager = self.engine.get_setting("lab_manager", "")
        if manager:
            self.add_line(f"Il Responsabile: {manager}")
        else:
            self.add_line("Il Responsabile: _______________________")
