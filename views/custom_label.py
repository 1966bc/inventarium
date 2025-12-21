#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Label - Generate custom text labels for Inventarium.

This module provides a dialog for creating and printing custom labels
with 1-3 text lines, useful for reagent bottles, calibrators, controls, etc.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk

from i18n import _
from tkinter import ttk
from tkinter import messagebox
import json
import os


class UI(tk.Toplevel):
    """Custom label generator window."""

    def __init__(self, parent):
        super().__init__(name="custom_label")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.minsize(500, 450)
        self.resizable(False, False)

        # Variables
        self.num_lines = tk.IntVar(value=1)
        self.line1_var = tk.StringVar()
        self.line2_var = tk.StringVar()
        self.line3_var = tk.StringVar()
        self.include_lab = tk.BooleanVar(value=True)
        self.font_size = tk.IntVar(value=28)

        # Templates file
        self.templates_file = self.engine.get_file("label_templates.json")
        self.templates = self.load_templates()

        self.init_ui()
        self.engine.center_window(self)


    def init_ui(self):
        """Build the user interface."""
        f0 = ttk.Frame(self, padding=10)
        f0.pack(fill=tk.BOTH, expand=1)

        # Number of lines selection
        lf_lines = ttk.LabelFrame(f0, text=_("Righe da stampare"), style="App.TLabelframe")
        lf_lines.pack(fill=tk.X, pady=(0, 10))

        rf = ttk.Frame(lf_lines)
        rf.pack(fill=tk.X, padx=10, pady=5)

        for i in range(1, 4):
            ttk.Radiobutton(
                rf, text=str(i), variable=self.num_lines,
                value=i, command=self.on_lines_changed,
                style="App.TRadiobutton"
            ).pack(side=tk.LEFT, padx=10)

        # Text fields
        lf_text = ttk.LabelFrame(f0, text=_("Testo Etichetta"), style="App.TLabelframe")
        lf_text.pack(fill=tk.X, pady=(0, 10))

        # Line 1
        r1 = ttk.Frame(lf_text)
        r1.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(r1, text=_("Riga 1:"), width=8).pack(side=tk.LEFT)
        self.entry1 = ttk.Entry(r1, textvariable=self.line1_var, width=40)
        self.entry1.pack(side=tk.LEFT, fill=tk.X, expand=1)

        # Line 2
        r2 = ttk.Frame(lf_text)
        r2.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(r2, text=_("Riga 2:"), width=8).pack(side=tk.LEFT)
        self.entry2 = ttk.Entry(r2, textvariable=self.line2_var, width=40)
        self.entry2.pack(side=tk.LEFT, fill=tk.X, expand=1)

        # Line 3
        r3 = ttk.Frame(lf_text)
        r3.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(r3, text=_("Riga 3:"), width=8).pack(side=tk.LEFT)
        self.entry3 = ttk.Entry(r3, textvariable=self.line3_var, width=40)
        self.entry3.pack(side=tk.LEFT, fill=tk.X, expand=1)

        # Font size control
        r4 = ttk.Frame(lf_text)
        r4.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(r4, text=_("Dim. Font:"), width=8).pack(side=tk.LEFT)
        self.spn_font = ttk.Spinbox(
            r4, from_=16, to=48, width=5,
            textvariable=self.font_size
        )
        self.spn_font.pack(side=tk.LEFT)
        ttk.Label(r4, text="(16-48)").pack(side=tk.LEFT, padx=5)

        # Include lab name checkbox
        ttk.Checkbutton(
            lf_text, text=_("Includi nome laboratorio"),
            variable=self.include_lab,
            style="App.TCheckbutton"
        ).pack(anchor=tk.W, padx=10, pady=5)

        # Templates section
        lf_templates = ttk.LabelFrame(f0, text=_("Modelli Salvati"), style="App.TLabelframe")
        lf_templates.pack(fill=tk.BOTH, expand=1, pady=(0, 10))

        # Templates listbox
        tf = ttk.Frame(lf_templates)
        tf.pack(fill=tk.BOTH, expand=1, padx=10, pady=5)

        self.lst_templates = tk.Listbox(tf, height=6)
        self.lst_templates.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.lst_templates.bind("<Double-1>", self.on_load_template)

        sb = ttk.Scrollbar(tf, orient=tk.VERTICAL, command=self.lst_templates.yview)
        self.lst_templates.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        # Template buttons
        tb = ttk.Frame(lf_templates)
        tb.pack(fill=tk.X, padx=10, pady=5)

        self.engine.create_button(tb, _("Carica"), self.on_load_template).pack(side=tk.LEFT, padx=2)
        self.engine.create_button(tb, _("Salva"), self.on_save_template).pack(side=tk.LEFT, padx=2)
        self.engine.create_button(tb, _("Elimina"), self.on_delete_template).pack(side=tk.LEFT, padx=2)

        # Action buttons
        bf = ttk.Frame(f0)
        bf.pack(fill=tk.X, pady=(10, 0))

        self.engine.create_button(bf, _("Anteprima"), self.on_preview, width=12).pack(side=tk.LEFT, padx=5)
        self.engine.create_button(bf, _("Stampa"), self.on_print, width=12).pack(side=tk.LEFT, padx=5)
        self.engine.create_button(bf, _("Chiudi"), self.on_cancel, width=12).pack(side=tk.RIGHT, padx=5)

        self.bind("<Escape>", lambda e: self.on_cancel())

        # Initialize state
        self.on_lines_changed()

    def on_open(self):
        """Initialize and show the window."""
        self.title(_("Etichetta Personalizzata"))
        self.engine.dict_instances["custom_label"] = self
        self.refresh_templates_list()
        self.entry1.focus_set()

    def on_lines_changed(self):
        """Update entry states based on number of lines selected."""
        n = self.num_lines.get()

        self.entry2.configure(state="normal" if n >= 2 else "disabled")
        self.entry3.configure(state="normal" if n >= 3 else "disabled")

        if n < 2:
            self.line2_var.set("")
        if n < 3:
            self.line3_var.set("")

    def load_templates(self):
        """Load templates from JSON file."""
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def save_templates(self):
        """Save templates to JSON file."""
        try:
            with open(self.templates_file, "w", encoding="utf-8") as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror(
                self.engine.app_title,
                _("Errore nel salvare i modelli:") + f"\n{e}",
                parent=self
            )

    def refresh_templates_list(self):
        """Refresh the templates listbox."""
        self.lst_templates.delete(0, tk.END)
        for name in sorted(self.templates.keys()):
            self.lst_templates.insert(tk.END, name)

    def on_save_template(self):
        """Save current settings as a template."""
        line1 = self.line1_var.get().strip()
        if not line1:
            messagebox.showwarning(
                self.engine.app_title,
                _("Inserire almeno la prima riga!"),
                parent=self
            )
            return

        # Use first line as template name (truncated)
        name = line1[:30]

        # Check if exists
        if name in self.templates:
            if not messagebox.askyesno(
                self.engine.app_title,
                _("Il modello '{}' esiste.\nSovrascrivere?").format(name),
                parent=self
            ):
                return

        self.templates[name] = {
            "num_lines": self.num_lines.get(),
            "line1": line1,
            "line2": self.line2_var.get().strip(),
            "line3": self.line3_var.get().strip(),
            "include_lab": self.include_lab.get(),
            "font_size": self.font_size.get()
        }

        self.save_templates()
        self.refresh_templates_list()

        messagebox.showinfo(
            self.engine.app_title,
            _("Modello '{}' salvato!").format(name),
            parent=self
        )

    def on_load_template(self, evt=None):
        """Load selected template into fields."""
        selection = self.lst_templates.curselection()
        if not selection:
            return

        name = self.lst_templates.get(selection[0])
        template = self.templates.get(name)

        if template:
            self.num_lines.set(template.get("num_lines", 1))
            self.on_lines_changed()

            self.line1_var.set(template.get("line1", ""))
            self.line2_var.set(template.get("line2", ""))
            self.line3_var.set(template.get("line3", ""))
            self.include_lab.set(template.get("include_lab", True))
            self.font_size.set(template.get("font_size", 28))

    def on_delete_template(self):
        """Delete selected template."""
        selection = self.lst_templates.curselection()
        if not selection:
            return

        name = self.lst_templates.get(selection[0])

        if messagebox.askyesno(
            self.engine.app_title,
            _("Eliminare il modello '{}'?").format(name),
            parent=self
        ):
            del self.templates[name]
            self.save_templates()
            self.refresh_templates_list()

    def get_label_lines(self):
        """Get list of lines to print."""
        lines = []
        n = self.num_lines.get()

        line1 = self.line1_var.get().strip()
        if line1:
            lines.append(line1)

        if n >= 2:
            line2 = self.line2_var.get().strip()
            if line2:
                lines.append(line2)

        if n >= 3:
            line3 = self.line3_var.get().strip()
            if line3:
                lines.append(line3)

        return lines

    def generate_label(self, show_only=False):
        """Generate the custom label image."""
        lines = self.get_label_lines()

        if not lines:
            messagebox.showwarning(
                self.engine.app_title,
                _("Inserire almeno una riga di testo!"),
                parent=self
            )
            return None

        # Get footer (lab name)
        footer = ""
        if self.include_lab.get():
            footer = self.engine.get_setting("lab_name", "")

        # Use BarcodeLabel to generate simple label
        from barcode_label import BarcodeLabel

        try:
            generator = BarcodeLabel(self.engine)
            path = generator.generate_simple_label(lines, footer, self.font_size.get())

            if show_only:
                # Show preview
                from PIL import Image
                img = Image.open(path)
                img.show()

            return path

        except Exception as e:
            messagebox.showerror(
                self.engine.app_title,
                _("Errore nella generazione:") + f"\n{e}",
                parent=self
            )
            return None

    def on_preview(self):
        """Show label preview."""
        self.generate_label(show_only=True)

    def on_print(self):
        """Print the label."""
        path = self.generate_label(show_only=False)

        if path:
            from barcode_label import BarcodeLabel

            try:
                generator = BarcodeLabel(self.engine)
                generator._print_label(path)

                messagebox.showinfo(
                    self.engine.app_title,
                    _("Etichetta inviata alla stampa!"),
                    parent=self
                )
            except Exception as e:
                messagebox.showerror(
                    self.engine.app_title,
                    _("Errore nella stampa:") + f"\n{e}",
                    parent=self
                )

    def on_cancel(self, evt=None):
        """Close the window."""
        if "custom_label" in self.engine.dict_instances:
            del self.engine.dict_instances["custom_label"]
        self.destroy()
