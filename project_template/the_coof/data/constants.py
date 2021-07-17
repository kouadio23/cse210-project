import os

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "The Coof"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 100
RIGHT_VIEWPORT_MARGIN = 864
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = 100
PLAYER_START_Y = 225

# Absolute paths
PATH = os.path.dirname(os.path.abspath(__file__))

MUSIC = os.path.join(PATH, '..', 'assets', 'music', 'Come Thou Fount.wav')
MASK_SOUND = os.path.join(PATH, '..', 'assets', 'music', 'upgrade3.wav')
JUMP_SOUND = os.path.join(PATH, '..', 'assets', 'music', 'jump3.wav')
GAME_OVER_SOUND = os.path.join(PATH, '..', 'assets', 'music', 'gameover3.wav')

BRO_NATE = os.path.join(PATH, '..', 'assets', 'images', 'bro nate norm.png')
GAME_SCREEN = os.path.join(PATH, '..', 'assets', 'images', 'game title.png')
INSTRUCTIONS_SCREEN = os.path.join(PATH, '..', 'assets', 'images', 'instructions.png')
GAME_OVER_SCREEN = os.path.join(PATH, '..', 'assets', 'images', 'game over.png')

HIGH_SCORE = os.path.join(PATH, '..', 'high_score.txt')

MAP = os.path.join(PATH, '..', 'assets', 'maps', 'map_day.tmx')