import pygame

from states.game_over import GameOverState
from states.records import RecordsState
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
            elif action == "records":
                records = RecordsState(screen)
                current_state = "records"
            elif action == "quit":
                running = False
            elif action:
                print("Переход в:", action)
                # Здесь будет логика смены состояния
        elif current_state == "game":
            action = game.handle_events(events)
            game_result = game.update()

            if game_result in ("game_over", "victory"):
                # Сохраняем экран игры и переходим в состояние GameOver
                game_screen = screen.copy()
                game_over = GameOverState(
                    screen=screen,
                    result=game_result,
                    score=game.score,
                    start_time=game.start_time,
                    end_time=game.end_time
                )
                current_state = "game_over"
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
        elif current_state == "records":
            action = records.handle_events(events)
            records.draw(menu_bg)
            if action == "menu":
                current_state = "menu"
        elif current_state == "game_over":
            action = game_over.handle_events(events)
            game_over.draw(game_screen)
            if action == "menu":
                current_state = "menu"

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
