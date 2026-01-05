#!/bin/bash
# Inventarium launcher script

INVENTARIUM_DIR="/usr/share/inventarium"
CONFIG_DIR="$HOME/.config/inventarium"

# Create user config directory if needed
if [ ! -d "$CONFIG_DIR" ]; then
    mkdir -p "$CONFIG_DIR"
fi

# Run Inventarium
# The app will show a config dialog if database is not configured
exec python3 "$INVENTARIUM_DIR/inventarium.py"
