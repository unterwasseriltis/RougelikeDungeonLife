from components.base import Component

class Actor(Component):
    """Markiert eine Entity als handlungsfähig (Spieler, Monster, etc.)."""
    def __init__(self, name: str = "Unbekannt"):
        self.name = name