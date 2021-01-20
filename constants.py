import pygame
import os.path
import sys

PROJECT_ROOT_DIR = os.path.dirname(__file__)
USER_DATA_PATH = os.path.join(PROJECT_ROOT_DIR, 'user_files/users.json')
LEVELS_DIRECTORY = os.path.join(PROJECT_ROOT_DIR, 'levels')

# https://www.pygame.org/docs/ref/color.html
# https://github.com/pygame/pygame/blob/master/src_py/colordict.py

class Color:
    RED = pygame.color.Color('red')
    BLUE = pygame.color.Color('blue')
    GREEN = pygame.color.Color('green')
    BLACK = pygame.color.Color('black')
    WHITE = pygame.color.Color('white')
    ORANGE = pygame.color.Color('orange')
    YELLOW = pygame.color.Color('yellow')
