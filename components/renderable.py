from components.base import Component

class Renderable(Component):
    """Bestimmt, wie eine Entity gerendert wird."""
    def __init__(self, char: str, fg: tuple[int, int, int], bg: tuple[int, int, int] = (0, 0, 0)):
        self.char = char
        self.fg = fg
        self.bg = bg