from datetime import datetime
import pygame
from classes.entities import Player, Ball
from classes.level_loader import LevelLoader
from classes.ui import Button
from utils.config import Config


class GameState:
    def __init__(self, screen, level_num=1, score=0, lives=Config.INITIAL_LIVES):
        self.start_time = datetime.now()
        self.end_time = None
        self.screen = screen
        self.score = score  # Сохраняем переданный счет
        self.lives = lives  # Сохраняем переданные жизни
        self.score_font = pygame.font.Font(
            Config.FONTS["buttons"],
            Config.SCORE_FONT_SIZE
        )

        self.background = pygame.image.load(Config.IMAGES_PATH / "main_bg.png").convert()
        self.background = pygame.transform.scale(self.background, Config.GAME_SIZE)

        # Загрузка данных игрока из JSON (предположим, что sprite_data уже загружена)
        self.player = Player(Config.DATA_JSON["player_sprite.png"])
        self.player.rect.midbottom = (Config.GAME_SIZE[0] // 2, Config.GAME_SIZE[1] - 20)

        # Мяч
        self.ball = Ball(Config.DATA_JSON["player_sprite.png"], self.player)

        self.running = True

        # загрузка уровней
        self.level_num = level_num
        self.blocks = LevelLoader.load_level(
            f"levels/level{level_num}.txt"
        )

        # Группа всех спрайтов
        self.all_sprites = pygame.sprite.Group(
            self.player,
            self.ball,
            self.blocks
        )

        self.lives = Config.INITIAL_LIVES
        self.respawn_timer = 0
        self.is_respawning = False
        self.heart_sprite = self.load_heart_sprite()

    def load_next_level(self):
        """Загрузка следующего уровня без сброса состояния"""
        self.level_num += 1
        self.blocks = LevelLoader.load_level(f"levels/level{self.level_num}.txt")
        self.all_sprites = pygame.sprite.Group(
            self.player,
            self.ball,
            self.blocks
        )
        self.reset_entities()

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
        if self.is_respawning:
            if pygame.time.get_ticks() - self.respawn_timer >= Config.RESPAWN_DELAY:
                self.is_respawning = False
                self.reset_entities()
            return None

        # Проверка завершения уровня
        if self.is_level_completed():
            next_level = self.level_num + 1
            level_path = f"levels/level{next_level}.txt"

            if self.level_exists(level_path):
                # Переход на следующий уровень
                self.load_next_level()
                return "level_up"
            else:
                # Сохраняем результат при завершении последнего уровня
                self.end_time = datetime.now()
                Config.db.save_record(
                    player_name="ИгрокТест",
                    score=self.score,
                    start_time=self.start_time,
                    end_time=self.end_time
                )
                return "victory"

        keys = pygame.key.get_pressed()
        self.player.update(keys, Config.GAME_SIZE[0])

        result = self.ball.update(Config.GAME_SIZE[0], Config.GAME_SIZE[1])

        if result == "death":
            game_over_status = self.handle_death()
            if game_over_status == "game_over":
                return "game_over"

        # Проверка всех столкновений
        self.check_collisions()  # С платформой
        self.check_block_collisions()  # С блоками

        # Обновление анимации блоков
        for block in self.blocks:
            block.update()

        if result == "game_over":
            return "game_over"
        return None

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)

        # Рендерим текст счёта
        score_text = self.score_font.render(
            f"{self.score}",
            True,
            Config.COLORS["score_text"]
        )
        self.screen.blit(score_text, (20, 20))

        # if not self.is_respawning:
        #     self.all_sprites.draw(self.screen)

        # Отрисовка жизней
        lives_text = self.score_font.render(
            f"{self.lives}X ",
            True,
            Config.COLORS["lives_text"]
        )
        text_x = Config.GAME_SIZE[0] - lives_text.get_width() - 60
        self.screen.blit(lives_text, (text_x, 20))
        heart_x = text_x + lives_text.get_width() + 10
        self.screen.blit(self.heart_sprite, (heart_x, 20))

    def check_block_collisions(self):
        # Получаем предполагаемую позицию мяча
        predicted_rect = self.ball.predict_collision(Config.GAME_SIZE[0], Config.GAME_SIZE[1])

        # Проверяем столкновения мяча с блоками
        block_hits = pygame.sprite.spritecollide(
            self.ball,
            self.blocks,
            False,
            pygame.sprite.collide_mask
        )

        for block in block_hits:
            if block.rect.colliderect(predicted_rect):
                # Расчёт точки столкновения
                dx = (self.ball.rect.centerx - block.rect.centerx) / block.rect.width
                dy = (self.ball.rect.centery - block.rect.centery) / block.rect.height
                if block.health == 0:
                    continue  # Пропускаем уже разрушенные блоки

                # Определяем направление отскока
                if abs(dx) > abs(dy):
                    self.ball.dx *= -1
                else:
                    self.ball.dy *= -1

                # Нанесение урона, если блок разрушаемый
                if not block.unbreakable:
                    block.take_damage()
                    self.score += block.score

                # Удаление блока при уничтожении
                if block.health <= 0 and not block.unbreakable:
                    block.kill()

    def load_heart_sprite(self):
        heart_data = Config.DATA_JSON["player_sprite.png"]["heart"]
        sheet = pygame.image.load(Config.IMAGES_PATH / "player_sprite.png").convert_alpha()
        sprite = sheet.subsurface(pygame.Rect(
            heart_data["x"], heart_data["y"],
            heart_data["w"], heart_data["h"]
        ))
        return pygame.transform.scale(sprite, Config.HEART_SIZE)

    def handle_death(self):
        self.lives -= 1

        if self.lives <= 0:
            self.end_time = datetime.now()
            # Сохраняем запись при завершении игры
            Config.db.save_record(
                player_name="ИгрокТест",
                score=self.score,
                start_time=self.start_time,
                end_time=self.end_time
            )
            return "game_over"

        if self.lives > 0:
            self.is_respawning = True
            self.respawn_timer = pygame.time.get_ticks()
            return None
        return "game_over"

    def reset_entities(self):
        self.player.rect.midbottom = (Config.GAME_SIZE[0] // 2, Config.GAME_SIZE[1] - 20)
        self.ball.reset_position()
        self.ball.attached = True

    def is_level_completed(self):
        # Проверяем остались ли разрушаемые блоки
        for block in self.blocks:
            if not block.unbreakable and block.health > 0:
                return False
        return True

    def level_exists(self, path):
        try:
            with open(path):
                return True
        except FileNotFoundError:
            return False


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

