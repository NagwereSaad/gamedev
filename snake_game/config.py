# config.py - Snake Game Configuration

# Game Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60

# Colors
BACKGROUND = (15, 15, 30)  # Dark blue
GRID_COLOR = (30, 30, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
DARK_GREEN = (20, 180, 20)
RED = (255, 50, 50)
YELLOW = (255, 255, 50)
GOLD = (255, 215, 0)
BLUE = (50, 150, 255)
PURPLE = (180, 70, 230)
ORANGE = (255, 150, 50)

# Snake
SNAKE_START_LENGTH = 3
SNAKE_COLOR = GREEN
SNAKE_HEAD_COLOR = (100, 255, 100)
SNAKE_SPEED = 10  # Moves per second
SPEED_INCREMENT = 0.5  # Speed increase per level
MAX_SPEED = 20

# Food
FOOD_COLOR = RED
GOLDEN_FOOD_COLOR = GOLD
SPEED_FOOD_COLOR = BLUE
FOOD_SIZE = GRID_SIZE - 2
FOOD_SPAWN_RATE = 0.95  # 95% normal, 5% special

# Obstacles
OBSTACLE_COLOR = (100, 100, 120)
OBSTACLE_COUNT_PER_LEVEL = [0, 2, 5, 8]  # Obstacles per level

# Game Settings
INITIAL_LIVES = 1  # Snake has 1 life
LEVEL_TARGET_LENGTH = [10, 20, 30]  # Target lengths to complete levels
COMBO_MULTIPLIER_THRESHOLD = 5  # Foods needed for combo
COMBO_MULTIPLIER = 1.5

# Scoring
FOOD_POINTS = 10
GOLDEN_FOOD_POINTS = 50
SPEED_FOOD_POINTS = 25
LEVEL_COMPLETE_BONUS = 100
COMBO_BONUS = 5

# Power-up duration (in seconds)
SPEED_BOOST_DURATION = 5
INVINCIBILITY_DURATION = 5

# Font sizes
TITLE_FONT_SIZE = 64
MENU_FONT_SIZE = 36
HUD_FONT_SIZE = 24
SCORE_FONT_SIZE = 28

# Level layouts (grid positions for obstacles)
LEVEL_OBSTACLES = [
    # Level 1 - No obstacles
    [],
    # Level 2 - Simple obstacles
    [
        (10, 10), (10, 11), (10, 12),
        (25, 15), (25, 16), (25, 17)
    ],
    # Level 3 - Maze-like pattern
    [
        (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
        (5, 20), (6, 20), (7, 20), (8, 20), (9, 20),
        (20, 8), (20, 9), (20, 10), (20, 11), (20, 12),
        (30, 8), (30, 9), (30, 10), (30, 11), (30, 12),
        (15, 15), (16, 15), (17, 15), (18, 15), (19, 15)
    ]
]