from components.base import Component

class Renderable(Component):
    """Bestimmt, wie eine Entity gerendert wird."""
    def __init__(self, 
                 char: str, 
                 fg: tuple[int, int, int], 
                 bg: tuple[int, int, int] = (0, 0, 0),
                 render_order: int = 0):
        self.char = char
        self.fg = fg
        self.bg = bg
        self.render_order = render_order   # 0 = Boden, 1 = Items, 2 = Kreaturen, 3 = Spieler