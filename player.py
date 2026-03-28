import pygame
import math

class Player:
    def __init__(self, x, y, arena):
        self.arena = arena
        self.rect = pygame.Rect(0, 0, 28, 28)
        self.rect.center = (x, y)
        self.hp = 100
        self.max_hp = 100
        self.speed = 220
        self.damage = 20
        self.fire_rate = 0.25
        self.fire_timer = 0
        self.multishot = 1
        self.piercing = False
        self.shield_orbs = 0
        self.orb_angle = 0
        self.dash_speed = 600
        self.dash_duration = 0.15
        self.dash_cooldown = 1.0
        self.dashing = False
        self.dash_timer = 0
        self.dash_cd_timer = 0
        self.dash_dir = (0, 0)
        self.vx = 0
        self.vy = 0
        self.angle = 0
        self.invincible_timer = 0
        self.collected_powerups = []

    def update(self, dt, keys, mx, my, dash, arena):
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1

        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length

        self.dash_cd_timer = max(0, self.dash_cd_timer - dt)
        self.fire_timer = max(0, self.fire_timer - dt)
        self.invincible_timer = max(0, self.invincible_timer - dt)

        if dash and not self.dashing and self.dash_cd_timer <= 0:
            self.dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cd_timer = self.dash_cooldown
            if length > 0:
                self.dash_dir = (dx, dy)
            else:
                cx = mx - self.rect.centerx
                cy = my - self.rect.centery
                cl = math.hypot(cx, cy)
                if cl > 0:
                    self.dash_dir = (cx/cl, cy/cl)
                else:
                    self.dash_dir = (1, 0)
            self.invincible_timer = self.dash_duration

        if self.dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.dashing = False
            move_x = self.dash_dir[0] * self.dash_speed * dt
            move_y = self.dash_dir[1] * self.dash_speed * dt
        else:
            move_x = dx * self.speed * dt
            move_y = dy * self.speed * dt

        self.rect.x += move_x
        self.rect.y += move_y
        self._clamp_to_arena(arena)

        self.angle = math.degrees(math.atan2(my - self.rect.centery, mx - self.rect.centerx))

    def _clamp_to_arena(self, arena):
        if self.rect.left < arena.left: self.rect.left = arena.left
        if self.rect.right > arena.right: self.rect.right = arena.right
        if self.rect.top < arena.top: self.rect.top = arena.top
        if self.rect.bottom > arena.bottom: self.rect.bottom = arena.bottom

    def shoot(self, mx, my, proj_mgr):
        if self.fire_timer > 0:
            return
        self.fire_timer = self.fire_rate
        cx, cy = self.rect.center
        base_angle = math.atan2(my - cy, mx - cx)
        spread = 0.2
        for i in range(self.multishot):
            if self.multishot == 1:
                a = base_angle
            else:
                a = base_angle + (i - (self.multishot - 1) / 2) * spread
            proj_mgr.spawn_player(cx, cy, a, self.damage, self.piercing)

    def take_damage(self, amount):
        if self.invincible_timer > 0:
            return
        self.hp -= amount
        self.hp = max(0, self.hp)

    def get_orb_positions(self):
        positions = []
        for i in range(self.shield_orbs):
            a = self.orb_angle + (2 * math.pi * i / self.shield_orbs)
            positions.append((math.cos(a) * 35, math.sin(a) * 35))
        return positions

    def update_shield(self, dt):
        self.orb_angle += dt * 2.0

    def draw(self, screen):
        color = (100, 200, 255) if not self.dashing else (255, 255, 100)
        pygame.draw.rect(screen, color, self.rect)
        # Direction indicator
        cx, cy = self.rect.center
        ex = cx + math.cos(math.radians(self.angle)) * 16
        ey = cy + math.sin(math.radians(self.angle)) * 16
        pygame.draw.line(screen, (200, 240, 255), (cx, cy), (int(ex), int(ey)), 3)
        # Shield orbs
        for ox, oy in self.get_orb_positions():
            pygame.draw.circle(screen, (100, 255, 200), (int(cx + ox), int(cy + oy)), 7)
        # HP bar
        bar_w = 30
        bar_h = 5
        ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(screen, (180, 30, 30), (self.rect.x, self.rect.y - 10, bar_w, bar_h))
        pygame.draw.rect(screen, (50, 220, 50), (self.rect.x, self.rect.y - 10, int(bar_w * ratio), bar_h))