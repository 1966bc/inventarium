#!/usr/bin/env python3
"""
License View - Display GPL License text.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
"""
import tkinter as tk
from tkinter import ttk


class UI(tk.Toplevel):

    _instance = None

    def __new__(cls, parent, index=None):
        if cls._instance is not None:
            try:
                if cls._instance.winfo_exists():
                    cls._instance.deiconify()
                    cls._instance.lift()
                    cls._instance.after_idle(cls._instance.focus_set)
                    return cls._instance
            except Exception:
                cls._instance = None
        obj = super().__new__(cls)
        cls._instance = obj
        return obj

    def __init__(self, parent):
        if getattr(self, "_is_init", False):
            self.parent = parent
            return

        super().__init__(name="license")

        self.parent = parent
        self.engine = self.nametowidget(".").engine
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.bind("<Escape>", self.on_cancel)

        self._build_ui()
        self.engine.center_window(self)
        self._is_init = True

    def _build_ui(self):
        main = ttk.Frame(self, padding=8)
        main.pack(fill=tk.BOTH, expand=True)

        # Text widget with scrollbar
        text_frame = ttk.Frame(main)
        text_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.txLicense = tk.Text(
            text_frame,
            width=80,
            height=25,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=("Courier", 9)
        )
        self.txLicense.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.txLicense.yview)

    def on_open(self):
        msg = self.engine.get_license()

        if msg:
            self.txLicense.insert("1.0", msg)
            self.txLicense.config(state=tk.DISABLED)

        self.title("License - GNU GPL v3")

    def on_cancel(self, _evt=None):
        type(self)._instance = None
        self.destroy()
