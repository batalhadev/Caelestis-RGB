#!/usr/bin/env bash

DIR="$HOME/.local/state/caelestia"
HOOK="$HOME/.config/caelestia/hooks/openrgbMYou/openrgbMYOU.sh"

# Execute 1 time at startup
"$HOOK"

inotifywait -m -q \
    -e close_write \
    -e moved_to \
    "$DIR" |
while read -r path event file; do
    [[ "$file" == "scheme.json" ]] || continue
    "$HOOK"
done