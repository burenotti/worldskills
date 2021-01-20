import pygame
import constants
from .base import BaseScene
from field import GameField, BaseField
from objects import *
from typing import List
from os.path import join

pygame.font.init()


field_map = [
    [None, None, None, None],
    [None, Wall, Wall, None],
    [None, Wall, Wall, None],
    [None, None, None, None],
]
len_x = len(field_map[0])
len_y = len(field_map)


class MainScene(BaseScene):

    font = pygame.font.SysFont('Consolas', 36)

    def __init__(self, game):
        self.field = None
        self.buttons: List[ButtonObject] = []
        super().__init__(game)

    def create_objects(self) -> None:
        self.buttons = [
            ButtonObject(self.game, 10, 10, 150, 50, text="Запуск", color=constants.Color.RED),
            ButtonObject(self.game, 10, 70, 150, 50, text="Стоп", color=constants.Color.RED),
            ButtonObject(self.game, 10, 130, 150, 50, text="Пауза", color=constants.Color.RED),
            ButtonObject(self.game, 10, 190, 150, 50, text="Запуск Обучения", color=constants.Color.RED),
            ButtonObject(self.game, 10, 250, 150, 50, text="Остановка обучения", color=constants.Color.RED),
            ButtonObject(self.game, 10, 310, 150, 50, text="Тест управления", color=constants.Color.RED),
        ]

        self.button_field = BaseField

        self.field = GameField(len_x, len_y)
        for x in range(len_x):
            for y in range(len_y):
                if field_map[y][x] is not None:
                    self.field.create_at(x, y, field_map[y][x])
                else:
                    self.field.set(x, y, None)


    def process_logic(self) -> None:
        self.field.step()
        self.additional_logic()

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_scene(self.game.PAUSE_SCENE_INDEX)

        self.field.process_event(event)

    def process_draw(self) -> None:
        screen_size = self.game.screen.get_size()
        screen_size = (screen_size[0] - 160, screen_size[1])
        field_surface = self.field.render(*screen_size, True)
        self.game.screen.blit(field_surface, (160, 0))
        for b in self.buttons:
            b.process_draw()

    def additional_logic(self) -> None:
        pass

    def on_activate(self) -> None:
        self.create_objects()
