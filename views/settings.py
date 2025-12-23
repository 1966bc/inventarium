#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Dialog - Configure laboratory settings for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from i18n import _, LANGUAGES
from views.child_view import ChildView


class UI(ChildView):
    """Settings configuration dialog."""

    def __init__(self, parent):
        super().__init__(parent, name="settings")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.resizable(0, 0)

        # Form variables
        self.company_name = tk.StringVar()
        self.lab_name = tk.StringVar()
        self.lab_manager = tk.StringVar()
        self.lab_room = tk.StringVar()
        self.lab_phone = tk.StringVar()
        self.idle_timeout = tk.StringVar()
        self.default_vat = tk.StringVar()
        self.language = tk.StringVar()
        self.printer_enabled = tk.BooleanVar()

        self.init_ui()
        self.engine.center_window(self)
        self.show()


    def init_ui(self):
        """Build the dialog UI."""
        w = ttk.Frame(self, padding=10)
        w.pack(fill=tk.BOTH, expand=1)

        entry_width = 40

        r = 0
        ttk.Label(w, text=_("Ospedale:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtCompany = ttk.Entry(w, textvariable=self.company_name, width=entry_width)
        self.txtCompany.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Laboratorio:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtLab = ttk.Entry(w, textvariable=self.lab_name, width=entry_width)
        self.txtLab.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Responsabile:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtManager = ttk.Entry(w, textvariable=self.lab_manager, width=entry_width)
        self.txtManager.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Stanza/Locale:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtRoom = ttk.Entry(w, textvariable=self.lab_room, width=entry_width)
        self.txtRoom.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        r += 1
        ttk.Label(w, text=_("Telefono:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtPhone = ttk.Entry(w, textvariable=self.lab_phone, width=entry_width)
        self.txtPhone.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Separator
        r += 1
        ttk.Separator(w, orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=2, sticky="ew", pady=10)

        # Default VAT
        r += 1
        ttk.Label(w, text=_("IVA predefinita %:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.txtVat = ttk.Entry(w, textvariable=self.default_vat, width=8)
        self.txtVat.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Idle timeout
        r += 1
        ttk.Label(w, text=_("Timeout inattività (min):")).grid(row=r, column=0, sticky=tk.W, pady=2)
        timeout_frame = ttk.Frame(w)
        timeout_frame.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        self.spnTimeout = ttk.Spinbox(timeout_frame, from_=0, to=120, width=5,
                                       textvariable=self.idle_timeout)
        self.spnTimeout.pack(side=tk.LEFT)
        ttk.Label(timeout_frame, text=_("(0 = disabilitato)")).pack(side=tk.LEFT, padx=5)

        # Language selection
        r += 1
        ttk.Label(w, text=_("Lingua") + ":").grid(row=r, column=0, sticky=tk.W, pady=2)
        lang_frame = ttk.Frame(w)
        lang_frame.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
        self.cmbLanguage = ttk.Combobox(lang_frame, textvariable=self.language,
                                         state="readonly", width=15, style="App.TCombobox")
        self.cmbLanguage["values"] = list(LANGUAGES.values())
        self.cmbLanguage.pack(side=tk.LEFT)

        # Separator for local settings
        r += 1
        ttk.Separator(w, orient=tk.HORIZONTAL).grid(row=r, column=0, columnspan=2, sticky="ew", pady=10)

        r += 1
        ttk.Label(w, text=_("Impostazioni locali"), font=("", 9, "bold")).grid(
            row=r, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Printer enabled (local setting - config.ini)
        r += 1
        ttk.Label(w, text=_("Stampa etichette:")).grid(row=r, column=0, sticky=tk.W, pady=2)
        self.chkPrinter = ttk.Checkbutton(w, text=_("Abilitata su questa postazione"),
                                           variable=self.printer_enabled, style="App.TCheckbutton")
        self.chkPrinter.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)

        # Buttons
        r += 1
        bf = ttk.Frame(w)
        bf.grid(row=r, column=0, columnspan=2, sticky=tk.E, pady=15)

        self.engine.create_button(bf, _("Salva"), self.on_save, width=12).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-s>", lambda e: self.on_save())

        self.engine.create_button(bf, _("Chiudi"), self.on_cancel, width=12).pack(side=tk.LEFT, padx=5)
        self.bind("<Alt-c>", lambda e: self.on_cancel())
        self.bind("<Escape>", lambda e: self.on_cancel())

    def on_open(self):
        """Initialize and show the dialog."""
        self.title(_("Impostazioni Laboratorio"))
        self.load_settings()
        self.txtCompany.focus()

    def load_settings(self):
        """Load current settings into form."""
        self.company_name.set(self.engine.get_setting("company_name", ""))
        self.lab_name.set(self.engine.get_setting("lab_name", ""))
        self.lab_manager.set(self.engine.get_setting("lab_manager", ""))
        self.lab_room.set(self.engine.get_setting("lab_room", ""))
        self.lab_phone.set(self.engine.get_setting("lab_phone", ""))
        self.default_vat.set(self.engine.get_setting("default_vat", "10"))
        self.idle_timeout.set(self.engine.get_setting("idle_timeout", "30"))
        # Load language - convert code to display name
        lang_code = self.engine.get_setting("language", "it")
        self.language.set(LANGUAGES.get(lang_code, "Italiano"))
        self._original_language = lang_code
        # Load printer setting from config.ini (local)
        self.printer_enabled.set(self.engine.is_printer_enabled())

    def on_save(self, evt=None):
        """Save settings."""
        if messagebox.askyesno(
            self.engine.app_title,
            _("Vuoi salvare?"),
            parent=self
        ):
            self.engine.set_setting("company_name", self.company_name.get().strip())
            self.engine.set_setting("lab_name", self.lab_name.get().strip())
            self.engine.set_setting("lab_manager", self.lab_manager.get().strip())
            self.engine.set_setting("lab_room", self.lab_room.get().strip())
            self.engine.set_setting("lab_phone", self.lab_phone.get().strip())
            self.engine.set_setting("default_vat", self.default_vat.get().strip())
            self.engine.set_setting("idle_timeout", self.idle_timeout.get().strip())

            # Save language - convert display name back to code
            lang_name = self.language.get()
            lang_code = "it"  # default
            for code, name in LANGUAGES.items():
                if name == lang_name:
                    lang_code = code
                    break
            self.engine.set_setting("language", lang_code)

            # Save printer setting to config.ini (local)
            self.engine.set_printer_enabled(self.printer_enabled.get())

            # Update idle monitor with new timeout
            self._update_monitor()

            messagebox.showinfo(
                self.engine.app_title,
                _("Impostazioni salvate."),
                parent=self
            )

            # Check if language changed - ask to restart
            if lang_code != self._original_language:
                if messagebox.askyesno(
                    self.engine.app_title,
                    _("Riavvio richiesto"),
                    parent=self
                ):
                    self.destroy()
                    self.nametowidget(".").on_exit(silent=True)
                    return

            self.on_cancel()
        else:
            messagebox.showinfo(
                self.engine.app_title,
                _("Operazione annullata."),
                parent=self
            )

    def _update_monitor(self):
        """Update idle monitor with new timeout value."""
        try:
            app = self.nametowidget(".")
            if hasattr(app, 'monitor') and app.monitor:
                timeout = int(self.idle_timeout.get().strip() or 30)
                if timeout > 0:
                    app.monitor.set_timeout(timeout)
                else:
                    app.monitor.stop()
        except Exception:
            pass

    def on_cancel(self, evt=None):
        """Close the dialog."""
        super().on_cancel()
