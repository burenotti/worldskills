from typing import *
import time
import pygame
from pygame import Surface


class Animation:

    """
    :param frames(List[pygame.Surface]): Кадры анимаций
    :param delay(int): Задержка между кадрами в тиках
    :param repeat(int): Количество повторов анимации (-1, если повторять не нужно)
    """
    def __init__(self, frames: List[pygame.Surface], delay=1, repeat=-1, paused=False):
        self.last_frame_show_at = 0
        self.frames = frames
        self.current_frame_index = 0
        self.delay = delay
        self.max_repeat = repeat
        self.__paused = paused

    def __len__(self) -> int:
        """
        :returns: Количество кадров в анимации
        """
        return len(self.frames)

    def get_rect(self) -> pygame.Rect:
        """
        :returns: Прямоугольник, описанный вокруг текущего кадра
        """
        return self.current_frame.get_rect()

    @property
    def repeat(self) -> int:
        """
        :returns: Количество повторений анимации
        """
        return self.current_frame_index // len(self)

    @property
    def current_frame(self) -> Surface:
        """
        :returns: Поверхность текущего кадра
        """
        return self.frames[self.current_frame_index % len(self)]

    @property
    def paused(self):
        return self.__paused

    def toggle(self):
        self.__paused = not self.paused

    def start(self):
        self.__paused = False

    def pause(self):
        self.__paused = True

    def set_frame(self, index: int):
        self.current_frame_index = index % len(self)

    @property
    def next_frame(self) -> Surface:
        """
        :returns: Поверхность кадра, который должен быть отрисован
        """
        ticks = pygame.time.get_ticks()
        if (self.max_repeat < 0 or self.repeat < self.max_repeat) and not self.paused:
            if ticks - self.last_frame_show_at >= self.delay:
                self.current_frame_index += 1
                self.last_frame_show_at = ticks
        return self.frames[self.current_frame_index % len(self)]
