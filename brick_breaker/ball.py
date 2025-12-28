import pygame
import math
from config import *


class Ball:
    def __init__(self, x=None, y=None):
        self.radius = BALL_RADIUS
        self.color = BALL_COLOR
        self.reset(x, y)

    def reset(self, x=None, y=None):
        if x is None:
            x = SCREEN_WIDTH // 2
        if y is None:
            y = SCREEN_HEIGHT // 2

        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                self.radius * 2, self.radius * 2)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.stuck_to_paddle = True
        self.slow_timer = 0

    def draw(self, screen):
        # Draw ball with gradient effect
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

        # Draw highlight
        highlight_pos = (self.rect.centerx - self.radius // 3,
                         self.rect.centery - self.radius // 3)
        pygame.draw.circle(screen, (255, 255, 200), highlight_pos, self.radius // 3)

        # Draw trail effect when moving fast
        if abs(self.speed_x) > 5 or abs(self.speed_y) > 5:
            for i in range(3):
                pos = (self.rect.centerx - self.speed_x * i * 0.2,
                       self.rect.centery - self.speed_y * i * 0.2)
                alpha = 255 - i * 80
                color = (*self.color[:3], alpha)
                # Would need surface with alpha for this effect

    def update(self, paddle=None):
        """Update ball position"""
        if self.stuck_to_paddle and paddle:
            self.rect.centerx = paddle.rect.centerx
            self.rect.bottom = paddle.rect.top - 5
            return

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Update slow timer
        if self.slow_timer > 0:
            self.slow_timer -= 1 / 60
            if self.slow_timer <= 0:
                self.speed_x *= 2
                self.speed_y *= 2

        # Wall collision (left/right)
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1

        # Ceiling collision
        if self.rect.top <= 0:
            self.speed_y *= -1

        # Keep ball in bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0

    def launch(self):
        """Launch ball from paddle"""
        if self.stuck_to_paddle:
            self.stuck_to_paddle = False

    def check_paddle_collision(self, paddle):
        """Check and handle collision with paddle"""
        if self.rect.colliderect(paddle.rect) and self.speed_y > 0:
            # Calculate hit position (from -1 to 1)
            relative_x = (self.rect.centerx - paddle.rect.centerx) / (paddle.width / 2)

            # Adjust angle based on hit position
            angle = relative_x * 60  # Max 60 degree angle
            angle_rad = math.radians(angle)

            # Calculate new speed maintaining magnitude
            speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
            self.speed_x = speed * math.sin(angle_rad)
            self.speed_y = -speed * math.cos(angle_rad)

            # Ensure minimum vertical speed
            if abs(self.speed_y) < 2:
                self.speed_y = -2 if self.speed_y < 0 else 2

            return True
        return False

    def check_brick_collision(self, brick):
        """Check and handle collision with brick"""
        if not brick.visible or not self.rect.colliderect(brick.rect):
            return False, 0, False

        # Determine collision side
        dx = self.rect.centerx - brick.rect.centerx
        dy = self.rect.centery - brick.rect.centery

        width = (self.rect.width + brick.rect.width) / 2
        height = (self.rect.height + brick.rect.height) / 2

        cross_width = width * dy
        cross_height = height * dx

        if abs(dx) <= width and abs(dy) <= height:
            if cross_width > cross_height:
                if cross_width > -cross_height:
                    # Bottom collision
                    self.speed_y = abs(self.speed_y)
                else:
                    # Left collision
                    self.speed_x = -abs(self.speed_x)
            else:
                if cross_width > -cross_height:
                    # Right collision
                    self.speed_x = abs(self.speed_x)
                else:
                    # Top collision
                    self.speed_y = -abs(self.speed_y)

            # Get hit result from brick
            points, destroyed = brick.hit()
            return True, points, destroyed  # Fixed: return 3 values consistently

        return False, 0, False  # Fixed: return 3 values consistently

    def increase_speed(self):
        """Gradually increase ball speed"""
        speed_factor = 1 + BALL_SPEED_INCREMENT
        current_speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)

        if current_speed < MAX_BALL_SPEED:
            self.speed_x *= speed_factor
            self.speed_y *= speed_factor

    def slow_down(self):
        """Slow down ball (power-up effect)"""
        self.slow_timer = POWERUP_DURATION
        self.speed_x /= 2
        self.speed_y /= 2