#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Warehouse View - Stock management for Inventarium.

This module provides the main warehouse interface for viewing and managing
inventory stock, batches, and labels.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView
from views import batch
from views import labels
from views import package_history


class UI(ParentView):
    """
    Warehouse management window.

    Displays products with stock levels, batches with expiration dates,
    and labels (barcodes) for inventory tracking.
    """

    def __init__(self, parent):
        super().__init__(parent, name="warehouse")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(900, 550)

        self.search_var = tk.StringVar()
        self.search_option = tk.IntVar()
        # 0=Stampa, 1=Evadi, 2=Elimina
        self.label_action = tk.IntVar(value=0)
        self.dict_categories = {}
        self.dict_labels = {}  # Maps listbox index to label_id
        self.selected_package_id = None
        self.selected_batch_id = None

        self.init_ui()
        self.engine.center_window(self)
        self.show()

    def init_ui(self):
        """Build the user interface."""

        # Main container
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Categories and Products
        f1 = ttk.Frame(f0, relief=tk.GROOVE, padding=8)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Categories combobox
        w = ttk.LabelFrame(f1, text=_("Categorie"), style="App.TLabelframe")
        self.cbCategories = ttk.Combobox(w, state="readonly", style="App.TCombobox")
        self.cbCategories.bind("<<ComboboxSelected>>", self.on_select_category)
        self.cbCategories.pack(fill=tk.X, expand=1)
        w.pack(side=tk.TOP, fill=tk.X, expand=0)

        # Products Treeview
        self.lbfProducts = ttk.LabelFrame(f1, text=_("Prodotti"), style="App.TLabelframe")

        cols = ("product", "stock")
        self.treeProducts = ttk.Treeview(self.lbfProducts, columns=cols, show="headings", height=12)

        self.treeProducts.column("product", width=250, minwidth=150, anchor=tk.W, stretch=True)
        self.treeProducts.heading("product", text=_("Prodotto"), anchor=tk.W)

        self.treeProducts.column("stock", width=40, minwidth=40, anchor=tk.CENTER, stretch=False)
        self.treeProducts.heading("stock", text=_("G."), anchor=tk.CENTER)

        sb = ttk.Scrollbar(self.lbfProducts, orient=tk.VERTICAL, command=self.treeProducts.yview)
        self.treeProducts.configure(yscrollcommand=sb.set)
        self.treeProducts.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeProducts.bind("<<TreeviewSelect>>", self.on_selected_product)
        self.treeProducts.bind("<Double-1>", self.on_details)

        # Tags for coloring
        self.treeProducts.tag_configure("no_stock", background="light coral")
        self.treeProducts.tag_configure("low_stock", background="khaki")

        self.lbfProducts.pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=5)

        # Center panel - Batches and Labels
        f2 = ttk.Frame(f0, relief=tk.GROOVE, padding=8)
        f2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Batches Treeview
        self.lbfBatches = ttk.LabelFrame(f2, text=_("Lotti"), style="App.TLabelframe")

        cols = ("lot", "expiration", "days")
        self.treeBatches = ttk.Treeview(self.lbfBatches, columns=cols, show="headings", height=8)

        self.treeBatches.column("lot", width=120, minwidth=80, anchor=tk.W, stretch=True)
        self.treeBatches.heading("lot", text=_("Lotto"), anchor=tk.W)

        self.treeBatches.column("expiration", width=90, minwidth=80, anchor=tk.CENTER, stretch=False)
        self.treeBatches.heading("expiration", text=_("Scadenza"), anchor=tk.CENTER)

        self.treeBatches.column("days", width=50, minwidth=40, anchor=tk.CENTER, stretch=False)
        self.treeBatches.heading("days", text=_("GG"), anchor=tk.CENTER)

        sb = ttk.Scrollbar(self.lbfBatches, orient=tk.VERTICAL, command=self.treeBatches.yview)
        self.treeBatches.configure(yscrollcommand=sb.set)
        self.treeBatches.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeBatches.bind("<<TreeviewSelect>>", self.on_selected_batch)
        self.treeBatches.bind("<Double-1>", self.on_activated_batch)

        # Tags for coloring batches
        self.treeBatches.tag_configure("expired", background="coral")
        self.treeBatches.tag_configure("expiring", background="khaki")

        self.lbfBatches.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Labels list
        self.lbfLabels = ttk.LabelFrame(f2, text=_("Etichette"), style="App.TLabelframe")

        sb = ttk.Scrollbar(self.lbfLabels, orient=tk.VERTICAL)
        self.lstLabels = tk.Listbox(
            self.lbfLabels,
            height=8,
            font=("Courier", 9),
            relief=tk.GROOVE,
            selectmode=tk.SINGLE,
            exportselection=0,
            yscrollcommand=sb.set
        )
        sb.config(command=self.lstLabels.yview)
        self.lstLabels.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.lstLabels.bind("<Double-Button-1>", self.on_activated_label)

        self.lbfLabels.pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=5)

        # Right panel - Search and buttons
        f3 = ttk.Frame(f0, relief=tk.GROOVE, padding=8)
        f3.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # Search
        w = ttk.LabelFrame(f3, text=_("Ricerca"), style="App.TLabelframe")
        self.txSearch = ttk.Entry(w, width=15, textvariable=self.search_var)
        self.txSearch.bind("<Return>", self.on_search)
        self.txSearch.pack(fill=tk.X, padx=2, pady=2)

        # Search options
        for idx, text in enumerate((_("Prodotto"), _("Codice"))):
            ttk.Radiobutton(w, text=text, variable=self.search_option,
                            value=idx, style="App.TRadiobutton").pack(anchor=tk.W)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Buttons
        buttons = [
            (_("Aggiorna"), self.on_refresh, "<Alt-a>", 0),
            (_("Dettagli"), self.on_details, "<Alt-d>", 0),
            (_("Storico"), self.on_history, "<Alt-s>", 0),
            (_("Nuovo Lotto"), self.on_new_batch, "<Alt-l>", 6),
            (_("Carica Etichette"), self.on_load_labels, "<Alt-e>", 7),
            (_("Chiudi"), self.on_cancel, "<Alt-c>", 0),
        ]

        for text, cmd, key, ul in buttons:
            self.engine.create_button(f3, text, cmd, underline=ul).pack(fill=tk.X, padx=5, pady=3)
            self.bind(key, lambda e, c=cmd: c())

        # Label action options
        w = ttk.LabelFrame(f3, text=_("Azione etichetta"), style="App.TLabelframe")
        for idx, text in enumerate((_("Stampa"), _("Evadi"), _("Elimina"))):
            ttk.Radiobutton(w, text=text, variable=self.label_action,
                            value=idx, style="App.TRadiobutton").pack(anchor=tk.W)
        w.pack(fill=tk.X, padx=5, pady=5)

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Magazzino"))
        self.engine.dict_instances["warehouse"] = self
        self.set_categories()
        # Don't load all products at startup - wait for category selection
        self.clear_lists()
        self.lbfProducts.config(text=_("Prodotti (selezionare categoria)"))

    def on_refresh(self, evt=None):
        """Refresh lists respecting current category selection."""
        # Get current category selection
        category_idx = self.cbCategories.current()
        if category_idx != -1:
            category_id = self.dict_categories.get(category_idx, 0)
            self.clear_lists()
            self.load_products(category_id=category_id)
        else:
            # No category selected - just clear lists
            self.clear_lists()
            self.lbfProducts.config(text=_("Prodotti (selezionare categoria)"))

    def clear_lists(self):
        """Clear all lists."""
        for item in self.treeProducts.get_children():
            self.treeProducts.delete(item)
        for item in self.treeBatches.get_children():
            self.treeBatches.delete(item)
        self.lstLabels.delete(0, tk.END)
        self.selected_package_id = None
        self.selected_batch_id = None
        self.update_counts()

    def update_counts(self):
        """Update item counts in labels."""
        prod_count = len(self.treeProducts.get_children())
        batch_count = len(self.treeBatches.get_children())
        label_count = self.lstLabels.size()
        self.lbfProducts.config(text=f"{_('Prodotti')} ({prod_count})")
        self.lbfBatches.config(text=f"{_('Lotti')} ({batch_count})")
        self.lbfLabels.config(text=f"{_('Etichette')} ({label_count})")

    def set_categories(self):
        """Load categories into combobox."""
        # Salva la categoria attualmente selezionata PRIMA di svuotare
        current_idx = self.cbCategories.current()
        current_category_id = self.dict_categories.get(current_idx) if current_idx != -1 else None

        self.dict_categories = {}
        voices = []

        sql = """SELECT category_id, description
                 FROM categories
                 WHERE reference_id = 1 AND status = 1
                 ORDER BY description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs):
                self.dict_categories[idx] = row["category_id"]
                voices.append(row["description"])

        # Add "All" option
        self.dict_categories[len(voices)] = 0
        voices.append(_("-- Tutte --"))

        self.cbCategories["values"] = voices

        # Ri-seleziona la stessa categoria (se esiste ancora)
        if current_category_id is not None:
            for idx, cat_id in self.dict_categories.items():
                if cat_id == current_category_id:
                    self.cbCategories.current(idx)
                    break

    def load_products(self, category_id=None, search_term=None):
        """Load products into treeview."""
        for item in self.treeProducts.get_children():
            self.treeProducts.delete(item)
        for item in self.treeBatches.get_children():
            self.treeBatches.delete(item)
        self.lstLabels.delete(0, tk.END)
        self.selected_package_id = None
        self.selected_batch_id = None

        sql = """
            SELECT
                pk.package_id,
                p.description AS product_name,
                p.reference AS product_code,
                pk.packaging,
                pk.reorder,
                s.description AS supplier,
                COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock
            FROM packages pk
            JOIN products p ON p.product_id = pk.product_id
            LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
            LEFT JOIN batches b ON b.package_id = pk.package_id
            LEFT JOIN labels lb ON lb.batch_id = b.batch_id
            WHERE pk.status = 1 AND p.status = 1
        """

        args = []

        if category_id and category_id != 0:
            sql += " AND pk.category_id = ?"
            args.append(category_id)

        if search_term:
            if self.search_option.get() == 0:
                sql += " AND p.description LIKE ?"
            else:
                sql += " AND p.reference LIKE ?"
            args.append(f"%{search_term}%")

        sql += " GROUP BY pk.package_id ORDER BY p.description"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for row in rs:
                package_id = row["package_id"]
                stock = row["in_stock"] or 0
                reorder = row["reorder"] or 0
                product = row["product_name"] or ""

                # Determine tag based on stock vs reorder level
                if stock == 0 and reorder > 0:
                    tag = "no_stock"
                elif stock <= reorder and reorder > 0:
                    tag = "low_stock"
                else:
                    tag = ""

                self.treeProducts.insert(
                    "", tk.END,
                    iid=package_id,
                    values=(product, stock),
                    tags=(tag,) if tag else ()
                )

        self.update_counts()

    def format_date(self, date_str):
        """Convert yyyy-mm-dd to dd-mm-yyyy."""
        if date_str and '-' in date_str:
            parts = date_str.split('-')
            if len(parts) == 3:
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
        return date_str or ""

    def load_batches(self, package_id):
        """Load batches for selected package."""
        for item in self.treeBatches.get_children():
            self.treeBatches.delete(item)
        self.lstLabels.delete(0, tk.END)
        self.selected_batch_id = None

        sql = """
            SELECT
                batch_id,
                description,
                expiration,
                CAST(julianday(expiration) - julianday('now') AS INTEGER) AS days_left
            FROM batches
            WHERE package_id = ? AND status = 1
            ORDER BY expiration
        """

        rs = self.engine.read(True, sql, (package_id,))

        if rs:
            for row in rs:
                batch_id = row["batch_id"]
                days = row["days_left"]
                lot = row["description"] or ""
                exp = self.format_date(row["expiration"])

                # Determine tag based on expiration
                if days is not None:
                    if days < 0:
                        tag = "expired"
                    elif days <= 30:
                        tag = "expiring"
                    else:
                        tag = ""
                else:
                    tag = ""

                days_str = str(days) if days is not None else ""

                self.treeBatches.insert(
                    "", tk.END,
                    iid=batch_id,
                    values=(lot, exp, days_str),
                    tags=(tag,) if tag else ()
                )

        self.update_counts()

    def load_labels(self, batch_id):
        """Load labels for selected batch."""
        self.lstLabels.delete(0, tk.END)
        self.dict_labels.clear()

        sql = """SELECT label_id, tick, status
                 FROM labels
                 WHERE batch_id = ?
                 ORDER BY label_id"""

        rs = self.engine.read(True, sql, (batch_id,))

        if rs:
            for idx, row in enumerate(rs):
                label_id = row["label_id"]
                tick = row["tick"]
                status = row["status"]

                # Map index to label_id for actions
                self.dict_labels[idx] = label_id

                # Display tick if available, otherwise label_id
                display = str(tick) if tick else str(label_id)
                self.lstLabels.insert(tk.END, display)

                # Color by status: 1=active, 0=used, -1=cancelled
                if status == 0:
                    self.lstLabels.itemconfig(idx, bg="light gray")
                elif status == -1:
                    self.lstLabels.itemconfig(idx, bg="light coral")

        self.update_counts()

    # -------------------------------------------------------------------------
    # Event handlers
    # -------------------------------------------------------------------------

    def on_select_category(self, evt=None):
        """Handle category selection."""
        if self.cbCategories.current() != -1:
            idx = self.cbCategories.current()
            category_id = self.dict_categories.get(idx, 0)
            self.load_products(category_id=category_id)

    def on_search(self, evt=None):
        """Handle search."""
        term = self.search_var.get().strip()
        if term:
            self.cbCategories.set("")
            self.load_products(search_term=term)

    def on_selected_product(self, evt=None):
        """Handle product selection - load batches."""
        selection = self.treeProducts.selection()
        if selection:
            package_id = int(selection[0])
            self.selected_package_id = package_id
            self.load_batches(package_id)

    def on_details(self, evt=None):
        """Show details of selected product/package."""
        selection = self.treeProducts.selection()
        if selection:
            package_id = int(selection[0])

            # Get full package details
            sql = """
                SELECT
                    p.description AS product_name,
                    p.reference AS product_code,
                    pk.packaging,
                    s.description AS supplier,
                    c.description AS conservation,
                    cat.description AS category,
                    pk.in_the_dark,
                    COUNT(CASE WHEN lb.status = 1 THEN 1 END) AS in_stock
                FROM packages pk
                JOIN products p ON p.product_id = pk.product_id
                LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
                LEFT JOIN conservations c ON c.conservation_id = pk.conservation_id
                LEFT JOIN categories cat ON cat.category_id = pk.category_id
                LEFT JOIN batches b ON b.package_id = pk.package_id
                LEFT JOIN labels lb ON lb.batch_id = b.batch_id
                WHERE pk.package_id = ?
                GROUP BY pk.package_id
            """
            row = self.engine.read(False, sql, (package_id,))

            if row:
                in_dark = "Sì" if row["in_the_dark"] == 1 else "No"
                msg = (
                    f"Prodotto: {row['product_name'] or '-'}\n"
                    f"Codice: {row['product_code'] or '-'}\n"
                    f"Fornitore: {row['supplier'] or '-'}\n"
                    f"Confezionamento: {row['packaging'] or '-'}\n"
                    f"Conservazione: {row['conservation'] or '-'}\n"
                    f"Al buio: {in_dark}\n"
                    f"Categoria: {row['category'] or '-'}\n"
                    f"Giacenza: {row['in_stock'] or 0}"
                )
                messagebox.showinfo(
                    _("Dettagli Prodotto"),
                    msg,
                    parent=self
                )
        else:
            messagebox.showwarning(
                self.engine.app_title,
                _("Selezionare un prodotto!"),
                parent=self
            )

    def on_history(self, evt=None):
        """Show order history for selected product/package."""
        selection = self.treeProducts.selection()
        if selection:
            package_id = int(selection[0])
            item = self.treeProducts.item(selection[0])
            product_name = item["values"][0]

            obj = package_history.UI(self)
            obj.on_open(package_id, product_name)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                _("Selezionare un prodotto!"),
                parent=self
            )

    def on_selected_batch(self, evt=None):
        """Handle batch selection - load labels."""
        selection = self.treeBatches.selection()
        if selection:
            batch_id = int(selection[0])
            self.selected_batch_id = batch_id
            self.load_labels(batch_id)

    def on_activated_batch(self, evt=None):
        """Handle batch double-click - open edit dialog."""
        selection = self.treeBatches.selection()
        if selection:
            batch_id = int(selection[0])

            # Get batch data
            selected_batch = self.engine.get_selected("batches", "batch_id", batch_id)

            if selected_batch and self.selected_package_id:
                # Get product name from treeview
                prod_selection = self.treeProducts.selection()
                if prod_selection:
                    item = self.treeProducts.item(prod_selection[0])
                    product_name = item["values"][0]
                    selected_package = (self.selected_package_id, product_name)

                    obj = batch.UI(self, index=batch_id)
                    obj.on_open(selected_package, selected_batch)

    def on_activated_label(self, evt=None):
        """Handle label click - action based on radio selection."""
        if self.lstLabels.curselection():
            idx = self.lstLabels.curselection()[0]
            label_id = self.dict_labels.get(idx)
            if not label_id:
                return

            selected_label = self.engine.get_selected("labels", "label_id", label_id)

            if selected_label:
                status = selected_label["status"]
                action = self.label_action.get()

                if action == 0:
                    # Stampa
                    self.on_print_label(label_id)

                elif action == 1:
                    # Evadi (scarica)
                    if status == 1:
                        msg = f"Scaricare l'etichetta {label_id}?"
                        if messagebox.askyesno(self.engine.app_title, msg, parent=self):
                            self.engine.unload_label(label_id)
                            self.load_labels(self.selected_batch_id)
                            self.reposition_label(label_id)
                    elif status == 0:
                        msg = f"Ripristinare l'etichetta {label_id}?"
                        if messagebox.askyesno(self.engine.app_title, msg, parent=self):
                            self.engine.restore_label(label_id)
                            self.load_labels(self.selected_batch_id)
                            self.reposition_label(label_id)
                    elif status == -1:
                        msg = f"Ripristinare l'etichetta annullata {label_id}?"
                        if messagebox.askyesno(self.engine.app_title, msg, parent=self):
                            self.engine.restore_label(label_id)
                            self.load_labels(self.selected_batch_id)
                            self.reposition_label(label_id)

                elif action == 2:
                    # Elimina (annulla)
                    if status == 1:
                        msg = f"Annullare l'etichetta {label_id}?"
                        if messagebox.askyesno(self.engine.app_title, msg, parent=self):
                            self.engine.cancel_label(label_id)
                            self.load_labels(self.selected_batch_id)
                            self.reposition_label(label_id)
                    elif status == -1:
                        msg = f"L'etichetta {label_id} è già annullata.\nRipristinare?"
                        if messagebox.askyesno(self.engine.app_title, msg, parent=self):
                            self.engine.restore_label(label_id)
                            self.load_labels(self.selected_batch_id)
                            self.reposition_label(label_id)
                    else:
                        messagebox.showwarning(
                            self.engine.app_title,
                            f"L'etichetta {label_id} è già stata evasa.\nUsare 'Evadi' per ripristinarla.",
                            parent=self
                        )

    def reposition_label(self, label_id):
        """Reposition listbox selection on the given label_id."""
        for idx, lid in self.dict_labels.items():
            if lid == label_id:
                self.lstLabels.selection_clear(0, tk.END)
                self.lstLabels.selection_set(idx)
                self.lstLabels.see(idx)
                break

    def on_print_label(self, label_id):
        """Print barcode label for the given label_id."""
        if not self.engine.is_printer_enabled():
            messagebox.showinfo(
                self.engine.app_title,
                _("Stampa disabilitata su questa postazione."),
                parent=self
            )
            return

        from barcode_label import BarcodeLabel

        try:
            generator = BarcodeLabel(self.engine)
            path = generator.generate_label(label_id)

            if not path:
                messagebox.showerror(
                    self.engine.app_title,
                    _("Etichetta non trovata!"),
                    parent=self
                )
        except Exception as e:
            messagebox.showerror(
                self.engine.app_title,
                _("Errore nella generazione dell'etichetta:") + f"\n{e}",
                parent=self
            )

    def on_new_batch(self, evt=None):
        """Create new batch for selected product."""
        selection = self.treeProducts.selection()
        if selection:
            package_id = int(selection[0])
            item = self.treeProducts.item(selection[0])
            product_name = item["values"][0]
            selected_package = (package_id, product_name)

            obj = batch.UI(self)
            obj.on_open(selected_package)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                _("Selezionare un prodotto!"),
                parent=self
            )

    def on_load_labels(self, evt=None):
        """Load labels for selected batch."""
        selection = self.treeBatches.selection()
        if selection:
            batch_id = int(selection[0])

            # Get batch data
            selected_batch = self.engine.get_selected("batches", "batch_id", batch_id)

            if selected_batch and self.selected_package_id:
                # Get product name from treeview
                prod_selection = self.treeProducts.selection()
                if prod_selection:
                    item = self.treeProducts.item(prod_selection[0])
                    product_name = item["values"][0]
                    selected_package = (self.selected_package_id, product_name)

                    obj = labels.UI(self)
                    obj.on_open(selected_package, selected_batch)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                _("Selezionare un lotto!"),
                parent=self
            )

    def refresh(self):
        """Public refresh method for external calls."""
        self.refresh_current_selection()

    def refresh_batches(self):
        """Refresh only the batches list for current product selection."""
        if self.selected_package_id:
            batch_id = self.selected_batch_id
            self.load_batches(self.selected_package_id)

            # Re-select the batch if it still exists
            if batch_id:
                for item in self.treeBatches.get_children():
                    if int(item) == batch_id:
                        self.treeBatches.selection_set(item)
                        self.treeBatches.see(item)
                        self.selected_batch_id = batch_id
                        self.load_labels(batch_id)
                        break

    def refresh_current_selection(self):
        """Refresh current selection after label operations."""
        # Save current selection
        package_id = self.selected_package_id
        batch_id = self.selected_batch_id

        # Reload products to update stock count
        category_idx = self.cbCategories.current()
        category_id = self.dict_categories.get(category_idx, 0) if category_idx != -1 else None
        search_term = self.search_var.get().strip() or None

        # Always reload products if a category is selected
        if category_id is not None or search_term:
            self.load_products(category_id=category_id, search_term=search_term)

        # Re-select the product if it was selected
        if package_id:
            for item in self.treeProducts.get_children():
                if int(item) == package_id:
                    self.treeProducts.selection_set(item)
                    self.treeProducts.see(item)
                    self.selected_package_id = package_id
                    self.load_batches(package_id)

                    # Re-select the batch
                    if batch_id:
                        for b_item in self.treeBatches.get_children():
                            if int(b_item) == batch_id:
                                self.treeBatches.selection_set(b_item)
                                self.treeBatches.see(b_item)
                                self.selected_batch_id = batch_id
                                self.load_labels(batch_id)
                                break
                    break

    def on_cancel(self, evt=None):
        """Close the window."""
        if "warehouse" in self.engine.dict_instances:
            del self.engine.dict_instances["warehouse"]
        super().on_cancel()
