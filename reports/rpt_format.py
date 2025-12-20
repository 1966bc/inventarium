#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report Format Base - Base class for text reports in Inventarium.

This module provides the base formatting class for generating plain text reports.
Vintage style, no dependencies!

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import os
import sys
import inspect
import datetime
import tempfile
import subprocess
import platform


class Format:
    """Base class for text report generation."""

    def __init__(self, caller):
        self.caller = caller
        self.engine = caller.engine
        self.today = datetime.date.today()
        self.lines = []
        self.width = 80  # Default report width

        # Add header
        self.add_header()

    def add_header(self):
        """Add report header with company/lab info."""
        self.lines.append("=" * self.width)

        # Company name
        company = self.engine.get_setting("company_name", "")
        if company:
            self.lines.append(self.center_text(company))

        # Lab name
        lab = self.engine.get_setting("lab_name", "")
        if lab:
            self.lines.append(self.center_text(lab))

        # Room/Location
        room = self.engine.get_setting("lab_room", "")
        if room:
            self.lines.append(self.center_text(room))

        self.lines.append("=" * self.width)
        self.lines.append(self.center_text(f"Data: {self.today.strftime('%d-%m-%Y')}"))
        self.lines.append("")

    def center_text(self, text):
        """Center text within report width."""
        return text.center(self.width)

    def add_line(self, text=""):
        """Add a line to the report."""
        self.lines.append(text)

    def add_separator(self, char="-"):
        """Add a separator line."""
        self.lines.append(char * self.width)

    def add_table_row(self, columns, widths):
        """
        Add a formatted table row.

        Args:
            columns: List of column values
            widths: List of column widths (positive=left align, negative=right align)
        """
        parts = []
        for col, w in zip(columns, widths):
            text = str(col) if col is not None else ""
            if w < 0:
                # Right align
                parts.append(text[:abs(w)].rjust(abs(w)))
            else:
                # Left align
                parts.append(text[:w].ljust(w))
        self.lines.append(" ".join(parts))

    def build_document(self):
        """Build and open the text document."""
        filename = tempfile.mktemp(".txt")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("\n".join(self.lines))

            self.open_file(filename)

        except Exception as e:
            self.engine.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__]
            )

    def open_file(self, filename):
        """Open file with system default application."""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', filename))
            elif platform.system() == 'Windows':
                os.startfile(filename)
            else:  # Linux
                subprocess.call(('xdg-open', filename))
        except Exception as e:
            self.engine.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__]
            )
