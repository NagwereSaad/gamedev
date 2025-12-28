import pygame
import math
import random
import time
from config import *
from paddle import Paddle
from ball import Ball
from bricks import Brick
from powerups import PowerUp
from particles import ParticleSystem
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brick Breaker - Defender of the Crystal Kingdom")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # Game state
        self.state = "menu"  # menu, playing, game_over, instructions
        self.score = 0
        self.high_score = 0
        self.lives = INITIAL_LIVES
        self.level = 0
        self.combo = 0
        self.combo_timer = 0
        self.bricks_left = 0

        # Game objects
        self.paddle = Paddle()
        self.balls = []  # Main list of balls
        self.bricks = []
        self.powerups = []
        self.particles = ParticleSystem()
        self.ui = UI()

        # Initialize first ball
        self.create_ball()

        # Load levels
        self.load_level(self.level)

        # Power-up timers
        self.powerup_timers = {
            "extend_paddle": 0,
            "slow_ball": 0
        }

    def create_ball(self, x=None, y=None):
        """Create a new ball"""
        ball = Ball(x, y)
        self.balls.append(ball)
        return ball

    def create_extra_balls(self, count):
        """Create extra balls (multi-ball power-up)"""
        if len(self.balls) == 0:
            return

        main_ball = self.balls[0]
        for _ in range(count):
            new_ball = Ball(main_ball.rect.centerx, main_ball.rect.centery)
            # Give random direction
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(3, 5)
            new_ball.speed_x = math.cos(angle) * speed
            new_ball.speed_y = math.sin(angle) * speed
            new_ball.stuck_to_paddle = False
            self.balls.append(new_ball)

    def load_level(self, level_index):
        """Load a level from the LEVELS configuration"""
        self.bricks = []
        self.powerups = []
        self.level = level_index % len(LEVELS)

        level_layout = LEVELS[self.level]
        self.bricks_left = 0

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                brick_type = level_layout[row][col]
                if brick_type > 0:
                    x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                    y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_MARGIN_TOP
                    brick = Brick(x, y, brick_type)
                    self.bricks.append(brick)
                    if brick_type != BRICK_UNBREAKABLE:
                        self.bricks_left += 1

        # Reset paddle and balls
        self.paddle.reset()
        self.balls = []
        self.create_ball()

        # Reset combo
        self.combo = 0
        self.combo_timer = 0

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

                elif event.key == pygame.K_SPACE and self.state == "playing":
                    for ball in self.balls:
                        if ball.stuck_to_paddle:
                            ball.launch()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        # Update mouse position for paddle control
        mouse_x = mouse_pos[0] if self.state == "playing" else None

        return mouse_pos, mouse_click, mouse_x

    def update_game(self, mouse_x):
        """Update game logic"""
        if self.paused or self.state != "playing":
            return

        # Update paddle
        keys = pygame.key.get_pressed()
        self.paddle.update(keys, mouse_x)

        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= 1 / 60
            if self.combo_timer <= 0:
                self.combo = 0

        # Update power-up timers
        for powerup_type in self.powerup_timers:
            if self.powerup_timers[powerup_type] > 0:
                self.powerup_timers[powerup_type] -= 1 / 60

        # Update balls
        balls_to_remove = []
        for ball in self.balls:
            ball.update(self.paddle if ball.stuck_to_paddle else None)

            # Check paddle collision
            if not ball.stuck_to_paddle:
                ball.check_paddle_collision(self.paddle)

            # Check brick collisions
            # Check brick collisions
            for brick in self.bricks:
                if brick.visible:
                    collided, points, destroyed = ball.check_brick_collision(brick)  # Fixed: unpack 3 values
                    if collided:
                        if points > 0:
                            # Add to combo
                            if self.combo_timer > 0:
                                self.combo += 1
                            else:
                                self.combo = 1
                            self.combo_timer = COMBO_TIMER

                            # Calculate score with combo bonus
                            points_earned = int(points + (self.combo - 1) * COMBO_BONUS)
                            self.score += points_earned

                            # Create particles
                            self.particles.add_brick_break(
                                brick.rect.centerx, brick.rect.centery,
                                brick.color
                            )

                        if destroyed:
                            self.bricks_left -= 1

                            # Spawn power-up from power-up bricks
                            if brick.type == BRICK_POWERUP:
                                self.spawn_powerup(brick.rect.centerx, brick.rect.centery)

                            # Check if level is complete
                            if self.bricks_left <= 0:
                                self.level_complete()
                                return

                        break  # Only one brick collision per frame

            # Check if ball fell off screen
            if ball.rect.top > SCREEN_HEIGHT:
                balls_to_remove.append(ball)

                # Create splash particles
                self.particles.add_brick_break(
                    ball.rect.centerx, SCREEN_HEIGHT,
                    ball.color
                )

        # Remove fallen balls
        for ball in balls_to_remove:
            self.balls.remove(ball)

        # If no balls left, lose a life
        if len(self.balls) == 0:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over()
            else:
                self.create_ball()

        # Update power-ups
        for powerup in self.powerups[:]:
            powerup.update()

            # Check power-up collection
            if powerup.active and powerup.rect.colliderect(self.paddle.rect):
                if powerup.collect(self):
                    # Create collection particles
                    self.particles.add_powerup_collect(
                        powerup.rect.centerx, powerup.rect.centery,
                        powerup.color
                    )

            # Remove inactive power-ups
            if not powerup.active:
                self.powerups.remove(powerup)

        # Update particles
        self.particles.update()

        # Gradually increase ball speed
        if random.random() < 0.01:  # 1% chance per frame
            for ball in self.balls:
                ball.increase_speed()

    def spawn_powerup(self, x, y):
        """Spawn a random power-up"""
        powerup_types = [
            POWERUP_MULTIBALL,
            POWERUP_EXTEND_PADDLE,
            POWERUP_SLOW_BALL,
            POWERUP_EXTRA_LIFE
        ]

        powerup_type = random.choice(powerup_types)
        powerup = PowerUp(x, y, powerup_type)
        self.powerups.append(powerup)

    def activate_powerup(self, powerup_type, duration):
        """Activate a power-up effect"""
        self.powerup_timers[powerup_type] = duration

        if powerup_type == "extend_paddle":
            self.paddle.extend()
        elif powerup_type == "slow_ball":
            for ball in self.balls:
                ball.slow_down()

    def level_complete(self):
        """Handle level completion"""
        # Add level completion bonus
        level_bonus = (self.level + 1) * 100
        self.score += level_bonus

        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score

        # Check if all levels are complete
        if self.level + 1 >= len(LEVELS):
            self.state = "game_over"
        else:
            # Load next level
            self.load_level(self.level + 1)
            self.state = "playing"

    def game_over(self):
        """Handle game over"""
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score

        self.state = "game_over"

    def reset_game(self):
        """Reset game to initial state"""
        self.score = 0
        self.lives = INITIAL_LIVES
        self.level = 0
        self.combo = 0
        self.combo_timer = 0
        self.load_level(self.level)
        self.powerups = []
        self.particles = ParticleSystem()

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
            # Draw game objects
            for brick in self.bricks:
                brick.draw(self.screen)

            for powerup in self.powerups:
                powerup.draw(self.screen)

            self.paddle.draw(self.screen)

            for ball in self.balls:
                ball.draw(self.screen)

            # Draw particles
            self.particles.draw(self.screen)

            # Draw HUD
            self.ui.draw_hud(
                self.screen, self.score, self.lives,
                self.level, self.bricks_left, self.combo
            )

            buttons = []

            # Draw pause indicator if paused
            if self.paused:
                self.ui.draw_pause(self.screen)

        elif self.state == "game_over":
            level_complete = (self.bricks_left <= 0 and self.lives > 0)
            buttons = self.ui.draw_game_over(self.screen, self.score, level_complete)

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
        while self.running:
            # Handle events
            mouse_pos, mouse_click, mouse_x = self.handle_events()

            # Update game state
            if self.state == "playing":
                self.update_game(mouse_x)

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
                            self.reset_game()
                            self.state = "playing"
                        elif button.text == "INSTRUCTIONS":
                            self.state = "instructions"
                        elif button.text == "QUIT":
                            self.running = False
                        elif button.text == "BACK TO MENU":
                            self.state = "menu"
                        elif button.text == "PLAY AGAIN":
                            self.reset_game()
                            self.state = "playing"
                        elif button.text == "NEXT LEVEL":
                            self.load_level(self.level + 1)
                            self.state = "playing"
                        elif button.text == "MAIN MENU":
                            self.state = "menu"

            # Cap the frame rate
            self.clock.tick(FPS)

        pygame.quit()