import pygame
from classes.ui import Button
from utils.config import Config


class MenuState:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.current_index = 0
        self.init_buttons()  # Убрал нижнее подчёркивание

    def init_buttons(self):
        button_params = [
            ("Старт", 250, "game"),
            ("Рекорды", 330, "records"),
            ("Выход", 410, "quit")
        ]

        for text, y, action in button_params:
            btn = Button(
                text=text,
                y=y,
                font_path=Config.FONTS["buttons"],
                font_size=48,
                text_color=Config.COLORS["button_normal"],
                hover_color=Config.COLORS["button_hover"],
                action=action
            )
            self.buttons.append(btn)

        self.buttons[self.current_index].is_hovered = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.change_selection(1)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.change_selection(-1)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                    return self.buttons[self.current_index].action
        return None

    def change_selection(self, step):
        self.buttons[self.current_index].is_hovered = False
        self.current_index = (self.current_index + step) % len(self.buttons)
        self.buttons[self.current_index].is_hovered = True

    def draw(self, background):
        self.screen.blit(background, (0, 0))

        # Рисуем заголовок
        draw_centered_text(
            surface=self.screen,
            text="Arcanoid",
            font=Config.FONTS["title"],
            size=72,
            color=Config.COLORS["title"],
            y=70
        )

        for btn in self.buttons:
            btn.draw(self.screen)


def draw_centered_text(surface, text, font, size, color, y):
    """Отрисовка текста по центру горизонтали"""
    font_obj = pygame.font.Font(font, size)
    text_surface = font_obj.render(text, False, color)
    text_rect = text_surface.get_rect(centerx=surface.get_width()//2, y=y)
    surface.blit(text_surface, text_rect)
