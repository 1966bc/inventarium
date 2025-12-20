#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Requests List - View and manage purchase requests for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk

from i18n import _
from tkinter import ttk
from tkinter import messagebox

from views import request_item


class UI(tk.Toplevel):
    """Requests list window with detail view."""

    def __init__(self, parent):
        super().__init__(name="requests")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.minsize(700, 500)

        self.table = "requests"
        self.primary_key = "request_id"
        self.obj = None
        self.status = tk.IntVar(value=1)
        self.dict_requests = {}
        self.dict_items = {}
        self.dict_categories = {}
        self.selected_request = None

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Left panel - Lists
        f1 = ttk.Frame(f0)

        # Requests Treeview
        w = ttk.LabelFrame(f1, text=_("Richieste"), style="App.TLabelframe")

        cols = ("reference", "date", "count")
        self.treeRequests = ttk.Treeview(w, columns=cols, show="headings", height=10)

        self.treeRequests.column("reference", width=150, minwidth=100, anchor=tk.W, stretch=True)
        self.treeRequests.heading("reference", text=_("Riferimento"), anchor=tk.W)

        self.treeRequests.column("date", width=90, minwidth=80, anchor=tk.CENTER, stretch=False)
        self.treeRequests.heading("date", text=_("Data"), anchor=tk.CENTER)

        self.treeRequests.column("count", width=50, minwidth=40, anchor=tk.CENTER, stretch=False)
        self.treeRequests.heading("count", text="Art.", anchor=tk.CENTER)

        sb = ttk.Scrollbar(w, orient=tk.VERTICAL, command=self.treeRequests.yview)
        self.treeRequests.configure(yscrollcommand=sb.set)
        self.treeRequests.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeRequests.bind("<<TreeviewSelect>>", self.on_request_selected)
        self.treeRequests.bind("<Double-1>", self.on_add_item)
        self.treeRequests.tag_configure("closed", foreground="gray")

        w.pack(fill=tk.BOTH, expand=1, pady=(0, 5))

        # Items Treeview (detail)
        self.lblItems = ttk.LabelFrame(f1, text=_("Dettaglio Richiesta"), style="App.TLabelframe")

        cols = ("product", "supplier", "packaging", "qty")
        self.treeItems = ttk.Treeview(self.lblItems, columns=cols, show="headings", height=10)

        self.treeItems.column("product", width=180, minwidth=120, anchor=tk.W, stretch=True)
        self.treeItems.heading("product", text=_("Prodotto"), anchor=tk.W)

        self.treeItems.column("supplier", width=100, minwidth=80, anchor=tk.W, stretch=False)
        self.treeItems.heading("supplier", text=_("Fornitore"), anchor=tk.W)

        self.treeItems.column("packaging", width=100, minwidth=80, anchor=tk.W, stretch=False)
        self.treeItems.heading("packaging", text="Conf.", anchor=tk.W)

        self.treeItems.column("qty", width=50, minwidth=40, anchor=tk.CENTER, stretch=False)
        self.treeItems.heading("qty", text="Qtà", anchor=tk.CENTER)

        sb = ttk.Scrollbar(self.lblItems, orient=tk.VERTICAL, command=self.treeItems.yview)
        self.treeItems.configure(yscrollcommand=sb.set)
        self.treeItems.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeItems.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.treeItems.bind("<Double-1>", self.on_edit_item)

        self.lblItems.pack(fill=tk.BOTH, expand=1)

        f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Right panel - Buttons and filters
        f2 = ttk.Frame(f0)

        # Category filter for adding items
        w = ttk.LabelFrame(f2, text=_("Categoria"), style="App.TLabelframe")
        self.cbCategories = ttk.Combobox(w, state="readonly", width=15, style="App.TCombobox")
        self.cbCategories.pack(fill=tk.X, padx=5, pady=5)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Action buttons
        buttons = [
            (_("Nuova Richiesta"), self.on_add, "<Alt-n>", 0),
            (_("Aggiungi Articolo"), self.on_add_item, "<Alt-a>", 0),
            (_("Modifica Articolo"), self.on_edit_item, "<Alt-m>", 0),
            (_("Elimina Articolo"), self.on_delete_item, "<Alt-e>", 0),
            (_("Stampa"), self.on_print, "<Alt-s>", 0),
            (_("Chiudi Richiesta"), self.on_close_request, "<Alt-r>", 7),
            (_("Elimina Richiesta"), self.on_delete_request, "<Alt-x>", 8),
            (_("Aggiorna"), self.on_reset, "<Alt-g>", 1),
            (_("Chiudi"), self.on_cancel, "<Alt-c>", 0),
        ]

        for text, cmd, key, ul in buttons:
            self.engine.create_button(f2, text, cmd, underline=ul).pack(fill=tk.X, padx=5, pady=3)
            self.bind(key, lambda e, c=cmd: c())

        # Status filter
        w = ttk.LabelFrame(f2, text=_("Stato"), style="App.TLabelframe")
        for text, value in ((_("Aperte"), 1), (_("Chiuse"), 0), (_("Tutte"), -1)):
            ttk.Radiobutton(
                w, text=text, variable=self.status,
                value=value,
                command=self.on_reset,
                style="App.TRadiobutton"
            ).pack(anchor=tk.W, padx=5, pady=2)
        w.pack(fill=tk.X, padx=5, pady=5)

        f2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Richieste"))
        self.engine.dict_instances["requests"] = self
        self.set_categories()
        self.on_reset()

    def set_categories(self):
        """Load categories into combobox."""
        self.dict_categories = {}
        voices = []

        # reference_id = 1 is for Products categories
        sql = """SELECT category_id, description
                 FROM categories
                 WHERE reference_id = 1 AND status = 1
                 ORDER BY description"""

        rs = self.engine.read(True, sql)

        if rs:
            for idx, row in enumerate(rs):
                self.dict_categories[idx] = row["category_id"]
                voices.append(row["description"])

        self.cbCategories["values"] = voices
        if voices:
            self.cbCategories.current(0)

    def on_reset(self, evt=None):
        """Reload requests list."""
        # Clear treeviews
        for item in self.treeRequests.get_children():
            self.treeRequests.delete(item)
        for item in self.treeItems.get_children():
            self.treeItems.delete(item)

        self.dict_requests = {}
        self.selected_request = None
        self.lblItems.config(text=_("Dettaglio Richiesta"))

        sql = """
            SELECT
                r.request_id,
                r.reference,
                r.issued,
                COUNT(i.item_id) AS items_count,
                r.status
            FROM requests r
            LEFT JOIN items i ON i.request_id = r.request_id AND i.status = 1
        """

        args = []
        status_val = self.status.get()

        if status_val in (0, 1):
            sql += " WHERE r.status = ?"
            args.append(status_val)

        sql += " GROUP BY r.request_id ORDER BY r.issued DESC, r.request_id DESC"

        rs = self.engine.read(True, sql, tuple(args))

        if rs:
            for row in rs:
                request_id = row["request_id"]
                self.dict_requests[request_id] = row

                # Format date
                issued = row["issued"] or ""
                if issued and "-" in issued:
                    parts = issued.split("-")
                    if len(parts) == 3:
                        issued = f"{parts[2]}-{parts[1]}-{parts[0]}"

                ref = row["reference"] or ""
                count = row["items_count"]

                # Tag for closed requests
                tag = ("closed",) if row["status"] == 0 else ()

                self.treeRequests.insert(
                    "", tk.END,
                    iid=request_id,
                    values=(ref, issued, count),
                    tags=tag
                )

    def on_request_selected(self, evt=None):
        """Handle request selection - load items."""
        selection = self.treeRequests.selection()
        if selection:
            request_id = int(selection[0])
            self.selected_request = self.engine.get_selected(
                self.table, self.primary_key, request_id
            )
            self.set_items(request_id)

    def set_items(self, request_id):
        """Load items for selected request."""
        # Clear items treeview
        for item in self.treeItems.get_children():
            self.treeItems.delete(item)
        self.dict_items = {}

        # Update label
        if self.selected_request:
            ref = self.selected_request.get("reference", "")
            self.lblItems.config(text=f"Dettaglio: {ref}")

        sql = """
            SELECT
                i.item_id,
                p.description AS product,
                s.description AS supplier,
                pk.packaging,
                i.quantity
            FROM items i
            INNER JOIN packages pk ON pk.package_id = i.package_id
            INNER JOIN products p ON p.product_id = pk.product_id
            INNER JOIN suppliers s ON s.supplier_id = pk.supplier_id
            WHERE i.request_id = ?
            AND i.status = 1
            ORDER BY p.description
        """

        rs = self.engine.read(True, sql, (request_id,))

        if rs:
            for row in rs:
                item_id = row["item_id"]
                self.dict_items[item_id] = row

                self.treeItems.insert(
                    "", tk.END,
                    iid=item_id,
                    values=(
                        row["product"] or "",
                        row["supplier"] or "",
                        row["packaging"] or "",
                        row["quantity"]
                    )
                )

    def on_item_selected(self, evt=None):
        """Handle item selection."""
        selection = self.treeItems.selection()
        if selection:
            item_id = int(selection[0])
            self.selected_item = self.engine.get_selected("items", "item_id", item_id)

    def on_add(self, evt=None):
        """Add new request."""
        if not messagebox.askyesno(
            self.engine.app_title,
            _("Generare una nuova richiesta?"),
            parent=self
        ):
            return

        import time

        # Generate unique reference
        reference = str(int(time.time() * 1000000))

        # Get current date
        issued = self.engine.get_date()

        sql = """INSERT INTO requests (reference, issued, status)
                 VALUES (?, ?, 1)"""

        last_id = self.engine.write(sql, (reference, issued))

        if last_id:
            self.on_reset()
            # Find and select the new request
            if str(last_id) in self.treeRequests.get_children():
                self.treeRequests.selection_set(last_id)
                self.treeRequests.see(last_id)
                self.on_request_selected()

    def on_add_item(self, evt=None):
        """Add item to selected request."""
        if self.selected_request is None:
            messagebox.showwarning(
                self.engine.app_title,
                "Selezionare prima una richiesta!",
                parent=self
            )
            return

        if self.selected_request["status"] == 0:
            messagebox.showwarning(
                self.engine.app_title,
                "Impossibile aggiungere articoli.\nLa richiesta è chiusa!",
                parent=self
            )
            return

        # Get selected category
        category_id = None
        if self.cbCategories.current() != -1:
            category_id = self.dict_categories.get(self.cbCategories.current())

        self.obj = request_item.UI(self)
        self.obj.on_open(self.selected_request, category_id=category_id)

    def on_edit_item(self, evt=None):
        """Edit selected item."""
        if self.selected_request is None:
            messagebox.showwarning(
                self.engine.app_title,
                "Selezionare prima una richiesta!",
                parent=self
            )
            return

        if self.selected_request["status"] == 0:
            messagebox.showwarning(
                self.engine.app_title,
                "Impossibile modificare articoli.\nLa richiesta è chiusa!",
                parent=self
            )
            return

        selection = self.treeItems.selection()
        if selection:
            item_id = int(selection[0])
            self.selected_item = self.engine.get_selected("items", "item_id", item_id)
            self.obj = request_item.UI(self, index=item_id)
            self.obj.on_open(self.selected_request, self.selected_item)
        else:
            messagebox.showwarning(
                self.engine.app_title,
                "Selezionare un articolo!",
                parent=self
            )

    def on_delete_item(self, evt=None):
        """Delete selected item."""
        if self.selected_request is None:
            messagebox.showwarning(
                self.engine.app_title,
                "Selezionare prima una richiesta!",
                parent=self
            )
            return

        if self.selected_request["status"] == 0:
            messagebox.showwarning(
                self.engine.app_title,
                "Impossibile eliminare articoli.\nLa richiesta è chiusa!",
                parent=self
            )
            return

        selection = self.treeItems.selection()
        if selection:
            item_id = int(selection[0])

            if messagebox.askyesno(
                self.engine.app_title,
                "Eliminare l'articolo selezionato?",
                parent=self
            ):
                sql = "UPDATE items SET status = 0 WHERE item_id = ?"
                self.engine.write(sql, (item_id,))
                self.set_items(self.selected_request["request_id"])
                # Refresh request list to update count
                self.refresh_request_list()
        else:
            messagebox.showwarning(
                self.engine.app_title,
                "Selezionare un articolo!",
                parent=self
            )

    def refresh_request_list(self):
        """Refresh only the requests list keeping selection."""
        if self.selected_request:
            current_id = self.selected_request["request_id"]
            self.on_reset()
            # Re-select
            if str(current_id) in self.treeRequests.get_children():
                self.treeRequests.selection_set(current_id)
                self.treeRequests.see(current_id)
                self.on_request_selected()

    def on_close_request(self, evt=None):
        """Close selected request (set status=0)."""
        if self.selected_request is None:
            messagebox.showwarning(
                self.engine.app_title,
                "Selezionare prima una richiesta!",
                parent=self
            )
            return

        if self.selected_request["status"] == 0:
            messagebox.showinfo(
                self.engine.app_title,
                "La richiesta è già chiusa!",
                parent=self
            )
            return

        if messagebox.askyesno(
            self.engine.app_title,
            "Chiudere la richiesta selezionata?",
            parent=self
        ):
            pk = self.selected_request["request_id"]

            sql = "UPDATE requests SET status = 0 WHERE request_id = ?"
            self.engine.write(sql, (pk,))

            # Also close all items
            sql = "UPDATE items SET status = 0 WHERE request_id = ?"
            self.engine.write(sql, (pk,))

            self.on_reset()

    def on_delete_request(self, evt=None):
        """Delete selected request and all its items."""
        if self.selected_request is None:
            messagebox.showwarning(
                self.engine.app_title,
                "Selezionare prima una richiesta!",
                parent=self
            )
            return

        ref = self.selected_request.get("reference", "")
        if messagebox.askyesno(
            self.engine.app_title,
            f"Eliminare la richiesta '{ref}' e tutti i suoi articoli?",
            parent=self
        ):
            pk = self.selected_request["request_id"]

            # Delete all items first
            sql = "DELETE FROM items WHERE request_id = ?"
            self.engine.write(sql, (pk,))

            # Delete request
            sql = "DELETE FROM requests WHERE request_id = ?"
            self.engine.write(sql, (pk,))

            self.selected_request = None
            self.on_reset()

    def on_print(self, evt=None):
        """Print selected request."""
        if self.selected_request is None:
            messagebox.showwarning(
                self.engine.app_title,
                "Selezionare prima una richiesta!",
                parent=self
            )
            return

        try:
            from reports import rpt_request

            # Get request data
            request_id = self.selected_request["request_id"]

            # Get items with full details
            sql = """
                SELECT
                    p.description AS product_name,
                    p.reference AS product_ref,
                    SUBSTR(s.description, 1, 15) AS supplier,
                    i.quantity
                FROM items i
                INNER JOIN packages pk ON pk.package_id = i.package_id
                INNER JOIN products p ON p.product_id = pk.product_id
                LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
                WHERE i.request_id = ? AND i.status = 1
                ORDER BY p.description
            """
            items = self.engine.read(True, sql, (request_id,))

            if items:
                report = rpt_request.Report(self)
                report.init_report(self.selected_request, items)
                report.create_doc()
            else:
                messagebox.showinfo(
                    self.engine.app_title,
                    "La richiesta non contiene articoli.",
                    parent=self
                )

        except Exception as e:
            messagebox.showerror(
                self.engine.app_title,
                f"Errore nella generazione del report:\n{e}",
                parent=self
            )

    def on_cancel(self, evt=None):
        """Close the window."""
        if self.obj is not None:
            try:
                self.obj.destroy()
            except:
                pass
        if "requests" in self.engine.dict_instances:
            del self.engine.dict_instances["requests"]
        self.destroy()
