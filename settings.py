import pygame
from os import path

# game options/settings
TITLE = "Space Game!"
WIDTH = 400
HEIGHT = 600
FPS = 30
ENEMIES = 40
FONT_NAME = pygame.font.match_font('arial')
IMG_DIR = path.join(path.dirname(__file__), 'images')

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)