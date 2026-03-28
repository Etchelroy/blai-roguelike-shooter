import pygame
import math

def get_font(size):
    return pygame.font.SysFont("monospace", size, bold=True)

def draw_hud(screen, player, wave_manager, screen_w, clock):
    font_sm = get_font(16)
    font_md = get_font(20)
    font_lg = get_font(26)

    # Header bar background
    pygame.draw.rect(screen, (10, 10, 20), (0, 0, screen_w, 40))
    pygame.draw.line(screen, (60, 60, 100), (0, 40), (screen_w, 40), 2)

    # Wave counter
    wave_text = font_lg.render(f"WAVE {wave_manager.wave_number}", True, (200, 200, 255))
    screen.blit(wave_text, (16, 8))

    # FPS
    fps = int(clock.get_fps())
    fps_color = (80, 255, 80) if fps >= 55 else (255, 200, 80) if fps >= 30 else (255, 80, 80)
    fps_text = font_sm.render(f"FPS: {fps}", True, fps_color)
    screen.blit(fps_text, (screen_w - fps_text.get_width() - 16, 12))

    # Left panel HP bar
    panel_x = 16
    bar_y = 54
    bar_w = 180
    bar_h = 18
    pygame.draw.rect(screen, (60, 10, 10), (panel_x, bar_y, bar_w, bar_h), border_radius=4)
    hp_frac = max(0, player.hp / player.max_hp)
    hp_color = (80, 220, 80) if hp_frac > 0.5 else (220, 180, 40) if hp_frac > 0.25 else (220, 60, 60)
    pygame.draw.rect(screen, hp_color, (panel_x, bar_y, int(bar_w * hp_frac), bar_h), border_radius=4)
    pygame.draw.rect(screen, (150, 150, 180), (panel_x, bar_y, bar_w, bar_h), 2, border_radius=4)
    hp_label = font_sm.render(f"HP {int(player.hp)}/{int(player.max_hp)}", True, (230, 230, 230))
    screen.blit(hp_label, (panel_x + 4, bar_y + 1))

    # Dash cooldown bar
    dash_y = bar_y + 26
    pygame.draw.rect(screen, (20, 20, 60), (panel_x, dash_y, bar_w, 10), border_radius=3)
    dash_frac = max(0, 1.0 - player.dash_cooldown / player.dash_max_cooldown)
    dash_color = (100, 100, 255) if dash_frac < 1.0 else (150, 150, 255)
    pygame.draw.rect(screen, dash_color, (panel_x, dash_y, int(bar_w * dash_frac), 10), border_radius=3)
    pygame.draw.rect(screen, (80, 80, 160), (panel_x, dash_y, bar_w, 10), 1, border_radius=3)
    dl = font_sm.render("DASH", True, (150, 150, 200))
    screen.blit(dl, (panel_x + 4, dash_y - 1))

    # Collected power-up icons
    icon_y = dash_y + 20
    for i, pu in enumerate(player.collected_powerups):
        ix = panel_x + (i % 6) * 28
        iy = icon_y + (i // 6) * 28
        color = pu["icon_color"]
        pygame.draw.rect(screen, (30, 30, 50), (ix, iy, 24, 24), border_radius=4)
        pygame.draw.rect(screen, color, (ix, iy, 24, 24), 2, border_radius=4)
        ch = font_sm.render(pu["icon_char"], True, color)
        screen.blit(ch, (ix + 6, iy + 4))


def draw_main_menu(screen, screen_w, screen_h, start_rect, quit_rect):
    screen.fill((8, 8, 18))
    font_title = get_font(64)
    font_sub = get_font(22)
    font_btn = get_font(24)

    # Title
    title = font_title.render("ROGUELIKE", True, (100, 200, 255))
    sub = font_title.render("SHOOTER", True, (255, 100, 150))
    screen.blit(title, (screen_w // 2 - title.get_width() // 2, screen_h // 2 - 200))
    screen.blit(sub, (screen_w // 2 - sub.get_width() // 2, screen_h // 2 - 130))

    hint = font_sub.render("Survive waves · Pick power-ups · Don't die", True, (120, 120, 160))
    screen.blit(hint, (screen_w // 2 - hint.get_width() // 2, screen_h // 2 - 50))

    mx, my = pygame.mouse.get_pos()

    for rect, label, base_color in [
        (start_rect, "START GAME", (60, 180, 100)),
        (quit_rect, "QUIT", (160, 60, 60)),
    ]:
        hover = rect.collidepoint(mx, my)
        color = tuple(min(255, c + 40) for c in base_color) if hover else base_color
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (200, 200, 255), rect, 2, border_radius=8)
        txt = font_btn.render(label, True, (230, 230, 230))
        screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))

    controls = [
        "WASD — Move",
        "Mouse — Aim",
        "LClick / Hold — Shoot",
        "Space — Dash",
    ]
    cy = screen_h - 130
    for line in controls:
        t = font_sub.render(line, True, (80, 80, 120))
        screen.blit(t, (screen_w // 2 - t.get_width() // 2, cy))
        cy += 26


def draw_death_screen(screen, waves_survived, enemies_killed, collected_powerups, screen_w, screen_h):
    overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font_big = get_font(56)
    font_md = get_font(24)
    font_sm = get_font(18)
    font_btn = get_font(22)

    dead = font_big.render("YOU DIED", True, (220, 60, 60))
    screen.blit(dead, (screen_w // 2 - dead.get_width() // 2, screen_h // 2 - 180))

    stats = [
        f"Waves Survived: {waves_survived}",
        f"Enemies Killed: {enemies_killed}",
        f"Power-ups Collected: {len(collected_powerups)}",
    ]
    sy = screen_h // 2 - 100
    for s in stats:
        t = font_md.render(s, True, (200, 200, 220))
        screen.blit(t, (screen_w // 2 - t.get_width() // 2, sy))
        sy += 36

    if collected_powerups:
        pu_label = font_sm.render("Power-ups:", True, (150, 150, 200))
        screen.blit(pu_label, (screen_w // 2 - pu_label.get_width() // 2, sy))
        sy += 24
        names = ", ".join(p["name"] for p in collected_powerups)
        nt = font_sm.render(names[:60], True, (180, 180, 255))
        screen.blit(nt, (screen_w // 2 - nt.get_width() // 2, sy))

    mx, my = pygame.mouse.get_pos()
    retry_rect = pygame.Rect(screen_w // 2 - 100, screen_h // 2 + 140, 200, 50)
    menu_rect = pygame.Rect(screen_
Looking at the acceptance checklist, I need to implement all 7 files completely. Let me write them all out.

```python
# filename: main.py
import pygame
import sys
from player import Player
from enemies import Swarmer, Shooter, Tank
from projectiles import ProjectileManager
from powerups import PowerUpManager, POWERUP_DEFS
from wave_manager import WaveManager
from ui import UI

SCREEN_W, SCREEN_H = 960, 720
FPS = 60
ARENA_MARGIN = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Arena Shooter")
    clock = pygame.time.Clock()

    arena = pygame.Rect(ARENA_MARGIN, ARENA_MARGIN, SCREEN_W - 2*ARENA_MARGIN, SCREEN_H - 2*ARENA_MARGIN)

    state = "menu"
    player = None
    proj_mgr = None
    wave_mgr = None
    powerup_mgr = None
    ui = UI(SCREEN_W, SCREEN_H)
    enemies = []
    pending_powerup_choices = None
    stats = {"waves": 0, "kills": 0, "powerups": []}

    def start_game():
        nonlocal player, proj_mgr, wave_mgr, powerup_mgr, enemies, stats
        player = Player(SCREEN_W // 2, SCREEN_H // 2, arena)
        proj_mgr = ProjectileManager()
        wave_mgr = WaveManager()
        powerup_mgr = PowerUpManager()
        enemies = []
        stats = {"waves": 0, "kills": 0, "powerups": []}

    while True:
        dt = clock.tick(FPS) / 1000.0
        dt = min(dt, 0.05)
        mx, my = pygame.mouse.get_pos()
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if state == "menu":
            clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)
            action = ui.draw_menu(screen, mx, my, clicked)
            if action == "start":
                start_game()
                state = "playing"
                wave_mgr.start_next_wave(enemies, arena)

        elif state == "playing":
            # Input
            keys = pygame.key.get_pressed()
            shoot = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)
            dash = any(e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE for e in events)

            player.update(dt, keys, mx, my, dash, arena)

            if shoot:
                player.shoot(mx, my, proj_mgr)

            proj_mgr.update(dt, arena)

            # Enemy update
            for en in enemies:
                en.update(dt, player, proj_mgr, arena, enemies)

            # Projectile-enemy collision
            to_remove_proj = set()
            to_remove_enemy = []
            for i, proj in enumerate(proj_mgr.player_projectiles):
                if i in to_remove_proj:
                    continue
                hit_any = False
                for en in enemies:
                    if en.dead:
                        continue
                    if proj.rect.colliderect(en.rect):
                        en.hp -= proj.damage
                        if not proj.piercing:
                            to_remove_proj.add(i)
                            hit_any = True
                            break
                        else:
                            hit_any = True
                if en.hp <= 0 if enemies else False:
                    pass

            # Remove dead projectiles
            proj_mgr.player_projectiles = [p for i, p in enumerate(proj_mgr.player_projectiles) if i not in to_remove_proj]

            # Kill enemies with hp<=0
            newly_dead = []
            for en in enemies:
                if en.hp <= 0 and not en.dead:
                    en.dead = True
                    newly_dead.append(en)
                    stats["kills"] += 1

            enemies = [en for en in enemies if not en.dead]

            # Enemy projectile-player collision
            hit_projs = set()
            for i, proj in enumerate(proj_mgr.enemy_projectiles):
                if proj.rect.colliderect(player.rect):
                    player.take_damage(proj.damage)
                    hit_projs.add(i)
            proj_mgr.enemy_projectiles = [p for i, p in enumerate(proj_mgr.enemy_projectiles) if i not in hit_projs]

            # Enemy-player contact
            for en in enemies:
                if en.rect.colliderect(player.rect):
                    player.take_damage(en.contact_damage * dt)

            # Shield orb collision with enemy projectiles
            if player.shield_orbs > 0:
                new_eprojs = []
                for proj in proj_mgr.enemy_projectiles:
                    blocked = False
                    for orb_angle in player.get_orb_positions():
                        ox = player.rect.centerx + orb_angle[0]
                        oy = player.rect.centery + orb_angle[1]
                        orb_rect = pygame.Rect(ox - 8, oy - 8, 16, 16)
                        if proj.rect.colliderect(orb_rect):
                            blocked = True
                            break
                    if not blocked:
                        new_eprojs.append(proj)
                proj_mgr.enemy_projectiles = new_eprojs

            player.update_shield(dt)

            if player.hp <= 0:
                stats["waves"] = wave_mgr.current_wave
                state = "death"

            if not enemies and wave_mgr.wave_active:
                wave_mgr.wave_active = False
                stats["waves"] = wave_mgr.current_wave
                pending_powerup_choices = powerup_mgr.get_choices(3)
                state = "powerup"

            # Draw
            screen.fill((20, 20, 30))
            pygame.draw.rect(screen, (40, 40, 60), arena)
            pygame.draw.rect(screen, (80, 80, 120), arena, 3)

            for en in enemies:
                en.draw(screen)
            proj_mgr.draw(screen)
            player.draw(screen)
            ui.draw_hud(screen, player, wave_mgr.current_wave, stats["kills"], player.collected_powerups)

        elif state == "powerup":
            clicked_idx = None
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    clicked_idx = ui.get_powerup_click(mx, my, pending_powerup_choices)
            if clicked_idx is not None:
                chosen = pending_powerup_choices[clicked_idx]
                powerup_mgr.apply(chosen, player)
                player.collected_powerups.append(chosen)
                stats["powerups"].append(chosen)
                wave_mgr.start_next_wave(enemies, arena)
                state = "playing"
            ui.draw_powerup_screen(screen, pending_powerup_choices, mx, my)

        elif state == "death":
            clicked = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)
            action = ui.draw_death_screen(screen, stats, mx, my, clicked)
            if action == "menu":
                state = "menu"
            elif action == "restart":
                start_game()
                state = "playing"
                wave_mgr.start_next_wave(enemies, arena)

        pygame.display.flip()

if __name__ == "__main__":
    main()