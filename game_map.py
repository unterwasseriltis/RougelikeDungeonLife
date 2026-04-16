import numpy as np
import tcod
from tile_types import tile_dt, floor, wall

class GameMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = np.full((width, height), fill_value=wall, dtype=tile_dt, order="F")
        
        self.visible = np.zeros((width, height), dtype=bool, order="F")
        self.explored = np.zeros((width, height), dtype=bool, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: tcod.console.Console) -> None:
        """Rendert die Karte mit FOV-Unterscheidung."""
        # Korrigierte Zuweisung (FutureWarning behoben)
        console.rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=self.tiles["dark"]
        )