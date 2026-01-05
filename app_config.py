#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration module for Inventarium.

Handles loading and saving of config.ini settings,
particularly the database path.

Author: 1966bc (Giuseppe Costanzi)
License: GNU GPL v3
Version: I (SQLite Edition)
"""
import os
import datetime
import configparser

# Configuration file
CONFIG_FILE = "config.ini"
# Default database path (fallback)
DEFAULT_DB_PATH = "sql/inventarium.db"
# User config directory (for system-wide install)
USER_CONFIG_DIR = os.path.expanduser("~/.config/inventarium")

# Application icon (base64 PNG)
APP_ICON = (
    "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAC1klEQVR4nO2dQVLjMBQFwxS3"
    "YS7AbODozAYuAOdhVlBMYtmSreRLv7tXUGDj8FpP3xQVn04iIiJC5K73CV8eHz57n1P+5/nt"
    "o1tuXU5k6HEcleHQwQY/DntF2HWQwY9Lqwi/Wn+A4Y9Naz5NAhj+HLTkVC2A4c9FbV5VAhj+"
    "nNTktimA4c/NVn6rAhh+DtZybL4LkFwUBXD156KUpw0AZ1EAV39OlnK1AeAoAJwLAaz/3Jzn"
    "awPAUQA499EXEMnT6/v3x3///A68kjiwDfAz/KXPKeAaYC3or6+R2gDVALWrnNQGiAbYEyil"
    "DVI3wNPrezH882BLQa+dIwMpBdgKrRT22mrPKkKqLWAroJo6//qe0rmybQ1pGmBrxbcGtnVM"
    "ljaYvgH2VH0La42QoQ2mFeDawZfOmU2E6baAvQNeL7INitM0QI8BrxeZBsUpGqD3gNeLDIPi"
    "0A0QWfUtzDwfDCnALMGfM6MIQ20B0QNeL2YaFC/eTCDifwJH+oXcmgipf76JRHgDkMM/neJf"
    "f9gMEP3CRyJyPri5AAZfJkKE8C1AYlEAOAoAJ/wPQbPc21+TyLnIBoCjAHAUAI4CwFEAOAoA"
    "RwHgKAAcBYCjAHAUAI4CwFEAOAoARwHgKAAcBYCjAHAUAI4CwFEAOAoARwHgKAAcBYCjAHAU"
    "AI4CwFEAOAoARwHgKAAcBYCjAHAUAI4CwFEAOAoARwHgKAAcBYCjAHAUAI4CwFEAOAoARwHg"
    "KAAcBYAT/sQQnyIWiw0ARwHgKACcm88APiVsLGwAOAoARwHgKAAcBYCjAHAUAM6FAM9vH3cR"
    "FyK34TxfGwCOAsBZFMBtICdLudoAcIoC2AK5KOVpA8BZFcAWyMFajpsNoARzs5Vf1RagBHNS"
    "k1v1DKAEc1GbV9MQqARz0JJT812AEoxNaz6Hwnx5fPg8crz0Y+/C7LKaFSGOo43cvc6V4fq4"
    "DYuISAf+AcyfAPRv+BokAAAAAElFTkSuQmCC"
)


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
    """
    Get the full path to config.ini.

    Search order:
    1. ~/.config/inventarium/config.ini (user config, for system install)
    2. ./config.ini (local development)
    """
    # First check user config directory (for system-wide install)
    user_config = os.path.join(USER_CONFIG_DIR, CONFIG_FILE)
    if os.path.exists(user_config):
        return user_config

    # Then check app directory (for local development)
    app_config = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    if os.path.exists(app_config):
        return app_config

    # If neither exists, prefer user config directory (will be created)
    if os.path.exists(USER_CONFIG_DIR):
        return user_config

    # Fallback to app directory (local development)
    return app_config


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
    # Prefer user config directory for saving
    if os.path.exists(USER_CONFIG_DIR):
        config_path = os.path.join(USER_CONFIG_DIR, CONFIG_FILE)
    else:
        config_path = get_config_path()

    config = configparser.ConfigParser()

    # Preserve existing config if present
    if os.path.exists(config_path):
        config.read(config_path)

    if "database" not in config:
        config.add_section("database")

    config.set("database", "path", db_path)

    try:
        # Create user config directory if needed
        config_dir = os.path.dirname(config_path)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir)

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
