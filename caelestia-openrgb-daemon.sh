#!/usr/bin/env bash

DIR="$HOME/.local/state/caelestia"
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SCRIPT="$SCRIPT_DIR/openrgbMYOU.sh"

# Execute once at startup
"$SCRIPT"

inotifywait -m -q \
    -e close_write \
    -e moved_to \
    "$DIR" |
while read -r path event file; do
    [[ "$file" == "scheme.json" ]] || continue
    "$SCRIPT"
done