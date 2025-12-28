import pygame
from config import *
import random
import math


class Grid:
    def __init__(self):
        self.obstacles = []
        self.current_level = 0

    def load_level(self, level):
        """Load obstacles for specified level"""
        self.current_level = level
        self.obstacles = []

        if 0 <= level < len(LEVEL_OBSTACLES):
            self.obstacles = LEVEL_OBSTACLES[level].copy()

        return self.obstacles

    def add_random_obstacles(self, count, snake_segments, food_position):
        """Add random obstacles avoiding snake and food"""
        added = 0
        attempts = 0
        max_attempts = count * 10

        while added < count and attempts < max_attempts:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            position = (x, y)

            # Check if position is free
            if (position not in snake_segments and
                    position != food_position and
                    position not in self.obstacles):
                self.obstacles.append(position)
                added += 1

            attempts += 1

        return added

    def is_obstacle(self, position):
        """Check if position contains an obstacle"""
        return position in self.obstacles

    def get_all_obstacles(self):
        """Get all obstacle positions"""
        return self.obstacles.copy()

    def draw(self, screen):
        """Draw grid and obstacles"""
        # Draw grid lines
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)

        # Draw obstacles
        for x, y in self.obstacles:
            screen_x = x * GRID_SIZE
            screen_y = y * GRID_SIZE

            # Draw obstacle with 3D effect
            pygame.draw.rect(screen, OBSTACLE_COLOR,
                             (screen_x, screen_y, GRID_SIZE, GRID_SIZE),
                             border_radius=GRID_SIZE // 6)

            # Draw highlight
            pygame.draw.rect(screen, (150, 150, 170),
                             (screen_x + 2, screen_y + 2,
                              GRID_SIZE - 4, GRID_SIZE // 3),
                             border_radius=GRID_SIZE // 8)

            # Draw cracks/texture
            for i in range(3):
                crack_x = screen_x + random.randint(5, GRID_SIZE - 5)
                crack_y = screen_y + random.randint(5, GRID_SIZE - 5)
                crack_length = random.randint(3, 8)
                angle = random.uniform(0, math.pi * 2)

                end_x = crack_x + math.cos(angle) * crack_length
                end_y = crack_y + math.sin(angle) * crack_length

                pygame.draw.line(screen, (80, 80, 100),
                                 (crack_x, crack_y), (end_x, end_y), 2)