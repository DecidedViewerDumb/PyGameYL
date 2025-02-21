from pathlib import Path


class Config:
    # Разрешения
    MENU_SIZE = (800, 600)
    GAME_SIZE = (800, 600)

    # Пути
    # Использование pathlib лучше чем os
    ASSETS_PATH = Path(__file__).parent.parent / "assets"
    FONTS = {
        "title": str(ASSETS_PATH / "fonts/MoscowMetroColor.otf"),
        "buttons": str(ASSETS_PATH / "fonts/Neoneon1.otf")
    }

    # Цвета
    COLORS = {
        "button_normal": (0, 255, 150),     # светло-зеленый
        "button_hover": (255, 50, 100),     # малиновый
        "title": (0, 255, 255)              # голубой
    }
