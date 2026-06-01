import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game


def main():
    pygame.init()
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=1)
    except Exception:
        pass

    info = pygame.display.Info()
    MONITOR_W, MONITOR_H = info.current_w, info.current_h

    screen = pygame.display.set_mode(
        (MONITOR_W, MONITOR_H), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Coin Runner")

    game = Game(screen, MONITOR_W, MONITOR_H)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
