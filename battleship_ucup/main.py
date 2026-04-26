# main.py
import pygame
import sys
from src.core.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Battleship UCUP-2026")
    clock = pygame.time.Clock()

    game = Game(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()