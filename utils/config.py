import json
from pathlib import Path


class Config:
    # Добавляем параметры блоков
    BLOCK_WIDTH, BLOCK_HEIGHT = None, None
    BLOCK_START_X = 100
    BLOCK_START_Y = 10
    BLOCK_TYPES = {
        "0": None,
        "1": {"health": 1, "score": 10, "color": "red"},
        "2": {"health": 2, "score": 20, "color": "orange"},
        "3": {"health": -1, "score": 0, "color": "wall"}
    }

    # Разрешения
    MENU_SIZE = (1200, 800)
    GAME_SIZE = (1200, 800)

    BALL_SPEED = 14
    PLAYER_SPEED = 15
    BALL_MAX_SPEED = 20
    # Пути
    # Использование pathlib лучше чем os
    ASSETS_PATH = Path(__file__).parent.parent / "assets"
    IMAGES_PATH = ASSETS_PATH / "images"
    FONTS = {
        "title": str(ASSETS_PATH / "fonts/MoscowMetroColor.otf"),
        "buttons": str(ASSETS_PATH / "fonts/Neoneon1.otf")
    }

    with open(str(IMAGES_PATH / "block_sprite.json"), 'r', encoding='utf-8') as f:
        DATA_JSON = json.load(f)

    # Цвета
    COLORS = {
        "button_normal": (0, 255, 150),     # светло-зеленый
        "button_hover": (255, 50, 100),     # малиновый
        "title": (0, 255, 255),              # голубой
        "score_text": (255, 255, 255),
        "lives_text": (255, 255, 255)
    }

    SCORE_FONT_SIZE = 36
    BALL_MIN_ANGLE = 30    # Минимальный угол от горизонтали
    BALL_MAX_ANGLE = 150   # Максимальный угол
    BALL_SPEED_INCREASE = 0.02  # Увеличение скорости с каждым ударом

    INITIAL_LIVES = 3
    RESPAWN_DELAY = 2000
    HEART_SIZE = (40, 40)
