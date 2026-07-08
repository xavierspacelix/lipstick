"""Fetch lipstick dataset, classify by RGB, output expanded seed data with English names."""
import json
import urllib.request
import sys

URL = "https://raw.githubusercontent.com/theBigDataDigest/lipsticks_detect/master/lipstick.json"

# Human-readable English name templates by category + brightness
NAME_TEMPLATES = {
    "Red": ["Ruby", "Crimson", "Scarlet", "Cherry", "Fire", "Flame", "Poppy", "Vermillion", "Cardinal", "Wine"],
    "Coral": ["Coral", "Salmon", "Peach", "Sunset", "Tangerine", "Melon", "Papaya", "Nectarine"],
    "Berry": ["Berry", "Raspberry", "Cranberry", "Mulberry", "Boysenberry", "Bilberry", "Logan"],
    "Mauve": ["Mauve", "Lilac", "Orchid", "Heather", "Lavender", "Wisteria", "Thistle"],
    "Plum": ["Plum", "Damson", "Sloe", "Prune", "Fig", "Date"],
    "Pink": ["Blush", "Rose", "Petal", "Camellia", "Peony", "Dahlia", "Azalea", "Lotus", "Bouquet"],
    "Nude": ["Nude", "Bare", "Shell", "Biscuit", "Mocha", "Sand", "Beige", "Almond", "Cashmere"],
    "Brown": ["Hazel", "Umber", "Sienna", "Cocoa", "Chestnut", "Walnut", "Pecan", "Carob"],
}

BRIGHTNESS_MODIFIERS = {  # (threshold, prefix)
    "light": (0.65, "Light"),
    "bright": (0.45, "Bright"),
    "deep": (0.25, "Deep"),
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def brightness(r, g, b):
    return (r + g + b) / (3 * 255)


def classify(r, g, b):
    bri = brightness(r, g, b)

    if bri < 0.25:
        lip_type = "Dark"
    elif bri < 0.45:
        lip_type = "Brownish"
    else:
        lip_type = "Pinkish"

    max_c = max(r, g, b)
    min_c = min(r, g, b)
    sat = (max_c - min_c) / max_c if max_c > 0 else 0

    if sat < 0.15:
        cat = "Nude"
    elif r >= g and r >= b:
        if r > 180 and g < 100 and b < 100:
            cat = "Red"
        elif g > b and g > 100:
            cat = "Coral"
        elif g > b:
            cat = "Red"
        else:
            cat = "Berry"
    elif b >= r and b >= g:
        cat = "Mauve" if r > 100 else ("Plum" if g > 80 else "Berry")
    elif g >= r and g >= b:
        cat = "Nude" if r > 120 else "Brown"
    elif r > b:
        cat = "Coral"
    elif g > b:
        cat = "Mauve"
    else:
        cat = "Pink"

    if lip_type == "Dark" and cat in ("Nude", "Coral"):
        cat = "Berry"
    if lip_type == "Pinkish" and cat in ("Brown",):
        cat = "Nude"

    return lip_type, cat, bri


ADJECTIVES = [
    "Silky", "Velvet", "Satin", "Matte", "Glossy", "Creamy", "Sheer",
    "Luminous", "Radiant", "Subtle", "Bold", "Rich", "Soft", "Warm",
    "Chilled", "Twilight", "Dewy", "Dreamy", "Cozy", "Gentle",
    "Vivid", "Vibrant", "Mellow", "Modern", "Classic", "Tender",
]

def generate_name(category, bri, index):
    adj = ADJECTIVES[index % len(ADJECTIVES)]
    names = NAME_TEMPLATES.get(category, ["Shade"])
    base = names[(index // len(ADJECTIVES)) % len(names)]

    prefix = ""
    if bri > 0.65:
        prefix = "Light "
    elif bri < 0.25:
        prefix = "Deep "

    return f"{prefix}{adj} {base}"


def main():
    try:
        with urllib.request.urlopen(URL, timeout=15) as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to fetch: {e}", file=sys.stderr)
        sys.exit(1)

    entries = []
    seen = set()

    # Start with original 18 curated entries
    original = [
        {"shade_name": "Rose Pink", "category": "Pink", "rgb_r": 200, "rgb_g": 120, "rgb_b": 140, "lip_type_tag": "Pinkish"},
        {"shade_name": "Warm Pink", "category": "Pink", "rgb_r": 210, "rgb_g": 130, "rgb_b": 150, "lip_type_tag": "Pinkish"},
        {"shade_name": "Soft Nude", "category": "Nude", "rgb_r": 180, "rgb_g": 140, "rgb_b": 130, "lip_type_tag": "Pinkish"},
        {"shade_name": "Coral Glow", "category": "Coral", "rgb_r": 220, "rgb_g": 140, "rgb_b": 120, "lip_type_tag": "Pinkish"},
        {"shade_name": "Blush Petal", "category": "Pink", "rgb_r": 195, "rgb_g": 125, "rgb_b": 145, "lip_type_tag": "Pinkish"},
        {"shade_name": "Dusty Rose", "category": "Pink", "rgb_r": 185, "rgb_g": 115, "rgb_b": 125, "lip_type_tag": "Pinkish"},
        {"shade_name": "Mauve Bliss", "category": "Mauve", "rgb_r": 170, "rgb_g": 110, "rgb_b": 130, "lip_type_tag": "Brownish"},
        {"shade_name": "Warm Nude", "category": "Nude", "rgb_r": 165, "rgb_g": 120, "rgb_b": 100, "lip_type_tag": "Brownish"},
        {"shade_name": "Caramel Kiss", "category": "Nude", "rgb_r": 175, "rgb_g": 125, "rgb_b": 95, "lip_type_tag": "Brownish"},
        {"shade_name": "Terracotta", "category": "Coral", "rgb_r": 180, "rgb_g": 100, "rgb_b": 80, "lip_type_tag": "Brownish"},
        {"shade_name": "Spice Brown", "category": "Brown", "rgb_r": 160, "rgb_g": 90, "rgb_b": 70, "lip_type_tag": "Brownish"},
        {"shade_name": "Cinnamon", "category": "Brown", "rgb_r": 155, "rgb_g": 85, "rgb_b": 65, "lip_type_tag": "Brownish"},
        {"shade_name": "Deep Berry", "category": "Berry", "rgb_r": 120, "rgb_g": 50, "rgb_b": 70, "lip_type_tag": "Dark"},
        {"shade_name": "Burgundy", "category": "Red", "rgb_r": 110, "rgb_g": 40, "rgb_b": 50, "lip_type_tag": "Dark"},
        {"shade_name": "Plum Wine", "category": "Plum", "rgb_r": 100, "rgb_g": 35, "rgb_b": 60, "lip_type_tag": "Dark"},
        {"shade_name": "Cherry Red", "category": "Red", "rgb_r": 130, "rgb_g": 45, "rgb_b": 55, "lip_type_tag": "Dark"},
        {"shade_name": "Midnight Mauve", "category": "Mauve", "rgb_r": 90, "rgb_g": 40, "rgb_b": 65, "lip_type_tag": "Dark"},
        {"shade_name": "Raisin", "category": "Brown", "rgb_r": 80, "rgb_g": 35, "rgb_b": 45, "lip_type_tag": "Dark"},
    ]
    for e in original:
        hex_key = f"{e['rgb_r']},{e['rgb_g']},{e['rgb_b']}"
        seen.add(hex_key)
        entries.append(e)

    index = 0
    for brand in data["brands"]:
        for series in brand["series"]:
            for ls in series["lipsticks"]:
                hex_color = ls["color"].strip()
                r, g, b = hex_to_rgb(hex_color)
                hex_key = f"{r},{g},{b}"
                if hex_key in seen:
                    continue
                seen.add(hex_key)

                lip_type, cat, bri = classify(r, g, b)
                name = generate_name(cat, bri, index)
                index += 1
                entries.append({
                    "shade_name": name,
                    "category": cat,
                    "rgb_r": r,
                    "rgb_g": g,
                    "rgb_b": b,
                    "lip_type_tag": lip_type,
                })

    type_order = {"Pinkish": 0, "Brownish": 1, "Dark": 2}
    entries.sort(key=lambda e: (type_order.get(e["lip_type_tag"], 9), e["category"], e["rgb_r"]))

    # Output
    print(f"# Auto-generated from {len(entries)} shades ({len(entries) - 18} new + 18 original)")
    print()
    print("lipstick_database = [")
    for e in entries:
        print(f'    {{"shade_name": {json.dumps(e["shade_name"])}, "category": {json.dumps(e["category"])}, "rgb_r": {e["rgb_r"]}, "rgb_g": {e["rgb_g"]}, "rgb_b": {e["rgb_b"]}, "lip_type_tag": {json.dumps(e["lip_type_tag"])}}},')
    print("]")


if __name__ == "__main__":
    main()
