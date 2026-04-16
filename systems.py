import tcod
from ecs import ECS, Entity
from game_map import GameMap
from components.position import Position
from components.renderable import Renderable
from components.actor import Actor

class RenderSystem:
    """Zeichnet alle Entities mit Renderable-Komponente."""
    
    @staticmethod
    def render(console: tcod.console.Console, ecs: ECS) -> None:
        for entity, renderable in ecs.get_entities_with(Renderable):
            position = ecs.get_component(entity, Position)
            if position:
                console.print(
                    position.x, position.y,
                    renderable.char,
                    fg=renderable.fg,
                    bg=renderable.bg
                )


class MovementSystem:
    """Bewegt Entities mit Position und Actor."""
    
    @staticmethod
    def handle_movement(ecs: ECS, game_map: GameMap, dx: int, dy: int) -> bool:
        for entity, position in ecs.get_entities_with(Position):
            # Nur Entities mit Actor-Komponente können sich bewegen (z.B. Spieler)
            if not entity.has_component(Actor):
                continue
                
            new_x = position.x + dx
            new_y = position.y + dy

            if (game_map.in_bounds(new_x, new_y) and 
                game_map.tiles["walkable"][new_x, new_y]):
                
                position.x = new_x
                position.y = new_y
                return True
        return False


class InputSystem:
    """Verarbeitet Tastatureingaben und gibt Bewegungsvektoren zurück."""
    
    @staticmethod
    def get_movement(event: tcod.event.KeyDown) -> tuple[int, int]:
        if event.sym == tcod.event.KeySym.UP:
            return 0, -1
        elif event.sym == tcod.event.KeySym.DOWN:
            return 0, 1
        elif event.sym == tcod.event.KeySym.LEFT:
            return -1, 0
        elif event.sym == tcod.event.KeySym.RIGHT:
            return 1, 0
        return 0, 0