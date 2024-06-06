#!/bin/bash

TARGET_DIR="/usr/local/bin"
SCRIPT_NAME="nkrypt"
SOURCE_FILE="nkrypt.py"

sudo cp "$SOURCE_FILE" "$TARGET_DIR/$SCRIPT_NAME"

sudo chmod +x "$TARGET_DIR/$SCRIPT_NAME"

if [ -x "$(command -v $SCRIPT_NAME)" ]; then
    echo "$SCRIPT_NAME installed successfully in $TARGET_DIR."
else
    echo "Installation failed."
    exit 1
fi
