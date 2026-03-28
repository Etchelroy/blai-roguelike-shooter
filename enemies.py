import pygame
import math
import random

class Swarmer:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 10
        self.speed = 160.0
        self.hp = 30.0
        self.max_hp = 30.0
        self.contact_damage = 25.0
        self.color = (220, 80, 80)
        self.wobble = random.uniform(0, math.pi * 2)

    def update(self, dt, player, arena_rect):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx /= dist
            dy /= dist
        self.wobble += dt * 3
        perp_x = -dy
        perp_y = dx
        self.x += (dx + perp_x * math.sin(self.wobble) * 0.3) * self.speed * dt
        self.y += (dy + perp_y * math.sin(self.wobble) * 0.3) * self.speed * dt
        self.x = max(arena_rect.left + self.radius, min(arena_rect.right - self.radius, self.x))
        self.y = max(arena_rect.top + self.radius, min(arena_rect.bottom - self.radius, self.y))
        return None

    def draw(self, screen):
        hp_frac = self.hp / self.max_hp
        draw_enemy_base(screen, self.x, self.y, self.radius, self.color, hp_frac)
        pts = []
        for i in range(6):
            ang = i * math.pi / 3 + self.wobble * 0.5
            px = self.x + math.cos(ang) * self.radius
            py = self.y + math.sin(ang) * self.radius
            pts.append((int(px), int(py)))
        if len(pts) >= 3:
            pygame.draw.polygon(screen, self.color, pts)
            pygame.draw.polygon(screen, (255, 150, 150), pts, 2)
        draw_hp_bar(screen, self.x, self.y, self.radius, hp_frac)


class Shooter:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 14
        self.speed = 80.0
        self.hp = 60.0
        self.max_hp = 60.0
        self.contact_damage = 10.0
        self.color = (80, 80, 220)
        self.shoot_timer = random.uniform(0, 2.0)
        self.shoot_interval = 2.0
        self.preferred_dist = 250.0

    def update(self, dt, player, arena_rect):
        from projectiles import EnemyBullet
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            ndx = dx / dist
            ndy = dy / dist
        else:
            ndx, ndy = 0, 0

        if dist < self.preferred_dist - 30:
            self.x -= ndx * self.speed * dt
            self.y -= ndy * self.speed * dt
        elif dist > self.preferred_dist + 30:
            self.x += ndx * self.speed * dt
            self.y += ndy * self.speed * dt

        self.x = max(arena_rect.left + self.radius, min(arena_rect.right - self.radius, self.x))
        self.y = max(arena_rect.top + self.radius, min(arena_rect.bottom - self.radius, self.y))

        self.shoot_timer += dt
        bullets = []
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            if dist > 0:
                b = EnemyBullet(self.x, self.y, ndx, ndy, 280.0, 12.0)
                bullets.append(b)
        return bullets if bullets else None

    def draw(self, screen):
        hp_frac = self.hp / self.max_hp
        draw_enemy_base(screen, self.x, self.y, self.radius, self.color, hp_frac)
        pygame.draw.rect(screen, self.color,
                         (int(self.x) - self.radius, int(self.y) - self.radius,
                          self.radius * 2, self.radius * 2))
        pygame.draw.rect(screen, (150, 150, 255),
                         (int(self.x) - self.radius, int(self.y) - self.radius,
                          self.radius * 2, self.radius * 2), 2)
        draw_hp_bar(screen, self.x, self.y, self.radius, hp_frac)


class Tank:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 26
        self.speed = 50.0
        self.hp = 250.0
        self.max_hp = 250.0
        self.contact_damage = 40.0
        self.color = (160, 100, 40)
        self.angle = 0.0

    def update(self, dt, player, arena_rect):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx /= dist
            dy /= dist
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt
        self.angle += dt * 60
        self.x = max(arena_rect.left + self.radius, min(arena_rect.right - self.radius, self.x))
        self.y = max(arena_rect.top + self.radius, min(arena_rect.bottom - self.radius, self.y))
        return None

    def draw(self, screen):
        hp_frac = self.hp / self.max_hp
        # Shadow
        pygame.draw.circle(screen, (40, 25, 10), (int(self.x) + 3, int(self.y) + 3), self.radius)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Armor segments
        for i in range(6):
            ang = math.radians(self.angle + i * 60)
            px = self.x + math.cos(ang) * (self.radius - 5)
            py = self.y + math.sin(ang) * (self.radius - 5)
            pygame.draw.circle(screen, (200, 150, 80), (int(px), int(py)), 6)
        pygame.draw.circle(screen, (220, 180, 100), (int(self.x), int(self.y)), self.radius, 3)
        draw_hp_bar(screen, self.x, self.y, self.radius, hp_frac)


def draw_enemy_base(screen, x, y, radius, color, hp_frac):
    shadow_color = tuple(max(0, c - 60) for c in color)
    pygame.draw.circle(screen, shadow_color, (int(x) + 2, int(y) + 2), radius)

def draw_hp_bar(screen, x, y, radius, hp_frac):
    bar_w = radius * 2 + 4
    bar_h = 4
    bx = int(x) - bar_w // 2
    by = int(y) - radius - 8
    pygame.draw.rect(screen, (80, 20, 20), (bx, by, bar_w, bar_h))
    pygame.draw.rect(screen, (60, 220, 60), (bx, by, int(bar_w * hp_frac), bar_h))