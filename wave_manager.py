import random
from enemies import Swarmer, Shooter, Tank
from powerups import POWERUP_DEFS

class WaveManager:
    def __init__(self):
        self.wave_number = 0
        self.spawned_count = 0
        self.total_this_wave = 0

    def start_next_wave(self):
        self.wave_number += 1
        self.spawned_count = 0

    def wave_complete(self):
        return self.spawned_count >= self.total_this_wave

    def spawn_enemies(self, arena_rect):
        w = self.wave_number
        enemies = []

        swarmers = 3 + w * 2
        shooters = max(0, w - 1)
        tanks = max(0, (w - 2) // 2)

        self.total_this_wave = swarmers + shooters + tanks

        positions = []

        def rand_pos(radius):
            for _ in range(50):
                margin = radius + 20
                x = random.randint(arena_rect.left + margin, arena_rect.right - margin)
                y = random.randint(arena_rect.top + margin, arena_rect.bottom - margin)
                positions.append((x, y))
                return x, y
            return arena_rect.centerx, arena_rect.centery

        def rand_edge():
            side = random.randint(0, 3)
            margin = 40
            if side == 0:
                return random.randint(arena_rect.left + margin, arena_rect.right - margin), arena_rect.top + margin
            elif side == 1:
                return random.randint(arena_rect.left + margin, arena_rect.right - margin), arena_rect.bottom - margin
            elif side == 2:
                return arena_rect.left + margin, random.randint(arena_rect.top + margin, arena_rect.bottom - margin)
            else:
                return arena_rect.right - margin, random.randint(arena_rect.top + margin, arena_rect.bottom - margin)

        for _ in range(swarmers):
            x, y = rand_edge()
            e = Swarmer(x, y)
            e.hp = 30 + w * 5
            e.max_hp = e.hp
            e.speed = min(220, 160 + w * 8)
            enemies.append(e)

        for _ in range(shooters):
            x, y = rand_edge()
            e = Shooter(x, y)
            e.hp = 60 + w * 10
            e.max_hp = e.hp
            e.shoot_interval = max(0.8, 2.0 - w * 0.1)
            enemies.append(e)

        for _ in range(tanks):
            x, y = rand_edge()
            e = Tank(x, y)
            e.hp = 250 + w * 40
            e.max_hp = e.hp
            enemies.append(e)

        self.spawned_count = self.total_this_wave
        random.shuffle(enemies)
        return enemies

    def pick_cards(self, count):
        return random.sample(POWERUP_DEFS, min(count, len(POWERUP_DEFS)))