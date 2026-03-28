import math

class WaveManager:
    def __init__(self):
        pass
    
    def get_wave(self, wave_num):
        """
        Returns a dict of enemy types and counts for a given wave.
        Difficulty scales with wave number.
        """
        base_count = 3 + (wave_num - 1) * 2
        
        if wave_num == 1:
            return {"swarmer": 5}
        elif wave_num == 2:
            return {"swarmer": 6, "shooter": 2}
        elif wave_num == 3:
            return {"swarmer": 4, "shooter": 3}
        elif wave_num == 4:
            return {"swarmer": 3, "shooter": 3, "tank": 1}
        elif wave_num == 5:
            return {"swarmer": 4, "shooter": 4, "tank": 2}
        else:
            # Exponential scaling
            swarmer_count = max(2, 6 - wave_num // 3)
            shooter_count = 3 + (wave_num - 5) // 2
            tank_count = 1 + (wave_num - 5) // 3
            
            return {
                "swarmer": swarmer_count,
                "shooter": shooter_count,
                "tank": tank_count
            }