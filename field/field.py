import pygame
from pygame.time import get_ticks
from typing import List
from .fieldnode import FieldNode
from objects import *
from .field_events import Rule, MoveConflict


class BaseField:
    def __init__(self, width: int, height: int, filler=None, fear_mode_duration=7000):
        super().__init__()
        self._width = width
        self._height = height
        self._rules = []
        self._fear_mode_duration = fear_mode_duration
        self._last_fear_mode_activate = get_ticks() - fear_mode_duration
        self._handlers: List[Rule] = []
        self._field: List[List[FieldNode]] = [[]]
        self.pacman_lives = 3
        self._init_field(filler)

    @property
    def fear_mode_activated(self) -> bool:
        return get_ticks() - self._last_fear_mode_activate <= self._fear_mode_duration

    def activate_fear_mode(self) -> None:
        self._last_fear_mode_activate = get_ticks()

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    # TODO: Придумать нормальное название
    def is_inside_field(self, cell_x: int, cell_y: int) -> bool:
        return 0 <= cell_x < self._width and 0 <= cell_y < self._height

    def get(self, cell_x: int, cell_y: int, filler=None) -> FieldNode:
        if self.is_inside_field(cell_x, cell_y):
            return self._field[cell_y][cell_x]
        else:
            return FieldNode(cell_x, cell_y, filler)

    def set(self, cell_x: int, cell_y: int, obj) -> None:
        if self.is_inside_field(cell_x, cell_y):
            self._field[cell_y][cell_x] = FieldNode(cell_x, cell_y, obj)

    def create_at(self, x, y, obj_type, *args, **kwargs):
        self.set(x, y, obj_type(*args, **kwargs))

    def move(self, x0: int, y0: int, x: int, y: int):
        self._resolve_conflict(x0, y0, x, y)

    def _resolve_conflict(self, x0: int, y0: int, x: int, y: int) -> bool:
        event = MoveConflict(self,
                             self.get(x0, y0),
                             self.get(x, y))
        for rule in self._rules:
            if called := rule(event):
                return called
        return False

    def _init_field(self, filler=None) -> None:
        self._field = [[FieldNode(j, i, filler) for j in range(self._width)] for i in range(self._height)]

    def step(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.get(x, y).step(self)

    def process_event(self, event) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.get(x, y).process_event(self, event)

    def add_rule(self, rule) -> None:
        self._rules.append(rule)

    def remove_rule(self, rule) -> bool:
        try:
            self._rules.remove(rule)
            return True
        except ValueError:
            return False


class GameField(BaseField):
    def __init__(self, width: int, height: int):
        super(GameField, self).__init__(width, height)
        self.__game_over = False

    # ну вообще этот класс в принципе не должен заниматься отрисовкой, так что
    # TODO заменить эту функцию
    def render(self, size_x: int, size_y: int, debug_grid=False) -> pygame.Surface:
        main_surface = pygame.Surface((size_x, size_y))
        cell_size_x = min(size_x // self._width, size_y // self._height)
        cell_size_y = cell_size_x
        surface = pygame.Surface((cell_size_x * self.width,
                                  cell_size_y * self.height))
        for i, row in enumerate(self._field):
            for j, item in enumerate(row):
                cell_rect = pygame.Rect(j * cell_size_x, i * cell_size_y, cell_size_x, cell_size_y)
                rendered_item = item.render(cell_size_x, cell_size_y)
                item_rect = rendered_item.get_rect()
                item_rect.center = cell_rect.center
                surface.blit(rendered_item, item_rect)
                if debug_grid:
                    pygame.draw.rect(surface, (255, 255, 255), cell_rect, 1)

        surf_rect = surface.get_rect()
        main_rect = main_surface.get_rect()
        surf_rect.center = main_rect.center
        main_surface.blit(surface, surf_rect)
        pygame.draw.rect(main_surface, (255, 255, 255), surf_rect, 1)
        return main_surface
