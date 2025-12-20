# -*- coding: utf-8 -*-
"""
Tools Module - Style and utilities for Inventarium.

This module provides style configuration and helper methods.
Used as a mixin class inherited by Engine.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import tkinter as tk
from tkinter import ttk
from typing import List


class Tools:
    """Style configuration and utilities."""

    BASE_BG_RGB = (240, 240, 237)

    def __init__(self) -> None:
        """Initialize shared style instance."""
        self._style = ttk.Style()

    def __str__(self) -> str:
        return f"class: {self.__class__.__name__}"

    def set_style(self, style: ttk.Style) -> None:
        """Set a unified theme and styles for the application widgets."""
        style.theme_use("clam")

        bg_color = self.get_rgb(*self.BASE_BG_RGB)
        style.configure(".", background=bg_color, font=('TkFixedFont'))

        # Treeview styling
        style.map('Treeview',
                  foreground=self.fixed_map('foreground'),
                  background=self.fixed_map('background'))

        style.configure("Treeview.Heading",
                        background=bg_color,
                        font=("TkFixedFont", 10))

        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # StatusBar styling
        style.configure("StatusBar.TFrame",
                        relief=tk.FLAT,
                        padding=4,
                        background=bg_color)

        style.configure("StatusBar.TLabel",
                        background=bg_color,
                        padding=2,
                        relief=tk.SUNKEN,
                        font="TkFixedFont")

        # Application widget styles
        style.configure("App.TLabel",
                        background=bg_color,
                        padding=2,
                        anchor=tk.W,
                        font="TkFixedFont")

        style.configure("App.TLabelframe",
                        background=bg_color,
                        relief=tk.GROOVE,
                        padding=2,
                        font="TkFixedFont")

        style.configure("App.TLabelframe.Label",
                        background=bg_color,
                        font="TkFixedFont")

        style.configure("Buttons.TFrame",
                        background=bg_color,
                        padding=8,
                        relief=tk.GROOVE)

        style.configure("App.TRadiobutton",
                        background=bg_color,
                        padding=4,
                        font="TkFixedFont")

        style.configure("App.TCheckbutton",
                        background=bg_color,
                        padding=4,
                        font="TkFixedFont")

        style.configure("App.TCombobox",
                        font="TkFixedFont")

    def create_button(self, parent, text: str, command, width: int = 10,
                       underline: int = 0, **kwargs) -> tk.Button:
        """
        Create a standard application button.

        Args:
            parent: Parent widget
            text: Button text
            command: Callback function
            width: Button width (default 10)
            underline: Index of character to underline for Alt+key (default 0)
            **kwargs: Additional button options

        Returns:
            tk.Button with standard application style
        """
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            underline=underline,
            font="TkFixedFont",
            relief=tk.RAISED,
            padx=5,
            pady=5,
            borderwidth=1,
            **kwargs
        )
        return btn

    def get_rgb(self, r: int, g: int, b: int) -> str:
        """Convert RGB integers to a Tkinter-friendly hex color."""
        return "#%02x%02x%02x" % (r, g, b)

    def get_base_bg_color_hex(self) -> str:
        """Returns the application's base background color in Tkinter hex format."""
        return self.get_rgb(*self.BASE_BG_RGB)

    def fixed_map(self, option: str) -> List[tuple]:
        """Fix style map for Treeview to support themed widgets in Tk 8.6.9."""
        style = ttk.Style()
        return [elm for elm in style.map('Treeview', query_opt=option)]

    def get_validate_integer(self, caller) -> tuple:
        """Return validation tuple for integer fields."""
        return (caller.register(self.validate_integer), '%d', '%P', '%S')

    def validate_integer(self, action: str, value_if_allowed: str, text: str) -> bool:
        """Validate integer input in real time."""
        if action == '1':  # Insert
            if text in '0123456789':
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            return False
        return True

    def get_validate_float(self, caller) -> tuple:
        """Return validation tuple for float fields."""
        return (caller.register(self.validate_float), '%d', '%P', '%S')

    def validate_float(self, action: str, value_if_allowed: str, text: str) -> bool:
        """Validate float input in real time. Accepts comma or dot as decimal separator."""
        if action == '1':  # Insert
            if text in '0123456789.,':
                # Replace comma with dot for validation
                test_value = value_if_allowed.replace(',', '.')
                # Allow single dot/comma even if not yet a valid float
                if test_value == '.' or test_value == '':
                    return True
                try:
                    float(test_value)
                    return True
                except ValueError:
                    return False
            return False
        return True

    @staticmethod
    def clean_text(value: str, compress: bool = True) -> str:
        """
        Normalize a textual input.

        Operations:
            - Strip leading/trailing whitespace.
            - Optionally collapse multiple internal spaces.

        Args:
            value: Raw string value.
            compress: If True, collapse multiple spaces into a single one.

        Returns:
            Normalized string (empty string if input is falsy).
        """
        if not value:
            return ""

        s = value.strip()

        if compress:
            s = " ".join(s.split())

        return s

    def center_window(self, window) -> None:
        """Center a window relative to its parent."""
        window.update_idletasks()
        parent = window.parent
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        width = window.winfo_width()
        height = window.winfo_height()
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        window.geometry(f"+{x}+{y}")
