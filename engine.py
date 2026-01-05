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


class _EngineMeta(type):
    """
    Metaclass that ensures only one Engine instance exists.

    This implements the Singleton pattern at the metaclass level,
    intercepting instance creation before __new__ and __init__ are called.

    How it works:
        1. First call to Engine(...) creates and stores the instance
        2. Subsequent calls return the stored instance, ignoring new arguments

    Attributes:
        _instance: The single Engine instance, or None if not yet created

    Example:
        >>> engine1 = Engine("db.sqlite")
        >>> engine2 = Engine("other.db")  # Returns same instance!
        >>> engine1 is engine2
        True
    """

    _instance = None

    def __call__(cls, *args, **kwargs):
        """
        Intercept instance creation.

        Returns the existing instance if one exists, otherwise creates
        a new one using the normal class instantiation process.
        """
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Engine(DBMS, Controller, Tools, Launcher, metaclass=_EngineMeta):
    """
    Main orchestrator for Inventarium.

    Combines all system components via mixin inheritance to provide
    a unified interface for all application functionality.

    Singleton:
        Engine uses _EngineMeta metaclass to ensure only one instance exists.
        Multiple calls to Engine() return the same instance.

    Mixin Architecture (in MRO order):
        1. DBMS: Database connection and query execution
        2. Controller: SQL builders and domain logic
        3. Tools: Shared utility functions
        4. Launcher: Cross-platform file opener

    Observer Pattern:
        Engine provides an event system for decoupled view communication:
        - subscribe(event, callback): Register for an event
        - unsubscribe(event, callback): Unregister from an event
        - notify(event, data): Emit an event to all subscribers

        Events:
        - "stock_changed": Fired when stock is modified (delivery)
        - "label_unloaded": Fired when a label is unloaded (barcode)
        - "batch_cancelled": Fired when a batch is cancelled (expiring)
        - "category_changed": Fired when a category is modified (category)
        - "package_changed": Fired when a package is modified (package)
        - "request_changed": Fired when a request is modified (requests)

    Attributes:
        dict_instances (dict): Registry of open GUI windows for singleton management
        _subscribers (dict): Event subscribers registry
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

        # Event system: event_name -> [callbacks]
        self._subscribers = {}

        # Initialize i18n from settings
        self._init_i18n()

        # App info
        self.title = APP_TITLE
        self.app_title = APP_TITLE

        # UI settings
        self.entry_width = 20

        # Standard messages (translated)
        self.ask_to_save = _("Do you want to save?")
        self.abort = _("Operation cancelled.")
        self.no_selected = _("Select an element!")

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

    # -------------------------------------------------------------------------
    # Observer Pattern: Event System
    # -------------------------------------------------------------------------

    def subscribe(self, event: str, callback) -> None:
        """
        Register a callback for an event.

        Views call this to receive notifications when something changes.
        Remember to unsubscribe in on_cancel() to avoid dead references.

        Args:
            event: Event name (e.g., "stock_changed", "request_changed")
            callback: Function to call when event fires

        Example:
            # In warehouse.__init__:
            self.engine.subscribe("stock_changed", self.on_stock_changed)
        """
        if event not in self._subscribers:
            self._subscribers[event] = []
        if callback not in self._subscribers[event]:
            self._subscribers[event].append(callback)

    def unsubscribe(self, event: str, callback) -> None:
        """
        Remove a callback from an event.

        Call this in on_cancel() before the window closes.

        Args:
            event: Event name
            callback: Function to remove
        """
        if event in self._subscribers:
            try:
                self._subscribers[event].remove(callback)
            except ValueError:
                pass

    def notify(self, event: str, data=None) -> None:
        """
        Notify all subscribers of an event.

        Views call this after making changes that other views might
        need to know about. Subscribers receive the event asynchronously.

        Args:
            event: Event name
            data: Optional data to pass to callbacks

        Example:
            # In delivery after saving:
            self.engine.notify("stock_changed")
        """
        for callback in self._subscribers.get(event, []):
            try:
                callback(data)
            except Exception:
                # Subscriber might be dead or have errors, ignore
                pass

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

    def get_printer_name(self) -> str:
        """Get the label printer name for this workstation."""
        config_path = self._get_config_path()

        if not os.path.exists(config_path):
            return ""  # Default to system default printer

        config = configparser.ConfigParser()
        config.read(config_path)

        try:
            return config.get("printer", "name", fallback="")
        except (configparser.NoSectionError, configparser.NoOptionError):
            return ""

    def set_printer_name(self, name: str) -> bool:
        """Set the label printer name for this workstation."""
        config_path = self._get_config_path()

        config = configparser.ConfigParser()
        if os.path.exists(config_path):
            config.read(config_path)

        if not config.has_section("printer"):
            config.add_section("printer")

        config.set("printer", "name", name.strip())

        try:
            with open(config_path, "w") as f:
                config.write(f)
            return True
        except Exception as e:
            self.on_log("set_printer_name", e, type(e), __import__(__name__))
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
