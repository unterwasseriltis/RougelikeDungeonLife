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
from systems import RenderSystem, MovementSystem, InputSystem, DamageSystem, AISystem, CombatSystem

WIDTH, HEIGHT = 120, 80

def main() -> None:
    tileset_path = Path("data/custom_tileset.png")
    if not tileset_path.exists():
        print("FEHLER: 'data/custom_tileset.png' nicht gefunden!")
        input("Drücken Sie Enter zum Beenden...")
        return

    # 32x32 Tileset laden
    tileset = tcod.tileset.load_tilesheet(
        str(tileset_path), columns=16, rows=16, charmap=tcod.tileset.CHARMAP_CP437
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)

    console = tcod.console.Console(WIDTH, HEIGHT, order="F")
    context = tcod.context.new(
        columns=console.width,
        rows=console.height,
        title="QudLike – 32x32 Tileset",
        tileset=tileset,
    )

    game_map = generate_asteroid_field(WIDTH, HEIGHT)
    ecs = ECS()

    player = ecs.create_entity()
    ecs.add_component(player, Position(WIDTH // 2, HEIGHT // 2))
    ecs.add_component(player, Renderable("@", (255, 255, 255), render_order=3))
    ecs.add_component(player, Actor(name="Spieler"))
    ecs.add_component(player, Fighter(hp=30, max_hp=30))

    drifter = ecs.create_entity()
    drifter_x = WIDTH // 2 + 12
    drifter_y = HEIGHT // 2 - 8
    ecs.add_component(drifter, Position(drifter_x, drifter_y))
    ecs.add_component(drifter, Renderable("d", (180, 100, 255), render_order=2))
    ecs.add_component(drifter, Actor(name="Raumdrifter"))
    ecs.add_component(drifter, Fighter(hp=12, max_hp=12))

    fov_radius = 12
    print("Spiel gestartet. Drücke T für Schaden, Space/A für Angriff.")

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
                algorithm=tcod.FOV_BASIC
            )
            game_map.explored |= game_map.visible

        console.clear()

        # Spielwelt + Entities rendern
        game_map.render(console)
        RenderSystem.render(console, ecs)

        # Einfache HP-Anzeige (ohne komplizierte Blit-Logik)
        if player_fighter and not player_dead:
            hp_text = f"HP: {player_fighter.hp}/{player_fighter.max_hp}"
            console.print(2, HEIGHT - 2, hp_text, fg=(255, 100, 100))

        if player_dead:
            console.print(WIDTH//2 - 15, HEIGHT//2 - 2, "=== GAME OVER ===", fg=(255, 50, 50))
            console.print(WIDTH//2 - 12, HEIGHT//2, "Drücke ESC zum Beenden", fg=(200, 200, 200))

        context.present(console)

        if not player_dead:
            AISystem.update(ecs, game_map)

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

            if isinstance(event, tcod.event.KeyDown):
                if player_dead:
                    if event.sym == tcod.event.KeySym.ESCAPE:
                        raise SystemExit()
                    continue

                # Angriff
                if event.sym in (tcod.event.KeySym.SPACE, tcod.event.KeySym.a):
                    drifter_pos = ecs.get_component(drifter, Position)
                    if drifter_pos:
                        dx = abs(player_pos.x - drifter_pos.x)
                        dy = abs(player_pos.y - drifter_pos.y)
                        if dx <= 1 and dy <= 1:
                            CombatSystem.attack(player, drifter, ecs)

                # Test-Schaden
                if event.sym == tcod.event.KeySym.t:
                    DamageSystem.apply_damage(ecs, player, 8)
                    print(f"Schaden zugefügt! Verbleibende HP: {player_fighter.hp if player_fighter else 0}")

                # Bewegung
                dx, dy = InputSystem.get_movement(event)
                if dx != 0 or dy != 0:
                    MovementSystem.handle_movement(ecs, game_map, dx, dy)


if __name__ == "__main__":
    main()