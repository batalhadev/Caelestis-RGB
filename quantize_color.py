#!/usr/bin/env python3
"""
quantize_color.py

Quantizacao perceptual usando CIELAB (Delta E 2000).

Paleta RYB:
  Primarias: Vermelho, Amarelo, Azul
  Secundarias: Laranja, Verde, Roxo
  Neutras: Preto, Branco
"""

import math

PALETTE = [
    {"grupo": "Primaria", "cor": "Vermelho", "versao": "Claro", "hex": "#FF6666", "rgb": (255, 102, 102)},
    {"grupo": "Primaria", "cor": "Vermelho", "versao": "Base", "hex": "#FF0000", "rgb": (255, 0, 0)},
    {"grupo": "Primaria", "cor": "Vermelho", "versao": "Escuro", "hex": "#8B0000", "rgb": (139, 0, 0)},
    {"grupo": "Primaria", "cor": "Amarelo", "versao": "Claro", "hex": "#FFFF99", "rgb": (255, 255, 153)},
    {"grupo": "Primaria", "cor": "Amarelo", "versao": "Base", "hex": "#FFFF00", "rgb": (255, 255, 0)},
    {"grupo": "Primaria", "cor": "Amarelo", "versao": "Escuro", "hex": "#DAA520", "rgb": (218, 165, 32)},
    {"grupo": "Primaria", "cor": "Azul", "versao": "Claro", "hex": "#66B2FF", "rgb": (102, 178, 255)},
    {"grupo": "Primaria", "cor": "Azul", "versao": "Base", "hex": "#0000FF", "rgb": (0, 0, 255)},
    {"grupo": "Primaria", "cor": "Azul", "versao": "Escuro", "hex": "#000080", "rgb": (0, 0, 128)},
    
    {"grupo": "Secundaria", "cor": "Laranja", "versao": "Claro", "hex": "#FFB266", "rgb": (255, 178, 102)},
    {"grupo": "Secundaria", "cor": "Laranja", "versao": "Base", "hex": "#FFA500", "rgb": (255, 165, 0)},
    {"grupo": "Secundaria", "cor": "Laranja", "versao": "Escuro", "hex": "#CC6600", "rgb": (204, 102, 0)},
    {"grupo": "Secundaria", "cor": "Verde", "versao": "Claro", "hex": "#99FF99", "rgb": (153, 255, 153)},
    {"grupo": "Secundaria", "cor": "Verde", "versao": "Base", "hex": "#008000", "rgb": (0, 128, 0)},
    {"grupo": "Secundaria", "cor": "Verde", "versao": "Escuro", "hex": "#004C00", "rgb": (0, 76, 0)},
    {"grupo": "Secundaria", "cor": "Roxo", "versao": "Claro", "hex": "#CC99FF", "rgb": (204, 153, 255)},
    {"grupo": "Secundaria", "cor": "Roxo", "versao": "Base", "hex": "#800080", "rgb": (128, 0, 128)},
    {"grupo": "Secundaria", "cor": "Roxo", "versao": "Escuro", "hex": "#4B0082", "rgb": (75, 0, 130)},
    
    {"grupo": "Neutra", "cor": "Branco", "versao": "Claro", "hex": "#FFFFFF", "rgb": (255, 255, 255)},
    {"grupo": "Neutra", "cor": "Branco", "versao": "Base", "hex": "#F5F5F5", "rgb": (245, 245, 245)},
    {"grupo": "Neutra", "cor": "Branco", "versao": "Escuro", "hex": "#FFFFF0", "rgb": (255, 255, 240)},
    {"grupo": "Neutra", "cor": "Preto", "versao": "Claro", "hex": "#333333", "rgb": (51, 51, 51)},
    {"grupo": "Neutra", "cor": "Preto", "versao": "Base", "hex": "#000000", "rgb": (0, 0, 0)},
    {"grupo": "Neutra", "cor": "Preto", "versao": "Escuro", "hex": "#0D0D0D", "rgb": (13, 13, 13)},
    {"grupo": "Neutra", "cor": "Cinza", "versao": "Claro", "hex": "#D3D3D3", "rgb": (211, 211, 211)},
    {"grupo": "Neutra", "cor": "Cinza", "versao": "Base", "hex": "#808080", "rgb": (128, 128, 128)},
    {"grupo": "Neutra", "cor": "Cinza", "versao": "Escuro", "hex": "#404040", "rgb": (64, 64, 64)}
]


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


def srgb_to_linear(component: float) -> float:
    if component <= 0.04045:
        return component / 12.92

    return ((component + 0.055) / 1.055) ** 2.4


def xyz_to_lab_component(component: float) -> float:
    delta = 6 / 29

    if component > delta**3:
        return component ** (1 / 3)

    return component / (3 * delta**2) + 4 / 29


def rgb_to_lab_color(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    r, g, b = (srgb_to_linear(component / 255) for component in rgb)

    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    fx = xyz_to_lab_component(x / 0.95047)
    fy = xyz_to_lab_component(y / 1.00000)
    fz = xyz_to_lab_component(z / 1.08883)

    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def color_distance(
    lab1: tuple[float, float, float],
    lab2: tuple[float, float, float],
) -> float:
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2

    c1 = math.hypot(a1, b1)
    c2 = math.hypot(a2, b2)
    c_mean = (c1 + c2) / 2
    c_mean7 = c_mean**7
    g = 0.5 * (1 - math.sqrt(c_mean7 / (c_mean7 + 25**7)))

    a1_prime = (1 + g) * a1
    a2_prime = (1 + g) * a2
    c1_prime = math.hypot(a1_prime, b1)
    c2_prime = math.hypot(a2_prime, b2)

    h1_prime = math.degrees(math.atan2(b1, a1_prime)) % 360
    h2_prime = math.degrees(math.atan2(b2, a2_prime)) % 360

    delta_l_prime = l2 - l1
    delta_c_prime = c2_prime - c1_prime

    if c1_prime * c2_prime == 0:
        angular_delta_h_prime = 0
    else:
        hue_diff = h2_prime - h1_prime

        if abs(hue_diff) <= 180:
            angular_delta_h_prime = hue_diff
        elif hue_diff > 180:
            angular_delta_h_prime = hue_diff - 360
        else:
            angular_delta_h_prime = hue_diff + 360

    delta_big_h_prime = (
        2
        * math.sqrt(c1_prime * c2_prime)
        * math.sin(math.radians(angular_delta_h_prime / 2))
    )

    l_mean_prime = (l1 + l2) / 2
    c_mean_prime = (c1_prime + c2_prime) / 2

    if c1_prime * c2_prime == 0:
        h_mean_prime = h1_prime + h2_prime
    elif abs(h1_prime - h2_prime) <= 180:
        h_mean_prime = (h1_prime + h2_prime) / 2
    elif h1_prime + h2_prime < 360:
        h_mean_prime = (h1_prime + h2_prime + 360) / 2
    else:
        h_mean_prime = (h1_prime + h2_prime - 360) / 2

    t = (
        1
        - 0.17 * math.cos(math.radians(h_mean_prime - 30))
        + 0.24 * math.cos(math.radians(2 * h_mean_prime))
        + 0.32 * math.cos(math.radians(3 * h_mean_prime + 6))
        - 0.20 * math.cos(math.radians(4 * h_mean_prime - 63))
    )

    s_l = 1 + (0.015 * (l_mean_prime - 50) ** 2) / math.sqrt(
        20 + (l_mean_prime - 50) ** 2
    )
    s_c = 1 + 0.045 * c_mean_prime
    s_h = 1 + 0.015 * c_mean_prime * t

    delta_theta = 30 * math.exp(-((h_mean_prime - 275) / 25) ** 2)
    c_mean_prime7 = c_mean_prime**7
    r_c = 2 * math.sqrt(c_mean_prime7 / (c_mean_prime7 + 25**7))
    r_t = -r_c * math.sin(math.radians(2 * delta_theta))

    return math.sqrt(
        (delta_l_prime / s_l) ** 2
        + (delta_c_prime / s_c) ** 2
        + (delta_big_h_prime / s_h) ** 2
        + r_t * (delta_c_prime / s_c) * (delta_big_h_prime / s_h)
    )


def build_palette_cache(palette: list[dict]) -> list[dict]:
    return [
        {
            **entry,
            "cor_key": entry["cor"].lower(),
            "lab": rgb_to_lab_color(entry["rgb"]),
        }
        for entry in palette
    ]


PALETTE_CACHE = build_palette_cache(PALETTE)


def ensure_palette_cache(palette: list[dict]) -> list[dict]:
    if palette and "lab" in palette[0]:
        return palette

    return build_palette_cache(palette)


# --------------------------------------------------
# Quantização
# --------------------------------------------------

def quantize1(hex_input: str, palette: list[dict] = PALETTE_CACHE) -> dict:
    palette = ensure_palette_cache(palette)

    rgb_in = hex_to_rgb(hex_input)
    lab_in = rgb_to_lab_color(rgb_in)

    best_entry = None
    best_distance = float("inf")

    for entry in palette:
        dist = color_distance(lab_in, entry["lab"])

        if dist < best_distance:
            best_distance = dist
            best_entry = entry

    base_entry = next(
        entry
        for entry in palette
        if entry["cor"] == best_entry["cor"] and entry["versao"] == "Base"
    )

    return {
        "input_hex": rgb_to_hex(*rgb_in),
        "input_rgb": rgb_in,
        "result_name": base_entry["cor_key"],
        "result_hex": base_entry["hex"],
        "result_rgb": base_entry["rgb"],
        "distance": round(best_distance, 2),
    }


def quantize2(hex_input: str, palette: list[dict] = PALETTE_CACHE) -> dict:
    palette = ensure_palette_cache(palette)

    rgb_in = hex_to_rgb(hex_input)
    lab_in = rgb_to_lab_color(rgb_in)

    # ==================================================
    # FASE 1
    # Descobre qual categoria venceu usando TODOS
    # os representantes do array.
    # ==================================================

    best_entry = None
    best_distance = float("inf")

    for entry in palette:
        dist = color_distance(lab_in, entry["lab"])

        if dist < best_distance:
            best_distance = dist
            best_entry = entry

    # ==================================================
    # FASE 2
    # Dentro da categoria vencedora, escolhe a melhor
    # cor ignorando a versao Claro.
    # ==================================================

    candidates = [
        entry
        for entry in palette
        if entry["cor"] == best_entry["cor"] and entry["versao"] != "Claro"
    ]

    best_output = None
    best_output_distance = float("inf")

    for entry in candidates:
        dist = color_distance(lab_in, entry["lab"])

        if dist < best_output_distance:
            best_output_distance = dist
            best_output = entry

    return {
        "input_hex": rgb_to_hex(*rgb_in),
        "input_rgb": rgb_in,
        "result_name": best_output["cor_key"],
        "result_hex": best_output["hex"],
        "result_rgb": best_output["rgb"],
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
