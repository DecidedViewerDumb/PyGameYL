import pygame
from classes.entities import Player, Ball
from classes.ui import Button
from utils.config import Config


class GameState:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(Config.IMAGES_PATH / "main_bg.png").convert()
        self.background = pygame.transform.scale(self.background, Config.GAME_SIZE)

        # Загрузка данных игрока из JSON (предположим, что sprite_data уже загружена)
        self.player = Player(Config.DATA_JSON["player_sprite.png"])
        self.player.rect.midbottom = (Config.GAME_SIZE[0] // 2, Config.GAME_SIZE[1] - 20)

        # Мяч
        self.ball = Ball(Config.DATA_JSON["player_sprite.png"], self.player)

        self.all_sprites = pygame.sprite.Group(self.player, self.ball)
        self.running = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "pause"
                if event.key == pygame.K_SPACE and self.ball.attached:
                    self.ball.launch()
        return None

    def check_collisions(self):
        # Столкновение мяча с платформой
        if pygame.sprite.collide_mask(self.ball, self.player):
            self.ball.calculate_bounce(self.player.rect)
            return True

        return False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, Config.GAME_SIZE[0])

        result = self.ball.update(Config.GAME_SIZE[0], Config.GAME_SIZE[1])

        # if not self.ball.attached:
        #     result = self.ball.update(Config.GAME_SIZE[0], Config.GAME_SIZE[1])
        #     if result == "game_over":
        #         return "game_over"
        if self.check_collisions():
            # Обработка столкновений
            pass

        if result == "game_over":
            return "game_over"
        return None

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)


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
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return self.buttons[self.current_index].action
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

