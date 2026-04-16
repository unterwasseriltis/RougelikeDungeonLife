import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", bool),
        ("transparent", bool),
        ("dark", graphic_dt),
        ("light", graphic_dt),
    ]
)

# Weltraum-Stil – dunkler Hintergrund
floor = np.array(
    (
        True, True,
        (ord("."), (40, 40, 55), (10, 10, 25)),   # dark
        (ord("."), (70, 80, 110), (15, 20, 40)),  # light
    ),
    dtype=tile_dt,
)

wall = np.array(   # Asteroiden / Hindernisse
    (
        False, False,
        (ord("#"), (90, 90, 110), (20, 20, 30)),     # dark
        (ord("#"), (160, 170, 190), (40, 45, 60)),   # light
    ),
    dtype=tile_dt,
)