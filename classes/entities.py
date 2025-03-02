import math
import random

import pygame
from utils.config import Config


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet):
        super().__init__()
        self.sprites = self.load_sprites(sprite_sheet["player"])
        self.current_frame = 0
        self.image = self.sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.speed = Config.PLAYER_SPEED
        self.animation_speed = 0.2
        self.mask = pygame.mask.from_surface(self.image)

    def load_sprites(self, frames):
        """Загрузка и масштабирование спрайтов"""
        if not frames:
            raise ValueError("Нет кадров для игрока")
        sprites = []
        sheet = pygame.image.load(Config.IMAGES_PATH / "player_sprite.png").convert_alpha()
        for frame in frames:
            x, y, w, h = frame["x"], frame["y"], frame["w"], frame["h"]
            sprite = sheet.subsurface(pygame.Rect(x, y, w, h))
            sprites.append(pygame.transform.scale(sprite, (243 // 2, 64 // 2)))  # Уменьшаем размер
        return sprites

    def update(self, keys, screen_width):
        # Движение
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Ограничение в рамках экрана
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))

        # Анимация
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.sprites):
            self.current_frame = 0
        self.image = self.sprites[int(self.current_frame)]


class Ball(pygame.sprite.Sprite):
    def __init__(self, sprite_data, player):
        super().__init__()
        self.sprite_data = sprite_data
        self.player = player
        self.image = self.load_sprite()
        self.rect = self.image.get_rect()
        self.attached = True
        self.speed = Config.BALL_SPEED
        self.dx = 0
        self.dy = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.reset_position()

    def load_sprite(self):
        """Загрузка спрайта мяча"""
        ball_data = self.sprite_data["ball"]
        sheet = pygame.image.load(Config.IMAGES_PATH / "player_sprite.png").convert_alpha()
        sprite = sheet.subsurface(pygame.Rect(
            ball_data["x"], ball_data["y"],
            ball_data["w"], ball_data["h"]
        ))
        return pygame.transform.scale(sprite, (32, 32))  # Масштабируем до удобного размера

    def reset_position(self):
        """Сброс позиции к центру платформы"""
        if self.player:
            self.rect.midbottom = self.player.rect.midtop
            self.rect.y -= 5  # Небольшой отступ от платформы

    def launch(self):
        """Запуск мяча под случайным углом"""
        angle = math.radians(random.uniform(Config.BALL_MIN_ANGLE, Config.BALL_MAX_ANGLE))
        self.dx = self.speed * math.cos(angle)
        self.dy = -self.speed * math.sin(angle)  # Отрицательное значение для движения вверх
        self.attached = False

    def calculate_bounce(self, player_rect):
        """Расчет угла отскока от платформы"""
        # Определяем точку столкновения относительно платформы
        hit_pos = (self.rect.centerx - player_rect.left) / player_rect.width
        # Нормализуем от -1 до 1
        hit_pos = hit_pos * 2 - 1
        # Максимальный угол отклонения (75 градусов от вертикали)
        max_angle = math.radians(75)
        angle = hit_pos * max_angle
        # Обновляем направление
        self.dx = self.speed * math.sin(angle)
        self.dy = -self.speed * math.cos(angle)
        # Увеличиваем скорость
        self.speed += Config.BALL_SPEED_INCREASE

    def update(self, screen_width, screen_height):
        if self.attached:
            self.reset_position()
            return None

        # Движение
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Коррекция при выходе за границы
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx *= -1
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.dx *= -1

        if self.rect.top < 0:
            self.rect.top = 0
            self.dy *= -1

        # Столкновение с нижней границей
        if self.rect.bottom >= screen_height:
            return "death"

        return None

    def predict_collision(self, screen_width, screen_height):
        # Рассчитываем следующую позицию
        next_x = self.rect.x + self.dx
        next_y = self.rect.y + self.dy

        # Проверяем выход за границы
        if next_x <= 0 or next_x >= screen_width - self.rect.width:
            self.dx *= -1
        if next_y <= 0:
            self.dy *= -1

        # Возвращаем предполагаемую позицию
        return pygame.Rect(next_x, next_y, self.rect.width, self.rect.height)
