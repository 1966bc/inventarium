# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Inventarium is a laboratory inventory management system built with Python 3 and Tkinter. It manages a four-level hierarchy: Products → Packages (SKUs) → Batches (lots) → Labels (individual stock units with barcodes). The application uses SQLite for data storage.

**Repository:** https://github.com/1966bc/inventarium

## Running the Application

```bash
source venv/bin/activate
python3 inventarium.py
```

To test core engine functionality without GUI:
```bash
python3 engine.py
```

### Requirements

Python 3.11+, Tkinter (usually included), Pillow, python-barcode

```bash
pip install -r requirements.txt
```

## Architecture

### Mixin-Based Engine Pattern

```
Engine (engine.py)
   ├── DBMS (dbms.py)         - SQLite connection, dict-based results
   ├── Controller (controller.py) - Domain queries, SQL builders
   ├── Tools (tools.py)       - Widget factories, validation, styling
   └── Launcher (launcher.py) - Cross-platform file opener
```

**Engine** is the central orchestrator accessed via `self.engine = self.nametowidget(".").engine` in all views.

### Application Bootstrap

`inventarium.py` → Creates `App(tk.Tk)` → Loads `config.ini` → Initializes `Engine(db_path)` → Opens `Main` window

### Database Operations

```python
# Read single row (returns dict or None)
row = self.engine.read(False, "SELECT * FROM products WHERE product_id = ?", (pk,))

# Read multiple rows (returns list of dicts)
rows = self.engine.read(True, "SELECT * FROM products WHERE status = 1")

# Write (returns lastrowid or rowcount)
result = self.engine.write("INSERT INTO products (reference, description) VALUES (?, ?)", args)

# Auto-generate SQL from table schema (PK assumed as first column)
sql = self.engine.build_sql("products", "insert")  # or "update"

# Get/set application settings
lang = self.engine.get_setting("language", "it")
self.engine.set_setting("language", "en")
```

### View Pattern

All dialog windows (in `views/`):
1. Inherit from `tk.Toplevel`
2. Access engine via `self.engine = self.nametowidget(".").engine`
3. Store parent reference: `self.parent = parent`
4. Implement `on_open(selected_item=None)` for initialization
5. Implement `on_save()` and `on_cancel()` for form handling
6. Use `self.engine.center_window(self)` for positioning

Example dialog structure:
```python
class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="dialog_name")
        self.parent = parent
        self.index = index  # None for new, row index for edit
        self.engine = self.nametowidget(".").engine
        # ... init UI ...

    def on_open(self, selected_item=None):
        if self.index is not None and selected_item:
            # Edit mode
            self.set_values()
        else:
            # New item mode
```

### Window Instance Registry

Engine maintains `dict_instances` to track open windows:
```python
self.engine.dict_instances["products"] = window_instance
```

Use `refresh_windows_for_table(table_name)` to trigger cross-window updates after data changes.

## Multi-language Support

Uses `i18n.py` with the `_()` function. Italian is the primary language.

```python
from i18n import _

label = _("Prodotti")  # Returns translated string based on current language
```

Languages: Italian (it), English (en), Spanish (es). Add translations to the `TRANSLATIONS` dict in `i18n.py`.

## Key Constants

### Label Status Values

| Status | Meaning |
|--------|---------|
| 1 | In stock |
| 0 | Used/Dispatched |
| -1 | Cancelled |

### Database Tables

`products`, `packages`, `batches`, `labels`, `requests`, `items`, `deliveries`, `suppliers`, `categories`, `locations`, `conservations`, `funding_sources`, `settings`

## Configuration

Database path configured in `config.ini`:
```ini
[database]
path = sql/inventarium.db
```

Reset to demo data:
```bash
sqlite3 sql/inventarium.db ".read sql/demo_data.sql"
```

## UI Conventions

- Use `ttk.Button` with `App.TButton` style via `self.engine.create_button()`
- Standard keyboard bindings: `Alt+S` (Save), `Alt+C` (Close), `Escape` (Cancel), `Return` (Submit)
- All user-facing strings should use `_()` for translation
