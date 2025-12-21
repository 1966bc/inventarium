#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window for Inventarium - Laboratory Inventory Management System.

This module provides the main application window with menu and toolbar
for managing laboratory inventory, requests, and deliveries.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _, LANGUAGES

from views import warehouse
from views import products
from views import categories
from views import suppliers
from views import locations
from views import conservations
from views import requests
from views import delivery
from views import stocks
from views import settings
from views import expiring
from views import barcode
from views import stats_dashboard
from views import stats_consumption
from views import stats_rotation
from views import stats_tat
from views import stats_suppliers
from views import stats_expiring
from views import custom_label
from views import funding_sources
from views import deliberations
from views import prices
from views import package_fundings
from views import report_fundings


class Main(tk.Toplevel):
    """
    Main application window for Inventarium.

    Provides menu bar, toolbar, and status bar for accessing
    all inventory management functions.
    """

    def __init__(self, parent):
        super().__init__(name="main")

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.status_bar_text = tk.StringVar()
        self.set_title()
        self.init_ui()
        self.init_toolbar()
        self.init_menu()
        self.init_status_bar()
        self.center_window()

    def set_title(self):
        """Set window title."""
        self.title(self.engine.app_title)

    def init_ui(self):
        """Initialize main UI frame."""
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

    def init_toolbar(self):
        """Initialize toolbar with icon buttons."""
        toolbar = ttk.Frame(self.main_frame)

        buttons = (
            ("📦", self.on_warehouse),
            ("🛒", self.on_open_requests),
            ("🖨", self.on_stocks),
            ("▮▯▮", self.on_barcode),
            ("ℹ", self.on_about),
            ("⏻", self.on_exit),
        )
        for text, callback in buttons:
            self.engine.create_button(toolbar, text, callback, width=3).pack(side=tk.TOP, padx=2, pady=2)

        toolbar.pack(side=tk.LEFT, fill=tk.Y, expand=0)

    def init_menu(self):
        """Initialize menu bar."""
        menubar = tk.Menu(self, bd=1)

        # File menu
        m_file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("File"), underline=0, menu=m_file)
        m_file.add_command(label=_("Impostazioni"), underline=0, command=self.on_settings)
        m_file.add_command(label=_("Configura Database"), underline=0, command=self.on_config_database)
        m_file.add_command(label=_("Backup Database"), underline=0, command=self.on_backup)
        m_file.add_command(label=_("Compatta Database"), underline=0, command=self.on_vacuum)
        m_file.add_command(label=_("Log"), underline=0, command=self.on_log)
        m_file.add_separator()
        m_file.add_command(label=_("Etichetta Personalizzata"), underline=0, command=self.on_custom_label)
        m_file.add_separator()

        # Language submenu
        m_lang = tk.Menu(m_file, tearoff=0)
        m_file.add_cascade(label=_("Lingua"), underline=0, menu=m_lang)
        current_lang = self.engine.get_setting("language", "it")
        for code, name in LANGUAGES.items():
            m_lang.add_radiobutton(
                label=name,
                command=lambda c=code: self.on_change_language(c),
                value=code,
                variable=tk.StringVar(value=current_lang)
            )

        m_file.add_separator()
        m_file.add_command(label=_("Esci"), underline=0, command=self.on_exit)

        # Magazzino menu
        m_warehouse = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("Magazzino"), underline=0, menu=m_warehouse)
        m_warehouse.add_command(label=_("Giacenze"), underline=0, command=self.on_warehouse)
        m_warehouse.add_command(label=_("Stampa Giacenze"), underline=0, command=self.on_stocks)
        m_warehouse.add_command(label=_("Scarico"), underline=0, command=self.on_barcode)
        m_warehouse.add_separator()
        m_warehouse.add_command(label=_("Scadenze"), underline=0, command=self.on_expiring)

        # Richieste menu
        m_requests = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("Richieste"), underline=0, menu=m_requests)
        m_requests.add_command(label=_("Richieste"), underline=0, command=self.on_open_requests)
        m_requests.add_separator()
        m_requests.add_command(label=_("Consegne"), underline=0, command=self.on_deliveries)

        # Admin menu
        m_admin = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("Anagrafiche"), underline=0, menu=m_admin)
        m_admin.add_command(label=_("Prodotti"), underline=0, command=self.on_products)
        m_admin.add_command(label=_("Fornitori"), underline=0, command=self.on_suppliers)
        m_admin.add_command(label=_("Categorie"), underline=0, command=self.on_categories)
        m_admin.add_command(label=_("Conservazioni"), underline=0, command=self.on_conservations)
        m_admin.add_command(label=_("Ubicazioni"), underline=0, command=self.on_locations)
        m_admin.add_command(label=_("Fonti Finanziamento"), underline=0, command=self.on_funding_sources)

        # Acquisti menu
        m_purchases = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("Acquisti"), underline=0, menu=m_purchases)
        m_purchases.add_command(label=_("Delibere"), underline=0, command=self.on_deliberations)
        m_purchases.add_command(label=_("Listino Prezzi"), underline=0, command=self.on_prices)
        m_purchases.add_separator()
        m_purchases.add_command(label=_("Fonti Package"), underline=0, command=self.on_package_fundings)
        m_purchases.add_separator()
        m_purchases.add_command(label=_("Report Fonti"), underline=0, command=self.on_report_fundings)

        # Statistiche menu
        m_stats = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_("Statistiche"), underline=0, menu=m_stats)
        m_stats.add_command(label=_("Dashboard"), underline=0, command=self.on_stats_dashboard)
        m_stats.add_separator()
        m_stats.add_command(label=_("Consumi"), underline=0, command=self.on_stats_consumption)
        m_stats.add_command(label=_("Rotazione"), underline=0, command=self.on_stats_rotation)
        m_stats.add_command(label=_("Tempi (TAT)"), underline=0, command=self.on_stats_tat)
        m_stats.add_separator()
        m_stats.add_command(label=_("Fornitori"), underline=0, command=self.on_stats_suppliers)
        m_stats.add_command(label=_("Scadenze"), underline=0, command=self.on_stats_expiring)

        # Help menu
        m_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="?", underline=0, menu=m_help)
        m_help.add_command(label=_("Informazioni"), underline=0, command=self.on_about)
        m_help.add_command(label=_("Licenza"), underline=0, command=self.on_license)
        m_help.add_separator()
        m_help.add_command(label=_("Versione Python"), underline=0, command=self.on_python_version)
        m_help.add_command(label=_("Versione Tkinter"), underline=0, command=self.on_tkinter_version)

        self.config(menu=menubar)

    def init_status_bar(self):
        """Initialize status bar."""
        company = self.engine.get_setting("company_name", "")
        lab = self.engine.get_setting("lab_name", "")
        if company and lab:
            status_text = f"{company} - {lab}"
        elif company:
            status_text = company
        elif lab:
            status_text = lab
        else:
            status_text = f"Ready - {self.engine.get_today()}"
        self.status_bar_text.set(status_text)
        self.status = ttk.Label(
            self,
            textvariable=self.status_bar_text,
            style="StatusBar.TLabel"
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def on_open(self):
        """Called when window opens."""
        self.engine.dict_instances["main"] = self

    # -------------------------------------------------------------------------
    # Menu callbacks - Warehouse
    # -------------------------------------------------------------------------

    def on_warehouse(self):
        """Open stock view."""
        obj = warehouse.UI(self)
        obj.on_open()

    def on_stocks(self):
        obj = stocks.UI(self)
        obj.on_open()

    def on_expiring(self):
        """Show expiring batches."""
        obj = expiring.UI(self)
        obj.on_open()

    def on_barcode(self):
        """Open barcode scanner to unload labels."""
        obj = barcode.UI(self)
        obj.on_open()

    def on_custom_label(self):
        """Open custom label generator."""
        obj = custom_label.UI(self)
        obj.on_open()

    # -------------------------------------------------------------------------
    # Menu callbacks - Requests
    # -------------------------------------------------------------------------

    def on_open_requests(self):
        """View open requests."""
        obj = requests.UI(self)
        obj.on_open()

    def on_deliveries(self):
        """Manage deliveries."""
        obj = delivery.UI(self)
        obj.on_open()

    # -------------------------------------------------------------------------
    # Menu callbacks - Admin
    # -------------------------------------------------------------------------

    def on_products(self):
        """Open products management."""
        obj = products.UI(self)
        obj.on_open()

    def on_suppliers(self):
        """Manage suppliers."""
        obj = suppliers.UI(self)
        obj.on_open()

    def on_categories(self):
        """Manage categories."""
        obj = categories.UI(self)
        obj.on_open()

    def on_conservations(self):
        """Manage conservations."""
        obj = conservations.UI(self)
        obj.on_open()

    def on_locations(self):
        """Manage locations."""
        obj = locations.UI(self)
        obj.on_open()

    def on_funding_sources(self):
        """Manage funding sources."""
        obj = funding_sources.UI(self)
        obj.on_open()

    # -------------------------------------------------------------------------
    # Menu callbacks - Purchases
    # -------------------------------------------------------------------------

    def on_deliberations(self):
        """Manage deliberations."""
        obj = deliberations.UI(self)
        obj.on_open()

    def on_prices(self):
        """Manage price list."""
        obj = prices.UI(self)
        obj.on_open()

    def on_package_fundings(self):
        """Manage package funding sources."""
        obj = package_fundings.UI(self)
        obj.on_open()

    def on_report_fundings(self):
        """Show funding sources report."""
        obj = report_fundings.UI(self)
        obj.on_open()

    # -------------------------------------------------------------------------
    # Menu callbacks - Statistics
    # -------------------------------------------------------------------------

    def on_stats_dashboard(self):
        """Open statistics dashboard."""
        obj = stats_dashboard.UI(self)
        obj.on_open()

    def on_stats_consumption(self):
        """Open consumption statistics."""
        obj = stats_consumption.UI(self)
        obj.on_open()

    def on_stats_rotation(self):
        """Open rotation/ABC analysis."""
        obj = stats_rotation.UI(self)
        obj.on_open()

    def on_stats_tat(self):
        """Open TAT analysis."""
        obj = stats_tat.UI(self)
        obj.on_open()

    def on_stats_suppliers(self):
        """Open suppliers analysis."""
        obj = stats_suppliers.UI(self)
        obj.on_open()

    def on_stats_expiring(self):
        """Open expiring analysis."""
        obj = stats_expiring.UI(self)
        obj.on_open()

    # -------------------------------------------------------------------------
    # Menu callbacks - Help
    # -------------------------------------------------------------------------

    def on_about(self):
        """Show about dialog."""
        import inventarium
        msg = (
            f"{self.engine.app_title}\n\n"
            f"Versio: {inventarium.__version__}\n"
            f"Dies: {inventarium.__date__}\n"
            f"Status: {inventarium.__status__}\n\n"
            f"Auctor: {inventarium.__author__}\n"
            f"Epistula: {inventarium.__email__}\n\n"
            f"Licentia: {inventarium.__license__}\n"
            f"{inventarium.__copyright__}"
        )
        messagebox.showinfo(self.engine.app_title, msg, parent=self)

    def on_python_version(self):
        """Show Python version."""
        msg = self.engine.get_python_version()
        messagebox.showinfo(self.engine.app_title, msg, parent=self)

    def on_tkinter_version(self):
        """Show Tkinter version."""
        msg = f"Tkinter patchlevel\n{self.tk.call('info', 'patchlevel')}"
        messagebox.showinfo(self.engine.app_title, msg, parent=self)

    def on_license(self):
        """Show license window."""
        from views.license import UI
        ui = UI(self)
        ui.on_open()

    # -------------------------------------------------------------------------
    # Utility methods
    # -------------------------------------------------------------------------

    def on_todo(self, feature):
        """Placeholder for unimplemented features."""
        msg = f"{feature}\n\nTo be implemented..."
        messagebox.showinfo(self.engine.app_title, msg, parent=self)

    def on_settings(self):
        """Open settings dialog."""
        obj = settings.UI(self)
        obj.on_open()

    def on_config_database(self):
        """Configure database path."""
        import inventarium

        # Get current path
        current_path = inventarium.load_db_path() or ""

        # Show config dialog
        dialog = inventarium.ConfigDialog(self)
        dialog.db_path.set(current_path)
        dialog.title("Configura Percorso Database")
        self.wait_window(dialog)

        if dialog.result is not None and dialog.result != current_path:
            # Save new path
            inventarium.save_db_path(dialog.result)

            # Ask to restart
            if messagebox.askyesno(
                self.engine.app_title,
                "Percorso database aggiornato.\n\n"
                "È necessario riavviare l'applicazione per utilizzare il nuovo database.\n\n"
                "Riavviare ora?",
                parent=self
            ):
                self.nametowidget(".").on_exit(silent=True)

    def on_backup(self):
        """Backup database to user-selected location."""
        import shutil
        import datetime
        import inventarium
        from tkinter import filedialog

        # Generate default filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"inventarium_backup_{timestamp}.db"

        # Ask user where to save
        filename = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")],
            initialfile=default_name,
            title="Salva Backup Database"
        )

        if filename:
            try:
                # Get source database path from config
                source_db = inventarium.load_db_path()

                # Copy database
                shutil.copy2(source_db, filename)

                messagebox.showinfo(
                    self.engine.app_title,
                    f"Backup completato!\n\n{filename}",
                    parent=self
                )
            except Exception as e:
                messagebox.showerror(
                    self.engine.app_title,
                    f"Errore durante il backup:\n{e}",
                    parent=self
                )

    def on_vacuum(self):
        """Compact the database using VACUUM."""
        import os
        import inventarium

        try:
            db_path = inventarium.load_db_path()
            size_before = os.path.getsize(db_path)

            # Run VACUUM
            self.engine.write("VACUUM")

            size_after = os.path.getsize(db_path)
            saved = size_before - size_after

            # Format sizes for display
            def fmt_size(s):
                if s >= 1024 * 1024:
                    return f"{s / (1024 * 1024):.1f} MB"
                elif s >= 1024:
                    return f"{s / 1024:.1f} KB"
                return f"{s} bytes"

            messagebox.showinfo(
                self.engine.app_title,
                f"{_('Database compattato!')}\n\n"
                f"{_('Prima')}: {fmt_size(size_before)}\n"
                f"{_('Dopo')}: {fmt_size(size_after)}\n"
                f"{_('Risparmiato')}: {fmt_size(saved)}",
                parent=self
            )
        except Exception as e:
            messagebox.showerror(
                self.engine.app_title,
                f"{_('Errore durante la compattazione')}:\n{e}",
                parent=self
            )

    def on_log(self):
        """Open log file."""
        self.engine.get_log_file()

    def refresh(self):
        """Refresh main window data."""
        pass

    def center_window(self):
        """Center window on screen."""
        width = 800
        height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def on_change_language(self, lang_code):
        """Change application language (requires restart)."""
        current = self.engine.get_setting("language", "it")
        if lang_code == current:
            return

        # Save new language
        self.engine.set_setting("language", lang_code)

        # Ask to restart
        if messagebox.askyesno(
            self.engine.app_title,
            _("Riavvio richiesto"),
            parent=self
        ):
            self.nametowidget(".").on_exit(silent=True)

    def on_exit(self):
        """Exit application."""
        self.nametowidget(".").on_exit()
