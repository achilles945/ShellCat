#!/usr/bin/env bash

# Makes the "shellcat" command available system-wide (user-level install).

SCRIPT_NAME="shellcat"
ENTRYPOINT="shellcat.py"
TARGET_DIR="$HOME/.local/bin"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[*] Installing ShellCat command..."

# Ensure entrypoint
if [ ! -f "$SOURCE_DIR/$ENTRYPOINT" ]; then
    echo "[!] ERROR: $ENTRYPOINT not found in $SOURCE_DIR"
    exit 1
fi

# Ensure target directory
mkdir -p "$TARGET_DIR"

# Make entrypoint executable
chmod +x "$SOURCE_DIR/$ENTRYPOINT"

# Remove old symlink
if [ -L "$TARGET_DIR/$SCRIPT_NAME" ]; then
    rm "$TARGET_DIR/$SCRIPT_NAME"
fi

# Create symlink
ln -s "$SOURCE_DIR/$ENTRYPOINT" "$TARGET_DIR/$SCRIPT_NAME"

# Add ~/.local/bin to PATH
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$PATH:$HOME/.local/bin"' >> "$HOME/.bashrc"
    echo "[+] Added ~/.local/bin to PATH. Run: source ~/.bashrc"
fi

echo
echo "[+] ShellCat installed successfully."
echo "[+] You can now run it from any directory using:"
echo
echo "    shellcat <options>"
echo
echo "Example:"
echo "    shellcat -l -p 4444"
echo
echo "[✓] Done."
