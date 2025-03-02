# states/game_over.py
import pygame
from utils.config import Config


class GameOverState:
    def __init__(self, screen, result, score, start_time, end_time):
        self.screen = screen
        self.result = result
        self.score = score
        self.start_time = start_time
        self.end_time = end_time
        self.player_name = ""
        self.background = self.create_overlay()
        self.font = pygame.font.Font(Config.FONTS["buttons"], 48)
        self.title_font = pygame.font.Font(Config.FONTS["title"], 72)
        self.cursor_visible = True
        self.cursor_timer = 0

    def create_overlay(self):
        overlay = pygame.Surface(Config.GAME_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        return overlay

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Сохраняем результат и возвращаемся в меню
                    if self.player_name.strip():
                        Config.db.save_record(
                            player_name=self.player_name,
                            score=self.score,
                            start_time=self.start_time,
                            end_time=self.end_time
                        )
                    return "menu"

                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if len(self.player_name) < 20 and event.unicode.isprintable():
                        self.player_name += event.unicode

        return None

    def draw(self, game_screen):
        # Рисуем игровой экран и затемнение
        self.screen.blit(game_screen, (0, 0))
        self.screen.blit(self.background, (0, 0))

        # Заголовок
        title_text = "ПОБЕДА!" if self.result == "victory" else "ИГРА ОКОНЧЕНА"
        title_color = (0, 255, 0) if self.result == "victory" else (255, 0, 0)
        title = self.title_font.render(title_text, False, title_color)
        title_rect = title.get_rect(center=(Config.GAME_SIZE[0] // 2, 200))
        self.screen.blit(title, title_rect)

        # Поле ввода
        input_text = self.font.render(f"Введите ваше имя: {self.player_name}", True, (255, 255, 255))
        input_rect = input_text.get_rect(center=(Config.GAME_SIZE[0] // 2, 350))
        self.screen.blit(input_text, input_rect)

        # Мигающий курсор
        if pygame.time.get_ticks() - self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = pygame.time.get_ticks()

        if self.cursor_visible:
            cursor_x = input_rect.right + 5
            cursor_surf = pygame.Surface((3, input_rect.height))
            cursor_surf.fill((255, 255, 255))
            self.screen.blit(cursor_surf, (cursor_x, input_rect.y))

        # Подсказка
        hint_text = self.font.render("Нажмите Enter для подтверждения", True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(Config.GAME_SIZE[0] // 2, 450))
        self.screen.blit(hint_text, hint_rect)
