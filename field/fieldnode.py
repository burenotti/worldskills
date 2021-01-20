import pygame


class FieldNode:
    def __init__(self, x: int, y: int, content):
        self._x = x
        self._y = y
        self._content = content

    def render(self, cell_size_x: int, cell_size_y: int) -> pygame.Surface:
        if hasattr(self.content, 'render'):
            return self.content.render(cell_size_x, cell_size_y)
        else:
            return pygame.Surface((cell_size_x, cell_size_y), pygame.SRCALPHA)

    def step(self, field):
        if hasattr(self.content, 'step'):
            self.content.step(field, self.x, self.y)

    def process_event(self, field, event):
        if hasattr(self.content, 'process_event'):
            self.content.process_event(field, event)

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def content(self):
        return self._content
