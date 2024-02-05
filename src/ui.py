import pygame
from enum import Enum
from dataclasses import dataclass
import numpy as np


class Color(Enum):
    BASE = (35, 33, 54)
    SURFACE = (42, 39, 63)
    OVERLAY = (57, 53, 82)
    MUTED = (110, 106, 134)
    SUBTLE = (144, 140, 170)
    TEXT = (224, 222, 244)
    LOVE = (235, 111, 146)
    GOLD = (246, 193, 119)
    ROSE = (234, 154, 151)
    PINE = (62, 143, 176)
    FOAM = (156, 207, 216)
    IRIS = (196, 167, 231)
    HIGHLIGHT_LOW = (42, 40, 62)
    HIGHLIGHT_MED = (68, 65, 90)
    HIGHLIGHT_HIGH = (86, 82, 110)


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, color: Color, label: str, text_color: Color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.label = label
        self.text_color = text_color

    def is_clicked(self, event_pos_x: int, event_pos_y: int) -> bool:
        return self.x <= event_pos_x <= self.x + self.width and self.y <= event_pos_y <= self.y + self.height


class ButtonFactory:
    def __init__(self, height: int):
        self.height = height

    def create_button(self, x: int, width: int, color: Color, label: str, text_color: Color) -> Button:
        return Button(x, self.height - 60, width, 50, color, label, text_color)


@dataclass
class RendererSettings:
    screen_height: int
    screen_width: int
    n_cells_x: int
    n_cells_y: int
    cell_height: int
    cell_width: int


class PygameRenderer:

    def __init__(self, screen: pygame.Surface, screen_settings: RendererSettings, buttons: list[Button]):
        self.screen: pygame.Surface = screen
        self.screen_settings: RendererSettings = screen_settings
        self.buttons = buttons

    def __draw_button(self, button: Button):
        pygame.draw.rect(self.screen, button.color.value, (button.x, button.y, button.width, button.height))
        font = pygame.font.Font(None, 36)
        text = font.render(button.label, True, button.text_color.value)
        text_rect = text.get_rect(
            center=(button.x + button.width // 2, button.y + button.height // 2)
        )
        self.screen.blit(text, text_rect)

    def __draw_grid(self):
        for y in range(0, self.screen_settings.screen_height, self.screen_settings.cell_height):
            for x in range(0, self.screen_settings.screen_width, self.screen_settings.cell_width):
                cell = pygame.Rect(x, y, self.screen_settings.cell_width, self.screen_settings.cell_height)
                pygame.draw.rect(self.screen, Color.SURFACE.value, cell, 1)

    def __draw_cells(self, current_generation: np.ndarray):
        for y in range(self.screen_settings.n_cells_y):
            for x in range(self.screen_settings.n_cells_x):
                cell = pygame.Rect(x * self.screen_settings.cell_width, y * self.screen_settings.cell_height,
                                   self.screen_settings.cell_width, self.screen_settings.cell_height)
                if current_generation[x, y] == 1:
                    pygame.draw.rect(self.screen, Color.IRIS.value, cell)

    def __draw_background(self):
        self.screen.fill(Color.BASE.value)

    def draw(self, current_generation: np.ndarray):
        self.__draw_background()
        self.__draw_grid()
        self.__draw_cells(current_generation)
        [self.__draw_button(button) for button in self.buttons]
        pygame.display.flip()
