# Inventarium

A lightweight laboratory inventory management system built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-07405e.svg)
![License](https://img.shields.io/badge/License-GPL%20v3-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)

## Overview

Inventarium is designed for small laboratory teams who need a simple, fast, and reliable way to track consumables, reagents, and supplies. No complex setup, no web server, no cloud dependencies - just a straightforward desktop application with a local SQLite database.

### Key Features

- **Product Hierarchy**: Products → Packages (SKUs) → Batches (Lots) → Labels (individual units)
- **Barcode Support**: Generate and scan barcodes for quick stock operations
- **Expiration Tracking**: FEFO (First Expired, First Out) management with alerts
- **Reorder Alerts**: Automatic notifications when stock falls below threshold
- **Request Workflow**: Create purchase requests and track deliveries
- **Statistics Dashboard**: Consumption analysis, rotation index, ABC classification
- **Multi-language**: Italian, English, and Spanish UI

## Screenshots

![Dashboard](screenshots/dashboard.png)
*Statistics Dashboard showing stock overview, reorder alerts, and expiration tracking*

## Installation

### Requirements

- Python 3.11 or higher
- Tkinter (usually included with Python)
- Pillow (PIL)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/1966bc/inventarium.git
cd inventarium
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install Pillow
```

4. Copy the config file:
```bash
cp config.ini.example config.ini
```

5. Run the application:
```bash
python3 inventarium.py
```

## Database

Inventarium uses SQLite - a single file database that requires no server setup. The demo database (`sql/inventarium.db`) includes sample data to get you started.

### Demo Data

The included database contains fictional data for testing:
- 15 products (solvents, standards, columns, consumables)
- 6 suppliers (Sigma-Aldrich, Thermo Fisher, etc.)
- Sample batches, labels, and requests

To reset to demo data:
```bash
sqlite3 sql/inventarium.db ".read sql/demo_data.sql"
```

## Configuration

Edit `config.ini` to set the database path:

```ini
[database]
path = sql/inventarium.db
```

For shared network access, use a network path:
```ini
path = //server/share/inventarium.db
```

## Usage

### Main Workflow

1. **Add Products**: Define base products (e.g., "Acetonitrile HPLC Grade")
2. **Create Packages**: Link products to suppliers with specific packaging (e.g., "2.5L bottle from Sigma")
3. **Register Batches**: Add lot numbers with expiration dates
4. **Load Labels**: Create individual stock units (each gets a unique barcode)
5. **Unload Labels**: Scan or click to mark items as used

### Keyboard Shortcuts

- `Alt+N` - New
- `Alt+S` - Save
- `Alt+C` - Close/Cancel
- `Escape` - Close window

## Project Structure

```
inventarium/
├── inventarium.py      # Application entry point
├── engine.py           # Core engine (combines all mixins)
├── dbms.py             # Database layer
├── controller.py       # Domain queries
├── tools.py            # Widget factories
├── i18n.py             # Translations
├── views/              # GUI windows
│   ├── main.py         # Main window
│   ├── warehouse.py    # Inventory management
│   ├── products.py     # Product list
│   └── ...
├── reports/            # Report generators
├── sql/                # Database and queries
│   ├── inventarium.db  # SQLite database
│   └── demo_data.sql   # Sample data
└── images/             # Application icons
```

## Architecture

The application uses a **mixin-based architecture** where the Engine class combines:

- `DBMS` - Database connection and query execution
- `Controller` - Domain-specific queries
- `Tools` - Tkinter widget factories
- `Launcher` - Cross-platform file opener

All views access the engine via `self.engine = self.nametowidget(".").engine`.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Authors

**Giuseppe Costanzi** ([@1966bc](https://github.com/1966bc))

**HAL 9000** ([Claude](https://claude.ai) by [Anthropic](https://anthropic.com))

---

*Built with Python, Tkinter, and SQLite. Keep it simple.*
