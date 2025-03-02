import pygame
from states.game import GameState
from states.pause import PauseState
from utils.config import Config
from states.menu import MenuState


def main():
    pygame.init()
    screen = pygame.display.set_mode(Config.MENU_SIZE)
    pygame.display.set_caption("Arcanoid")

    # Загрузка ресурсов
    menu_bg = pygame.image.load(Config.IMAGES_PATH / "menu_bg.png").convert()
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

            if action == "game":
                game = GameState(screen)
                current_state = "game"
            elif action == "quit":
                running = False
            elif action:
                print("Переход в:", action)
                # Здесь будет логика смены состояния
        elif current_state == "game":
            action = game.handle_events(events)
            game_result = game.update()

            if game_result == "game_over":
                current_state = "menu"
            elif game_result == "death":
                pass
            elif game_result == "level_up":
                pass
            elif game_result == "menu":
                current_state = "menu"
            elif action == "pause":
                game_screen = screen.copy()
                pause = PauseState(screen)
                current_state = "pause"

            game.draw()

        elif current_state == "pause":
            action = pause.handle_events(events)
            pause.draw(game_screen)  # Передаём сохранённый экран

            if action == "resume":
                current_state = "game"
            elif action == "menu":
                current_state = "menu"

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
