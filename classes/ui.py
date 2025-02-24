import pygame


class Button:
    def __init__(self, text, x, y, font_path, font_size, text_color, hover_color, action=None):
        self.text = text
        self.action = action
        self.is_hovered = False

        # Загрузка шрифта
        self.font = pygame.font.Font(font_path, font_size)

        # Создаём поверхности
        self.normal_surf = self.font.render(text, False, text_color)
        self.hover_surf = self.font.render(text, False, hover_color)

        # Позиционирование
        self.rect = self.normal_surf.get_rect(center=(x, y))

    def draw(self, surface):
        current_surf = self.hover_surf if self.is_hovered else self.normal_surf
        surface.blit(current_surf, self.rect)
