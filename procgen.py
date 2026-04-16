import numpy as np
import random
from game_map import GameMap
from tile_types import floor, wall

def generate_asteroid_field(
    width: int = 120,
    height: int = 80,
    density: float = 0.085          # Wie viele Hindernis-Blöcke (0.08–0.10 wirkt gut)
) -> GameMap:
    """Erzeugt eine offene Asteroidenfeld-Map mit verstreuten einzelnen Hindernis-Blöcken."""
    game_map = GameMap(width, height)

    # Alles zunächst als offener Weltraum (Boden)
    game_map.tiles[...] = floor

    # Zufällige Hindernis-Blöcke platzieren
    for x in range(width):
        for y in range(height):
            if random.random() < density:
                # Etwas Abstand zum Rand und zum Spieler-Startbereich (optional später)
                if 5 < x < width - 5 and 5 < y < height - 5:
                    game_map.tiles[x, y] = wall

    # Rand immer als leichte Begrenzung (damit der Chunk-Übergang klar ist)
    game_map.tiles[0, :] = wall
    game_map.tiles[-1, :] = wall
    game_map.tiles[:, 0] = wall
    game_map.tiles[:, -1] = wall

    return game_map