#!/usr/bin/env python3
"""
quantize_color.py

Quantização perceptual usando CIELAB (ΔE76).

Paleta RYB:
  Primárias: Vermelho, Amarelo, Azul
  Secundárias: Laranja, Verde, Violeta
  Neutras: Preto, Branco
"""

import math

PALETTE = {
    "vermelho": [
        "#A06060",  # Dessaturada (Cinza avermelhado)
        "#FF0000",  # Mais Saturada (Explosiva no RGB)
        "#E63946",  # Ideal/Pura (Equilibrada e confortável aos olhos)
    ],

    "laranja": [
        "#B08A5A",  # Dessaturada (Tom terroso/pastel)
        "#FF6A00",  # Mais Saturada (Laranja neon)
        "#FF6A00",  # Ideal/Pura (Laranja confortável, tipo "tangerina")
    ],

    "amarelo": [
        "#C9C27A",  # Dessaturada (Amarelo gema pálido)
        "#FFFF00",  # Mais Saturada (Amarelo puro RGB - caneta marca-texto)
        "#EBCB8B",  # Ideal/Pura (Amarelo nórdico, não agride os olhos)
    ],

    "verde": [
        "#5F8F5F",  # Dessaturada (Verde sálvia)
        "#00FF00",  # Mais Saturada (Verde limão puro RGB)
        "#2A9D8F",  # Ideal/Pura (Verde esmeralda/azulado, super harmônico)
    ],

    "azul": [
        "#6A7CA8",  # Dessaturada (Azul acinzentado/jeans)
        "#0000FF",  # Mais Saturada (Azul puro RGB)
        "#4A90E2",  # Ideal/Pura (Azul corporativo/padrão limpo)
    ],

    "violeta": [
        "#77729A",  # Dessaturada (Roxo pálido/lavanda acinzentada)
        "#7F00FF",  # Mais Saturada (Violeta elétrico)
        "#8B5CF6",  # Ideal/Pura (Roxo moderno, estilo interface moderna)
    ],

    # Como preto/branco não têm saturação, ajustei para: [Suave, Profundo/Puro, Variante Útil]
    "preto": [
        "#2B2D42",  # Suave (Preto azulado/Asfalto)
        "#000000",  # Puro (Preto absoluto)
        "#1A1A1A",  # Variante (Grafite escuro para fundos)
    ],

    "branco": [
        "#F4F4F9",  # Suave (Gelo/Off-white confortável)
        "#FFFFFF",  # Puro (Branco absoluto)
        "#E5E5E5",  # Variante (Cinza claro para bordas/divisores)
    ],

    "cinza": [
        "#404040",  # escuro
        "#808080",  # médio
        "#C0C0C0",  # claro
]
}


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.strip().lstrip("#")

    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)

    if len(hex_color) != 6:
        raise ValueError(f"Cor HEX inválida: #{hex_color}")

    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"


# --------------------------------------------------
# RGB → XYZ
# --------------------------------------------------

def srgb_to_linear(c: float) -> float:
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def rgb_to_xyz(r: int, g: int, b: int):
    r = srgb_to_linear(r / 255.0)
    g = srgb_to_linear(g / 255.0)
    b = srgb_to_linear(b / 255.0)

    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    return x, y, z


# --------------------------------------------------
# XYZ → LAB
# --------------------------------------------------

def f(t):
    delta = 6 / 29

    if t > delta**3:
        return t ** (1 / 3)

    return (t / (3 * delta**2)) + (4 / 29)


def xyz_to_lab(x, y, z):
    # Illuminant D65
    xn = 0.95047
    yn = 1.00000
    zn = 1.08883

    fx = f(x / xn)
    fy = f(y / yn)
    fz = f(z / zn)

    l = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)

    return l, a, b


def rgb_to_lab(rgb):
    return xyz_to_lab(*rgb_to_xyz(*rgb))


# --------------------------------------------------
# Delta E (CIELAB)
# --------------------------------------------------

def delta_e(lab1, lab2):
    return math.sqrt(
        (lab1[0] - lab2[0]) ** 2 +
        (lab1[1] - lab2[1]) ** 2 +
        (lab1[2] - lab2[2]) ** 2
    )


# --------------------------------------------------
# Quantização
# --------------------------------------------------

def quantize1(hex_input: str, palette: dict = PALETTE) -> dict:

    rgb_in = hex_to_rgb(hex_input)
    lab_in = rgb_to_lab(rgb_in)

    best_name = None
    best_hex = None
    best_distance = float("inf")

    for name, variants in palette.items():

        # Cor "oficial" que será retornada
        pure_hex = variants[1]

        for variant_hex in variants:

            rgb_target = hex_to_rgb(variant_hex)
            lab_target = rgb_to_lab(rgb_target)

            dist = delta_e(lab_in, lab_target)

            if dist < best_distance:
                best_distance = dist
                best_name = name
                best_hex = pure_hex

    return {
        "input_hex": rgb_to_hex(*rgb_in),
        "input_rgb": rgb_in,
        "result_name": best_name,
        "result_hex": best_hex,
        "result_rgb": hex_to_rgb(best_hex),
        "distance": round(best_distance, 2),
    }


def quantize2(hex_input: str, palette: dict = PALETTE) -> dict:

    rgb_in = hex_to_rgb(hex_input)
    lab_in = rgb_to_lab(rgb_in)

    # ==================================================
    # FASE 1
    # Descobre qual categoria venceu usando TODOS
    # os representantes do array.
    # ==================================================

    best_name = None
    best_distance = float("inf")

    for name, variants in palette.items():

        for variant_hex in variants:

            rgb_target = hex_to_rgb(variant_hex)
            lab_target = rgb_to_lab(rgb_target)

            dist = delta_e(lab_in, lab_target)

            if dist < best_distance:
                best_distance = dist
                best_name = name

    # ==================================================
    # FASE 2
    # Dentro da categoria vencedora, escolhe a melhor
    # cor ignorando o índice 0 (dessaturado).
    # ==================================================

    candidates = palette[best_name][1:]

    best_hex = None
    best_output_distance = float("inf")

    for variant_hex in candidates:

        rgb_target = hex_to_rgb(variant_hex)
        lab_target = rgb_to_lab(rgb_target)

        dist = delta_e(lab_in, lab_target)

        if dist < best_output_distance:
            best_output_distance = dist
            best_hex = variant_hex

    return {
        "input_hex": rgb_to_hex(*rgb_in),
        "input_rgb": rgb_in,
        "result_name": best_name,
        "result_hex": best_hex,
        "result_rgb": hex_to_rgb(best_hex),
        "distance": round(best_output_distance, 2),
    }



if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        samples = [
            "#F7F9FD",
            "#EAECEF",
            "#121212",
            "#2A2A2A",
            "#8C4FBC",
            "#4CAF50",
            "#1E90FF",
            "#FFD700",
        ]

        print(f"{'Input':<12} {'→':<2} {'Nome':<12} {'HEX':<10} {'ΔE'}")
        print("-" * 50)

        for color in samples:
            r = quantize1(color)

            print(
                f"{r['input_hex']:<12} "
                f"→ "
                f"{r['result_name']:<12} "
                f"{r['result_hex']:<10} "
                f"{r['distance']}"
            )

    else:
        for arg in sys.argv[1:]:
            r = quantize1(arg)

            print(
                f"{r['input_hex']} → "
                f"{r['result_name']} "
                f"{r['result_hex']} "
                f"(ΔE={r['distance']})"
            )