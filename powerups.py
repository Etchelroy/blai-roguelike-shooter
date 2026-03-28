import random

class PowerUp:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def apply(self, player):
        pass

class DamageUp(PowerUp):
    def __init__(self):
        super().__init__("Damage Up", "+5 damage")
    
    def apply(self, player):
        player.damage += 5

class FireRateUp(PowerUp):
    def __init__(self):
        super().__init__("Fire Rate Up", "+2 fire rate")
    
    def apply(self, player):
        player.fire_rate += 2

class SpeedUp(PowerUp):
    def __init__(self):
        super().__init__("Speed Up", "+50 movement speed")
    
    def apply(self, player):
        player.speed += 50

class MultiShot(PowerUp):
    def __init__(self):
        super().__init__("MultiShot", "Fire 3 bullets")
    
    def apply(self, player):
        player.multishot = 3

class Piercing(PowerUp):
    def __init__(self):
        super().__init__("Piercing Shots", "Bullets pierce enemies")
    
    def apply(self, player):
        player.piercing = 1

class HealthRestore(PowerUp):
    def __init__(self):
        super().__init__("Heal", "+40 HP")
    
    def apply(self, player):
        player.heal(40)

class MaxHealthUp(PowerUp):
    def __init__(self):
        super().__init__("Max HP Up", "+20 max HP")
    
    def apply(self, player):
        player.max_health += 20
        player.health = player.max_health

class ShieldOrb(PowerUp):
    def __init__(self):
        super().__init__("Shield Orb", "Gain 30 shield")
    
    def apply(self, player):
        player.shield_timer = player.shield_max_timer
        player.shield_health = 30
        player.shield_orb_active = True

class DashRecharge(PowerUp):
    def __init__(self):
        super().__init__("Dash Recharge", "Dash recharges faster")
    
    def apply(self, player):
        player.dash_cooldown = 0.5

def get_power_up_cards():
    all_ups = [
        DamageUp(),
        FireRateUp(),
        SpeedUp(),
        MultiShot(),
        Piercing(),
        HealthRestore(),
        MaxHealthUp(),
        ShieldOrb(),
        DashRecharge()
    ]
    return random.sample(all_ups, 3)