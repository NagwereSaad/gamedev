import pygame
import math
from config import *


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset snake to initial state"""
        # Start in the middle of the grid
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        # Create initial segments
        self.segments = []
        for i in range(SNAKE_START_LENGTH):
            self.segments.append((start_x - i, start_y))

        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)
        self.grow_pending = 0
        self.speed = SNAKE_SPEED
        self.move_timer = 0
        self.length = SNAKE_START_LENGTH
        self.alive = True

        # Power-up states
        self.speed_boost_timer = 0
        self.invincible_timer = 0
        self.is_invincible = False

        # Visual effects
        self.wiggle_offset = 0
        self.color_shift = 0

    def update(self, dt):
        """Update snake state"""
        # Update timers
        self.wiggle_offset += dt * 10
        self.color_shift += dt * 2

        # Update power-up timers
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0:
                self.speed = SNAKE_SPEED

        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            self.is_invincible = self.invincible_timer > 0
            if not self.is_invincible:
                # Flash effect when invincibility ends
                pass

        # Update movement timer
        self.move_timer += dt
        move_interval = 1.0 / self.speed

        if self.move_timer >= move_interval:
            self.move_timer = 0
            self._move()

    def _move(self):
        """Move snake one step"""
        # Update direction
        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.segments[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Add new head
        self.segments.insert(0, new_head)

        # Remove tail if not growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
            self.length += 1
        else:
            self.segments.pop()

    def change_direction(self, new_direction):
        """Change snake direction (prevent 180-degree turns)"""
        dx, dy = new_direction
        current_dx, current_dy = self.direction

        # Prevent reversing into self
        if not (dx == -current_dx and dy == -current_dy):
            self.next_direction = new_direction

    def grow(self, amount=1):
        """Make snake grow by specified amount"""
        self.grow_pending += amount

    def increase_speed(self, amount=SPEED_INCREMENT):
        """Increase snake speed"""
        self.speed = min(self.speed + amount, MAX_SPEED)

    def activate_speed_boost(self):
        """Activate speed boost power-up"""
        self.speed_boost_timer = SPEED_BOOST_DURATION
        self.speed = min(self.speed * 1.5, MAX_SPEED * 1.5)

    def activate_invincibility(self):
        """Activate invincibility power-up"""
        self.invincible_timer = INVINCIBILITY_DURATION
        self.is_invincible = True

    def check_self_collision(self):
        """Check if snake collides with itself"""
        if self.is_invincible:
            return False

        head = self.segments[0]
        return head in self.segments[1:]

    def check_wall_collision(self):
        """Check if snake hits wall"""
        if self.is_invincible:
            return False

        x, y = self.segments[0]
        return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT

    def check_obstacle_collision(self, obstacles):
        """Check if snake hits obstacle"""
        if self.is_invincible:
            return False

        head_x, head_y = self.segments[0]
        for obs_x, obs_y in obstacles:
            if head_x == obs_x and head_y == obs_y:
                return True
        return False

    def get_head_position(self):
        """Get current head position"""
        return self.segments[0]

    def get_body_positions(self):
        """Get all body positions (excluding head)"""
        return self.segments[1:]

    def draw(self, screen):
        """Draw snake on screen"""
        for i, (x, y) in enumerate(self.segments):
            # Calculate screen position
            screen_x = x * GRID_SIZE
            screen_y = y * GRID_SIZE

            # Calculate color based on position and effects
            if i == 0:  # Head
                color = SNAKE_HEAD_COLOR
                size = GRID_SIZE

                # Add invincibility glow effect
                if self.is_invincible:
                    # Pulsing effect for invincibility
                    pulse = abs(math.sin(self.color_shift * 3)) * 0.3 + 0.7
                    color = (
                        int(color[0] * pulse),
                        int(color[1] * pulse),
                        int(color[2] * pulse)
                    )

            else:  # Body
                # Gradient from head to tail
                gradient = 1.0 - (i / len(self.segments))
                color = (
                    int(SNAKE_COLOR[0] * gradient),
                    int(SNAKE_COLOR[1] * gradient),
                    int(SNAKE_COLOR[2] * gradient)
                )
                size = GRID_SIZE - 2

                # Add wiggle effect
                wiggle = math.sin(self.wiggle_offset + i * 0.5) * 2
                screen_x += wiggle
                screen_y += wiggle
                size -= abs(wiggle) * 0.5

            # Draw snake segment
            rect = pygame.Rect(screen_x, screen_y, size, size)
            pygame.draw.rect(screen, color, rect, border_radius=int(size // 4))

            # Draw segment border
            pygame.draw.rect(screen, DARK_GREEN, rect, 2, border_radius=int(size//4))

            # Draw eyes on head
            if i == 0:
                # Calculate eye positions based on direction
                dx, dy = self.direction
                eye_size = size // 5

                if dx != 0:  # Moving horizontally
                    eye1_x = screen_x + size * 0.7 if dx > 0 else screen_x + size * 0.3
                    eye2_x = eye1_x
                    eye1_y = screen_y + size * 0.3
                    eye2_y = screen_y + size * 0.7
                else:  # Moving vertically
                    eye1_x = screen_x + size * 0.3
                    eye2_x = screen_x + size * 0.7
                    eye1_y = screen_y + size * 0.7 if dy > 0 else screen_y + size * 0.3
                    eye2_y = eye1_y

                pygame.draw.circle(screen, WHITE, (int(eye1_x), int(eye1_y)), eye_size)
                pygame.draw.circle(screen, WHITE, (int(eye2_x), int(eye2_y)), eye_size)
                pygame.draw.circle(screen, BLACK, (int(eye1_x), int(eye1_y)), eye_size // 2)
                pygame.draw.circle(screen, BLACK, (int(eye2_x), int(eye2_y)), eye_size // 2)