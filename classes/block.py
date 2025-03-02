import pprint

import pygame
from utils.config import Config


class Block(pygame.sprite.Sprite):
    def __init__(self, block_type, x, y, health, score, sprite_data, unbreakable=False):
        super().__init__()
        self.type = block_type
        self.max_health = health
        self.health = health
        self.score = score
        self.sprites = self.load_sprites(sprite_data)
        self.destruction_animation = self.load_destruction_animation(sprite_data)
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_frame = 0
        self.is_destroying = False
        self.unbreakable = unbreakable

    def load_sprites(self, data):
        """Загрузка спрайтов состояний при ударах"""
        sprites = []
        sheet = pygame.image.load(Config.IMAGES_PATH / "block_sprite.png").convert_alpha()

        # Основной спрайт (hit[0])
        if "hit" in data and len(data["hit"]) > 0:
            for hit_frame in data["hit"]:
                sprite = sheet.subsurface(
                    pygame.Rect(
                        hit_frame["x"], hit_frame["y"],
                        hit_frame["w"], hit_frame["h"]
                    )
                )
                sprites.append(pygame.transform.scale(sprite, (Config.BLOCK_WIDTH, Config.BLOCK_HEIGHT)))
        else:
            # Для блоков без hit (например, стена)
            sprite = sheet.subsurface(
                pygame.Rect(
                    data["x"], data["y"],
                    data["w"], data["h"]
                )
            )
            sprites.append(pygame.transform.scale(sprite, (Config.BLOCK_WIDTH, Config.BLOCK_HEIGHT)))

        return sprites

    def load_destruction_animation(self, data):
        """Загрузка анимации разрушения"""
        animation = []
        if "animation" in data:
            sheet = pygame.image.load(Config.IMAGES_PATH / "block_sprite.png").convert_alpha()
            for frame in data["animation"]:
                sprite = sheet.subsurface(
                    pygame.Rect(
                        frame["x"], frame["y"],
                        frame["w"], frame["h"]
                    )
                )
                animation.append(pygame.transform.scale(sprite, (Config.BLOCK_WIDTH, Config.BLOCK_HEIGHT)))
        return animation

    def take_damage(self):
        """Обработка получения урона"""
        if self.unbreakable or self.health <= 0:
            return
        self.health -= 1

        # Обновление спрайта
        if 0 < self.health < len(self.sprites):
            self.image = self.sprites[self.health]

        # Запуск анимации разрушения
        if self.health <= 0 and self.destruction_animation:
            self.is_destroying = True
            self.animation_frame = 0

    def update(self):
        """Обновление анимации разрушения"""
        if self.is_destroying:
            self.animation_frame += 0.2
            if self.animation_frame >= len(self.destruction_animation):
                self.kill()
                return True
            else:
                self.image = self.destruction_animation[int(self.animation_frame)]
        return False
