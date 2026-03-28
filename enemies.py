import pygame
import math
import random

class BaseEnemy:
    dead = False
    contact_damage = 10

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        bar_w = self.rect.width
        ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(screen, (150, 20, 20), (self.rect.x, self.rect.y - 7, bar_w, 4))
        pygame.draw.rect(screen, (50, 200, 50), (self.rect.x, self.rect.y - 7, int(bar_w * ratio), 4))


class Swarmer(BaseEnemy):
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 18, 18)
        self.rect.center = (x, y)
        self.hp = 30
        self.max_hp = 30
        self.speed = 180
        self.color = (220, 80, 80)
        self.contact_damage = 15

    def update(self, dt, player, proj_mgr, arena, enemies):
        cx, cy = self.rect.center
        px, py = player.rect.center
        dx, dy = px - cx, py - cy
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx /= dist
            dy /= dist
        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt
        _clamp(self.rect, arena)


class Shooter(BaseEnemy):
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 24, 24)
        self.rect.center = (x, y)
        self.hp = 60
        self.max_hp = 60
        self.speed = 80
        self.color = (80, 80, 220)
        self.fire_timer = random.uniform(1, 2)
        self.fire_rate = 2.0
        self.contact_damage = 8
        self.preferred_dist = 300

    def update(self, dt, player, proj_mgr, arena, enemies):
        cx, cy = self.rect.center
        px, py = player.rect.center
        dx, dy = px - cx, py - cy
        dist = math.hypot(dx, dy)
        if dist > 0:
            ndx, ndy = dx / dist, dy / dist
        else:
            ndx, ndy = 0, 0

        if dist < self.preferred_dist - 30:
            self.rect.x -= ndx * self.speed * dt
            self.rect.y -= ndy * self.speed * dt
        elif dist > self.preferred_dist + 30:
            self.rect.x += ndx * self.speed * dt
            self.rect.y += ndy * self.speed * dt

        _clamp(self.rect, arena)

        self.fire_timer -= dt
        if self.fire_timer <= 0:
            self.fire_timer = self.fire_rate
            angle = math.atan2(py - cy, px - cx)
            proj_mgr.spawn_enemy(cx, cy, angle, 12)


class Tank(BaseEnemy):
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)
        self.hp = 200
        self.max_hp = 200
        self.speed = 55
        self.color = (80, 180, 80)
        self.contact_damage = 25
        self.charge_timer = random.uniform(3, 5)
        self.charging = False
        self.charge_dir = (0, 0)
        self.charge_speed = 350
        self.charge_duration = 0
        self.fire_timer = random.uniform(2, 4)
        self.fire_rate = 3.5

    def update(self, dt, player, proj_mgr, arena, enemies):
        cx, cy = self.rect.center
        px, py = player.rect.center
        dx, dy = px - cx, py - cy
        dist = math.hypot(dx, dy)
        ndx, ndy = (dx/dist, dy/dist) if dist > 0 else (0, 0)

        self.fire_timer -= dt
        if self.fire_timer <= 0:
            self.fire_timer = self.fire_rate
            for angle_offset in [-0.3, 0, 0.3]:
                a = math.atan2(py - cy, px - cx) + angle_offset
                proj_mgr.spawn_enemy(cx, cy, a, 18)

        if self.charging:
            self.charge_duration -= dt
            self.rect.x += self.charge_dir[0] * self.charge_speed * dt
            self.rect.y += self.charge_dir[1] * self.charge_speed * dt
            _clamp(self.rect, arena)
            if self.charge_duration <= 0:
                self.charging = False
                self.charge_timer = random.uniform(3, 5)
        else:
            self.charge_timer -= dt
            if self.charge_timer <= 0:
                self.charging = True
                self.charge_dir = (ndx, ndy)
                self.charge_duration = 0.4
            else:
                self.rect.x += ndx * self.speed * dt
                self.rect.y += ndy * self.speed * dt
                _clamp(self.rect, arena)


def _clamp(rect, arena):
    if rect.left < arena.left: rect.left = arena.left
    if rect.right > arena.right: rect.right = arena.right
    if rect.top < arena.top: rect.top = arena.top
    if rect.bottom > arena.bottom: rect.bottom = arena.bottom