POWERUP_DEFS = [
    {
        "id": "damage",
        "name": "Sharp Rounds",
        "desc": "+25% bullet damage",
        "icon_color": (255, 100, 100),
        "icon_char": "D",
    },
    {
        "id": "fire_rate",
        "name": "Auto Fire",
        "desc": "+30% fire rate",
        "icon_color": (255, 200, 80),
        "icon_char": "F",
    },
    {
        "id": "speed",
        "name": "Adrenaline",
        "desc": "+20% move speed",
        "icon_color": (80, 200, 255),
        "icon_char": "S",
    },
    {
        "id": "multishot",
        "name": "Multishot",
        "desc": "+1 extra bullet per shot",
        "icon_color": (180, 80, 255),
        "icon_char": "M",
    },
    {
        "id": "piercing",
        "name": "Piercing",
        "desc": "Bullets pierce all enemies",
        "icon_color": (80, 255, 220),
        "icon_char": "P",
    },
    {
        "id": "heal",
        "name": "Medkit",
        "desc": "Restore 40 HP",
        "icon_color": (80, 255, 120),
        "icon_char": "H",
    },
    {
        "id": "max_hp",
        "name": "Iron Will",
        "desc": "+30 max HP & heal",
        "icon_color": (255, 150, 80),
        "icon_char": "W",
    },
    {
        "id": "shield_orb",
        "name": "Shield Orb",
        "desc": "Orbiting shield blocks bullets",
        "icon_color": (100, 180, 255),
        "icon_char": "O",
    },
    {
        "id": "dash_cooldown",
        "name": "Fleet Feet",
        "desc": "-25% dash cooldown",
        "icon_color": (200, 255, 100),
        "icon_char": "T",
    },
]


def apply_powerup(player, powerup_def):
    pid = powerup_def["id"]
    player.collected_powerups.append(powerup_def)
    if pid == "damage":
        player.damage *= 1.25
    elif pid == "fire_rate":
        player.fire_rate *= 1.30
    elif pid == "speed":
        player.speed *= 1.20
    elif pid == "multishot":
        player.multishot = min(player.multishot + 1, 4)
    elif pid == "piercing":
        player.piercing = True
    elif pid == "heal":
        player.hp = min(player.max_hp, player.hp + 40)
    elif pid == "max_hp":
        player.max_hp += 30
        player.hp = min(player.max_hp, player.hp + 30)
    elif pid == "shield_orb":
        player.shield_orb = True
    elif pid == "dash_cooldown":
        player.dash_max_cooldown = max(0.3, player.dash_max_cooldown * 0.75)