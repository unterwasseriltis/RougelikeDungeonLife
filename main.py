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
from components.death import Death
from systems import RenderSystem, MovementSystem, InputSystem, DamageSystem, AISystem

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
        title="QudLike – Erste Kreatur",
        tileset=tileset,
    )

    game_map = generate_asteroid_field(WIDTH, HEIGHT)
    ecs = ECS()

    # === Spieler ===
    player = ecs.create_entity()
    ecs.add_component(player, Position(WIDTH // 2, HEIGHT // 2))
    ecs.add_component(player, Renderable("@", (255, 255, 255), render_order=3))
    ecs.add_component(player, Actor(name="Spieler"))
    ecs.add_component(player, Fighter(hp=30, max_hp=30))

    # === Erste Kreatur: Raumdrifter ===
    drifter = ecs.create_entity()
    drifter_x = WIDTH // 2 + 12
    drifter_y = HEIGHT // 2 - 8
    ecs.add_component(drifter, Position(drifter_x, drifter_y))
    ecs.add_component(drifter, Renderable("d", (180, 100, 255), render_order=2))  # Lila "d"
    ecs.add_component(drifter, Actor(name="Raumdrifter"))
    ecs.add_component(drifter, Fighter(hp=12, max_hp=12))

    fov_radius = 12
    print("Erste Kreatur (Raumdrifter) hinzugefügt. Drücke 'T' für Test-Schaden.")

    game_over = False

    while True:
        player_pos = ecs.get_component(player, Position)
        player_fighter = ecs.get_component(player, Fighter)
        player_dead = ecs.get_component(player, Death) is not None

        if not player_dead:
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

        # HP-Anzeige mittig unten
        if player_fighter and not player_dead:
            hp_text = f" HP: {player_fighter.hp} / {player_fighter.max_hp} "
            bar_width = 40
            bar_x = (WIDTH - bar_width) // 2
            bar_y = HEIGHT - 3

            console.print(bar_x, bar_y, " " * bar_width, fg=(0,0,0), bg=(60, 20, 20))
            hp_percent = player_fighter.hp / player_fighter.max_hp
            filled = int(bar_width * hp_percent)
            console.print(bar_x, bar_y, "█" * filled, fg=(255, 70, 70), bg=(60, 20, 20))
            text_x = bar_x + (bar_width - len(hp_text)) // 2
            console.print(text_x, bar_y, hp_text, fg=(255, 255, 255))

        if player_dead:
            console.print(WIDTH//2 - 15, HEIGHT//2 - 2, "=== GAME OVER ===", fg=(255, 50, 50))
            console.print(WIDTH//2 - 12, HEIGHT//2 + 1, "Drücke ESC zum Beenden", fg=(180, 180, 180))

        context.present(console)

        # KI aktualisieren (nur wenn Spieler lebt)
        if not player_dead:
            AISystem.update(ecs, game_map)

        # Eingabe
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

            if isinstance(event, tcod.event.KeyDown):
                if player_dead:
                    if event.sym == tcod.event.KeySym.ESCAPE:
                        raise SystemExit()
                    continue

                # Test-Schaden mit 'T' (auf Spieler)
                if event.sym == tcod.event.KeySym.t:
                    DamageSystem.apply_damage(ecs, player, 8)
                    print(f"Schaden zugefügt! Verbleibende HP: {player_fighter.hp}")

                # Normale Bewegung
                dx, dy = InputSystem.get_movement(event)
                if dx != 0 or dy != 0:
                    MovementSystem.handle_movement(ecs, game_map, dx, dy)


if __name__ == "__main__":
    main()