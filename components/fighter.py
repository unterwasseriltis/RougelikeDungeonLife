from components.base import Component

class Fighter(Component):
    """Komponente für Entities mit Lebenspunkten (Spieler, Monster)."""
    def __init__(self, hp: int, max_hp: int):
        self.hp = hp
        self.max_hp = max_hp

    def take_damage(self, amount: int) -> int:
        """Fügt Schaden zu und gibt den tatsächlich verursachten Schaden zurück."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        return amount

    def is_dead(self) -> bool:
        return self.hp <= 0