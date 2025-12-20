#!/usr/bin/env python3
"""
Launcher Mixin - Cross-platform file opener for Inventarium.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import os
import sys
import subprocess


class Launcher:
    """Mixin for opening files with default system application."""

    def launch(self, path):
        """
        Open a file with the default system application.

        Args:
            path: Path to file to open

        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(path):
                return False

            if sys.platform == "win32":
                os.startfile(path)
                return True
            elif sys.platform == "darwin":
                subprocess.call(["open", path])
                return True
            else:
                # Linux
                ret = subprocess.call(["xdg-open", path])
                return ret == 0

        except Exception as e:
            if hasattr(self, 'on_log'):
                self.on_log("launch", str(e), type(e).__name__)
            return False                
