import pygame
from config import *


class Brick:
    def __init__(self, x, y, brick_type):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.type = brick_type
        self.color = BRICK_COLORS[brick_type]
        self.hits = 0
        self.hits_needed = BRICK_HITS_NEEDED[brick_type]
        self.points = BRICK_POINTS[brick_type]
        self.visible = True

    def draw(self, screen):
        if not self.visible:
            return

        # Draw brick with border
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        # Draw hit counter for tough bricks
        if self.type == BRICK_TOUGH:
            font = pygame.font.Font(None, 20)
            hits_left = self.hits_needed - self.hits
            text = font.render(str(hits_left), True, WHITE)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)
        # Draw "P" for power-up bricks
        elif self.type == BRICK_POWERUP:
            font = pygame.font.Font(None, 24)
            text = font.render("P", True, WHITE)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)
        # Draw "U" for unbreakable bricks
        elif self.type == BRICK_UNBREAKABLE:
            font = pygame.font.Font(None, 24)
            text = font.render("U", True, WHITE)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

    def hit(self):
        """Handle brick being hit. Returns points and whether it should be destroyed."""
        if self.type == BRICK_UNBREAKABLE:
            return 0, False

        self.hits += 1

        if self.hits >= self.hits_needed:
            self.visible = False
            return self.points, True

        # Update color based on damage (for tough bricks)
        if self.type == BRICK_TOUGH:
            # Fade from orange to red
            damage_ratio = self.hits / self.hits_needed
            self.color = (
                int(255 * (1 - damage_ratio * 0.5)),
                int(150 * (1 - damage_ratio)),
                50
            )

        return self.points / self.hits_needed, False