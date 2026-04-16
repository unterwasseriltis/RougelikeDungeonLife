import tcod
import tcod.event
import random
from pathlib import Path

from game_map import GameMap
from procgen import generate_asteroid_field
from ecs import ECS
from components.position import Position
from components.renderable import Renderable
from components.actor import Actor
from components.fighter import Fighter
from systems import RenderSystem, MovementSystem, InputSystem

WIDTH, HEIGHT = 120, 80

def main() -> None:
    tileset_path = Path("data/dejavu10x10_gs_tc.png")
    if not tileset_path.exists():
        raise FileNotFoundError(f"Tileset nicht gefunden: {tileset_path.resolve()}")

    tileset = tcod.tileset.load_tilesheet(
        str(tileset_path), columns=32, rows=8, charmap=tcod.tileset.CHARMAP_TCOD
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)

    console = tcod.console.Console(WIDTH, HEIGHT, order="F")
    context = tcod.context.new(
        columns=console.width,
        rows=console.height,
        title="QudLike – HP-Anzeige mittig unten",
        tileset=tileset,
    )

    game_map = generate_asteroid_field(WIDTH, HEIGHT)
    ecs = ECS()

    # Spieler
    player = ecs.create_entity()
    ecs.add_component(player, Position(WIDTH // 2, HEIGHT // 2))
    ecs.add_component(player, Renderable("@", (255, 255, 255), render_order=3))
    ecs.add_component(player, Actor(name="Spieler"))
    ecs.add_component(player, Fighter(hp=30, max_hp=30))

    # Statisches Trümmerteil
    debris = ecs.create_entity()
    ecs.add_component(debris, Position(WIDTH // 2 + 8, HEIGHT // 2 - 5))
    ecs.add_component(debris, Renderable("■", (130, 130, 150), render_order=1))

    fov_radius = 12
    print("HP-Anzeige jetzt mittig unten platziert.")

    while True:
        player_pos = ecs.get_component(player, Position)
        player_fighter = ecs.get_component(player, Fighter)

        # FOV
        game_map.visible = tcod.map.compute_fov(
            transparency=game_map.tiles["transparent"],
            pov=(player_pos.x, player_pos.y),
            radius=fov_radius,
            light_walls=True,
            algorithm=tcod.FOV_SHADOW
        )
        game_map.explored |= game_map.visible

        console.clear()

        # Karte + Entities rendern
        game_map.render(console)
        RenderSystem.render(console, ecs)

        # === HP-ANZEIGE MITTIG UNTEN ===
        if player_fighter:
            hp_text = f" HP: {player_fighter.hp} / {player_fighter.max_hp} "
            bar_width = 40

            # Position mittig unten
            bar_x = (WIDTH - bar_width) // 2
            bar_y = HEIGHT - 3

            # Hintergrund-Leiste
            console.print(bar_x, bar_y, " " * bar_width, fg=(0,0,0), bg=(60, 20, 20))
            
            # Rote Füllung (proportional)
            hp_percent = player_fighter.hp / player_fighter.max_hp
            filled = int(bar_width * hp_percent)
            console.print(bar_x, bar_y, "█" * filled, fg=(255, 70, 70), bg=(60, 20, 20))

            # Text mittig auf der Leiste
            text_x = bar_x + (bar_width - len(hp_text)) // 2
            console.print(text_x, bar_y, hp_text, fg=(255, 255, 255))

        context.present(console)

        # Eingabe
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

            if isinstance(event, tcod.event.KeyDown):
                dx, dy = InputSystem.get_movement(event)
                if dx != 0 or dy != 0:
                    MovementSystem.handle_movement(ecs, game_map, dx, dy)


if __name__ == "__main__":
    main()