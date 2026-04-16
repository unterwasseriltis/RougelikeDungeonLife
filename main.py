import tcod
import tcod.event
import random
from pathlib import Path

from game_map import GameMap
from procgen import generate_caves

WIDTH, HEIGHT = 80, 50

def main() -> None:
    # Tileset laden
    tileset_path = Path("data/dejavu10x10_gs_tc.png")
    if not tileset_path.exists():
        raise FileNotFoundError(f"Tileset nicht gefunden: {tileset_path.resolve()}")

    tileset = tcod.tileset.load_tilesheet(
        str(tileset_path),
        columns=32,
        rows=8,
        charmap=tcod.tileset.CHARMAP_TCOD
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)

    console = tcod.console.Console(WIDTH, HEIGHT, order="F")

    context = tcod.context.new(
        columns=console.width,
        rows=console.height,
        title="Qud-like Roguelite – Caves of Qud Stil",
        tileset=tileset,
    )

    # Prozedurale Höhlengenerierung
    random.seed()
    game_map: GameMap = generate_caves(WIDTH, HEIGHT, fill_probability=0.45, iterations=6)

    # Spieler-Startposition auf begehbarem Feld
    player_x = random.randint(5, WIDTH - 6)
    player_y = random.randint(5, HEIGHT - 6)
    while not game_map.tiles["walkable"][player_x, player_y]:
        player_x = random.randint(5, WIDTH - 6)
        player_y = random.randint(5, HEIGHT - 6)

    fov_radius = 10

    print("Spiel gestartet – Bewegung mit Pfeiltasten. FOV ist aktiv.")

    while True:
        # Field of View berechnen
        game_map.visible = tcod.map.compute_fov(
            transparency=game_map.tiles["transparent"],
            pov=(player_x, player_y),
            radius=fov_radius,
            light_walls=True,
            algorithm=tcod.FOV_SHADOW
        )

        # Erkannte Bereiche merken (wichtig für Fog of War)
        game_map.explored |= game_map.visible

        console.clear()

        # Karte mit FOV rendern
        game_map.render(console)

        # Spieler rendern (immer sichtbar)
        console.print(player_x, player_y, "@", fg=(255, 255, 255))

        context.present(console)

        # Eingabe verarbeiten
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()
            elif isinstance(event, tcod.event.KeyDown):
                dx, dy = 0, 0
                if event.sym == tcod.event.KeySym.UP:
                    dy = -1
                elif event.sym == tcod.event.KeySym.DOWN:
                    dy = 1
                elif event.sym == tcod.event.KeySym.LEFT:
                    dx = -1
                elif event.sym == tcod.event.KeySym.RIGHT:
                    dx = 1

                new_x = player_x + dx
                new_y = player_y + dy

                if (game_map.in_bounds(new_x, new_y) and 
                    game_map.tiles["walkable"][new_x, new_y]):
                    player_x, player_y = new_x, new_y


if __name__ == "__main__":
    main()