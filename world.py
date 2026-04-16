import random
from game_map import GameMap
from procgen import generate_asteroid_field

class GameWorld:
    def __init__(self, chunk_width: int = 120, chunk_height: int = 80):
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        self.chunks: dict[tuple[int, int], GameMap] = {}   # (chunk_x, chunk_y) -> GameMap

        # Start-Chunk generieren
        self.current_cx, self.current_cy = 0, 0
        self.chunks[(0, 0)] = generate_asteroid_field(chunk_width, chunk_height)

    def get_current_map(self) -> GameMap:
        return self.chunks[(self.current_cx, self.current_cy)]

    def change_chunk(self, dx: int, dy: int) -> None:
        """Wechselt zum benachbarten Chunk und generiert ihn bei Bedarf."""
        self.current_cx += dx
        self.current_cy += dy

        key = (self.current_cx, self.current_cy)
        if key not in self.chunks:
            self.chunks[key] = generate_asteroid_field(self.chunk_width, self.chunk_height)