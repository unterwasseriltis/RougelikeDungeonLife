import tcod
import tcod.event
import random
from pathlib import Path

from game_map import GameMap
from procgen import generate_asteroid_field
from ecs import ECS, Entity
from components.position import Position
from components.renderable import Renderable

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
        title="QudLike – ECS + FOV",
        tileset=tileset,
    )

    # Karte generieren
    game_map = generate_asteroid_field(WIDTH, HEIGHT)

    # ECS initialisieren
    ecs = ECS()

    # Spieler als Entity erstellen
    player = ecs.create_entity()
    player_pos = Position(WIDTH // 2, HEIGHT // 2)
    ecs.add_component(player, player_pos)
    ecs.add_component(player, Renderable("@", (255, 255, 255)))

    fov_radius = 12
    print("ECS + FOV gestartet. Der Lichtkegel sollte wieder sichtbar sein.")

    while True:
        # === FOV BERECHNEN (wichtig!) ===
        game_map.visible = tcod.map.compute_fov(
            transparency=game_map.tiles["transparent"],
            pov=(player_pos.x, player_pos.y),   # Position aus der Entity
            radius=fov_radius,
            light_walls=True,
            algorithm=tcod.FOV_SHADOW
        )
        game_map.explored |= game_map.visible

        console.clear()

        # Karte mit FOV rendern
        game_map.render(console)

        # Spieler rendern (über ECS)
        rend = ecs.get_component(player, Renderable)
        if rend:
            console.print(player_pos.x, player_pos.y, rend.char, fg=rend.fg)

        context.present(console)

        # Bewegung
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

            if isinstance(event, tcod.event.KeyDown):
                dx = dy = 0
                if event.sym == tcod.event.KeySym.UP:    dy = -1
                elif event.sym == tcod.event.KeySym.DOWN:  dy = 1
                elif event.sym == tcod.event.KeySym.LEFT:  dx = -1
                elif event.sym == tcod.event.KeySym.RIGHT: dx = 1

                if dx == 0 and dy == 0:
                    continue

                new_x = player_pos.x + dx
                new_y = player_pos.y + dy

                if (game_map.in_bounds(new_x, new_y) and 
                    game_map.tiles["walkable"][new_x, new_y]):
                    player_pos.x = new_x
                    player_pos.y = new_y


if __name__ == "__main__":
    main()