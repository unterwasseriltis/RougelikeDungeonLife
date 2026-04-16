import numpy as np
import random
from game_map import GameMap
from tile_types import floor, wall

def generate_caves(
    map_width: int = 80,
    map_height: int = 50,
    fill_probability: float = 0.45,
    iterations: int = 6
) -> GameMap:
    """Erzeugt eine höhlenartige Karte mit Cellular Automata."""
    game_map = GameMap(map_width, map_height)

    # Zufällige Initialisierung
    for x in range(map_width):
        for y in range(map_height):
            if random.random() < fill_probability:
                game_map.tiles[x, y] = wall
            else:
                game_map.tiles[x, y] = floor

    # Glättungsdurchläufe
    for _ in range(iterations):
        new_tiles = game_map.tiles.copy()
        for x in range(1, map_width - 1):
            for y in range(1, map_height - 1):
                wall_count = count_walls(game_map, x, y)
                if wall_count > 4:
                    new_tiles[x, y] = wall
                else:
                    new_tiles[x, y] = floor
        game_map.tiles = new_tiles

    # Feste Ränder als Wände
    game_map.tiles[0, :] = wall
    game_map.tiles[-1, :] = wall
    game_map.tiles[:, 0] = wall
    game_map.tiles[:, -1] = wall

    return game_map


def count_walls(game_map: GameMap, x: int, y: int) -> int:
    """Zählt benachbarte Wände."""
    wall_count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if game_map.in_bounds(nx, ny) and not game_map.tiles[nx, ny]["walkable"]:
                wall_count += 1
    return wall_count