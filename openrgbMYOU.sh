#!/bin/bash
DEBUG=false

for arg in "$@"; do
    case "$arg" in
        -d|--debug|debug)
            DEBUG=true
            ;;
        -h|--help)
            printf "Uso: %s [--debug]\n" "$(basename "$0")"
            printf "  --debug, -d, debug  calcula e imprime as cores sem executar openrgb\n"
            exit 0
            ;;
        *)
            printf "Parametro desconhecido: %s\n" "$arg" >&2
            printf "Use --help para ver as opcoes.\n" >&2
            exit 2
            ;;
    esac
done

SCHEME="$HOME/.local/state/caelestia/scheme.json"
HEX=$(jq -r '.colours.primaryPaletteKeyColor' "$SCHEME")
FALLBACK_HEX=$(jq -r '.colours.secondaryPaletteKeyColor' "$SCHEME")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

QUANTIZED=$(python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from quantize_color import quantize
print(quantize('$HEX')['result_hex'])
")

if [[ "${QUANTIZED^^}" == "#000000" ]]; then
    HEX="$FALLBACK_HEX"

    QUANTIZED=$(python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from quantize_color import quantize
print(quantize('$HEX')['result_hex'])
")

    [[ "${QUANTIZED^^}" == "#000000" ]] && QUANTIZED="#000000"
fi

QUANTIZED="${QUANTIZED#\#}"

if [[ "$DEBUG" == true ]]; then
    printf "Debug: comando openrgb ignorado.\n"
else
    openrgb --mode static --color "$QUANTIZED" -v -sp caelestia
fi

printf "Scheme: %s\nHex: %s\nFallback Hex: %s\nQuantized: %s\n" "$SCHEME" "$HEX" "$FALLBACK_HEX" "$QUANTIZED"
