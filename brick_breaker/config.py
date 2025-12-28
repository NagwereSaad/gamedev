import pygame

# Game Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BACKGROUND = (26, 26, 46)  # Dark blue
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 150, 50)
PURPLE = (180, 70, 230)

# Paddle
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_COLOR = BLUE
PADDLE_SPEED = 8
PADDLE_EXTENDED_WIDTH = 150

# Ball
BALL_RADIUS = 10
BALL_COLOR = WHITE
BALL_SPEED_X = 4
BALL_SPEED_Y = -4
BALL_SPEED_INCREMENT = 0.2
MAX_BALL_SPEED = 10

# Bricks
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
BRICK_PADDING = 5
BRICK_MARGIN_TOP = 70
BRICK_ROWS = 5
BRICK_COLS = 9

# Brick Types
BRICK_NORMAL = 1      # 1 hit
BRICK_TOUGH = 2       # 2 hits
BRICK_POWERUP = 3     # Drops power-up
BRICK_UNBREAKABLE = 4 # Indestructible

BRICK_COLORS = {
    BRICK_NORMAL: GREEN,
    BRICK_TOUGH: ORANGE,
    BRICK_POWERUP: PURPLE,
    BRICK_UNBREAKABLE: (100, 100, 100)
}

BRICK_POINTS = {
    BRICK_NORMAL: 10,
    BRICK_TOUGH: 25,
    BRICK_POWERUP: 50,
    BRICK_UNBREAKABLE: 0
}

BRICK_HITS_NEEDED = {
    BRICK_NORMAL: 1,
    BRICK_TOUGH: 2,
    BRICK_POWERUP: 1,
    BRICK_UNBREAKABLE: -1  # Infinite
}

# Power-ups
POWERUP_WIDTH = 40
POWERUP_HEIGHT = 20
POWERUP_SPEED = 3
POWERUP_DURATION = 10  # seconds

POWERUP_MULTIBALL = 1
POWERUP_EXTEND_PADDLE = 2
POWERUP_SLOW_BALL = 3
POWERUP_EXTRA_LIFE = 4

POWERUP_COLORS = {
    POWERUP_MULTIBALL: YELLOW,
    POWERUP_EXTEND_PADDLE: BLUE,
    POWERUP_SLOW_BALL: GREEN,
    POWERUP_EXTRA_LIFE: RED
}

POWERUP_NAMES = {
    POWERUP_MULTIBALL: "MULTI-BALL",
    POWERUP_EXTEND_PADDLE: "EXTEND PADDLE",
    POWERUP_SLOW_BALL: "SLOW BALL",
    POWERUP_EXTRA_LIFE: "EXTRA LIFE"
}

# Game Settings
INITIAL_LIVES = 3
COMBO_TIMER = 1.0  # seconds for combo chain
COMBO_BONUS = 5    # points per consecutive brick

# Font sizes
TITLE_FONT_SIZE = 64
MENU_FONT_SIZE = 36
HUD_FONT_SIZE = 24
SCORE_FONT_SIZE = 28

# Level layouts (1 = normal, 2 = tough, 3 = power-up, 4 = unbreakable)
LEVELS = [
    # Level 1 - Simple pattern
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    # Level 2 - Patterned
    [
        [2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    # Level 3 - Complex with power-ups
    [
        [4, 3, 4, 3, 4, 3, 4, 3, 4],
        [3, 2, 3, 2, 3, 2, 3, 2, 3],
        [2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]