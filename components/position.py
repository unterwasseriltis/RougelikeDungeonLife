from components.base import Component

class Position(Component):
    """Speichert die Position einer Entity."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y