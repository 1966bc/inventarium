#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Delivery View - Manage deliveries for purchase requests in Inventarium.

This module handles the "evasione" (fulfillment) of purchase requests,
creating delivery records, batches, and labels when goods arrive.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import sys
import inspect
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _
from views.parent_view import ParentView
from calendarium import Calendarium


class UI(ParentView):
    """Deliveries management window for fulfilling purchase requests."""

    def __init__(self, parent):
        super().__init__(parent, name="deliveries")

        if self._reusing:
            return

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.minsize(900, 600)

        # State variables
        self.batch_mode = tk.IntVar(value=0)  # 0=select existing, 1=create new
        self.quantity = tk.IntVar(value=1)
        self.labels_count = tk.IntVar(value=1)  # Numero etichette da creare
        self.ddt = tk.StringVar()
        self.new_lot = tk.StringVar()
        self.print_labels_var = tk.IntVar(value=1)  # 1=stampa automatica attiva

        # Display variables (readonly)
        self.product_name = tk.StringVar()
        self.supplier_name = tk.StringVar()
        self.packaging = tk.StringVar()
        self.ordered_qty = tk.StringVar()
        self.delivered_qty = tk.StringVar()

        # Dictionaries for ID mappings
        self.dict_requests = {}
        self.dict_items = {}
        self.dict_batches = {}

        # Selected records
        self.selected_request = None
        self.selected_item = None

        self.init_ui()
        self.engine.center_window(self)
        self.show()


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=8)
        f0.pack(fill=tk.BOTH, expand=1)

        # Column 3 - Buttons (fixed, pack first)
        f3 = ttk.Frame(f0)
        f3.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # PanedWindow for resizable panels
        paned = ttk.PanedWindow(f0, orient=tk.HORIZONTAL)
        paned.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, pady=5)

        # Column 1 - Lists (two treeviews stacked)
        f1 = ttk.Frame(paned)
        paned.add(f1, weight=1)

        # Requests Treeview
        w = ttk.LabelFrame(f1, text=_("Richieste Aperte"), style="App.TLabelframe")

        cols = ("reference", "date", "pending")
        self.treeRequests = ttk.Treeview(w, columns=cols, show="headings", height=12)

        self.treeRequests.column("reference", width=120, minwidth=100, anchor=tk.W, stretch=True)
        self.treeRequests.heading("reference", text=_("Riferimento"), anchor=tk.W)

        self.treeRequests.column("date", width=90, minwidth=80, anchor=tk.CENTER, stretch=False)
        self.treeRequests.heading("date", text=_("Data"), anchor=tk.CENTER)

        self.treeRequests.column("pending", width=40, minwidth=30, anchor=tk.CENTER, stretch=False)
        self.treeRequests.heading("pending", text="P.", anchor=tk.CENTER)

        sb = ttk.Scrollbar(w, orient=tk.VERTICAL, command=self.treeRequests.yview)
        self.treeRequests.configure(yscrollcommand=sb.set)
        self.treeRequests.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeRequests.tag_configure("sent", foreground="blue")

        self.treeRequests.bind("<<TreeviewSelect>>", self.on_request_selected)

        w.pack(fill=tk.BOTH, expand=1, pady=(0, 5))

        # Items Treeview
        self.lbfItems = ttk.LabelFrame(f1, text=_("Articoli da Evadere"), style="App.TLabelframe")

        cols = ("product", "ordered", "delivered")
        self.treeItems = ttk.Treeview(self.lbfItems, columns=cols, show="headings", height=12)

        self.treeItems.column("product", width=150, minwidth=100, anchor=tk.W, stretch=True)
        self.treeItems.heading("product", text=_("Prodotto"), anchor=tk.W)

        self.treeItems.column("ordered", width=40, minwidth=30, anchor=tk.CENTER, stretch=False)
        self.treeItems.heading("ordered", text="O.", anchor=tk.CENTER)

        self.treeItems.column("delivered", width=40, minwidth=30, anchor=tk.CENTER, stretch=False)
        self.treeItems.heading("delivered", text="E.", anchor=tk.CENTER)

        sb = ttk.Scrollbar(self.lbfItems, orient=tk.VERTICAL, command=self.treeItems.yview)
        self.treeItems.configure(yscrollcommand=sb.set)
        self.treeItems.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeItems.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.treeItems.tag_configure("completed", foreground="gray", background="light gray")

        self.lbfItems.pack(fill=tk.BOTH, expand=1)

        # Column 2 - Forms (three LabelFrames stacked)
        f2 = ttk.Frame(paned)
        paned.add(f2, weight=0)

        # Item details (readonly)
        w = ttk.LabelFrame(f2, text=_("Dettaglio Articolo"), style="App.TLabelframe")
        r = 0
        ttk.Label(w, text=_("Prodotto:")).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(w, textvariable=self.product_name, state="readonly", width=25).grid(
            row=r, column=1, sticky=tk.W, padx=5, pady=2
        )
        r += 1
        ttk.Label(w, text=_("Fornitore:")).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(w, textvariable=self.supplier_name, state="readonly", width=25).grid(
            row=r, column=1, sticky=tk.W, padx=5, pady=2
        )
        r += 1
        ttk.Label(w, text=_("Confezionamento:")).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(w, textvariable=self.packaging, state="readonly", width=25).grid(
            row=r, column=1, sticky=tk.W, padx=5, pady=2
        )
        r += 1
        ttk.Label(w, text=_("Ordinato:")).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(w, textvariable=self.ordered_qty, state="readonly", width=10).grid(
            row=r, column=1, sticky=tk.W, padx=5, pady=2
        )
        r += 1
        ttk.Label(w, text=_("Già Evaso:")).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(w, textvariable=self.delivered_qty, state="readonly", width=10).grid(
            row=r, column=1, sticky=tk.W, padx=5, pady=2
        )
        w.pack(fill=tk.X, padx=5, pady=5)

        # Delivery form
        w = ttk.LabelFrame(f2, text=_("Nuova Consegna"), style="App.TLabelframe")
        r = 0
        ttk.Label(w, text=_("DDT:")).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(w, textvariable=self.ddt, width=15).grid(
            row=r, column=1, sticky=tk.W, padx=5, pady=2
        )
        r += 1
        ttk.Label(w, text=_("Data Consegna:")).grid(row=r, column=0, sticky=tk.NW, padx=5, pady=2)
        self.cal_delivered = Calendarium(w, "")
        self.cal_delivered.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        r += 1
        ttk.Label(w, text=_("Quantità:")).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        vcmd = self.engine.get_validate_integer(self)
        self.txt_quantity = ttk.Entry(
            w, textvariable=self.quantity, width=10,
            validate="key", validatecommand=vcmd
        )
        self.txt_quantity.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        # Auto-update labels count when quantity changes
        self.quantity.trace_add("write", self.on_quantity_changed)
        r += 1
        ttk.Label(w, text=_("Etichette:")).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        self.txt_labels = ttk.Entry(
            w, textvariable=self.labels_count, width=10,
            validate="key", validatecommand=vcmd
        )
        self.txt_labels.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Batch selection
        w = ttk.LabelFrame(f2, text=_("Lotto"), style="App.TLabelframe")
        r = 0
        ttk.Radiobutton(
            w, text=_("Seleziona esistente:"),
            variable=self.batch_mode, value=0,
            command=self.on_batch_mode_changed,
            style="App.TRadiobutton"
        ).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        self.cb_batches = ttk.Combobox(w, state="readonly", width=25, style="App.TCombobox")
        self.cb_batches.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        r += 1
        ttk.Radiobutton(
            w, text=_("Crea nuovo:"),
            variable=self.batch_mode, value=1,
            command=self.on_batch_mode_changed,
            style="App.TRadiobutton"
        ).grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
        r += 1
        ttk.Label(w, text=_("Lotto:")).grid(row=r, column=0, sticky=tk.E, padx=5, pady=2)
        self.txt_new_lot = ttk.Entry(w, textvariable=self.new_lot, width=20, state="disabled")
        self.txt_new_lot.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        r += 1
        ttk.Label(w, text=_("Scadenza:")).grid(row=r, column=0, sticky=tk.NE, padx=5, pady=2)
        self.cal_expiration = Calendarium(w, "")
        self.cal_expiration.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        self._set_calendarium_state(self.cal_expiration, False)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Print options
        w = ttk.LabelFrame(f2, text=_("Opzioni"), style="App.TLabelframe")
        ttk.Checkbutton(
            w, text=_("Stampa etichette"),
            variable=self.print_labels_var,
            style="App.TCheckbutton"
        ).pack(anchor=tk.W, padx=5, pady=5)
        w.pack(fill=tk.X, padx=5, pady=5)

        # Buttons (f3 already created at top)
        w = ttk.LabelFrame(f3, text=_("Comandi"), style="App.TLabelframe")
        buttons = [
            (_("Salva"), self.on_save, "<Alt-s>", 0),
            (_("Aggiorna"), self.refresh, "<Alt-a>", 0),
            (_("Chiudi"), self.on_cancel, "<Alt-c>", 0),
        ]
        for text, cmd, key, ul in buttons:
            self.engine.create_button(w, text, cmd, underline=ul).pack(fill=tk.X, padx=5, pady=3)
            self.bind(key, lambda e, c=cmd: c())
        w.pack(fill=tk.X, padx=5, pady=5)

        # Keyboard shortcuts
        self.bind("<Escape>", lambda e: self.on_cancel())

    def _set_calendarium_state(self, cal, enabled):
        """Enable or disable a Calendarium widget."""
        state = "normal" if enabled else "disabled"
        for spinbox in cal._spinboxes.values():
            spinbox.config(state=state)

    def on_batch_mode_changed(self):
        """Toggle between selecting existing batch and creating new one."""
        if self.batch_mode.get() == 0:
            # Select existing mode
            self.cb_batches.config(state="readonly")
            self.txt_new_lot.config(state="disabled")
            self._set_calendarium_state(self.cal_expiration, False)
        else:
            # Create new mode
            self.cb_batches.config(state="disabled")
            self.txt_new_lot.config(state="normal")
            self._set_calendarium_state(self.cal_expiration, True)

    def on_quantity_changed(self, *args):
        """Auto-calculate labels count when quantity changes."""
        try:
            qty = self.quantity.get()
            if self.selected_item:
                pieces_per_label = self.selected_item.get("pieces_per_label", 1) or 1
                labels_per_unit = self.selected_item.get("labels_per_unit", 1) or 1
                labels = (qty * labels_per_unit) // pieces_per_label
                if labels < 1:
                    labels = 1
                self.labels_count.set(labels)
        except (tk.TclError, ValueError):
            pass  # Ignore errors during typing

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Consegne"))
        self.engine.dict_instances["deliveries"] = self
        self.cal_delivered.set_today()
        self.cal_expiration.set_today()
        self.load_requests()

    def load_requests(self):
        """Load sent requests that have pending items."""
        # Clear treeviews
        for item in self.treeRequests.get_children():
            self.treeRequests.delete(item)
        self.dict_requests.clear()

        sql = """
            SELECT
                r.request_id,
                r.reference,
                r.issued,
                COUNT(CASE WHEN i.quantity > COALESCE(
                    (SELECT SUM(d.quantity) FROM deliveries d WHERE d.item_id = i.item_id AND d.status = 1), 0
                ) THEN 1 END) AS pending_items
            FROM requests r
            INNER JOIN items i ON i.request_id = r.request_id AND i.status = 1
            WHERE r.status = 2
            GROUP BY r.request_id
            HAVING pending_items > 0
            ORDER BY r.issued DESC
        """

        rs = self.engine.read(True, sql)

        if rs:
            for row in rs:
                request_id = row["request_id"]
                self.dict_requests[request_id] = row

                ref = row["reference"] or ""
                issued_raw = row["issued"] or ""
                # Convert from yyyy-mm-dd to dd-mm-yyyy
                if issued_raw and "-" in issued_raw:
                    parts = issued_raw.split("-")
                    if len(parts) == 3:
                        issued = f"{parts[2]}-{parts[1]}-{parts[0]}"
                    else:
                        issued = issued_raw[:10]
                else:
                    issued = issued_raw[:10]

                self.treeRequests.insert(
                    "", tk.END,
                    iid=request_id,
                    values=(ref, issued, row["pending_items"]),
                    tags=("sent",)
                )

        # Clear dependent lists
        for item in self.treeItems.get_children():
            self.treeItems.delete(item)
        self.dict_items.clear()
        self.clear_item_details()

    def on_request_selected(self, evt=None):
        """Handle request selection - load pending items."""
        selection = self.treeRequests.selection()
        if not selection:
            return

        request_id = int(selection[0])
        self.selected_request = self.dict_requests.get(request_id)

        if self.selected_request:
            self.load_items(self.selected_request["request_id"])

    def load_items(self, request_id):
        """Load items for selected request that are not fully delivered."""
        # Clear items treeview
        for item in self.treeItems.get_children():
            self.treeItems.delete(item)
        self.dict_items.clear()
        self.clear_item_details()

        sql = """
            SELECT
                i.item_id,
                i.package_id,
                p.description AS product_name,
                s.description AS supplier,
                pk.packaging,
                pk.pieces_per_label,
                pk.labels_per_unit,
                i.quantity AS ordered,
                COALESCE(
                    (SELECT SUM(d.quantity) FROM deliveries d WHERE d.item_id = i.item_id AND d.status = 1), 0
                ) AS delivered
            FROM items i
            INNER JOIN packages pk ON pk.package_id = i.package_id
            INNER JOIN products p ON p.product_id = pk.product_id
            LEFT JOIN suppliers s ON s.supplier_id = pk.supplier_id
            WHERE i.request_id = ? AND i.status = 1
            ORDER BY p.description
        """

        rs = self.engine.read(True, sql, (request_id,))

        if rs:
            for row in rs:
                item_id = row["item_id"]
                self.dict_items[item_id] = row
                ordered = row["ordered"]
                delivered = row["delivered"]

                # Tag for fully delivered items
                tag = ("completed",) if delivered >= ordered else ()

                self.treeItems.insert(
                    "", tk.END,
                    iid=item_id,
                    values=(row["product_name"] or "", ordered, delivered),
                    tags=tag
                )

    def on_item_selected(self, evt=None):
        """Handle item selection - show details and load batches."""
        selection = self.treeItems.selection()
        if not selection:
            return

        item_id = int(selection[0])
        item = self.dict_items.get(item_id)

        if item:
            # Check if fully delivered - don't allow selection
            if item["delivered"] >= item["ordered"]:
                self.treeItems.selection_remove(item_id)
                self.clear_item_details()
                return

            self.selected_item = item
            self.show_item_details()
            self.load_batches(self.selected_item["package_id"])
            self.update_quantity_default()

    def show_item_details(self):
        """Display selected item details in the form."""
        if not self.selected_item:
            return

        self.product_name.set(self.selected_item.get("product_name", ""))
        self.supplier_name.set(self.selected_item.get("supplier", "") or "")
        self.packaging.set(self.selected_item.get("packaging", "") or "")
        self.ordered_qty.set(str(self.selected_item.get("ordered", 0)))
        self.delivered_qty.set(str(self.selected_item.get("delivered", 0)))

    def clear_item_details(self):
        """Clear item detail fields."""
        self.selected_item = None
        self.product_name.set("")
        self.supplier_name.set("")
        self.packaging.set("")
        self.ordered_qty.set("")
        self.delivered_qty.set("")
        self.cb_batches.set("")
        self.cb_batches["values"] = []
        self.dict_batches.clear()

    def load_batches(self, package_id):
        """Load existing batches for the package into combobox."""
        self.cb_batches.set("")
        self.cb_batches["values"] = []
        self.dict_batches.clear()

        sql = """
            SELECT
                b.batch_id,
                b.description AS lot,
                b.expiration
            FROM batches b
            WHERE b.package_id = ? AND b.status = 1
            ORDER BY b.expiration DESC
        """

        rs = self.engine.read(True, sql, (package_id,))

        if rs:
            values = []
            for idx, row in enumerate(rs):
                self.dict_batches[idx] = row
                lot = row["lot"] or ""
                exp = row["expiration"] or ""
                values.append(f"{lot} ({_('Scad')}: {exp})")
            self.cb_batches["values"] = values
            if values:
                self.cb_batches.current(0)

    def update_quantity_default(self):
        """Set default quantity based on remaining items."""
        if not self.selected_item:
            return

        ordered = self.selected_item.get("ordered", 0)
        delivered = self.selected_item.get("delivered", 0)
        remaining = ordered - delivered

        self.quantity.set(min(remaining, 1) if remaining > 0 else 1)

    def validate_delivery(self):
        """Validate all delivery fields before save."""
        # Check item selected
        if not self.selected_item:
            messagebox.showwarning(
                self.engine.app_title,
                _("Selezionare un articolo da evadere!"),
                parent=self
            )
            return False

        # Check DDT
        if not self.ddt.get().strip():
            messagebox.showwarning(
                self.engine.app_title,
                _("Inserire il numero DDT!"),
                parent=self
            )
            return False

        # Check delivery date
        if not self.cal_delivered.is_valid:
            messagebox.showwarning(
                self.engine.app_title,
                _("Data consegna non valida!"),
                parent=self
            )
            return False

        # Check quantity
        ordered = self.selected_item.get("ordered", 0)
        delivered = self.selected_item.get("delivered", 0)
        remaining = ordered - delivered
        qty = self.quantity.get()

        if qty < 1 or qty > remaining:
            messagebox.showwarning(
                self.engine.app_title,
                _("La quantità deve essere tra 1 e") + f" {remaining}!",
                parent=self
            )
            return False

        # Check quantity is multiple of pieces_per_label
        pieces_per_label = self.selected_item.get("pieces_per_label", 1) or 1
        if pieces_per_label > 1 and qty % pieces_per_label != 0:
            messagebox.showwarning(
                self.engine.app_title,
                _("La quantità deve essere un multiplo di") + f" {pieces_per_label}!",
                parent=self
            )
            return False

        # Check batch
        if self.batch_mode.get() == 0:
            # Select existing mode
            if not self.cb_batches.get():
                messagebox.showwarning(
                    self.engine.app_title,
                    _("Selezionare un lotto esistente!"),
                    parent=self
                )
                return False
        else:
            # Create new mode
            if not self.new_lot.get().strip():
                messagebox.showwarning(
                    self.engine.app_title,
                    _("Inserire il numero di lotto!"),
                    parent=self
                )
                return False

            if not self.cal_expiration.is_valid:
                messagebox.showwarning(
                    self.engine.app_title,
                    _("Data scadenza non valida!"),
                    parent=self
                )
                return False

            # Check expiration date is in the future
            expiration_date = self.cal_expiration.get_date()
            today = datetime.date.today()
            if expiration_date and expiration_date <= today:
                messagebox.showwarning(
                    self.engine.app_title,
                    _("La data di scadenza deve essere futura!"),
                    parent=self
                )
                return False

            # Check duplicate lot (same lot number + same expiration for this package)
            lot_number = self.new_lot.get().strip()
            exp_str = expiration_date.isoformat() if expiration_date else None
            sql = """SELECT batch_id FROM batches
                     WHERE package_id = ? AND description = ? AND expiration = ? AND status = 1"""
            existing = self.engine.read(False, sql, (
                self.selected_item["package_id"],
                lot_number,
                exp_str
            ))
            if existing:
                messagebox.showwarning(
                    self.engine.app_title,
                    _("Il lotto") + f" '{lot_number}' " + _("con scadenza") + f" {exp_str} " + _("esiste già!") + "\n" +
                    _("Selezionarlo dalla lista dei lotti esistenti."),
                    parent=self
                )
                return False

        return True

    def on_save(self, evt=None):
        """Save delivery and generate labels."""
        if not self.validate_delivery():
            return

        # Get values from form
        qty = self.quantity.get()
        labels_to_create = self.labels_count.get()
        if labels_to_create < 1:
            labels_to_create = 1

        # Confirm
        msg = _("Registrare la consegna di") + f" {qty} " + _("unità?") + "\n\n" + _("Verranno create") + f" {labels_to_create} " + _("etichette.")
        if not messagebox.askyesno(self.engine.app_title, msg, parent=self):
            return

        try:
            # Get or create batch
            batch_id = self.get_or_create_batch()
            if not batch_id:
                messagebox.showerror(
                    self.engine.app_title,
                    _("Errore nella creazione del lotto!"),
                    parent=self
                )
                return

            # Create delivery record
            delivery_id = self.create_delivery()
            if not delivery_id:
                messagebox.showerror(
                    self.engine.app_title,
                    _("Errore nella registrazione della consegna!"),
                    parent=self
                )
                return

            # Create labels
            labels_created = self.create_labels(batch_id, labels_to_create)

            # Success message
            label_word = _("etichetta") if labels_created == 1 else _("etichette")
            messagebox.showinfo(
                self.engine.app_title,
                _("Consegna registrata con successo!") + "\n\n" +
                _("Create") + f" {labels_created} {label_word}.",
                parent=self
            )

            # Remember current selection for repositioning
            current_request_id = self.selected_request["request_id"] if self.selected_request else None
            current_item_id = self.selected_item["item_id"] if self.selected_item else None

            # Check if all items in this request are now fully delivered
            if current_request_id:
                self.check_and_close_request(current_request_id)

            # Refresh and reposition
            self.clear_form()
            self.refresh_and_reposition(current_request_id, current_item_id)

            # Refresh warehouse batches list if open
            if "warehouse" in self.engine.dict_instances:
                self.engine.dict_instances["warehouse"].refresh_batches()

        except Exception as e:
            self.engine.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__]
            )
            messagebox.showerror(
                self.engine.app_title,
                _("Errore durante il salvataggio:") + f"\n{e}",
                parent=self
            )

    def check_and_close_request(self, request_id):
        """Check if all items are delivered and close the request if so."""
        sql = """
            SELECT COUNT(*) AS pending
            FROM items i
            WHERE i.request_id = ? AND i.status = 1
            AND i.quantity > COALESCE(
                (SELECT SUM(d.quantity) FROM deliveries d WHERE d.item_id = i.item_id AND d.status = 1), 0
            )
        """
        result = self.engine.read(False, sql, (request_id,))

        if result and result["pending"] == 0:
            # All items delivered - close the request
            sql = "UPDATE requests SET status = 0 WHERE request_id = ?"
            self.engine.write(sql, (request_id,))
            messagebox.showinfo(
                self.engine.app_title,
                _("Tutti gli articoli sono stati evasi.") + "\n" + _("La richiesta è stata chiusa."),
                parent=self
            )

    def get_or_create_batch(self):
        """Get selected batch_id or create new batch and return its id."""
        if self.batch_mode.get() == 0:
            # Select existing
            idx = self.cb_batches.current()
            if idx >= 0 and idx in self.dict_batches:
                return self.dict_batches[idx]["batch_id"]
            return None
        else:
            # Create new
            sql = """
                INSERT INTO batches (package_id, description, expiration, status)
                VALUES (?, ?, ?, 1)
            """
            expiration_date = self.cal_expiration.get_date()
            return self.engine.write(sql, (
                self.selected_item["package_id"],
                self.new_lot.get().strip(),
                expiration_date.isoformat() if expiration_date else None
            ))

    def create_delivery(self):
        """Create delivery record."""
        sql = """
            INSERT INTO deliveries (item_id, package_id, ddt, delivered, quantity, status)
            VALUES (?, ?, ?, ?, ?, 1)
        """
        delivered_date = self.cal_delivered.get_date()
        return self.engine.write(sql, (
            self.selected_item["item_id"],
            self.selected_item["package_id"],
            self.ddt.get().strip(),
            delivered_date.isoformat() if delivered_date else None,
            self.quantity.get()
        ))

    def create_labels(self, batch_id, count):
        """Create N labels for the batch and optionally print them."""
        created = 0
        label_ids = []
        for _ in range(count):
            label_id = self.engine.load_label(batch_id)
            if label_id:
                created += 1
                label_ids.append(label_id)
        
        # Print labels if checkbox is checked and labels were created
        if self.print_labels_var.get() == 1 and label_ids:
            self.print_labels(label_ids)
        
        return created

    def print_labels(self, label_ids):
        """Print barcode labels for the given label IDs."""
        from barcode_label import BarcodeLabel
        
        try:
            generator = BarcodeLabel(self.engine)
            for label_id in label_ids:
                generator.generate_label(label_id)
        except Exception as e:
            messagebox.showwarning(
                self.engine.app_title,
                _("Etichette create ma errore nella stampa:") + f"\n{e}",
                parent=self
            )

    def clear_form(self):
        """Clear form fields (keeps DDT and delivery date for multiple deliveries)."""
        # Don't reset DDT and delivery date for multiple deliveries
        # self.ddt.set("")
        # self.cal_delivered.set_today()
        self.quantity.set(1)
        self.labels_count.set(1)
        self.batch_mode.set(0)
        self.new_lot.set("")
        self.cal_expiration.set_today()
        self.on_batch_mode_changed()

    def refresh(self):
        """Refresh all lists."""
        # Remember current selection by ID
        current_request_id = self.selected_request["request_id"] if self.selected_request else None
        current_item_id = self.selected_item["item_id"] if self.selected_item else None
        self.refresh_and_reposition(current_request_id, current_item_id)

    def refresh_and_reposition(self, request_id, item_id):
        """Refresh lists and try to reposition on the given request/item."""
        self.load_requests()

        # Try to find and select the request by ID
        if request_id and str(request_id) in self.treeRequests.get_children():
            self.treeRequests.selection_set(request_id)
            self.treeRequests.see(request_id)
            self.on_request_selected()

            # Try to find and select the item by ID
            if item_id and str(item_id) in self.treeItems.get_children():
                self.treeItems.selection_set(item_id)
                self.treeItems.see(item_id)
                self.on_item_selected()

    def on_cancel(self, evt=None):
        """Close the window."""
        if "deliveries" in self.engine.dict_instances:
            del self.engine.dict_instances["deliveries"]
        super().on_cancel()
