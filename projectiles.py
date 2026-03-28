import pygame
import math

class Projectile:
    def __init__(self, x, y, angle, speed, damage, color, radius, piercing=False):
        self.x = float(x)
        self.y = float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.damage = damage
        self.color = color
        self.radius = radius
        self.piercing = piercing
        self.rect = pygame.Rect(0, 0, radius*2, radius*2)
        self.rect.center = (int(x), int(y))

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def out_of_bounds(self, arena):
        return not arena.colliderect(self.rect)


class ProjectileManager:
    def __init__(self):
        self.player_projectiles = []
        self.enemy_projectiles = []

    def spawn_player(self, x, y, angle, damage, piercing=False):
        p = Projectile(x, y, angle, 600, damage, (255, 240, 80), 5, piercing)
        self.player_projectiles.append(p)

    def spawn_enemy(self, x, y, angle, damage):
        p = Projectile(x, y, angle, 280, damage, (255, 100, 50), 6)
        self.enemy_projectiles.append(p)

    def update(self, dt, arena):
        for p in self.player_projectiles:
            p.update(dt)
        for p in self.enemy_projectiles:
            p.update(dt)
        self.player_projectiles = [p for p in self.player_projectiles if not p.out_of_bounds(arena)]
        self.enemy_projectiles = [p for p in self.enemy_projectiles if not p.out_of_bounds(arena)]

    def draw(self, screen):
        for p in self.player_projectiles:
            p.draw(screen)
        for p in self.enemy_projectiles:
            p.draw(screen)