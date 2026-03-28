import random
from enemies import Swarmer, Shooter, Tank

class WaveManager:
    def __init__(self):
        self.current_wave = 0
        self.wave_active = False

    def start_next_wave(self, enemies_list, arena):
        self.current_wave += 1
        self.wave_active = True
        new_enemies = self._generate_enemies(self.current_wave, arena)
        enemies_list.clear()
        enemies_list.extend(new_enemies)

    def _generate_enemies(self, wave, arena):
        enemies = []
        base = wave + 2
        n_swarmers = base + random.randint(0, wave)
        n_shooters = max(0, wave - 1) + random.randint(0, max(1, wave // 2))
        n_tanks = max(0, (wave - 2) // 2)

        margin = 80
        def rand_pos():
            x = random.randint(arena.left + margin, arena.right - margin)
            y = random.randint(arena.top + margin, arena.bottom - margin)
            return x, y

        for _ in range(n_swarmers):
            x, y = rand_pos()
            enemies.append(Swarmer(x, y))
        for _ in range(n_shooters):
            x, y = rand_pos()
            enemies.append(Shooter(x, y))
        for _ in range(n_tanks):
            x, y = rand_pos()
            enemies.append(Tank(x, y))

        return enemies