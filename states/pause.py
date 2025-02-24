import pygame
from classes.ui import Button
from utils.config import Config


class PauseState:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.current_index = 0
        self.background = self.create_overlay()
        self.init_buttons()

    def create_overlay(self):
        overlay = pygame.Surface(Config.GAME_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Полупрозрачный чёрный
        return overlay

    def init_buttons(self):
        button_params = [
            ("Продолжить", Config.GAME_SIZE[1] // 2 - 60, "resume"),
            ("Выйти в меню", Config.GAME_SIZE[1] // 2 + 60, "menu")
        ]

        for text, y, action in button_params:
            btn = Button(
                text=text,
                x=Config.GAME_SIZE[0] // 2,
                y=y,
                font_path=Config.FONTS["buttons"],
                font_size=56,
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
                elif event.key == pygame.K_ESCAPE:
                    return self.buttons[0].action
        return None

    def change_selection(self, step):
        self.buttons[self.current_index].is_hovered = False
        self.current_index = (self.current_index + step) % len(self.buttons)
        self.buttons[self.current_index].is_hovered = True

    def draw(self, game_screen):
        self.screen.blit(game_screen, (0, 0))
        self.screen.blit(self.background, (0, 0))
        for btn in self.buttons:
            btn.draw(self.screen)
