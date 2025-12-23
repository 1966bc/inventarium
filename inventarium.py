#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventarium - Laboratory Inventory Management System.

Entry point for the Inventarium application.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from app_config import load_db_path, save_db_path, log_to_file, APP_ICON
from engine import Engine
from views.main import Main
from views.config_dialog import ConfigDialog
from monitor import Monitor

__author__ = "1966bc"
__copyright__ = "Copyleft"
__credits__ = ["hal9000", ]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "I"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "ver MMXXV"
__status__ = "Beta"


class App(tk.Tk):
    """
    Main application class for Inventarium.

    Initializes the database engine and opens the main window.
    """

    def __init__(self):
        super().__init__()

        self.withdraw()  # Hide root window

        self.title("Inventarium")

        # Get database path from config
        db_path = load_db_path()

        # If no config or path not found, show config dialog
        if db_path is None or not os.path.exists(db_path):
            if db_path is None:
                log_to_file("No config.ini found, showing config dialog")
            else:
                log_to_file(f"Database not found at {db_path}, showing config dialog")

            # Show config dialog (deiconify needed for transient to work)
            self.deiconify()
            icon = tk.PhotoImage(data=APP_ICON)
            self.call("wm", "iconphoto", self._w, "-default", icon)
            dialog = ConfigDialog(self)
            self.wait_window(dialog)
            self.withdraw()  # Hide again after dialog closes

            if dialog.result is None:
                # User cancelled
                self.destroy()
                return

            db_path = dialog.result

            # Make path absolute if relative
            if not os.path.isabs(db_path):
                db_path = os.path.join(os.path.dirname(__file__), db_path)

            # Save to config
            save_db_path(dialog.result)

        # Final check
        if not os.path.exists(db_path):
            messagebox.showerror(
                "Inventarium",
                f"Database non trovato:\n{db_path}"
            )
            self.destroy()
            return

        log_to_file(f"Using database: {db_path}")

        self.engine = Engine(db_path)
        self.set_style()
        self.set_icon()

        # Build info string
        self.info = (
            f"Inventarium\n\n"
            f"Version: {__version__}\n"
            f"Author: {__author__}\n"
            f"License: {__license__}"
        )

        self._exit_in_progress = False
        self.monitor = None

        # Open main window
        main = Main(self)
        main.on_open()

        # Start idle monitor (auto-close after inactivity)
        self._start_monitor()

    def set_style(self) -> None:
        """Initialize and configure TTK style themes."""
        self.style = ttk.Style()
        self.engine.set_style(self.style)

    def set_icon(self) -> None:
        """Load and set application icon from engine."""
        icon = tk.PhotoImage(data=self.engine.get_icon())
        self.call("wm", "iconphoto", self._w, "-default", icon)

    def _start_monitor(self):
        """Start the idle monitor thread."""
        try:
            # Get timeout from settings (default 30 minutes)
            timeout = int(self.engine.get_setting("idle_timeout", 30))
            if timeout > 0:
                self.monitor = Monitor(self, timeout_minutes=timeout)
                self.monitor.start()
        except Exception:
            pass

    def on_about(self):
        """Show about dialog."""
        messagebox.showinfo("Inventarium", self.info)

    def on_exit(self, evt=None, silent=False):
        """Handle application exit.

        Args:
            evt: Event object (optional)
            silent: If True, close without asking confirmation (e.g., idle timeout)
        """
        if self._exit_in_progress:
            return

        self._exit_in_progress = True

        # Stop idle monitor
        if self.monitor:
            self.monitor.stop()

        # Ask confirmation only if not silent
        if not silent:
            msg = "Do you want to quit Inventarium?"
            if not messagebox.askokcancel("Inventarium", msg):
                self._exit_in_progress = False
                # Restart monitor if user cancels
                if self.monitor:
                    self._start_monitor()
                return

        # Cleanup and exit
        try:
            if self.engine:
                self.engine.rotate_log()
                self.engine.cleanup_barcodes()
                self.engine.close()
        except Exception:
            pass

        self.quit()


def main():
    """Application entry point."""
    log_to_file("=" * 60)
    log_to_file("Inventarium starting...")
    log_to_file("=" * 60)

    try:
        app = App()
        app.mainloop()
    except Exception as e:
        log_to_file(f"Fatal error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        messagebox.showerror("Inventarium", f"Fatal error:\n{e}")
    finally:
        log_to_file("Inventarium terminated.")


if __name__ == "__main__":
    main()
