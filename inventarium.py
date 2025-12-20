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
import sys
import datetime
import configparser
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from engine import Engine
from views.main import Main
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

# Configuration file
CONFIG_FILE = "config.ini"
# Default database path (fallback)
DEFAULT_DB_PATH = "sql/inventarium.db"


def log_to_file(message: str, level: str = "INFO") -> None:
    """Simple logging before Engine is available."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} - inventarium.py - {level} - {message}\n"
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(log_line)
        print(f"[{level}] {message}")
    except Exception:
        pass


def get_config_path() -> str:
    """Get the full path to config.ini."""
    return os.path.join(os.path.dirname(__file__), CONFIG_FILE)


def load_db_path() -> str:
    """
    Load database path from config.ini.

    Returns:
        str: Database path (absolute or relative to app directory)
    """
    config_path = get_config_path()

    if not os.path.exists(config_path):
        # Try to create from template
        template_path = os.path.join(os.path.dirname(__file__), "config.ini.example")
        if os.path.exists(template_path):
            try:
                import shutil
                shutil.copy(template_path, config_path)
                log_to_file("Created config.ini from template")
            except Exception as e:
                log_to_file(f"Could not create config.ini from template: {e}", "WARNING")
                return None
        else:
            return None

    config = configparser.ConfigParser()
    config.read(config_path)

    try:
        db_path = config.get("database", "path")
        # If relative path, make it absolute relative to app directory
        if not os.path.isabs(db_path):
            db_path = os.path.join(os.path.dirname(__file__), db_path)
        return db_path
    except (configparser.NoSectionError, configparser.NoOptionError):
        return None


def save_db_path(db_path: str) -> bool:
    """
    Save database path to config.ini.

    Args:
        db_path: Path to the database file

    Returns:
        bool: True if saved successfully
    """
    config_path = get_config_path()
    config = configparser.ConfigParser()

    # Preserve existing config if present
    if os.path.exists(config_path):
        config.read(config_path)

    if "database" not in config:
        config.add_section("database")

    config.set("database", "path", db_path)

    try:
        with open(config_path, "w") as f:
            f.write("[database]\n")
            f.write("# Percorso del database SQLite\n")
            f.write("# Può essere relativo alla cartella dell'applicazione o assoluto\n")
            f.write("# Esempi:\n")
            f.write("#   path = sql/inventarium.db                    (locale, sviluppo)\n")
            f.write("#   path = /mnt/share/inventarium/inventarium.db (cartella condivisa)\n")
            f.write("#   path = //server/share/inventarium.db         (UNC Windows)\n")
            f.write(f"path = {db_path}\n")
        return True
    except Exception as e:
        log_to_file(f"Error saving config: {e}", "ERROR")
        return False


class ConfigDialog(tk.Toplevel):
    """Dialog for configuring database path."""

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.result = None

        self.title("Configurazione Database")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self.db_path = tk.StringVar(value=DEFAULT_DB_PATH)

        self.init_ui()
        self.center_on_screen()

    def center_on_screen(self):
        """Center dialog on screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"+{x}+{y}")

    def init_ui(self):
        """Build dialog UI."""
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Message
        msg = ttk.Label(
            frame,
            text="Configurazione del percorso database.\n\n"
                 "Selezionare il file database SQLite (.db)\n"
                 "o inserire manualmente il percorso.",
            justify=tk.LEFT
        )
        msg.pack(fill=tk.X, pady=(0, 15))

        # Path entry with browse button
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill=tk.X, pady=5)

        ttk.Label(path_frame, text="Percorso:").pack(side=tk.LEFT)

        self.entry = ttk.Entry(path_frame, textvariable=self.db_path, width=50)
        self.entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Button(
            path_frame,
            text="Sfoglia...",
            command=self.on_browse
        ).pack(side=tk.LEFT)

        # Test connection button and status
        test_frame = ttk.Frame(frame)
        test_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            test_frame,
            text="Test Connessione",
            command=self.on_test_connection
        ).pack(side=tk.LEFT)

        self.test_status = tk.StringVar()
        self.lbl_status = ttk.Label(test_frame, textvariable=self.test_status)
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(
            btn_frame,
            text="OK",
            command=self.on_ok,
            width=10
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            btn_frame,
            text="Annulla",
            command=self.on_cancel,
            width=10
        ).pack(side=tk.RIGHT)

        self.bind("<Return>", self.on_ok)
        self.bind("<Escape>", self.on_cancel)

    def on_test_connection(self):
        """Test database connection."""
        import sqlite3

        path = self.db_path.get().strip()
        if not path:
            self.test_status.set("Inserire un percorso")
            self.lbl_status.configure(foreground="red")
            return

        # Make path absolute if relative
        check_path = path
        if not os.path.isabs(check_path):
            check_path = os.path.join(os.path.dirname(__file__), check_path)

        # Check file exists
        if not os.path.exists(check_path):
            self.test_status.set("File non trovato")
            self.lbl_status.configure(foreground="red")
            return

        # Try to connect and query
        try:
            con = sqlite3.connect(check_path)
            cursor = con.cursor()

            # Check if it's a valid Inventarium database by checking for key tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
            if cursor.fetchone() is None:
                self.test_status.set("Database non valido (tabella products mancante)")
                self.lbl_status.configure(foreground="orange")
                con.close()
                return

            # Count products as a simple test
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]

            con.close()

            self.test_status.set(f"OK - {count} prodotti trovati")
            self.lbl_status.configure(foreground="green")

        except sqlite3.Error as e:
            self.test_status.set(f"Errore: {e}")
            self.lbl_status.configure(foreground="red")
        except Exception as e:
            self.test_status.set(f"Errore: {e}")
            self.lbl_status.configure(foreground="red")

    def on_browse(self):
        """Browse for database file."""
        initial_dir = os.path.dirname(self.db_path.get()) or os.path.dirname(__file__)

        filename = filedialog.askopenfilename(
            parent=self,
            title="Seleziona Database",
            initialdir=initial_dir,
            filetypes=[
                ("SQLite Database", "*.db"),
                ("Tutti i file", "*.*")
            ]
        )

        if filename:
            self.db_path.set(filename)

    def on_ok(self, evt=None):
        """Validate and accept."""
        path = self.db_path.get().strip()

        if not path:
            messagebox.showwarning(
                "Configurazione",
                "Inserire un percorso valido.",
                parent=self
            )
            return

        # Check if file exists
        check_path = path
        if not os.path.isabs(check_path):
            check_path = os.path.join(os.path.dirname(__file__), check_path)

        if not os.path.exists(check_path):
            if not messagebox.askyesno(
                "Configurazione",
                f"Il file non esiste:\n{check_path}\n\nContinuare comunque?",
                parent=self
            ):
                return

        self.result = path
        self.destroy()

    def on_cancel(self, evt=None):
        """Cancel dialog."""
        self.result = None
        self.destroy()


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

            # Show config dialog
            dialog = ConfigDialog(self)
            self.wait_window(dialog)

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
