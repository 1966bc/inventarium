# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Inventarium is a laboratory inventory management system built with Python 3 and Tkinter. It manages products, packages (SKUs), batches (lots), and labels (individual stock units with barcodes) for laboratory consumables. The application uses SQLite for data storage.

**Database tables:** products, packages, batches, labels, requests, items, deliveries, suppliers, categories, locations, conservations, settings

**SQL Views:** v_stock, v_expiring, v_open_requests

## Running the Application

```bash
python3 inventarium.py
```

Or with virtual environment:
```bash
source venv/bin/activate
python3 inventarium.py
```

Requirements: Python 3.11+, Tkinter, Pillow (PIL)

## Architecture

### Mixin-Based Engine Pattern

The core architecture uses Python's multiple inheritance to combine specialized components:

```
Engine (engine.py)
   ├── DBMS (dbms.py)         - SQLite connection, query execution
   ├── Controller (controller.py) - Domain queries, window refresh
   ├── Tools (tools.py)       - Tkinter widget factories (Treeview, Listbox, Toolbar)
   └── Launcher (launcher.py) - Cross-platform file opener (xdg-open/open/startfile)
```

**Engine** is the central orchestrator passed to all views via `self.nametowidget(".").engine`.

### Key Engine Responsibilities
- `dict_instances`: Window registry for singleton enforcement and cross-window refresh
- `on_log()`: Centralized error logging to `log.txt`
- Domain queries: `get_stock()`, `get_expiring_batches()`, `get_open_requests()`
- Label operations: `load_label()`, `unload_label()`, `cancel_label()`, `restore_label()`

### View Pattern

All GUI windows follow this pattern:
1. Inherit from `tk.Toplevel`
2. Access engine via `self.engine = self.nametowidget(".").engine`
3. Register in `engine.dict_instances` for singleton management
4. Implement `on_open()`, `on_cancel()`, and optionally `refresh()`

### Database Schema (SQLite)

Core tables and their relationships:
- **products**: Base product definitions (reference, description)
- **packages**: SKUs linking products to suppliers, categories, locations
- **batches**: Lot/batch records with expiration dates (linked to packages)
- **labels**: Individual stock units with status tracking (linked to batches)
- **requests/items/deliveries**: Purchase order workflow

Label status values: `1` = in stock, `0` = used/dispatched, `-1` = cancelled

Entity hierarchy: `products` → `packages` → `batches` → `labels`

## Key Files

| File | Purpose |
|------|---------|
| `inventarium.py` | Application entry point, creates `App(tk.Tk)` |
| `engine.py` | Main orchestrator combining all mixins |
| `dbms.py` | Database layer with `read()` and `write()` methods |
| `controller.py` | Domain-specific queries and SQL builders |
| `tools.py` | Tkinter widget factories and validation helpers |
| `views/main.py` | Main application window with menu/toolbar |
| `views/warehouse.py` | Primary inventory management interface |
| `calendarium.py` | Reusable date picker widget |

## Database Operations

**Reading data:**
```python
# Single row (returns dict or None)
row = self.engine.read(False, "SELECT * FROM products WHERE product_id = ?", (pk,))

# Multiple rows (returns list of dicts)
rows = self.engine.read(True, "SELECT * FROM products WHERE status = 1")
```

**Writing data:**
```python
# Returns lastrowid for INSERT or rowcount for UPDATE
result = self.engine.write("INSERT INTO batches (package_id, description) VALUES (?, ?)", (pkg_id, lot))
```

**Dynamic SQL with `WHERE 1=1` pattern:**
```python
# Start with always-true condition, then append optional filters with AND
sql = "SELECT * FROM products WHERE 1=1"

if status_filter:
    sql += " AND status = ?"
    args.append(status_filter)

if search_text:
    sql += " AND description LIKE ?"
    args.append(f"%{search_text}%")

# No need to track if it's the first condition - always use AND
```
This pattern simplifies dynamic query building: `1=1` is optimized away by the database, and every condition can use `AND` without checking if `WHERE` was already added.

## Testing Queries

Run diagnostic queries directly:
```bash
sqlite3 sql/inventarium.db ".read sql/dql/queries.sql"
```

## UI Conventions

**Follow Microsoft Windows UI Guidelines** (target platform: Windows 10/11)

- Dialog buttons: **action button (Save) on left, Cancel on right**, positioned at bottom of dialog
- Button spacing: 6 pixels apart
- Use specific verbs ("Salva", "Elimina") instead of generic "OK"
- Use `tk.Button` (not `ttk.Button`) with `underline` parameter to show keyboard shortcuts
- Keyboard shortcuts use Alt+letter pattern (e.g., Alt-s for Save, Alt-c for Cancel)
- Italian labels in UI (e.g., "Magazzino", "Lotto", "Scadenza")
- Treeview tags for visual status: `no_stock` (coral), `low_stock` (yellow), `expired` (red), `near_expired` (yellow)

## View Module Naming

List views use plural names, edit dialogs use singular:
- `products.py` (list) / `product.py` (dialog)
- `packages.py` (list) / `package.py` (dialog)
- `suppliers.py` (list) / `supplier.py` (dialog)

## Window Singleton Pattern

The `dict_instances` registry prevents duplicate windows:

```python
# Check before opening a new window
if "products" in self.engine.dict_instances:
    self.engine.dict_instances["products"].lift()
    return
# Otherwise create new window and register it
```

When closing, always unregister: `del self.engine.dict_instances["window_name"]`

## Cross-Window Refresh

After modifying data, call `self.engine.refresh_windows_for_table("table_name")` to notify related windows:

```python
def on_save(self):
    self.engine.write(sql, args)
    self.engine.refresh_windows_for_table("products")  # Triggers refresh() in related windows
    self.destroy()
```

## Error Handling Pattern

Use `engine.on_log()` for centralized error logging:

```python
try:
    result = self.engine.write(sql, args)
except Exception as e:
    self.engine.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__])
    return None
```

## Additional Components

| File | Purpose |
|------|---------|
| `monitor.py` | Idle timeout - auto-closes app after inactivity (configurable via `idle_timeout` setting) |
| `calendarium.py` | Reusable date picker widget |
| `convert_mysql_to_sqlite.py` | Migration utility for MariaDB → SQLite |

## Application Settings

Settings are stored in the `settings` table and accessed via:

```python
value = self.engine.get_setting("key_name", "default_value")
self.engine.set_setting("key_name", "new_value")
```

Key settings: `idle_timeout` (minutes), `company`, `lab`

## Internationalization (i18n)

The application supports multiple languages: **Italian (it)**, **English (en)**, and **Spanish (es)**.

### How it works

```python
from i18n import _, LANGUAGES

# Use _() to wrap any translatable string
label = _("Salva")  # Returns "Salva", "Save", or "Guardar" based on current language

# LANGUAGES dict contains available languages
# {"it": "Italiano", "en": "English", "es": "Español"}
```

### Translation file structure (`i18n.py`)

```python
TRANSLATIONS = {
    "Salva": {"it": "Salva", "en": "Save", "es": "Guardar"},
    "Chiudi": {"it": "Chiudi", "en": "Close", "es": "Cerrar"},
    # ... all UI strings
}
```

### Adding new translatable strings

1. Wrap the string with `_()`: `text=_("Nuovo Testo")`
2. Add entry to `TRANSLATIONS` dict in `i18n.py` with all language versions
3. The Italian key is always the lookup key

### Language selection

Users change language via **File → Impostazioni**. The setting is stored in the database and requires app restart to take effect.

## Statistics & Analytics

The application includes several statistical views accessible from **Statistiche** menu:

| View | Purpose |
|------|---------|
| `stats_dashboard.py` | Overview: stock counts, reorder alerts, expiring batches, movements |
| `stats_consumption.py` | Product consumption analysis by period, category filter, CSV export |
| `stats_rotation.py` | ABC classification, rotation index, coverage days calculation |
| `stats_expiring.py` | Expiration analysis, FEFO efficiency metrics |
| `stats_tat.py` | Turnaround time analysis (request → delivery, load → unload) |

## Notes

- UI labels default to Italian (e.g., "Magazzino", "Lotto", "Scadenza") but support EN/ES
- The app has an idle monitor that auto-closes after configurable minutes of inactivity
- Barcode images are generated in `barcodes/` directory and cleaned up on exit
- Error logging goes to `log.txt` with automatic rotation
- Database path is configured in `config.ini` (supports relative and absolute paths)

## Development Philosophy

This project was developed with a pragmatic approach:

- **Python + Tkinter**: Chosen for simplicity, portability, and ease of maintenance. No complex frameworks, no web stack, no JavaScript - just straightforward desktop application development.
- **SQLite**: Single-file database, no server setup, easy backup (just copy the file).
- **Keep it simple**: The application is designed for a small team in a spectrometry lab. Features are practical, not over-engineered. If it works and is maintainable, that's the goal.
- **Minimal dependencies**: Only Pillow (PIL) for image handling beyond the standard library.

The `_()` function convention for translations is a standard pattern used across many frameworks (gettext, Django, Flask) - short, unobtrusive, and universally recognized.
