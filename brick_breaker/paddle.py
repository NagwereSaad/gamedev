import pygame
from config import *


class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = PADDLE_COLOR
        self.speed = PADDLE_SPEED
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - self.width // 2,
            SCREEN_HEIGHT - self.height - 20,
            self.width,
            self.height
        )
        self.extended = False
        self.extend_timer = 0

    def draw(self, screen):
        # Draw paddle with 3D effect
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)

        # Draw top highlight
        highlight = pygame.Rect(
            self.rect.x + 2,
            self.rect.y + 2,
            self.rect.width - 4,
            5
        )
        pygame.draw.rect(screen, (min(255, self.color[0] + 50),
                                  min(255, self.color[1] + 50),
                                  min(255, self.color[2] + 50)),
                         highlight, border_radius=2)

        # Draw power-up timer if active
        if self.extended and self.extend_timer > 0:
            # Draw timer bar above paddle
            timer_width = (self.extend_timer / POWERUP_DURATION) * self.width
            timer_rect = pygame.Rect(
                self.rect.x,
                self.rect.y - 10,
                timer_width,
                5
            )
            pygame.draw.rect(screen, BLUE, timer_rect)

    def update(self, keys, mouse_x):
        # Mouse control (primary)
        if mouse_x is not None:
            self.rect.centerx = mouse_x

        # Keyboard controls (alternative)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Keep paddle on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Update power-up timer
        if self.extended and self.extend_timer > 0:
            self.extend_timer -= 1 / 60  # Assuming 60 FPS
            if self.extend_timer <= 0:
                self.width = PADDLE_WIDTH
                self.rect.width = self.width
                self.extended = False

    def extend(self):
        """Extend paddle width"""
        self.extended = True
        self.extend_timer = POWERUP_DURATION
        old_center = self.rect.centerx
        self.width = PADDLE_EXTENDED_WIDTH
        self.rect.width = self.width
        self.rect.centerx = old_center