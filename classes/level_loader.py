import pygame
from utils.config import Config
from .block import Block


class LevelLoader:
    @staticmethod
    def load_level(level_path):
        with open(level_path, 'r') as f:
            content = f.read().split('\n')

        # Парсинг мета-данных
        meta = {}
        grid = []
        section = None

        for line in content:
            line = line.strip()
            if not line:
                continue

            if line.startswith('# meta'):
                section = 'meta'
                continue
            elif line.startswith('# grid'):
                section = 'grid'
                continue

            if section == 'meta':
                key, value = line.split('=')
                meta[key.strip()] = value.strip()
            elif section == 'grid':
                grid.append(line.split())

        # Рассчитываем параметры блоков
        screen_width = Config.GAME_SIZE[0]
        screen_height = Config.GAME_SIZE[1]
        cols = int(meta.get('cols', 20))
        rows = int(meta.get('rows', 4))
        padding = int(meta.get('padding', 0))

        # Автоматический расчет размеров блоков
        if 'block_size' in meta:
            bw, bh = map(int, meta['block_size'].split('x'))
        else:
            bw = (screen_width - (cols - 1) * padding) // cols
            bh = 50  # Стандартная высота

        Config.BLOCK_WIDTH = bw
        Config.BLOCK_HEIGHT = bh

        # Генерация позиций блоков
        blocks = pygame.sprite.Group()
        start_x = (screen_width - (cols * (bw + padding))) // 2

        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell == '0':
                    continue

                if cell == '3':  # Стена
                    health = Config.BLOCK_TYPES[cell]["health"]
                    score = Config.BLOCK_TYPES[cell]["score"]
                else:
                    health = Config.BLOCK_TYPES[cell]["health"]
                    score = Config.BLOCK_TYPES[cell]["score"]

                x = start_x + col_idx * (bw + padding)
                y = Config.BLOCK_START_Y + row_idx * (bh + padding)

                if cell == '3':
                    block_data = Config.DATA_JSON["block_sprite.png"]["blocks"]["wall"]
                    unbreakable = block_data["unbreakable"]
                    blocks.add(
                        Block(
                            block_type=cell,
                            x=x,
                            y=y,
                            health=Config.BLOCK_TYPES[cell]["health"],
                            score=Config.BLOCK_TYPES[cell]["score"],
                            sprite_data=block_data,
                            unbreakable=unbreakable  # Передаём флаг
                        )
                    )
                else:
                    block_data = Config.DATA_JSON["block_sprite.png"]["blocks"][Config.BLOCK_TYPES[cell]["color"]]
                    blocks.add(
                        Block(
                            block_type=cell,
                            x=x,
                            y=y,
                            health=health,  # Передаём параметры в конструктор
                            score=score,
                            sprite_data=block_data  # Отдельно передаём спрайты
                        )
                    )


        return blocks
