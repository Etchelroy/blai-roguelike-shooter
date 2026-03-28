import math

class Bullet:
    def __init__(self, x, y, angle, damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = damage
        self.speed = 500
    
    def update(self, dt):
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt

class PiercingBullet(Bullet):
    def __init__(self, x, y, angle, damage):
        super().__init__(x, y, angle, damage)
        self.speed = 450

class EnemyBullet:
    def __init__(self, x, y, angle, damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = damage
        self.speed = 250
    
    def update(self, dt):
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt