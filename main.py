import pygame
import sys
import math
import random
from player import Player
from enemies import Swarmer, Shooter, Tank
from projectiles import Bullet, EnemyBullet, PiercingBullet
from powerups import PowerUp, get_power_up_cards
from ui import render_main_menu, render_hud, render_death_screen, render_card_select
from wave_manager import WaveManager

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ARENA_WIDTH = 1200
ARENA_HEIGHT = 600
ARENA_X = 40
ARENA_Y = 60

FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Roguelike Shooter")

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_WAVE_COMPLETE = 2
STATE_DEAD = 3

class Game:
    def __init__(self):
        self.state = STATE_MENU
        self.player = None
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.wave_manager = None
        self.wave_num = 0
        self.enemies_killed = 0
        self.power_ups_collected = []
        self.card_options = []
        self.selected_card = None
        
    def start_new_game(self):
        self.player = Player(ARENA_WIDTH // 2 + ARENA_X, ARENA_HEIGHT // 2 + ARENA_Y)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.wave_manager = WaveManager()
        self.wave_num = 0
        self.enemies_killed = 0
        self.power_ups_collected = []
        self.state = STATE_PLAYING
        self.spawn_wave()
        
    def spawn_wave(self):
        self.wave_num += 1
        wave_data = self.wave_manager.get_wave(self.wave_num)
        self.enemies = []
        for enemy_type, count in wave_data.items():
            for _ in range(count):
                x = random.randint(ARENA_X + 50, ARENA_X + ARENA_WIDTH - 50)
                y = random.randint(ARENA_Y + 50, ARENA_Y + ARENA_HEIGHT - 50)
                # Ensure enemy doesn't spawn too close to player
                while math.hypot(x - self.player.x, y - self.player.y) < 150:
                    x = random.randint(ARENA_X + 50, ARENA_X + ARENA_WIDTH - 50)
                    y = random.randint(ARENA_Y + 50, ARENA_Y + ARENA_HEIGHT - 50)
                
                if enemy_type == "swarmer":
                    self.enemies.append(Swarmer(x, y))
                elif enemy_type == "shooter":
                    self.enemies.append(Shooter(x, y))
                elif enemy_type == "tank":
                    self.enemies.append(Tank(x, y))
    
    def show_card_select(self):
        self.card_options = get_power_up_cards()
        self.selected_card = None
        self.state = STATE_WAVE_COMPLETE
    
    def apply_power_up(self, card_idx):
        if 0 <= card_idx < len(self.card_options):
            pu = self.card_options[card_idx]
            pu.apply(self.player)
            self.power_ups_collected.append(pu.name)
        self.state = STATE_PLAYING
        self.spawn_wave()
    
    def player_died(self):
        self.state = STATE_DEAD
    
    def update(self, dt):
        if self.state == STATE_PLAYING:
            self.player.update(dt, self.enemies)
            
            # Player shooting
            new_bullets = self.player.get_fired_bullets()
            self.player_bullets.extend(new_bullets)
            
            # Update player bullets
            for bullet in self.player_bullets[:]:
                bullet.update(dt)
                if bullet.x < ARENA_X or bullet.x > ARENA_X + ARENA_WIDTH or \
                   bullet.y < ARENA_Y or bullet.y > ARENA_Y + ARENA_HEIGHT:
                    self.player_bullets.remove(bullet)
            
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.update(dt, self.player)
                new_enemy_bullets = enemy.get_fired_bullets()
                self.enemy_bullets.extend(new_enemy_bullets)
                
                # Check collision with player bullets
                for bullet in self.player_bullets[:]:
                    if math.hypot(bullet.x - enemy.x, bullet.y - enemy.y) < enemy.radius + 5:
                        enemy.take_damage(bullet.damage)
                        if not isinstance(bullet, PiercingBullet):
                            if bullet in self.player_bullets:
                                self.player_bullets.remove(bullet)
                        if enemy.health <= 0:
                            self.enemies.remove(enemy)
                            self.enemies_killed += 1
                        break
            
            # Update enemy bullets
            for bullet in self.enemy_bullets[:]:
                bullet.update(dt)
                if bullet.x < ARENA_X or bullet.x > ARENA_X + ARENA_WIDTH or \
                   bullet.y < ARENA_Y or bullet.y > ARENA_Y + ARENA_HEIGHT:
                    self.enemy_bullets.remove(bullet)
            
            # Check collision between player and enemy bullets
            for bullet in self.enemy_bullets[:]:
                if math.hypot(bullet.x - self.player.x, bullet.y - self.player.y) < self.player.radius + 5:
                    self.player.take_damage(bullet.damage)
                    self.enemy_bullets.remove(bullet)
                    if self.player.health <= 0:
                        self.player_died()
            
            # Check collision between player and enemies
            for enemy in self.enemies[:]:
                if math.hypot(self.player.x - enemy.x, self.player.y - enemy.y) < self.player.radius + enemy.radius:
                    self.player.take_damage(1)
                    if self.player.health <= 0:
                        self.player_died()
            
            # Check if wave complete
            if len(self.enemies) == 0:
                self.show_card_select()
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_RETURN:
                        self.start_new_game()
                
                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.player.dash()
                
                elif self.state == STATE_WAVE_COMPLETE:
                    if event.key == pygame.K_1:
                        self.apply_power_up(0)
                    elif event.key == pygame.K_2:
                        self.apply_power_up(1)
                    elif event.key == pygame.K_3:
                        self.apply_power_up(2)
                
                elif self.state == STATE_DEAD:
                    if event.key == pygame.K_RETURN:
                        self.state = STATE_MENU
        
        return True
    
    def draw(self):
        screen.fill((20, 20, 20))
        
        # Draw arena border
        pygame.draw.rect(screen, (100, 100, 100), (ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT), 2)
        
        if self.state == STATE_MENU:
            render_main_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        elif self.state == STATE_PLAYING:
            # Draw player
            pygame.draw.circle(screen, (0, 200, 100), (int(self.player.x), int(self.player.y)), self.player.radius)
            
            # Draw dash effect
            if self.player.dash_time > 0:
                alpha = int(100 * (self.player.dash_time / self.player.dash_duration))
                s = pygame.Surface((self.player.radius * 2, self.player.radius * 2))
                s.set_alpha(alpha)
                s.fill((150, 255, 150))
                screen.blit(s, (int(self.player.x - self.player.radius), int(self.player.y - self.player.radius)))
            
            # Draw shield orb
            if self.player.shield_timer > 0:
                pygame.draw.circle(screen, (100, 150, 255), (int(self.player.x), int(self.player.y)), self.player.radius + 10, 2)
            
            # Draw player bullets
            for bullet in self.player_bullets:
                pygame.draw.circle(screen, (255, 200, 50), (int(bullet.x), int(bullet.y)), 3)
            
            # Draw enemies
            for enemy in self.enemies:
                color = (255, 100, 100)
                if enemy.__class__.__name__ == "Shooter":
                    color = (255, 150, 50)
                elif enemy.__class__.__name__ == "Tank":
                    color = (150, 50, 50)
                pygame.draw.circle(screen, color, (int(enemy.x), int(enemy.y)), enemy.radius)
                # Draw health bar above enemy
                bar_width = 20
                bar_height = 3
                bar_x = int(enemy.x - bar_width / 2)
                bar_y = int(enemy.y - enemy.radius - 10)
                pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                fill_width = int((enemy.health / enemy.max_health) * bar_width)
                pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))
            
            # Draw enemy bullets
            for bullet in self.enemy_bullets:
                pygame.draw.circle(screen, (255, 50, 50), (int(bullet.x), int(bullet.y)), 2)
            
            # Draw HUD
            render_hud(screen, self.player, self.wave_num, self.power_ups_collected)
        
        elif self.state == STATE_WAVE_COMPLETE:
            render_card_select(screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.card_options)
        
        elif self.state == STATE_DEAD:
            render_death_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.wave_num - 1, 
                              self.enemies_killed, self.power_ups_collected)
        
        pygame.display.flip()

def main():
    game = Game()
    running = True
    
    while running:
        running = game.handle_input()
        dt = clock.tick(FPS) / 1000.0
        game.update(dt)
        game.draw()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()