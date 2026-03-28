import random

POWERUP_DEFS = [
    {"id": "damage",       "name": "Damage Up",     "desc": "+25% bullet damage",    "color": (255, 80, 80),   "icon": "D"},
    {"id": "fire_rate",    "name": "Rapid Fire",     "desc": "-25% fire interval",    "color": (255, 160, 40),  "icon": "R"},
    {"id": "speed",        "name": "Speed Boost",    "desc": "+20% move speed",       "color": (80, 200, 255),  "icon": "S"},
    {"id": "multishot",    "name": "Multishot",      "desc": "+1 bullet per shot",    "color": (200, 80, 255),  "icon": "M"},
    {"id": "piercing",     "name": "Piercing",       "desc": "Bullets pierce enemies","color": (80, 255, 180),  "icon": "P"},
    {"id": "health",       "name": "Heal",           "desc": "Restore 40 HP",         "color": (80, 255, 80),   "icon": "H"},
    {"id": "max_hp",       "name": "Vitality",       "desc": "+30 max HP",            "color": (40, 200, 100),  "icon": "V"},
    {"id": "shield",       "name": "Shield Orb",     "desc": "+1 shield orb",         "color": (100, 200, 255), "icon": "O"},
    {"id": "dash_cd",      "name": "Quick Dash",     "desc": "-30% dash cooldown",    "color": (255, 220, 80),  "icon": "Q"},
]

class PowerUpManager:
    def __init__(self):
        self.pool = POWERUP_DEFS[:]

    def get_choices(self, n):
        if len(self.pool) >= n:
            return random.sample(self.pool, n)
        else:
            return random.choices(self.pool, k=n)

    def apply(self, powerup, player):
        pid = powerup["id"]
        if pid == "damage":
            player.damage = int(player.damage * 1.25)
        elif pid == "fire_rate":
            player.fire_rate = max(0.05, player.fire_rate * 0.75)
        elif pid == "speed":
            player.speed = int(player.speed * 1.2)
        elif pid == "multishot":
            player.multishot += 1
        elif pid == "piercing":
            player.piercing = True
        elif pid == "health":
            player.hp = min(player.max_hp, player.hp + 40)
        elif pid == "max_hp":
            player.max_hp += 30
            player.hp += 30
        elif pid == "shield":
            player.shield_orbs += 1
        elif pid == "dash_cd":
            player.dash_cooldown = max(0.2, player.dash_cooldown * 0.7)