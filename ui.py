import pygame

def render_main_menu(screen, width, height):
    font_title = pygame.font.Font(None, 72)
    font_btn = pygame.font.Font(None, 48)
    
    title = font_title.render("ROGUELIKE SHOOTER", True, (0, 200, 100))
    btn = font_btn.render("Press ENTER to Start", True, (200, 200, 200))
    
    screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 100))
    screen.blit(btn, (width // 2 - btn.get_width() // 2, height // 2 + 50))

def render_hud(screen, player, wave_num, power_ups_collected):
    font_small = pygame.font.Font(None, 24)
    font_medium = pygame.font.Font(None, 32)
    
    # Wave counter
    wave_text = font_medium.render(f"Wave {wave_num}", True, (255, 255, 255))
    screen.blit(wave_text, (50, 70))
    
    # Health bar
    bar_width = 200
    bar_height = 20
    bar_x = 50
    bar_y = 110
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    health_fill = int((player.health / player.max_health) * bar_width)
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_fill, bar_height))
    pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
    
    hp_text = font_small.render(f"HP: {int(player.health)}/{int(player.max_health)}", True, (255, 255, 255))
    screen.blit(hp_text, (bar_x + 5, bar_y + 2))
    
    # Shield indicator
    if player.shield_timer > 0:
        shield_text = font_small.render(f"SHIELD: {int(player.shield_health)}", True, (100, 150, 255))
        screen.blit(shield_text, (50, 140))
    
    # Power-ups collected
    pu_text = font_small.render("Power-ups:", True, (200, 200, 200))
    screen.blit(pu_text, (50, 170))
    
    for i, pu_name in enumerate(power_ups_collected[-4:]):
        pu_display = font_small.render(f"• {pu_name}", True, (150, 200, 255))
        screen.blit(pu_display, (70, 195 + i * 20))

def render_card_select(screen, width, height, cards):
    font_title = pygame.font.Font(None, 48)
    font_card = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)
    
    title = font_title.render("Pick One:", True, (255, 200, 100))
    screen.blit(title, (width // 2 - title.get_width() // 2, 50))
    
    card_width = 200
    card_height = 280
    spacing = 50
    start_x = (width - (card_width * 3 + spacing * 2)) // 2
    start_y = 150
    
    for i, card in enumerate(cards):
        x = start_x + i * (card_width + spacing)
        y = start_y
        
        # Draw card background
        pygame.draw.rect(screen, (50, 50, 100), (x, y, card_width, card_height))
        pygame.draw.rect(screen, (100, 150, 255), (x, y, card_width, card_height), 3)
        
        # Card title
        title_text = font_card.render(card.name, True, (255, 200, 100))
        screen.blit(title_text, (x + 10, y + 20))
        
        # Card description
        desc_lines = card.description.split('\n')
        for j, line in enumerate(desc_lines):
            desc_text = font_small.render(line, True, (200, 200, 200))
            screen.blit(desc_text, (x + 10, y + 80 + j * 30))
        
        # Key hint
        key_text = font_small.render(f"Press {i+1}", True, (150, 255, 150))
        screen.blit(key_text, (x + 10, y + card_height - 30))

def render_death_screen(screen, width, height, waves, enemies_killed, power_ups):
    font_title = pygame.font.Font(None, 72)
    font_stat = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 28)
    
    title = font_title.render("GAME OVER", True, (255, 50, 50))
    screen.blit(title, (width // 2 - title.get_width() // 2, 80))
    
    waves_text = font_stat.render(f"Waves Survived: {waves}", True, (255, 200, 100))
    screen.blit(waves_text, (width // 2 - waves_text.get_width() // 2, 200))
    
    enemies_text = font_stat.render(f"Enemies Killed: {enemies_killed}", True, (100, 200, 255))
    screen.blit(enemies_text, (width // 2 - enemies_text.get_width() // 2, 270))
    
    powerups_text = font_small.render(f"Power-ups Collected: {len(power_ups)}", True, (200, 200, 200))
    screen.blit(powerups_text, (width // 2 - powerups_text.get_width() // 2, 350))
    
    restart = font_small.render("Press ENTER to return to menu", True, (150, 255, 150))
    screen.blit(restart, (width // 2 - restart.get_width() // 2, 500))