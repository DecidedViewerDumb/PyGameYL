import pygame
from utils.config import Config
from states.menu import MenuState


def main():
    pygame.init()
    screen = pygame.display.set_mode(Config.MENU_SIZE)
    pygame.display.set_caption("Arcanoid")

    # Загрузка ресурсов
    menu_bg = pygame.image.load(Config.ASSETS_PATH / "images/menu_bg.png").convert()
    menu_bg = pygame.transform.scale(menu_bg, Config.MENU_SIZE)

    menu = MenuState(screen)
    clock = pygame.time.Clock()

    running = True
    current_state = "menu"

    while running:
        events = pygame.event.get()

        if current_state == "menu":
            action = menu.handle_events(events)
            menu.draw(menu_bg)

            if action == "quit":
                running = False
            elif action:
                print("Переход в:", action)
                # Здесь будет логика смены состояния

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
