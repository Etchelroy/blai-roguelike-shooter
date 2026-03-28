import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 14
        self.speed = 220.0
        self.hp = 100.0
        self.max_hp = 100.0
        self.damage = 20.0
        self.fire_rate = 5.0
        self.bullet_speed = 500.0
        self.multishot = 1
        self.piercing = False
        self.shield_orb = False
        self.shield_orb_angle = 0.0
        self.dashing = False
        self.dash_timer = 0.0
        self.dash_cooldown = 0.0
        self.dash_duration = 0.18
        self.dash_speed = 600.0
        self.dash_dx = 0.0
        self.dash_dy = 0.0
        self.dash_max_cooldown = 1.0
        self.collected_powerups = []
        self.invincible_timer = 0.0

    def try_dash(self, mx, my):
        if self.dash_cooldown <= 0:
            dx = mx - self.x
            dy = my - self.y
            dist = math.hypot(dx, dy)
            if dist == 0:
                dx, dy = 1, 0
            else:
                dx /= dist
                dy /= dist
            self.dash_dx = dx
            self.dash_dy = dy
            self.dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = self.dash_max_cooldown
            self.invincible_timer = self.dash_duration

    def take_damage(self, amount):
        if self.invincible_timer > 0:
            return
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def update(self, dt, keys, arena_rect):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

        if self.dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.dashing = False
            else:
                self.x += self.dash_dx * self.dash_speed * dt
                self.y += self.dash_dy * self.dash_speed * dt
        else:
            dx, dy = 0, 0
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy += 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += 1
            if dx != 0 and dy != 0:
                n = math.sqrt(2)
                dx /= n
                dy /= n
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt

        self.x = max(arena_rect.left + self.radius, min(arena_rect.right - self.radius, self.x))
        self.y = max(arena_rect.top + self.radius, min(arena_rect.bottom - self.radius, self.y))

        if self.shield_orb:
            self.shield_orb_angle += 2.0 * dt
            if self.shield_orb_angle > math.pi * 2:
                self.shield_orb_angle -= math.pi * 2

    def shoot(self, mx, my):
        from projectiles import Bullet, PiercingBullet
        dx = mx - self.x
        dy = my - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return []
        dx /= dist
        dy /= dist
        bullets = []
        angles = [0]
        if self.multishot >= 2:
            angles = [-0.2, 0.2]
        if self.multishot >= 3:
            angles = [-0.3, 0, 0.3]
        if self.multishot >= 4:
            angles = [-0.35, -0.12, 0.12, 0.35]
        base_angle = math.atan2(dy, dx)
        for a in angles:
            ang = base_angle + a
            bdx = math.cos(ang)
            bdy = math.sin(ang)
            if self.piercing:
                b = PiercingBullet(self.x, self.y, bdx, bdy, self.bullet_speed, self.damage)
            else:
                b = Bullet(self.x, self.y, bdx, bdy, self.bullet_speed, self.damage)
            bullets.append(b)
        return bullets

    def draw(self, screen, mx, my):
        if self.shield_orb:
            orb_x = int(self.x + math.cos(self.shield_orb_angle) * 50)
            orb_y = int(self.y + math.sin(self.shield_orb_angle) * 50)
            pygame.draw.circle(screen, (80, 200, 255), (orb_x, orb_y), 12)
            pygame.draw.circle(screen, (180, 240, 255), (orb_x, orb_y), 12, 2)

        color = (80, 200, 120)
        if self.dashing:
            color = (180, 255, 200)
        if self.invincible_timer > 0 and not self.dashing:
            color = (200, 200, 80)

        pygame.draw.circle(screen, (30, 80, 50), (int(self.x) + 2, int(self.y) + 2), self.radius)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (150, 255, 180), (int(self.x), int(self.y)), self.radius, 2)

        angle = math.atan2(my - self.y, mx - self.x)
        ex = self.x + math.cos(angle) * (self.radius + 6)
        ey = self.y + math.sin(angle) * (self.radius + 6)
        pygame.draw.line(screen, (200, 255, 200), (int(self.x), int(self.y)), (int(ex), int(ey)), 3)

        # Dash cooldown arc
        if self.dash_cooldown > 0:
            fraction = self.dash_cooldown / self.dash_max_cooldown
            rect = pygame.Rect(int(self.x) - self.radius, int(self.y) - self.radius, self.radius * 2, self.radius * 2)
            end_angle = -math.pi / 2 + fraction * 2 * math.pi
            pygame.draw.arc(screen, (100, 100, 200), rect, -math.pi / 2, end_angle if end_angle > -math.pi / 2 else -math.pi / 2 + 0.01, 3)