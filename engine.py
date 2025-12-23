#!/usr/bin/env python3
"""
Engine Module - Main Orchestrator for Inventarium.

This module provides the Engine class, which serves as the central orchestrator
combining all system components through multiple inheritance (mixin architecture).

Architecture (Mixin Pattern):
    Engine combines multiple specialized mixins:
    - DBMS: Database connection and query execution
    - Controller: SQL builders and domain logic
    - Tools: Shared utility functions
    - Launcher: Cross-platform file opener

Key Responsibilities:
    - Global state management
    - Window registry (dict_instances: track open GUI windows)
    - Cross-component communication and coordination
    - Error logging (on_log method)

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import os
import sys
import traceback
import datetime
import time
import configparser
from typing import Optional

from tools import Tools
from dbms import DBMS
from controller import Controller
from launcher import Launcher
from app_config import APP_ICON
from i18n import set_language, _

APP_TITLE = "Inventarium"


class Engine(DBMS, Controller, Tools, Launcher):
    """
    Main orchestrator for Inventarium.

    Combines all system components via mixin inheritance to provide
    a unified interface for all application functionality.

    Mixin Architecture (in MRO order):
        1. DBMS: Database connection and query execution
        2. Controller: SQL builders and domain logic
        3. Tools: Shared utility functions
        4. Launcher: Cross-platform file opener

    Attributes:
        dict_instances (dict): Registry of open GUI windows for singleton management
        title (str): Application title
        entry_width (int): Standard entry width for forms

    Example:
        >>> engine = Engine("sql/inventarium.db")
        >>> stock = engine.get_stock()
        >>> for item in stock:
        ...     print(f"{item['product_name']}: {item['in_stock']}")
    """

    def __init__(self, database: str, autocommit: bool = True):
        super().__init__(database=database, autocommit=autocommit)

        # Windows registry: name -> widget
        self.dict_instances = {}

        # Initialize i18n from settings
        self._init_i18n()

        # App info
        self.title = APP_TITLE
        self.app_title = APP_TITLE

        # UI settings
        self.entry_width = 20

        # Standard messages (translated)
        self.ask_to_save = _("Vuoi salvare?")
        self.abort = _("Operazione annullata.")
        self.no_selected = _("Seleziona un elemento!")

    def _init_i18n(self):
        """Initialize internationalization from settings."""
        lang = self.get_setting("language", "it")
        set_language(lang)

    def get_instance(self, name):
        """
        Get a registered window instance by name.

        If the instance exists and is still alive, brings it to front
        and returns it. Otherwise returns None.

        Use this for ParentView windows where you want to reuse
        the existing window instead of creating a new one.

        Args:
            name: Window name as registered in dict_instances

        Returns:
            The window instance if alive, None otherwise
        """
        instance = self.dict_instances.get(name)
        if instance is not None:
            try:
                if instance.winfo_exists():
                    instance.lift()
                    instance.focus_set()
                    return instance
            except Exception:
                pass
            # Dead reference, clean up
            self.dict_instances.pop(name, None)
        return None

    def close_instance(self, name):
        """
        Close a registered window instance by name.

        If the instance exists and is still alive, closes it.
        Use this for ChildView dialogs before creating a new one
        to switch context (e.g., editing a different record).

        Args:
            name: Window name as registered in dict_instances
        """
        instance = self.dict_instances.get(name)
        if instance is not None:
            try:
                if instance.winfo_exists():
                    instance.on_cancel()
            except Exception:
                pass
            # Ensure cleanup
            self.dict_instances.pop(name, None)

    def __str__(self):
        return "class: {0}\nMRO: {1}".format(
            self.__class__.__name__,
            [x.__name__ for x in Engine.__mro__]
        )

    def get_log_file(self):
        """Open log file in default application."""
        path = self.get_file("log.txt")
        self.launch(path)

    def on_log(self, function, exc_value, exc_type, module, caller=None):
        """
        Write error to log.txt.

        Args:
            function: Name of the function where error occurred
            exc_value: Exception value
            exc_type: Exception type
            module: Module where error occurred
            caller: Optional caller information
        """
        try:
            now = datetime.datetime.now().astimezone()
            ts = now.isoformat(sep=" ", timespec="seconds")
            module_name = getattr(module, "__name__", str(module))
            tb_text = traceback.format_exc()

            header = f"{ts}\n{type(self).__name__}.{function}"
            if caller:
                header += f"  (caller: {caller})"

            log_text = (
                f"{header}\n"
                f"{exc_type.__name__}: {exc_value}\n"
                f"{module_name}\n"
                f"{tb_text}\n"
            )

            path = self.get_file("log.txt")
            with open(path, "a", encoding="utf-8", errors="backslashreplace") as fh:
                fh.write(log_text)

        except Exception:
            pass

    def rotate_log(self, max_size_kb=500):
        """
        Rotate log file if it exceeds max size.

        Args:
            max_size_kb: Maximum log size in KB before rotation (default 500)
        """
        try:
            path = self.get_file("log.txt")
            if not os.path.exists(path):
                return

            size = os.path.getsize(path)
            max_bytes = max_size_kb * 1024

            if size > max_bytes:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                keep_lines = lines[len(lines) // 2:]

                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"--- Log rotated {datetime.datetime.now().isoformat()} ---\n")
                    f.writelines(keep_lines)

        except Exception:
            pass

    def cleanup_barcodes(self):
        """Remove all barcode images from barcodes directory."""
        try:
            barcodes_dir = self.get_file("barcodes")
            if not os.path.exists(barcodes_dir):
                return

            for filename in os.listdir(barcodes_dir):
                if filename.endswith(".png"):
                    filepath = os.path.join(barcodes_dir, filename)
                    try:
                        os.remove(filepath)
                    except Exception:
                        pass

        except Exception:
            pass

    def get_python_version(self) -> str:
        """Return Python version string."""
        return "Python version: %s" % ".".join(map(str, sys.version_info[:3]))

    def get_file(self, filename: str) -> str:
        """Return full path of file in program directory."""
        return os.path.join(os.path.dirname(__file__), filename)

    def busy(self, caller):
        """Set busy cursor on widget."""
        caller.config(cursor="watch")

    def not_busy(self, caller):
        """Reset cursor on widget."""
        caller.config(cursor="")

    def get_license(self) -> Optional[str]:
        """Get license text from LICENSE file."""
        try:
            path = self.get_file("LICENSE")
            with open(path, "r") as f:
                return f.read()
        except Exception:
            return None

    def get_date(self) -> str:
        """Return current date as YYYY-MM-DD (ISO format)."""
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def get_today(self) -> str:
        """Return current date as DD-MM-YYYY (display format)."""
        return datetime.datetime.now().strftime("%d-%m-%Y")

    def get_icon(self) -> str:
        """Return embedded application icon as base64 PNG."""
        return APP_ICON

    def get_entry_width(self) -> int:
        """Return standard entry width for forms."""
        return self.entry_width

    def get_tick(self) -> int:
        """Return current timestamp in microseconds."""
        return int(time.time() * 1e6)

    def _get_config_path(self) -> str:
        """Return full path to config.ini."""
        return self.get_file("config.ini")

    def is_printer_enabled(self) -> bool:
        """Check if label printing is enabled on this workstation."""
        config_path = self._get_config_path()

        if not os.path.exists(config_path):
            return True  # Default to enabled

        config = configparser.ConfigParser()
        config.read(config_path)

        try:
            return config.getboolean("printer", "enabled", fallback=True)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return True

    def set_printer_enabled(self, enabled: bool) -> bool:
        """Set label printing enabled/disabled on this workstation."""
        config_path = self._get_config_path()

        config = configparser.ConfigParser()
        if os.path.exists(config_path):
            config.read(config_path)

        if not config.has_section("printer"):
            config.add_section("printer")

        config.set("printer", "enabled", "1" if enabled else "0")

        try:
            with open(config_path, "w") as f:
                config.write(f)
            return True
        except Exception as e:
            self.on_log("set_printer_enabled", e, type(e), __import__(__name__))
            return False


def main():
    """Test/debug entry point."""
    engine = Engine("sql/inventarium.db")
    print(engine)
    print()

    print("=== Stock ===")
    stock = engine.get_stock()
    for item in stock[:5]:
        print(f"  {item['product_name']}: {item['in_stock']} in stock")

    print()
    print("=== Expiring (90 days) ===")
    expiring = engine.get_expiring_batches(90)
    for item in expiring[:5]:
        print(f"  {item['product_name']} - {item['lot']}: {item['days_left']} days")

    print()
    print("=== Open Requests ===")
    requests = engine.get_open_requests()
    for req in requests[:5]:
        print(f"  {req['reference']}: {req['qty_delivered']}/{req['qty_ordered']} delivered")

    engine.close()
    print("\nOK!")


if __name__ == "__main__":
    main()
