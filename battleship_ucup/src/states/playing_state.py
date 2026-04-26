# src/states/playing_state.py
import pygame
import random
from src.states.base_state import BaseState
from src.core.board import Board
from config import *
from constants import LETTERS


class PlayingState(BaseState):
    def __init__(self, game, player_board):
        super().__init__(game)
        self.player_board = player_board
        self.enemy_board = Board()
        self.enemy_board.auto_place_all()

        self.current_player = "player"  # player / ai
        self.message = "Ваша черга! Клікніть по полю суперника"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.current_player == "player":
            mx, my = pygame.mouse.get_pos()
            enemy_offset_x = BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE + 150

            grid_x = (mx - enemy_offset_x) // CELL_SIZE
            grid_y = (my - BOARD_OFFSET_Y) // CELL_SIZE

            if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
                result = self.enemy_board.shoot(grid_x, grid_y)

                if result in ["hit", "sunk"]:
                    self.message = "Влучили! Додатковий хід"
                else:
                    self.message = "Мимо. Хід AI"
                    self.current_player = "ai"

                # Перевірка перемоги
                if all(ship.is_sunk() for ship in self.enemy_board.ships):
                    self.message = "🎉 ВИ ПЕРЕМОГЛИ! 🎉"

    def update(self):
        if self.current_player == "ai":
            pygame.time.wait(300)  # невелика затримка
            self.ai_make_move()

    def ai_make_move(self):
        while True:
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - 1)
            if (x, y) not in self.player_board.shots:
                result = self.player_board.shoot(x, y)
                if result in ["hit", "sunk"]:
                    self.message = "AI влучив! AI ходить знову"
                else:
                    self.message = "AI промахнувся. Ваш хід"
                    self.current_player = "player"
                break

    def draw(self, screen):
        screen.fill(COLOR_BG)

        title = FONT_BIG.render("МОРСЬКИЙ БІЙ", True, (255, 215, 0)) if FONT_BIG else pygame.font.SysFont("Arial", 48,
                                                                                                          bold=True).render(
            "МОРСЬКИЙ БІЙ", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        # Ваше поле (ліворуч)
        self.draw_board(screen, self.player_board, BOARD_OFFSET_X, BOARD_OFFSET_Y, "ВАШЕ ПОЛЕ", hide_ships=False)

        # Поле суперника (праворуч)
        enemy_x = BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE + 150
        self.draw_board(screen, self.enemy_board, enemy_x, BOARD_OFFSET_Y, "ПОЛЕ СУПЕРНИКА", hide_ships=True)

        msg = FONT_MEDIUM.render(self.message, True, (255, 255, 100)) if FONT_MEDIUM else pygame.font.SysFont("Arial",
                                                                                                              32).render(
            self.message, True, (255, 255, 100))
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 620))

    def draw_board(self, screen, board, offset_x, offset_y, title_text, hide_ships=True):
        # Заголовок поля
        t = FONT_MEDIUM.render(title_text, True, (200, 220, 255)) if FONT_MEDIUM else pygame.font.SysFont("Arial",
                                                                                                          28).render(
            title_text, True, (200, 220, 255))
        screen.blit(t, (offset_x + 50, offset_y - 40))

        pygame.draw.rect(screen, COLOR_WATER, (offset_x, offset_y, BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE))

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLOR_GRID, rect, 1)

                # Кораблі (тільки на своєму полі)
                if not hide_ships and board.grid[y][x]:
                    pygame.draw.rect(screen, COLOR_SHIP, rect)

                # Постріли
                if (x, y) in board.hits:
                    pygame.draw.rect(screen, COLOR_HIT, rect)
                elif (x, y) in board.misses:
                    pygame.draw.rect(screen, COLOR_MISS, rect)