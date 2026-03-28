import math
import random

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8
        self.health = 20
        self.max_health = 20
        self.speed = 100
        self.fired_bullets = []
    
    def update(self, dt, player):
        pass
    
    def get_fired_bullets(self):
        bullets = self.fired_bullets[:]
        self.fired_bullets = []
        return bullets
    
    def take_damage(self, amount):
        self.health -= amount

class Swarmer(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 15
        self.max_health = 15
        self.radius = 5
        self.speed = 150
    
    def update(self, dt, player):
        # Move toward player
        dist = math.hypot(player.x - self.x, player.y - self.y)
        if dist > 0:
            self.x += (player.x - self.x) / dist * self.speed * dt
            self.y += (player.y - self.y) / dist * self.speed * dt

class Shooter(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 30
        self.max_health = 30
        self.radius = 7
        self.speed = 60
        self.fire_cooldown = 0
        self.fire_rate = 1.5
    
    def update(self, dt, player):
        # Move toward player slowly
        dist = math.hypot(player.x - self.x, player.y - self.y)
        if dist > 0 and dist > 200:
            self.x += (player.x - self.x) / dist * self.speed * dt
            self.y += (player.y - self.y) / dist * self.speed * dt
        
        # Shoot at player
        self.fire_cooldown -= dt
        if self.fire_cooldown <= 0:
            from projectiles import EnemyBullet
            angle = math.atan2(player.y - self.y, player.x - self.x)
            self.fired_bullets.append(EnemyBullet(self.x, self.y, angle, 8))
            self.fire_cooldown = 1.0 / self.fire_rate

class Tank(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 80
        self.max_health = 80
        self.radius = 12
        self.speed = 40
        self.fire_cooldown = 0
        self.fire_rate = 0.8
    
    def update(self, dt, player):
        # Barely move
        dist = math.hypot(player.x - self.x, player.y - self.y)
        if dist > 0 and dist > 250:
            self.x += (player.x - self.x) / dist * self.speed * dt
            self.y += (player.y - self.y) / dist * self.speed * dt
        
        # Shoot frequently
        self.fire_cooldown -= dt
        if self.fire_cooldown <= 0:
            from projectiles import EnemyBullet
            angle = math.atan2(player.y - self.y, player.x - self.x)
            self.fired_bullets.append(EnemyBullet(self.x, self.y, angle, 12))
            self.fire_cooldown = 1.0 / self.fire_rate