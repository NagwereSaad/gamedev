import pygame
from config import *


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        self.font = pygame.font.Font(None, MENU_FONT_SIZE)

    def draw(self, screen):
        # Draw button with hover effect
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)

        # Draw text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
        return self.is_hovered

    def is_clicked(self, pos, mouse_down):
        return self.rect.collidepoint(pos) and mouse_down


class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.font_medium = pygame.font.Font(None, MENU_FONT_SIZE)
        self.font_small = pygame.font.Font(None, HUD_FONT_SIZE)
        self.font_score = pygame.font.Font(None, SCORE_FONT_SIZE)

    def draw_main_menu(self, screen):
        """Draw the main menu"""
        screen.fill(BACKGROUND)

        # Draw title with glow effect
        title = self.font_large.render("EMERALD SERPENT", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))

        # Draw glow effect
        for offset in range(5, 0, -1):
            glow_color = (0, min(100 + offset * 30, 255), 0)
            glow_surf = self.font_large.render("EMERALD SERPENT", True, glow_color)
            glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2 + offset, 100 + offset))
            screen.blit(glow_surf, glow_rect)

        screen.blit(title, title_rect)

        # Draw subtitle
        subtitle = self.font_small.render("The Mystical Garden Quest", True, YELLOW)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(subtitle, subtitle_rect)

        # Create buttons
        button_width = 300
        button_height = 60
        button_y_start = 250
        button_spacing = 80

        play_button = Button(
            SCREEN_WIDTH // 2 - button_width // 2,
            button_y_start,
            button_width, button_height,
            "PLAY", GREEN, (100, 255, 100)
        )

        instructions_button = Button(
            SCREEN_WIDTH // 2 - button_width // 2,
            button_y_start + button_spacing,
            button_width, button_height,
            "INSTRUCTIONS", BLUE, (100, 150, 255)
        )

        quit_button = Button(
            SCREEN_WIDTH // 2 - button_width // 2,
            button_y_start + button_spacing * 2,
            button_width, button_height,
            "QUIT", RED, (255, 100, 100)
        )

        # Draw buttons
        buttons = [play_button, instructions_button, quit_button]
        return buttons

    def draw_instructions(self, screen):
        """Draw instructions screen"""
        screen.fill(BACKGROUND)

        # Title
        title = self.font_large.render("INSTRUCTIONS", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)

        # Instructions text
        instructions = [
            "CONTROLS:",
            "- Move Up: UP ARROW or W",
            "- Move Down: DOWN ARROW or S",
            "- Move Left: LEFT ARROW or A",
            "- Move Right: RIGHT ARROW or D",
            "- Pause: P key",
            "- Menu: ESC key",
            "",
            "GAMEPLAY:",
            "- Eat food to grow and earn points",
            "- Avoid walls, obstacles, and yourself",
            "- Complete levels by reaching target length",
            "",
            "FOOD TYPES:",
            "- Red: Normal food (10 points, +1 segment)",
            "- Gold: Golden food (50 points, +2 segments)",
            "- Blue: Speed food (25 points, speed boost)",
            "",
            "SPECIAL ABILITIES:",
            "- Combo: Eat 5 foods quickly for 1.5x points",
            "- Invincibility: Temporary no-collision (rare)",
            "",
            "Press ESC to return to menu"
        ]

        y_offset = 150
        for line in instructions:
            if ":" in line and not line.startswith("-"):
                # Section headers
                text = self.font_medium.render(line, True, BLUE)
            elif line.startswith("-"):
                # List items
                text = self.font_small.render(line, True, WHITE)
            else:
                # Regular text
                text = self.font_small.render(line, True, YELLOW)

            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30 if ":" in line and not line.startswith("-") else 25

        # Back button
        back_button = Button(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 100,
            300, 50,
            "BACK TO MENU", GREEN, (100, 255, 100)
        )
        back_button.draw(screen)

        return back_button

    def draw_hud(self, screen, score, length, level, speed, combo, target_length):
        """Draw heads-up display during gameplay"""
        # Draw score
        score_text = self.font_score.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        # Draw level and progress
        level_text = self.font_score.render(f"LEVEL: {level + 1}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(level_text, level_rect)

        # Draw length and target
        length_text = self.font_small.render(f"LENGTH: {length}/{target_length}", True, WHITE)
        length_rect = length_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        screen.blit(length_text, length_rect)

        # Draw speed
        speed_text = self.font_small.render(f"SPEED: {speed:.1f}", True, WHITE)
        speed_rect = speed_text.get_rect(right=SCREEN_WIDTH - 20, top=20)
        screen.blit(speed_text, speed_rect)

        # Draw combo if active
        if combo > 1:
            combo_text = self.font_medium.render(f"COMBO x{combo}!", True, YELLOW)
            combo_rect = combo_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(combo_text, combo_rect)

        # Draw power-up indicators
        # (These would show active power-ups)

    def draw_game_over(self, screen, score, length, level_complete):
        """Draw game over or level complete screen"""
        screen.fill(BACKGROUND)

        if level_complete:
            title_text = "LEVEL COMPLETE!"
            title_color = GREEN
        else:
            title_text = "GAME OVER"
            title_color = RED

        title = self.font_large.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)

        # Draw stats
        stats = [
            f"SCORE: {score}",
            f"LENGTH: {length}",
            f"LEVEL: {level_complete if level_complete else 'Failed'}"
        ]

        y_offset = 250
        for stat in stats:
            stat_text = self.font_medium.render(stat, True, WHITE)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(stat_text, stat_rect)
            y_offset += 50

        # Create buttons
        button_width = 300
        button_height = 60

        if level_complete:
            next_button = Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                400,
                button_width, button_height,
                "NEXT LEVEL", GREEN, (100, 255, 100)
            )
            menu_button = Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                480,
                button_width, button_height,
                "MAIN MENU", BLUE, (100, 150, 255)
            )
            buttons = [next_button, menu_button]
        else:
            restart_button = Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                400,
                button_width, button_height,
                "PLAY AGAIN", GREEN, (100, 255, 100)
            )
            menu_button = Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                480,
                button_width, button_height,
                "MAIN MENU", BLUE, (100, 150, 255)
            )
            buttons = [restart_button, menu_button]

        for button in buttons:
            button.draw(screen)

        return buttons

    def draw_pause(self, screen):
        """Draw pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font_large.render("PAUSED", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pause_text, pause_rect)

        # Instructions
        continue_text = self.font_small.render("Press P to continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(continue_text, continue_rect)