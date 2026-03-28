import pygame
import math

class UI:
    def __init__(self, sw, sh):
        self.sw = sw
        self.sh = sh
        pygame.font.init()
        self.font_lg = pygame.font.SysFont("monospace", 52, bold=True)
        self.font_md = pygame.font.SysFont("monospace", 28, bold=True)
        self.font_sm = pygame.font.SysFont("monospace", 20)
        self.font_xs = pygame.font.SysFont("monospace", 16)
        self._powerup_rects = []

    def draw_menu(self, screen, mx, my, clicked):
        screen.fill((10, 10, 25))
        title = self.font_lg.render("ARENA SHOOTER", True, (100, 200, 255))
        screen.blit(title, title.get_rect(center=(self.sw//2, self.sh//2 - 100)))

        sub = self.font_sm.render("Survive the waves. Pick your power.", True, (160, 160, 200))
        screen.blit(sub, sub.get_rect(center=(self.sw//2, self.sh//2 - 40)))

        btn = pygame.Rect(0, 0, 200, 55)
        btn.center = (self.sw//2, self.sh//2 + 60)
        hovered = btn.collidepoint(mx, my)
        pygame.draw.rect(screen, (60, 120, 220) if hovered else (40, 80, 160), btn, border_radius=8)
        pygame.draw.rect(screen, (120, 180, 255), btn, 2, border_radius=8)
        label = self.font_md.render("START", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=btn.center))

        hint = self.font_xs.render("WASD move | Mouse aim | LClick shoot | Space dash | ESC quit", True, (80, 80, 120))
        screen.blit(hint, hint.get_rect(center=(self.sw//2, self.sh//2 + 150)))

        if clicked and hovered:
            return "start"
        return None

    def draw_hud(self, screen, player, wave, kills, collected_powerups):
        # Wave / kills
        wt = self.font_sm.render(f"Wave: {wave}  Kills: {kills}", True, (220, 220, 255))
        screen.blit(wt, (10, 10))

        # HP bar
        bar_x, bar_y, bar_w, bar_h = 10, 40, 200, 18
        ratio = max(0, player.hp / player.max_hp)
        pygame.draw.rect(screen, (100, 20, 20), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, (50, 210, 80), (bar_x, bar_y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_w, bar_h), 2)
        hp_text = self.font_xs.render(f"HP {int(player.hp)}/{player.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, (bar_x + 4, bar_y + 1))

        # Dash cooldown indicator
        dash_ratio = 1.0 - (player.dash_cd_timer / player.dash_cooldown) if player.dash_cooldown > 0 else 1.0
        dash_ratio = max(0, min(1, dash_ratio))
        dbar_x, dbar_y = 10, 65
        pygame.draw.rect(screen, (40, 40, 80), (dbar_x, dbar_y, 80, 8))
        pygame.draw.rect(screen, (255, 220, 60), (dbar_x, dbar_y, int(80 * dash_ratio), 8))
        dt_label = self.font_xs.render("DASH", True, (200, 200, 120))
        screen.blit(dt_label, (dbar_x + 84, dbar_y - 2))

        # Collected powerup icons
        icon_x = 10
        icon_y = 85
        for pu in collected_powerups[-10:]:
            col = pu.get("color", (180, 180, 180))
            icon_rect = pygame.Rect(icon_x, icon_y, 22, 22)
            pygame.draw.rect(screen, col, icon_rect, border_radius=4)
            pygame.draw.rect(screen, (255, 255, 255), icon_rect, 1, border_radius=4)
            icon_label = self.font_xs.render(pu.get("icon", "?"), True, (0, 0, 0))
            screen.blit(icon_label, icon_label.get_rect(center=icon_rect.center))
            icon_x += 26
            if icon_x > 250:
                icon_x = 10
                icon_y += 26

    def draw_powerup_screen(self, screen, choices, mx, my):
        overlay = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.font_lg.render("CHOOSE A POWER-UP", True, (255, 220, 80))
        screen.blit(title, title.get_rect(center=(self.sw//2, 120)))

        self._powerup_rects = []
        card_w, card_h = 240, 160
        total_w = card_w * 3 + 40 * 2
        start_x = (self.sw - total_w) // 2
        card_y = self.sh // 2 - card_h // 2

        for i, pu in enumerate(choices):
            cx = start_x + i * (card_w + 40)
            rect = pygame.Rect(cx, card_y, card_w, card_h)
            self._powerup_rects.append(rect)
            hovered = rect.collidepoint(mx, my)
            bg = (60, 60, 90) if not hovered else (90, 90, 140)
            pygame.draw.rect(screen, bg, rect, border_radius=12)
            pygame.draw.rect(screen, pu["color"], rect, 3, border_radius=12)

            # Icon circle
            pygame.draw.circle(screen, pu["color"], (rect.centerx, rect.top + 45), 28)
            icon_surf = self.font_md.render(pu["icon"], True, (0, 0, 0))
            screen.blit(icon_surf, icon_surf.get_rect(center=(rect.centerx, rect.top + 45)))

            name_surf = self.font_sm.render(pu["name"], True, (255, 255, 255))
            screen.blit(name_surf, name_surf.get_rect(center=(rect.centerx, rect.top + 90)))

            desc_surf = self.font_xs.render(pu["desc"], True, (180, 180, 220))
            screen.blit(desc_surf, desc_surf.get_rect(center=(rect.centerx, rect.top + 120)))

        hint = self.font_xs.render("Click a card to select", True, (140, 140, 180))
        screen.blit(hint, hint.get_rect(center=(self.sw//2, card_y + card_h + 40)))

    def get_powerup_click(self, mx, my, choices):
        for i, rect in enumerate(self._powerup_rects):
            if rect.collidepoint(mx, my) and i < len(choices):
                return i
        return None

    def draw_death_screen(self, screen, stats, mx, my, clicked):
        screen.fill((15, 5, 10))
        title = self.font_lg.render("YOU DIED", True, (220, 60, 60))
        screen.blit(title, title.get_rect(center=(self.sw//2, self.sh//2 - 160)))

        lines = [
            f"Waves Survived: {stats['waves']}",
            f"Enemies Killed: {stats['kills']}",
            f"Power-ups Collected: {len(stats['powerups'])}",
        ]
        for i, line in enumerate(lines):
            surf = self.font_md.render(line, True, (200, 200, 240))
            screen.blit(surf, surf.get_rect(center=(self.sw//2, self.sh//2 - 60 + i * 45)))

        if stats["powerups"]:
            pu_label = self.font_sm.render("Power-ups:", True, (180, 180, 255))
            screen.blit(pu_label, pu_label.get_rect(center=(self.sw//2, self.sh//2 + 80)))
            icon_x = self.sw//2 - min(len(stats["powerups"]), 10) * 14
            for pu in stats["powerups"][:10]:
                col = pu.get("color", (180, 180, 180))
                r = pygame.Rect(icon_x, self.sh//2 + 100, 22, 22)
                pygame.draw.rect(screen, col, r, border_radius=4)
                il = self.font_xs.render(pu.get("icon", "?"), True, (0, 0, 0))
                screen.blit(il, il.get_rect(center=r.center))
                icon_x += 26

        action = None
        buttons = [("RESTART", "restart", self.sw//2 - 120), ("MENU", "menu", self.sw//2 + 40)]
        for label, act, bx in buttons:
            btn = pygame.Rect(bx, self.sh//2 + 160, 140, 48)
            hovered = btn.collidepoint(mx, my)
            pygame.draw.rect(screen, (80, 40, 40) if not hovered else (130, 60, 60), btn, border_radius=8)
            pygame.draw.rect(screen, (220, 100, 100), btn, 2, border_radius=8)
            ls = self.font_md.render(label, True, (255, 255, 255))
            screen.blit(ls, ls.get_rect(center=btn.center))
            if clicked and hovered:
                action = act

        return action