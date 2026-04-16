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
        title="QudLike – ECS mit InputSystem",
        tileset=tileset,
    )

    # Karte
    game_map = generate_asteroid_field(WIDTH, HEIGHT)

    # ECS
    ecs = ECS()

    # Spieler als Entity
    player = ecs.create_entity()
    ecs.add_component(player, Position(WIDTH // 2, HEIGHT // 2))
    ecs.add_component(player, Renderable("@", (255, 255, 255)))
    ecs.add_component(player, Actor(name="Spieler"))

    fov_radius = 12
    print("ECS + InputSystem + Actor gestartet.")

    while True:
        # FOV
        player_pos = ecs.get_component(player, Position)
        game_map.visible = tcod.map.compute_fov(
            transparency=game_map.tiles["transparent"],
            pov=(player_pos.x, player_pos.y),
            radius=fov_radius,
            light_walls=True,
            algorithm=tcod.FOV_SHADOW
        )
        game_map.explored |= game_map.visible

        console.clear()
        game_map.render(console)
        RenderSystem.render(console, ecs)
        context.present(console)

        # Eingabe über InputSystem
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

            if isinstance(event, tcod.event.KeyDown):
                dx, dy = InputSystem.get_movement(event)
                if dx != 0 or dy != 0:
                    MovementSystem.handle_movement(ecs, game_map, dx, dy)


if __name__ == "__main__":
    main()