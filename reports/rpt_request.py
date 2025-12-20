#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Request Report - Purchase request report for email attachment.

This module generates a text report for a purchase request,
suitable for sending to suppliers via email.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
from reports.rpt_format import Format


class Report(Format):
    """Purchase request report."""

    def __init__(self, caller):
        super().__init__(caller)

    def init_report(self, request, items):
        """
        Initialize report data.

        Args:
            request: Dict with request header data
            items: List of item records
        """
        self.request = request
        self.items = items

    def format_date(self, date_str):
        """Convert yyyy-mm-dd to dd-mm-yyyy."""
        if date_str and '-' in date_str:
            parts = date_str.split('-')
            if len(parts) == 3:
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
        return date_str or ""

    def create_doc(self):
        """Build the text document."""
        # Request header
        self.add_line("RICHIESTA MATERIALI")
        self.add_separator("=")
        self.add_line()

        self.add_line(f"Riferimento:  {self.request.get('reference', '-')}")
        self.add_line(f"Data:         {self.format_date(self.request.get('issued', ''))}")
        if self.request.get('supplier'):
            self.add_line(f"Fornitore:    {self.request.get('supplier', '-')}")
        self.add_line()
        self.add_separator("-")
        self.add_line()

        # Items table header
        self.add_table_row(
            ["#", "Codice", "Prodotto", "Produttore", "Q.tà"],
            [-3, 12, 40, 15, -5]
        )
        self.add_separator("-")

        # Items
        total_qty = 0
        for idx, item in enumerate(self.items, start=1):
            self.add_table_row(
                [
                    idx,
                    item.get('product_ref', '-'),
                    item.get('product_name', '-'),
                    item.get('supplier', '-'),
                    item.get('quantity', 0)
                ],
                [-3, 12, 40, 15, -5]
            )
            total_qty += item.get('quantity', 0) or 0

        # Footer
        self.add_separator("=")
        self.add_line()
        self.add_line(f"Totale articoli: {len(self.items)}")
        #self.add_line(f"Totale quantità: {total_qty}")
        self.add_line()

        if self.request.get('note'):
            self.add_line("Note:")
            self.add_line(self.request.get('note', ''))
            self.add_line()

        self.add_separator("-")
        self.add_line()
        
        manager = self.engine.get_setting("lab_manager", "")
        self.add_line("Il Responsabile")
        self.add_line()
        if manager:
            self.add_line(manager)
        else:
            self.add_line("_______________________")
        self.build_document()
