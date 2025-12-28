# powerups.py
import pygame
import math
from config import *


class PowerUp:
    def __init__(self, x, y, power_type):
        self.rect = pygame.Rect(x, y, POWERUP_WIDTH, POWERUP_HEIGHT)
        self.type = power_type
        self.color = POWERUP_COLORS[power_type]
        self.name = POWERUP_NAMES[power_type]
        self.active = True
        self.speed = POWERUP_SPEED

    def draw(self, screen):
        if not self.active:
            return

        # Draw power-up with pulsing effect
        time = pygame.time.get_ticks() / 1000
        pulse = abs(math.sin(time * 3)) * 0.2 + 0.8  # Fixed: use math.sin

        width = int(POWERUP_WIDTH * pulse)
        height = int(POWERUP_HEIGHT * pulse)

        draw_rect = pygame.Rect(
            self.rect.centerx - width // 2,
            self.rect.centery - height // 2,
            width,
            height
        )

        pygame.draw.rect(screen, self.color, draw_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, draw_rect, 2, border_radius=5)

        # Draw power-up symbol
        font = pygame.font.Font(None, 20)
        symbol = self.name[0]  # First letter
        text = font.render(symbol, True, WHITE)
        text_rect = text.get_rect(center=draw_rect.center)
        screen.blit(text, text_rect)

    def update(self):
        """Move power-up down the screen"""
        if self.active:
            self.rect.y += self.speed

            # Deactivate if off screen
            if self.rect.top > SCREEN_HEIGHT:
                self.active = False

    def collect(self, game):
        """Apply power-up effect to the game"""
        if not self.active:
            return False

        self.active = False

        if self.type == POWERUP_MULTIBALL:
            game.create_extra_balls(2)
            return True
        elif self.type == POWERUP_EXTEND_PADDLE:
            game.activate_powerup("extend_paddle", POWERUP_DURATION)
            return True
        elif self.type == POWERUP_SLOW_BALL:
            game.activate_powerup("slow_ball", POWERUP_DURATION)
            return True
        elif self.type == POWERUP_EXTRA_LIFE:
            game.lives += 1
            return True

        return False