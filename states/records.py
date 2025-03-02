import pygame
from datetime import datetime
from utils.config import Config


class RecordsState:
    def __init__(self, screen):
        self.screen = screen
        self.background = self.create_overlay()
        self.records = Config.db.get_records()
        self.font = pygame.font.Font(Config.FONTS["buttons"], 36)
        self.title_font = pygame.font.Font(Config.FONTS["title"], 72)

    def create_overlay(self):
        overlay = pygame.Surface(Config.GAME_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        return overlay

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        return None

    def draw(self, menu_bg):
        # Рисуем фон меню с затемнением
        self.screen.blit(menu_bg, (0, 0))
        self.screen.blit(self.background, (0, 0))

        # Заголовок
        title = self.title_font.render("Таблица рекордов", False, Config.COLORS["title"])
        title_rect = title.get_rect(center=(Config.GAME_SIZE[0]//2, 100))
        self.screen.blit(title, title_rect)

        # Заголовки столбцов
        headers = ["Игрок", "Дата окончания", "Счет"]
        for i, header in enumerate(headers):
            text = self.font.render(header, True, (255, 255, 255))
            x = 150 + i * 400
            self.screen.blit(text, (x, 200))

        # Данные записей
        for row, record in enumerate(self.records[:10]):  # Первые 10 записей
            player_name = record[0]
            end_date = datetime.fromisoformat(record[1]).strftime("%d.%m.%Y %H:%M")
            score = str(record[2])

            for col, value in enumerate([player_name, end_date, score]):
                text = self.font.render(value, True, (255, 255, 255))
                x = 200 + col * 350
                y = 250 + row * 40
                self.screen.blit(text, (x, y))
