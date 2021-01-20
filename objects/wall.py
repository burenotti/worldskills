import pygame
from constants import Color, PROJECT_ROOT_DIR
from os.path import join


class Wall:

    images = [
        pygame.Surface((50, 50), pygame.SRCALPHA),
        pygame.image.load(join(PROJECT_ROOT_DIR, 'images/Wbrick_horizontal.png')),
        pygame.image.load(join(PROJECT_ROOT_DIR, 'images/W4points.png'))
    ]

    delta_x = {0, 1, 1, 1, 0, -1, -1, -1}
    delta_y = {1, 1, 0, -1, -1, -1, 0, 1}

    def __init__(self, wall_type=1, rotate=1):
        self.type = wall_type
        self.rotate = rotate

    def render(self, size_x: int, size_y: int) -> pygame.Surface:
        surface = pygame.Surface((size_x, size_y), pygame.SRCALPHA)
        scaled = pygame.transform.scale(self.images[self.type], (size_x, size_y))
        rotated = pygame.transform.rotate(scaled, 90 * self.rotate)
        surface.blit(rotated, (0, 0))
        return rotated
