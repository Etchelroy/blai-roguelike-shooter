import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 6
        self.health = 100
        self.max_health = 100
        self.speed = 250
        self.fire_rate = 10  # bullets per second
        self.fire_cooldown = 0
        self.damage = 10
        self.piercing = 0  # 0 or 1
        self.multishot = 1
        self.dash_speed = 400
        self.dash_duration = 0.3
        self.dash_time = 0
        self.dash_cooldown = 0
        self.dash_ready = True
        self.shield_health = 0
        self.shield_timer = 0
        self.shield_max_timer = 5
        self.shield_orb_active = False
        
    def update(self, dt, enemies):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        
        # Dash movement
        if self.dash_time > 0:
            dash_angle = self.dash_angle
            dash_dx = math.cos(dash_angle) * self.dash_speed
            dash_dy = math.sin(dash_angle) * self.dash_speed
            self.x += dash_dx * dt
            self.y += dash_dy * dt
            self.dash_time -= dt
        else:
            if dx != 0 or dy != 0:
                dist = math.hypot(dx, dy)
                self.x += (dx / dist) * self.speed * dt
                self.y += (dy / dist) * self.speed * dt
        
        # Boundary clamping (arena is 1200x600 at 40, 60)
        self.x = max(40 + self.radius, min(40 + 1200 - self.radius, self.x))
        self.y = max(60 + self.radius, min(60 + 600 - self.radius, self.y))
        
        # Fire cooldown
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt
        
        # Dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
        else:
            self.dash_ready = True
        
        # Shield timer
        if self.shield_timer > 0:
            self.shield_timer -= dt
        
    def get_fired_bullets(self):
        bullets = []
        if self.fire_cooldown <= 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
            
            if self.multishot == 1:
                bullets.append(self._create_bullet(angle))
            else:
                spread = 0.2
                for i in range(self.multishot):
                    offset = (i - self.multishot / 2 + 0.5) * spread
                    bullets.append(self._create_bullet(angle + offset))
            
            self.fire_cooldown = 1.0 / self.fire_rate
        
        return bullets
    
    def _create_bullet(self, angle):
        from projectiles import Bullet, PiercingBullet
        if self.piercing:
            return PiercingBullet(self.x, self.y, angle, self.damage)
        else:
            return Bullet(self.x, self.y, angle, self.damage)
    
    def dash(self):
        if self.dash_ready:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.dash_angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
            self.dash_time = self.dash_duration
            self.dash_cooldown = 1.0
            self.dash_ready = False
    
    def take_damage(self, amount):
        if self.shield_timer > 0:
            self.shield_health -= amount
            if self.shield_health <= 0:
                self.shield_timer = 0
        else:
            self.health -= amount
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)