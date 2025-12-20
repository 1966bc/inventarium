#!/usr/bin/env python3
"""
Idle Monitor - Auto-close application after inactivity.

This module monitors mouse activity and closes the application
after a configurable period of inactivity.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import threading
from time import sleep


class Monitor(threading.Thread):
    """
    Monitor thread that tracks mouse movement and closes app after idle timeout.

    The monitor checks mouse position every second. If the mouse hasn't moved
    for the configured timeout period, it triggers application shutdown.
    """

    def __init__(self, parent, timeout_minutes=30):
        """
        Initialize the idle monitor.

        Args:
            parent: The main Tk window (must have winfo_pointerxy and on_exit methods)
            timeout_minutes: Minutes of inactivity before auto-close (default: 30)
        """
        threading.Thread.__init__(self, daemon=True)

        self.parent = parent
        self.timeout_minutes = timeout_minutes
        self.check = True
        self.idle = 0
        self.old_coord = None

    def stop(self):
        """Stop the monitor thread."""
        self.check = False

    def set_timeout(self, minutes):
        """Update timeout value."""
        self.timeout_minutes = minutes
        self.idle = 0  # Reset idle counter

    def reset(self):
        """Reset idle counter (call on user activity)."""
        self.idle = 0

    def run(self):
        """Main monitoring loop."""
        timeout_seconds = self.timeout_minutes * 60

        while self.check:
            if not self.check:
                break

            try:
                # Get current mouse position
                coord = self.parent.winfo_pointerxy()

                if self.old_coord != coord:
                    # Mouse moved - reset idle counter
                    self.old_coord = coord
                    self.idle = 0
                else:
                    # Mouse not moved - increment idle counter
                    self.idle += 1

                # Check if timeout reached
                if self.idle >= timeout_seconds:
                    self.check = False
                    # Schedule exit on main thread
                    self.parent.after(100, self._trigger_exit)
                else:
                    sleep(1)

            except Exception:
                # Window might be destroyed
                self.check = False
                break

    def _trigger_exit(self):
        """Trigger silent application exit from main thread (idle timeout)."""
        try:
            if hasattr(self.parent, 'on_exit'):
                self.parent.on_exit(silent=True)
        except Exception:
            pass
