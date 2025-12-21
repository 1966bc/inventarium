#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report Fundings - Report view for package funding sources in Inventarium.

Shows how packages are purchased: funding source, deliberation, supplier.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
import csv
import os

from i18n import _
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


class UI(tk.Toplevel):
    """Report window showing package funding sources."""

    def __init__(self, parent):
        super().__init__(name="report_fundings")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.minsize(1100, 500)

        self.status = tk.IntVar(value=1)
        self.funding_filter = tk.StringVar(value="")
        self.supplier_filter = tk.StringVar(value="")

        self.init_ui()
        self.engine.center_window(self)

    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Report treeview
        f1 = ttk.Frame(f0)

        # Treeview with count
        self.lbf = ttk.LabelFrame(f1, text=f"{_('Totale')}: 0", style="App.TLabelframe")
        w = self.lbf

        cols = ("product", "package", "supplier", "funding", "deliberation", "cig", "valid_from")
        self.treeview = ttk.Treeview(w, columns=cols, show="headings", height=18)

        # Columns
        self.treeview.column("product", width=180, anchor=tk.W)
        self.treeview.heading("product", text=_("Prodotto"), command=lambda: self.sort_column("product"))

        self.treeview.column("package", width=130, anchor=tk.W)
        self.treeview.heading("package", text=_("Confezionamento"), command=lambda: self.sort_column("package"))

        self.treeview.column("supplier", width=150, anchor=tk.W)
        self.treeview.heading("supplier", text=_("Fornitore"), command=lambda: self.sort_column("supplier"))

        self.treeview.column("funding", width=120, anchor=tk.W)
        self.treeview.heading("funding", text=_("Fonte"), command=lambda: self.sort_column("funding"))

        self.treeview.column("deliberation", width=150, anchor=tk.W)
        self.treeview.heading("deliberation", text=_("Delibera"), command=lambda: self.sort_column("deliberation"))

        self.treeview.column("cig", width=120, anchor=tk.W)
        self.treeview.heading("cig", text=_("CIG"), command=lambda: self.sort_column("cig"))

        self.treeview.column("valid_from", width=100, anchor=tk.CENTER)
        self.treeview.heading("valid_from", text=_("Valido dal"), command=lambda: self.sort_column("valid_from"))

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(w, orient=tk.VERTICAL, command=self.treeview.yview)
        scrollbar_x = ttk.Scrollbar(w, orient=tk.HORIZONTAL, command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.treeview.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        w.grid_rowconfigure(0, weight=1)
        w.grid_columnconfigure(0, weight=1)

        # Tags for different funding types
        self.treeview.tag_configure("in_gara", background="#e6ffe6")  # Green - In tender
        self.treeview.tag_configure("economia", background="#fff9e6")  # Yellow - Direct purchase
        self.treeview.tag_configure("inactive", background="light gray")

        w.pack(fill=tk.BOTH, expand=1)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Right panel - Buttons and filters
        f2 = ttk.Frame(f0)

        # Action buttons
        buttons = [
            (_("Aggiorna"), self.on_refresh, "<Alt-a>", 0),
            (_("Esporta CSV"), self.on_export_csv, "<Alt-e>", 0),
            (_("Chiudi"), self.on_cancel, "<Alt-c>", 0),
        ]

        for text, cmd, key, ul in buttons:
            self.engine.create_button(f2, text, cmd, underline=ul).pack(fill=tk.X, padx=5, pady=3)
            self.bind(key, lambda e, c=cmd: c())

        # Funding source filter
        w = ttk.LabelFrame(f2, text=_("Fonte"), style="App.TLabelframe")
        self.cbFundingFilter = ttk.Combobox(w, width=18, state="readonly", textvariable=self.funding_filter)
        self.cbFundingFilter.pack(padx=5, pady=5)
        self.cbFundingFilter.bind("<<ComboboxSelected>>", self.on_refresh)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Supplier filter
        w = ttk.LabelFrame(f2, text=_("Fornitore"), style="App.TLabelframe")
        self.cbSupplierFilter = ttk.Combobox(w, width=18, state="readonly", textvariable=self.supplier_filter)
        self.cbSupplierFilter.pack(padx=5, pady=5)
        self.cbSupplierFilter.bind("<<ComboboxSelected>>", self.on_refresh)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Status filter
        w = ttk.LabelFrame(f2, text=_("Stato"), style="App.TLabelframe")
        for text, value in ((_("Attivi"), 1), (_("Non Attivi"), 0), (_("Tutti"), -1)):
            ttk.Radiobutton(
                w, text=text, variable=self.status,
                value=value,
                command=self.on_refresh,
                style="App.TRadiobutton"
            ).pack(anchor=tk.W, padx=5, pady=2)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Legend
        w = ttk.LabelFrame(f2, text=_("Legenda"), style="App.TLabelframe")

        f_leg1 = tk.Frame(w)
        f_leg1.pack(fill=tk.X, padx=5, pady=2)
        tk.Frame(f_leg1, bg="#e6ffe6", height=15, width=15).pack(side=tk.LEFT)
        ttk.Label(f_leg1, text=_("In Gara"), style="App.TLabel").pack(side=tk.LEFT, padx=5)

        f_leg2 = tk.Frame(w)
        f_leg2.pack(fill=tk.X, padx=5, pady=2)
        tk.Frame(f_leg2, bg="#fff9e6", height=15, width=15).pack(side=tk.LEFT)
        ttk.Label(f_leg2, text=_("Economia"), style="App.TLabel").pack(side=tk.LEFT, padx=5)

        w.pack(fill=tk.X, padx=5, pady=5)

        # Summary
        self.lbfSummary = ttk.LabelFrame(f2, text=_("Riepilogo"), style="App.TLabelframe")
        self.lblInGara = ttk.Label(self.lbfSummary, text="In Gara: 0", style="App.TLabel")
        self.lblInGara.pack(anchor=tk.W, padx=5, pady=2)
        self.lblEconomia = ttk.Label(self.lbfSummary, text="Economia: 0", style="App.TLabel")
        self.lblEconomia.pack(anchor=tk.W, padx=5, pady=2)
        self.lbfSummary.pack(fill=tk.X, padx=5, pady=5)

        f2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    def load_filters(self):
        """Load filter comboboxes."""
        # Load funding sources
        sql = "SELECT funding_id, description FROM funding_sources WHERE status = 1 ORDER BY description"
        rs = self.engine.read(True, sql)

        self.fundings_filter = {_("Tutti"): None}
        values = [_("Tutti")]

        if rs:
            for row in rs:
                self.fundings_filter[row["description"]] = row["funding_id"]
                values.append(row["description"])

        self.cbFundingFilter["values"] = values
        self.cbFundingFilter.set(_("Tutti"))

        # Load suppliers
        sql = "SELECT supplier_id, description FROM suppliers WHERE status = 1 ORDER BY description"
        rs = self.engine.read(True, sql)

        self.suppliers_filter = {_("Tutti"): None}
        values = [_("Tutti")]

        if rs:
            for row in rs:
                self.suppliers_filter[row["description"]] = row["supplier_id"]
                values.append(row["description"])

        self.cbSupplierFilter["values"] = values
        self.cbSupplierFilter.set(_("Tutti"))

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Report Fonti Finanziamento"))
        self.engine.dict_instances["report_fundings"] = self
        self.load_filters()
        self.on_refresh()

    def on_refresh(self, evt=None):
        """Reload report data."""
        self.load_data()

    def load_data(self):
        """Load report data with current filters."""
        # Clear treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        sql = """SELECT p.description AS product,
                        pk.packaging,
                        s.description AS supplier,
                        fs.description AS funding,
                        d.reference AS deliberation,
                        d.cig,
                        pf.valid_from,
                        pf.status,
                        pf.deliberation_id,
                        pf.funding_id,
                        pk.supplier_id
                 FROM package_fundings pf
                 JOIN packages pk ON pk.package_id = pf.package_id
                 JOIN products p ON p.product_id = pk.product_id
                 JOIN suppliers s ON s.supplier_id = pk.supplier_id
                 JOIN funding_sources fs ON fs.funding_id = pf.funding_id
                 LEFT JOIN deliberations d ON d.deliberation_id = pf.deliberation_id
                 WHERE 1=1"""

        args = []
        status_val = self.status.get()

        if status_val in (0, 1):
            sql += " AND pf.status = ?"
            args.append(status_val)

        # Funding filter
        funding_name = self.cbFundingFilter.get()
        funding_id = self.fundings_filter.get(funding_name)
        if funding_id:
            sql += " AND pf.funding_id = ?"
            args.append(funding_id)

        # Supplier filter
        supplier_name = self.cbSupplierFilter.get()
        supplier_id = self.suppliers_filter.get(supplier_name)
        if supplier_id:
            sql += " AND pk.supplier_id = ?"
            args.append(supplier_id)

        sql += " ORDER BY p.description, pk.packaging"

        rs = self.engine.read(True, sql, tuple(args))

        count_gara = 0
        count_economia = 0

        if rs:
            for row in rs:
                tags = []
                if row["status"] != 1:
                    tags.append("inactive")
                elif row["deliberation_id"]:
                    tags.append("in_gara")
                    count_gara += 1
                else:
                    tags.append("economia")
                    count_economia += 1

                deliberation_text = row["deliberation"] or _("Economia")

                self.treeview.insert("", tk.END, values=(
                    row["product"] or "",
                    row["packaging"] or "",
                    row["supplier"] or "",
                    row["funding"] or "",
                    deliberation_text,
                    row["cig"] or "",
                    row["valid_from"] or ""
                ), tags=tuple(tags) if tags else ())

        total = len(self.treeview.get_children())
        self.lbf.config(text=f"{_('Totale')}: {total}")
        self.lblInGara.config(text=f"{_('In Gara')}: {count_gara}")
        self.lblEconomia.config(text=f"{_('Economia')}: {count_economia}")

    def sort_column(self, col):
        """Sort treeview by column."""
        items = [(self.treeview.set(k, col), k) for k in self.treeview.get_children("")]
        items.sort()

        for index, (val, k) in enumerate(items):
            self.treeview.move(k, "", index)

    def on_export_csv(self, evt=None):
        """Export report to CSV file."""
        if not self.treeview.get_children():
            messagebox.showwarning(
                self.engine.app_title,
                _("Nessun dato da esportare!"),
                parent=self
            )
            return

        filename = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="report_fonti.csv",
            title=_("Esporta CSV")
        )

        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=';')

                    # Header
                    writer.writerow([
                        _("Prodotto"),
                        _("Confezionamento"),
                        _("Fornitore"),
                        _("Fonte"),
                        _("Delibera"),
                        _("CIG"),
                        _("Valido dal")
                    ])

                    # Data
                    for item in self.treeview.get_children():
                        values = self.treeview.item(item, "values")
                        writer.writerow(values)

                messagebox.showinfo(
                    self.engine.app_title,
                    f"{_('File esportato')}: {filename}",
                    parent=self
                )

                # Open file location
                if os.name == 'nt':
                    os.startfile(os.path.dirname(filename))
                else:
                    import subprocess
                    subprocess.run(['xdg-open', os.path.dirname(filename)])

            except Exception as e:
                messagebox.showerror(
                    self.engine.app_title,
                    _("Errore durante esportazione") + f": {e}",
                    parent=self
                )

    def on_cancel(self, evt=None):
        """Close the window."""
        if "report_fundings" in self.engine.dict_instances:
            del self.engine.dict_instances["report_fundings"]
        self.destroy()
