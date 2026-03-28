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