import pygame
from pygame.math import Vector2


class MoveableObject:

    _move_vector = (
        Vector2(1, 0),
        Vector2(0, -1),
        Vector2(-1, 0),
        Vector2(0, 1)
    )

    def __init__(self, relative_speed=0.05, direction=0):
        self.__relative_offset = Vector2(0, 0)
        self.__relative_speed = relative_speed  # Скорость смещения относительно размеров клетки
        self.__direction = direction

    @property
    def direction(self) -> int:
        return self.__direction

    @direction.setter
    def direction(self, value) -> None:
        self.__direction = value % 4
        self.reset_offset()

    @property
    def move_vector(self):
        return self._move_vector[self.direction]

    def reset_offset(self):
        self.__relative_offset.update(0, 0)

    def process_event(self, field, event: pygame.event.Event) -> None:
        '''
        Обрабатывает события pygame
        :param field: Экземпляр поля, на котором расположен объект
        :param event: Событие pygame
        '''
        pass

    def can_move(self, field, pos) -> bool:
        """
        Проверяет, возможно ли перемещение объекта в точку pos
        :param field: Экземпляр поля, на котором расположен объект
        :param pos: Позиция, возможность перемещения в которую необходимо проверить
        :return: True, если перемещение возможно, иначе - False
        """
        pass

    def _render(self, size_x: int, size_y: int) -> pygame.Surface:
        """
        Отрисовывает объект с учетом размеров клетки.
        :param size_x: Ширина клетки
        :param size_y: Высота клетки
        :return: Поверхность, с отрисованным на ней объектом
        """
        pass

    def _before_move(self, field, x, y) -> None:
        """
        Логика, которую необходимо выполнить до вызова field.move
        :param field: Экземпляр поля, на котором расположен объект
        :param x: Текущая x-координата объекта
        :param y: Текущая y-координата объекта
        """
        pass

    def _after_move(self, field, x, y):
        """
        Логика, которую необходимо выполнить сразу после вызова field.move
        :param field: Экземпляр поля, на котором расположен объект
        :param x: x-координата объекта после перемещения
        :param y: y-координата объекта после перемещения
        """
        pass

    def _additional_logic(self, field, x, y):
        """
        Логика, которую необходимо выполнять каждый раз
        при вызове MovableObject.step
        :param field: Экземпляр поля, на котором расположен объект
        :param x: Текущая x-координата объекта
        :param y: Текущая y-координата объекта
        :return:
        """
        pass

    """
    Следующине далее функции переопределять без особой необходимости действительно не стоит
    Наказание: часы дебага
    """
    def render(self, size_x: int, size_y: int) -> pygame.Surface:
        """
        Отрисовывает результат функции Pacman._render
        с поправкой на относительное смещение.
        Переопределение и изменение не подразумевается
        :param size_x: длина клетки
        :param size_y: ширина клетки
        :return: отрисованную поверхность
        """
        cell_rect = pygame.Rect((0, 0), (size_x, size_y))
        offset = Vector2(self.__relative_offset.x * size_x,
                         self.__relative_offset.y * size_y)
        offset_rect = pygame.Rect(cell_rect)
        offset_rect.center += offset
        surface = pygame.Surface(cell_rect.union(offset_rect).size, pygame.SRCALPHA)
        rendered = self._render(size_x, size_y)
        rect = rendered.get_rect()
        if self.direction == 1 or self.direction == 2:
            surface.blit(rendered, rect)
        else:
            surface.blit(rendered, offset_rect)
        return surface

    def process_transition(self):
        if self.direction % 2 == 0:
            self.__relative_offset.x += self.__relative_speed
        else:
            self.__relative_offset.y += self.__relative_speed

    def step(self, field, x: int, y: int):
        new_pos = tuple(map(int, Vector2(x, y) + self.move_vector))
        if abs(self.__relative_offset.x) >= 2 or abs(self.__relative_offset.y) >= 2:
            self._before_move(field, x, y)
            field.move(x, y, *new_pos)
            self._after_move(field, x, y)
            self.__relative_offset.update(0, 0)
        if self.can_move(field, new_pos):
            self.process_transition()
        self._additional_logic(field, x, y)
