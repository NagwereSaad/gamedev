import pygame
import random
import math
from config import *


class Food:
    def __init__(self, snake_segments=None, obstacles=None):
        self.snake_segments = snake_segments or []
        self.obstacles = obstacles or []
        self.type = "normal"  # normal, golden, speed
        self.position = (0, 0)
        self.spawn_time = 0
        self.lifetime = 15  # seconds
        self.spawn()

    def spawn(self):
        """Spawn food at random position"""
        attempts = 0
        max_attempts = 100

        while attempts < max_attempts:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            position = (x, y)

            # Check if position is free
            if (position not in self.snake_segments and
                    position not in self.obstacles):
                self.position = position

                # Determine food type
                rand = random.random()
                if rand < 0.05:  # 5% golden food
                    self.type = "golden"
                elif rand < 0.10:  # 5% speed food
                    self.type = "speed"
                else:  # 90% normal food
                    self.type = "normal"

                self.spawn_time = pygame.time.get_ticks() / 1000
                return True

            attempts += 1

        # Couldn't find valid position
        return False

    def update(self, current_time):
        """Update food state (check expiration)"""
        elapsed = current_time - self.spawn_time
        return elapsed < self.lifetime

    def check_collision(self, snake_head):
        """Check if snake head collides with food"""
        return snake_head == self.position

    def get_points(self):
        """Get points value for this food type"""
        if self.type == "normal":
            return FOOD_POINTS
        elif self.type == "golden":
            return GOLDEN_FOOD_POINTS
        elif self.type == "speed":
            return SPEED_FOOD_POINTS
        return 0

    def get_effect(self):
        """Get special effect for this food type"""
        if self.type == "golden":
            return {"grow": 2}  # Grow by 2 segments
        elif self.type == "speed":
            return {"speed_boost": True}
        return {"grow": 1}  # Normal food grows by 1

    def draw(self, screen):
        """Draw food on screen"""
        x, y = self.position
        screen_x = x * GRID_SIZE + GRID_SIZE // 2
        screen_y = y * GRID_SIZE + GRID_SIZE // 2

        # Choose color based on type
        if self.type == "normal":
            color = FOOD_COLOR
            size = FOOD_SIZE
        elif self.type == "golden":
            color = GOLDEN_FOOD_COLOR
            size = FOOD_SIZE + 2
        elif self.type == "speed":
            color = SPEED_FOOD_COLOR
            size = FOOD_SIZE

        # Animate the food
        time = pygame.time.get_ticks() / 1000
        pulse = abs(math.sin(time * 3)) * 0.2 + 0.8

        # Draw pulsing circle
        radius = int(size * pulse / 2)
        pygame.draw.circle(screen, color, (screen_x, screen_y), radius)

        # Draw highlight
        highlight_radius = radius // 2
        highlight_pos = (
            screen_x - radius // 3,
            screen_y - radius // 3
        )
        pygame.draw.circle(screen, WHITE, highlight_pos, highlight_radius)

        # Draw sparkle effect for golden food
        if self.type == "golden":
            for i in range(4):
                angle = time * 2 + i * math.pi / 2
                sparkle_x = screen_x + math.cos(angle) * radius * 1.5
                sparkle_y = screen_y + math.sin(angle) * radius * 1.5
                sparkle_size = abs(math.sin(time * 4 + i)) * 2 + 1
                pygame.draw.circle(screen, YELLOW,
                                   (int(sparkle_x), int(sparkle_y)),
                                   int(sparkle_size))

        # Draw timer ring for expiration
        elapsed = time - self.spawn_time
        if elapsed > self.lifetime * 0.7:  # Last 30% of lifetime
            progress = (elapsed - self.lifetime * 0.7) / (self.lifetime * 0.3)
            angle = 360 * progress

            # Draw warning ring
            if progress > 0.5:
                ring_color = RED
            else:
                ring_color = ORANGE

            pygame.draw.arc(screen, ring_color,
                            (screen_x - radius - 2, screen_y - radius - 2,
                             (radius + 2) * 2, (radius + 2) * 2),
                            0, math.radians(angle), 3)