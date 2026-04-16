import tcod
from ecs import ECS, Entity
from game_map import GameMap
from components.position import Position
from components.renderable import Renderable
from components.actor import Actor
from components.fighter import Fighter
from components.death import Death

class RenderSystem:
    @staticmethod
    def render(console: tcod.console.Console, ecs: ECS) -> None:
        entities_to_render = []
        for entity, renderable in ecs.get_entities_with(Renderable):
            position = ecs.get_component(entity, Position)
            if position:
                entities_to_render.append((renderable.render_order, position, renderable))
        
        for _, position, renderable in sorted(entities_to_render):
            console.print(position.x, position.y, renderable.char, fg=renderable.fg, bg=renderable.bg)


class MovementSystem:
    @staticmethod
    def handle_movement(ecs: ECS, game_map: GameMap, dx: int, dy: int) -> bool:
        for entity, position in ecs.get_entities_with(Position):
            if not entity.has_component(Actor):
                continue
            if entity.has_component(Death):
                continue  # Tote Entities können sich nicht bewegen
                
            new_x = position.x + dx
            new_y = position.y + dy

            if (game_map.in_bounds(new_x, new_y) and 
                game_map.tiles["walkable"][new_x, new_y]):
                
                position.x = new_x
                position.y = new_y
                return True
        return False


class InputSystem:
    @staticmethod
    def get_movement(event: tcod.event.KeyDown) -> tuple[int, int]:
        if event.sym == tcod.event.KeySym.UP:    return 0, -1
        elif event.sym == tcod.event.KeySym.DOWN:  return 0, 1
        elif event.sym == tcod.event.KeySym.LEFT:  return -1, 0
        elif event.sym == tcod.event.KeySym.RIGHT: return 1, 0
        return 0, 0


class DamageSystem:
    """Behandelt Schaden und Tod von Entities."""
    
    @staticmethod
    def apply_damage(ecs: ECS, entity: Entity, amount: int) -> None:
        fighter = ecs.get_component(entity, Fighter)
        if not fighter:
            return

        fighter.take_damage(amount)

        if fighter.is_dead():
            ecs.add_component(entity, Death())
            print(f"{ecs.get_component(entity, Actor).name} ist gestorben!")

class AISystem:
    """Sehr einfache KI für Nicht-Spieler-Entities (zufällige Bewegung)."""
    
    @staticmethod
    def update(ecs: ECS, game_map: GameMap) -> None:
        import random
        
        for entity, actor in ecs.get_entities_with(Actor):
            # Nur Nicht-Spieler Entities sollen sich bewegen
            if ecs.get_component(entity, Actor).name == "Spieler":
                continue
            if entity.has_component(Death):
                continue
                
            position = ecs.get_component(entity, Position)
            if not position:
                continue
                
            # Zufällige Bewegung (50% Chance, sich zu bewegen)
            if random.random() < 0.5:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                
                if dx == 0 and dy == 0:
                    continue
                    
                new_x = position.x + dx
                new_y = position.y + dy
                
                if (game_map.in_bounds(new_x, new_y) and 
                    game_map.tiles["walkable"][new_x, new_y]):
                    position.x = new_x
                    position.y = new_y