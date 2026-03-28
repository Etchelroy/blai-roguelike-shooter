import pygame
import math

class Bullet:
    def __init__(self, x, y, dx, dy, speed, damage):
        self.x = float(x)
        self.y = float(y)
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.radius = 5
        self.piercing = False
        self.color = (255, 240, 80)
        self.trail = []

    def update(self, dt):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

    def draw(self, screen):
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(120 * (i + 1) / len(self.trail)) if self.trail else 0
            r = max(1, self.radius - (len(self.trail) - i))
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color[:3], alpha), (r, r), r)
            screen.blit(s, (int(tx) - r, int(ty) - r))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 200), (int(self.x), int(self.y)), self.radius - 2)


class PiercingBullet(Bullet):
    def __init__(self, x, y, dx, dy, speed, damage):
        super().__init__(x, y, dx, dy, speed, damage)
        self.piercing = True
        self.radius = 6
        self.color = (80, 255, 220)
        self.hits = set()


class EnemyBullet:
    def __init__(self, x, y, dx, dy, speed, damage):
        self.x = float(x)
        self.y = float(y)
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.radius = 6
        self.color = (255, 80, 80)

    def update(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, (120, 20, 20), (int(self.x) + 1, int(self.y) + 1), self.radius)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 180, 180), (int(self.x), int(self.y)), self.radius - 2)