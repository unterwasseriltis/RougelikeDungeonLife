import tcod
import tcod.event
import random
from pathlib import Path

from game_map import GameMap
from world import GameWorld

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
        columns=console.width, rows=console.height,
        title="QudLike – Asteroidenfeld (Chunk-System)",
        tileset=tileset,
    )

    world = GameWorld(chunk_width=WIDTH, chunk_height=HEIGHT)
    game_map = world.get_current_map()

    # Spieler-Start
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    while not game_map.tiles["walkable"][player_x, player_y]:
        player_x = random.randint(20, WIDTH - 20)
        player_y = random.randint(20, HEIGHT - 20)

    fov_radius = 12
    print("=== Chunk-System gestartet ===")
    print(f"Start-Chunk: ({world.current_cx}, {world.current_cy})")
    print("Gehen Sie bis zum Rand – Chunk-Wechsel sollte jetzt funktionieren.")

    while True:
        # FOV
        game_map.visible = tcod.map.compute_fov(
            transparency=game_map.tiles["transparent"],
            pov=(player_x, player_y),
            radius=fov_radius,
            light_walls=True,
            algorithm=tcod.FOV_SHADOW
        )
        game_map.explored |= game_map.visible

        console.clear()
        game_map.render(console)

        # Chunk-Rand-Markierung (zur visuellen Kontrolle)
        for x in range(WIDTH):
            console.print(x, 0, "─", fg=(100, 100, 100))
            console.print(x, HEIGHT-1, "─", fg=(100, 100, 100))
        for y in range(HEIGHT):
            console.print(0, y, "│", fg=(100, 100, 100))
            console.print(WIDTH-1, y, "│", fg=(100, 100, 100))

        console.print(player_x, player_y, "@", fg=(255, 255, 255))
        context.present(console)

        # Eingabe & Bewegung
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

            elif isinstance(event, tcod.event.KeyDown):
                dx = dy = 0
                if event.sym == tcod.event.KeySym.UP:    dy = -1
                elif event.sym == tcod.event.KeySym.DOWN:  dy = 1
                elif event.sym == tcod.event.KeySym.LEFT:  dx = -1
                elif event.sym == tcod.event.KeySym.RIGHT: dx = 1

                if dx == 0 and dy == 0:
                    continue

                new_x = player_x + dx
                new_y = player_y + dy

                chunk_changed = False

                # === CHUNK-WECHSEL VOR der normalen Kollisionsprüfung ===
                if new_x < 0:
                    world.change_chunk(-1, 0)
                    new_x = WIDTH - 1
                    chunk_changed = True
                elif new_x >= WIDTH:
                    world.change_chunk(1, 0)
                    new_x = 0
                    chunk_changed = True
                elif new_y < 0:
                    world.change_chunk(0, -1)
                    new_y = HEIGHT - 1
                    chunk_changed = True
                elif new_y >= HEIGHT:
                    world.change_chunk(0, 1)
                    new_y = 0
                    chunk_changed = True

                if chunk_changed:
                    game_map = world.get_current_map()
                    print(f"→ Chunk gewechselt! Neuer Chunk: ({world.current_cx}, {world.current_cy})")

                # Normale Bewegung innerhalb des aktuellen (oder neuen) Chunks
                if game_map.in_bounds(new_x, new_y) and game_map.tiles["walkable"][new_x, new_y]:
                    player_x, player_y = new_x, new_y
                elif chunk_changed:
                    # Falls nach Chunk-Wechsel das neue Feld blockiert ist, trotzdem setzen
                    player_x, player_y = new_x, new_y
                    print("   Hinweis: Neues Feld war blockiert, Spieler wurde trotzdem gesetzt.")

if __name__ == "__main__":
    main()