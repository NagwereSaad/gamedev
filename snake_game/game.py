import pygame
import random
import time
import math
from config import *
from snake import Snake
from food import Food
from grid import Grid
from particles import ParticleSystem
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Emerald Serpent - The Mystical Garden Quest")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # Game state
        self.state = "menu"  # menu, playing, game_over, instructions
        self.score = 0
        self.high_score = 0
        self.level = 0
        self.combo = 0
        self.combo_counter = 0
        self.combo_timer = 0
        self.consecutive_foods = 0

        # Game objects
        self.snake = Snake()
        self.grid = Grid()
        self.food = None
        self.particles = ParticleSystem()
        self.ui = UI()

        # Game timers
        self.game_time = 0
        self.last_food_time = 0

        # Initialize game
        self.start_new_game()

    def start_new_game(self):
        """Start a new game from scratch"""
        self.score = 0
        self.level = 0
        self.combo = 1
        self.combo_counter = 0
        self.combo_timer = 0
        self.consecutive_foods = 0
        self.game_time = 0

        self.snake.reset()
        self.grid.load_level(self.level)
        self.spawn_food()

    def spawn_food(self):
        """Spawn new food in valid position"""
        snake_positions = self.snake.segments
        obstacle_positions = self.grid.get_all_obstacles()

        self.food = Food(snake_positions, obstacle_positions)
        self.last_food_time = time.time()

    def get_target_length(self):
        """Get target length for current level"""
        if self.level < len(LEVEL_TARGET_LENGTH):
            return LEVEL_TARGET_LENGTH[self.level]
        return 30 + (self.level - len(LEVEL_TARGET_LENGTH)) * 10

    def handle_events(self):
        """Handle pygame events"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "playing":
                        self.state = "menu"
                    elif self.state in ["instructions", "game_over"]:
                        self.state = "menu"

                elif event.key == pygame.K_p and self.state == "playing":
                    self.paused = not self.paused

                # Snake controls
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake.change_direction((1, 0))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        return mouse_pos, mouse_click

    def update_game(self, dt):
        """Update game logic"""
        if self.paused or self.state != "playing":
            return

        self.game_time += dt

        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo = 1
                self.combo_counter = 0

        # Update snake
        self.snake.update(dt)

        # Check for collisions
        if self.check_collisions():
            return

        # Check food collision
        if self.food and self.food.check_collision(self.snake.get_head_position()):
            self.handle_food_collection()

        # Update food expiration
        if self.food and not self.food.update(self.game_time):
            self.spawn_food()

        # Update particles
        self.particles.update()

        # Add trail particles
        head_x, head_y = self.snake.get_head_position()
        screen_x = head_x * GRID_SIZE + GRID_SIZE // 2
        screen_y = head_y * GRID_SIZE + GRID_SIZE // 2

        self.particles.add_trail_particles(screen_x, screen_y, GREEN, 1)

        # Check level completion
        if self.snake.length >= self.get_target_length():
            self.level_complete()

    def check_collisions(self):
        """Check all collision types"""
        # Check wall collision
        if self.snake.check_wall_collision():
            self.game_over()
            return True

        # Check self collision
        if self.snake.check_self_collision():
            self.game_over()
            return True

        # Check obstacle collision
        if self.snake.check_obstacle_collision(self.grid.get_all_obstacles()):
            self.game_over()
            return True

        return False

    def handle_food_collection(self):
        """Handle food collection and scoring"""
        if not self.food:
            return

        # Calculate points with combo
        base_points = self.food.get_points()
        points_earned = int(base_points * self.combo)
        self.score += points_earned

        # Get food effect
        effect = self.food.get_effect()

        # Apply growth effect
        if "grow" in effect:
            self.snake.grow(effect["grow"])

        # Apply speed boost
        if effect.get("speed_boost"):
            self.snake.activate_speed_boost()

        # Update combo
        self.consecutive_foods += 1
        current_time = time.time()

        # Check if food was eaten quickly enough for combo
        if current_time - self.last_food_time < 2.0:  # 2 second window
            self.combo_counter += 1
            if self.combo_counter >= COMBO_MULTIPLIER_THRESHOLD:
                self.combo = COMBO_MULTIPLIER
                self.combo_timer = 3.0  # 3 seconds of combo
                self.combo_counter = 0
        else:
            # Reset combo if too slow
            self.combo_counter = 1
            self.combo = 1

        self.last_food_time = current_time

        # Create particles at food position
        food_x, food_y = self.food.position
        screen_x = food_x * GRID_SIZE + GRID_SIZE // 2
        screen_y = food_y * GRID_SIZE + GRID_SIZE // 2

        self.particles.add_food_particles(screen_x, screen_y, self.food.type)

        # Spawn new food
        self.spawn_food()

        # Gradually increase speed
        if self.consecutive_foods % 5 == 0:
            self.snake.increase_speed()

    def level_complete(self):
        """Handle level completion"""
        # Add level completion bonus
        level_bonus = LEVEL_COMPLETE_BONUS * (self.level + 1)
        self.score += level_bonus

        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score

        # Move to next level
        self.level += 1

        if self.level >= len(LEVEL_OBSTACLES):
            # All levels completed
            self.state = "game_over"
        else:
            # Start next level
            self.snake.reset()
            self.grid.load_level(self.level)
            self.spawn_food()
            self.consecutive_foods = 0
            self.combo = 1
            self.combo_counter = 0

            # Add some random obstacles
            extra_obstacles = random.randint(2, 5)
            snake_positions = self.snake.segments
            food_position = self.food.position if self.food else None
            self.grid.add_random_obstacles(extra_obstacles, snake_positions, food_position)

            self.state = "playing"

    def game_over(self):
        """Handle game over"""
        # Create collision particles
        head_x, head_y = self.snake.get_head_position()
        screen_x = head_x * GRID_SIZE + GRID_SIZE // 2
        screen_y = head_y * GRID_SIZE + GRID_SIZE // 2

        self.particles.add_collision_particles(screen_x, screen_y, RED, 30)

        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score

        self.state = "game_over"

    def draw(self):
        """Draw everything to the screen"""
        self.screen.fill(BACKGROUND)

        if self.state == "menu":
            buttons = self.ui.draw_main_menu(self.screen)
            # Draw high score
            high_score_text = self.ui.font_medium.render(
                f"HIGH SCORE: {self.high_score}", True, YELLOW
            )
            high_score_rect = high_score_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
            )
            self.screen.blit(high_score_text, high_score_rect)

        elif self.state == "instructions":
            back_button = self.ui.draw_instructions(self.screen)
            buttons = [back_button]

        elif self.state == "playing":
            # Draw grid
            self.grid.draw(self.screen)

            # Draw food
            if self.food:
                self.food.draw(self.screen)

            # Draw snake
            self.snake.draw(self.screen)

            # Draw particles
            self.particles.draw(self.screen)

            # Draw HUD
            target_length = self.get_target_length()
            self.ui.draw_hud(
                self.screen, self.score, self.snake.length,
                self.level, self.snake.speed, self.combo, target_length
            )

            buttons = []

            # Draw pause indicator if paused
            if self.paused:
                self.ui.draw_pause(self.screen)

        elif self.state == "game_over":
            level_complete = (self.snake.length >= self.get_target_length())
            buttons = self.ui.draw_game_over(
                self.screen, self.score, self.snake.length, level_complete
            )

            # Draw high score
            high_score_text = self.ui.font_medium.render(
                f"HIGH SCORE: {self.high_score}", True, YELLOW
            )
            high_score_rect = high_score_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            )
            self.screen.blit(high_score_text, high_score_rect)

        pygame.display.flip()
        return buttons

    def run(self):
        """Main game loop"""
        last_time = time.time()

        while self.running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            # Handle events
            mouse_pos, mouse_click = self.handle_events()

            # Update game state
            if self.state == "playing":
                self.update_game(dt)

            # Draw everything
            buttons = self.draw()

            # Handle button hover effects
            if buttons:
                for button in buttons:
                    button.check_hover(mouse_pos)

            # Handle button clicks
            if mouse_click and buttons:
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):  # Fixed click detection
                        if button.text == "PLAY":
                            self.start_new_game()
                            self.state = "playing"
                        elif button.text == "INSTRUCTIONS":
                            self.state = "instructions"
                        elif button.text == "QUIT":
                            self.running = False
                        elif button.text == "BACK TO MENU":
                            self.state = "menu"
                        elif button.text == "PLAY AGAIN":
                            self.start_new_game()
                            self.state = "playing"
                        elif button.text == "NEXT LEVEL":
                            self.level += 1
                            self.snake.reset()
                            self.grid.load_level(self.level)
                            self.spawn_food()
                            self.state = "playing"
                        elif button.text == "MAIN MENU":
                            self.state = "menu"

            # Cap the frame rate
            self.clock.tick(FPS)

        pygame.quit()