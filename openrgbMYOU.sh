#!/bin/bash
SCHEME="$HOME/.local/state/caelestia/scheme.json"
HEX=$(jq -r '.colours.primaryPaletteKeyColor' "$SCHEME")
FALLBACK_HEX=$(jq -r '.colours.background' "$SCHEME")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

QUANTIZED=$(python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from quantize_color import quantize2
print(quantize2('$HEX')['result_hex'])
")

if [[ "${QUANTIZED^^}" == "#000000" ]]; then
    HEX="$FALLBACK_HEX"

    QUANTIZED=$(python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from quantize_color import quantize2
print(quantize2('$HEX')['result_hex'])
")

    [[ "${QUANTIZED^^}" == "#000000" ]] && QUANTIZED="#000000"
fi

QUANTIZED="${QUANTIZED#\#}"

openrgb --mode static --color "$QUANTIZED" -v -sp caelestia

printf "Scheme: %s\nHex: %s\nFallback Hex: %s\nQuantized: %s\n" "$SCHEME" "$HEX" "$FALLBACK_HEX" "$QUANTIZED"