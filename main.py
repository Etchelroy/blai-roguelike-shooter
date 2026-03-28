import pygame
import sys
import math
from player import Player
from enemies import Swarmer, Shooter, Tank
from projectiles import Bullet, EnemyBullet
from powerups import POWERUP_DEFS, apply_powerup
from ui import draw_hud, draw_main_menu, draw_death_screen, draw_card_selection
from wave_manager import WaveManager

pygame.init()

SCREEN_W, SCREEN_H = 1280, 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Roguelike Shooter")
clock = pygame.time.Clock()

ARENA_MARGIN = 60
ARENA_RECT = pygame.Rect(ARENA_MARGIN, ARENA_MARGIN + 40, SCREEN_W - ARENA_MARGIN * 2, SCREEN_H - ARENA_MARGIN * 2 - 40)

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_CARD_SELECT = "card_select"
STATE_DEATH = "death"

def run_game():
    state = STATE_MENU
    player = None
    enemies = []
    player_bullets = []
    enemy_bullets = []
    wave_manager = None
    selected_cards = []
    enemies_killed = 0
    shoot_timer = 0.0
    spawn_timer = 0.0

    menu_start_rect = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H // 2, 200, 50)
    menu_quit_rect = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H // 2 + 70, 200, 50)

    def reset_game():
        nonlocal player, enemies, player_bullets, enemy_bullets, wave_manager, enemies_killed, shoot_timer, spawn_timer
        player = Player(SCREEN_W // 2, SCREEN_H // 2)
        enemies = []
        player_bullets = []
        enemy_bullets = []
        wave_manager = WaveManager()
        enemies_killed = 0
        shoot_timer = 0.0
        spawn_timer = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        dt = min(dt, 0.05)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if menu_start_rect.collidepoint(mx, my):
                        reset_game()
                        wave_manager.start_next_wave()
                        enemies = wave_manager.spawn_enemies(ARENA_RECT)
                        state = STATE_PLAYING
                    elif menu_quit_rect.collidepoint(mx, my):
                        running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    reset_game()
                    wave_manager.start_next_wave()
                    enemies = wave_manager.spawn_enemies(ARENA_RECT)
                    state = STATE_PLAYING

            elif state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.try_dash(mx, my)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    bullets = player.shoot(mx, my)
                    player_bullets.extend(bullets)

            elif state == STATE_CARD_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    card_rects = get_card_rects()
                    for i, rect in enumerate(card_rects):
                        if rect.collidepoint(mx, my) and i < len(selected_cards):
                            apply_powerup(player, selected_cards[i])
                            player_bullets = []
                            enemy_bullets = []
                            enemies = []
                            wave_manager.start_next_wave()
                            enemies = wave_manager.spawn_enemies(ARENA_RECT)
                            state = STATE_PLAYING
                            break

            elif state == STATE_DEATH:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    dr = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H // 2 + 140, 200, 50)
                    mr = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H // 2 + 200, 200, 50)
                    if dr.collidepoint(mx, my):
                        reset_game()
                        wave_manager.start_next_wave()
                        enemies = wave_manager.spawn_enemies(ARENA_RECT)
                        state = STATE_PLAYING
                    elif mr.collidepoint(mx, my):
                        state = STATE_MENU
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        wave_manager.start_next_wave()
                        enemies = wave_manager.spawn_enemies(ARENA_RECT)
                        state = STATE_PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        state = STATE_MENU

        if state == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            player.update(dt, keys, ARENA_RECT)

            shoot_timer += dt
            fire_interval = 1.0 / player.fire_rate
            if pygame.mouse.get_pressed()[0] and shoot_timer >= fire_interval:
                bullets = player.shoot(mx, my)
                player_bullets.extend(bullets)
                shoot_timer = 0.0

            for b in player_bullets:
                b.update(dt)
            for b in enemy_bullets:
                b.update(dt)

            for e in enemies:
                result = e.update(dt, player, ARENA_RECT)
                if result:
                    enemy_bullets.extend(result)

            # Player bullets vs enemies
            bullets_to_remove = set()
            enemies_to_remove = set()
            for bi, b in enumerate(player_bullets):
                if not ARENA_RECT.collidepoint(b.x, b.y):
                    bullets_to_remove.add(bi)
                    continue
                for ei, e in enumerate(enemies):
                    if math.hypot(b.x - e.x, b.y - e.y) < e.radius + b.radius:
                        e.hp -= b.damage
                        if not b.piercing:
                            bullets_to_remove.add(bi)
                        if e.hp <= 0:
                            enemies_to_remove.add(ei)
                            enemies_killed += 1

            player_bullets = [b for i, b in enumerate(player_bullets) if i not in bullets_to_remove]
            enemies = [e for i, e in enumerate(enemies) if i not in enemies_to_remove]

            # Enemy bullets vs player
            ebs_to_remove = set()
            for bi, b in enumerate(enemy_bullets):
                if not ARENA_RECT.collidepoint(b.x, b.y):
                    ebs_to_remove.add(bi)
                    continue
                if math.hypot(b.x - player.x, b.y - player.y) < player.radius + b.radius:
                    if not player.dashing:
                        player.take_damage(b.damage)
                    ebs_to_remove.add(bi)
            enemy_bullets = [b for i, b in enumerate(enemy_bullets) if i not in ebs_to_remove]

            # Enemy contact with player
            for e in enemies:
                dist = math.hypot(e.x - player.x, e.y - player.y)
                if dist < e.radius + player.radius:
                    if not player.dashing:
                        player.take_damage(e.contact_damage * dt)

            # Shield orb collision
            if player.shield_orb:
                orb_angle = player.shield_orb_angle
                orb_x = player.x + math.cos(orb_angle) * 50
                orb_y = player.y + math.sin(orb_angle) * 50
                orb_r = 12
                ebs_to_remove2 = set()
                for bi, b in enumerate(enemy_bullets):
                    if math.hypot(b.x - orb_x, b.y - orb_y) < orb_r + b.radius:
                        ebs_to_remove2.add(bi)
                enemy_bullets = [b for i, b in enumerate(enemy_bullets) if i not in ebs_to_remove2]
                enemies_to_remove2 = set()
                for ei, e in enumerate(enemies):
                    if math.hypot(e.x - orb_x, e.y - orb_y) < orb_r + e.radius:
                        e.hp -= 15 * dt
                        if e.hp <= 0:
                            enemies_to_remove2.add(ei)
                            enemies_killed += 1
                enemies = [e for i, e in enumerate(enemies) if i not in enemies_to_remove2]

            if player.hp <= 0:
                state = STATE_DEATH

            if len(enemies) == 0 and wave_manager.wave_complete():
                selected_cards = wave_manager.pick_cards(3)
                state = STATE_CARD_SELECT

        screen.fill((15, 15, 25))

        if state == STATE_MENU:
            draw_main_menu(screen, SCREEN_W, SCREEN_H, menu_start_rect, menu_quit_rect)

        elif state == STATE_PLAYING:
            draw_arena(screen, ARENA_RECT)
            for e in enemies:
                e.draw(screen)
            for b in enemy_bullets:
                b.draw(screen)
            for b in player_bullets:
                b.draw(screen)
            player.draw(screen, mx, my)
            draw_hud(screen, player, wave_manager, SCREEN_W, clock)

        elif state == STATE_CARD_SELECT:
            draw_arena(screen, ARENA_RECT)
            draw_hud(screen, player, wave_manager, SCREEN_W, clock)
            draw_card_selection(screen, selected_cards, SCREEN_W, SCREEN_H, get_card_rects())

        elif state == STATE_DEATH:
            draw_death_screen(screen, wave_manager.wave_number - 1, enemies_killed, player.collected_powerups, SCREEN_W, SCREEN_H)

        draw_crosshair(screen, mx, my)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def get_card_rects():
    card_w, card_h = 220, 300
    gap = 40
    total_w = 3 * card_w + 2 * gap
    start_x = (SCREEN_W - total_w) // 2
    y = (SCREEN_H - card_h) // 2
    rects = []
    for i in range(3):
        rects.append(pygame.Rect(start_x + i * (card_w + gap), y, card_w, card_h))
    return rects

def draw_arena(screen, arena_rect):
    pygame.draw.rect(screen, (20, 20, 35), arena_rect)
    for x in range(arena_rect.left, arena_rect.right, 60):
        pygame.draw.line(screen, (25, 25, 45), (x, arena_rect.top), (x, arena_rect.bottom))
    for y in range(arena_rect.top, arena_rect.bottom, 60):
        pygame.draw.line(screen, (25, 25, 45), (arena_rect.left, y), (arena_rect.right, y))
    pygame.draw.rect(screen, (80, 80, 120), arena_rect, 3)

def draw_crosshair(screen, mx, my):
    size = 10
    gap = 4
    color = (220, 220, 220)
    pygame.draw.line(screen, color, (mx - size - gap, my), (mx - gap, my), 2)
    pygame.draw.line(screen, color, (mx + gap, my), (mx + size + gap, my), 2)
    pygame.draw.line(screen, color, (mx, my - size - gap), (mx, my - gap), 2)
    pygame.draw.line(screen, color, (mx, my + gap), (mx, my + size + gap), 2)
    pygame.draw.circle(screen, color, (mx, my), 2)

if __name__ == "__main__":
    pygame.mouse.set_visible(False)
    run_game()