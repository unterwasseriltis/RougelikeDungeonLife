import numpy as np

# Strukturierter Datentyp, der exakt zu console.tiles_rgb passt
graphic_dt = np.dtype(
    [
        ("ch", np.int32),   # Unicode-Zeichen (z. B. ord(".") oder ord("#"))
        ("fg", "3B"),       # Vordergrundfarbe RGB (light)
        ("bg", "3B"),       # Hintergrundfarbe RGB (meist schwarz oder dunkel)
    ]
)

# Tile-Datentyp für die GameMap (erweitert um Spiel-Logik)
tile_dt = np.dtype(
    [
        ("walkable", bool),
        ("transparent", bool),
        ("dark", graphic_dt),    # Darstellung im Dunkeln / unerforscht
        ("light", graphic_dt),   # Darstellung bei Beleuchtung / sichtbar
    ]
)

# Vordefinierte Tile-Typen
floor = np.array(
    (
        True,                          # walkable
        True,                          # transparent
        (ord("."), (50, 50, 50), (0, 0, 0)),   # dark: Zeichen, fg, bg
        (ord("."), (100, 100, 100), (0, 0, 0)), # light
    ),
    dtype=tile_dt,
)

wall = np.array(
    (
        False,                         # walkable
        False,                         # transparent
        (ord("#"), (60, 60, 60), (0, 0, 0)),   # dark
        (ord("#"), (120, 120, 120), (0, 0, 0)), # light
    ),
    dtype=tile_dt,
)