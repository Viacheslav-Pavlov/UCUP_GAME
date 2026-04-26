# src/states/placement_state.py
import pygame
from src.states.base_state import BaseState
from src.core.board import Board
from src.core.ship import Ship
from config import *
from constants import SHIP_SET

class PlacementState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.player_board = Board()
        self.current_ship_index = 0
        self.current_ship = None
        self.dragging = False
        self.hover_pos = None
        self.vertical = True
        self.message = "Розставте кораблі (R — повернути, ПКМ — авто)"

        self.next_ship()

    def next_ship(self):
        if self.current_ship_index < len(SHIP_SET):
            data = SHIP_SET[self.current_ship_index]
            count = data["count"]
            # Для простоти беремо по одному кораблю за раз
            self.current_ship = Ship(data["length"], data["name"])
        else:
            self.current_ship = None
            # Переходимо до гри
            from src.states.playing_state import PlayingState
            self.game.change_state(PlayingState(self.game, self.player_board))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x = (x - BOARD_OFFSET_X) // CELL_SIZE
            grid_y = (y - BOARD_OFFSET_Y) // CELL_SIZE

            if event.button == 1:  # ЛКМ
                if self.current_ship:
                    if self.player_board.place_ship(self.current_ship, grid_x, grid_y, self.vertical):
                        self.current_ship_index += 1
                        self.next_ship()
            elif event.button == 3:  # ПКМ — авто
                self.player_board.auto_place_all()
                self.current_ship_index = len(SHIP_SET)
                self.next_ship()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.vertical = not self.vertical
            if event.key == pygame.K_a:  # авто
                self.player_board.auto_place_all()
                self.current_ship_index = len(SHIP_SET)
                self.next_ship()

    def update(self):
        # Hover
        mx, my = pygame.mouse.get_pos()
        self.hover_pos = (
            (mx - BOARD_OFFSET_X) // CELL_SIZE,
            (my - BOARD_OFFSET_Y) // CELL_SIZE
        )

    def draw(self, screen):
        screen.fill(COLOR_BG)

        # Заголовок
        title = FONT_BIG.render("РОЗМІЩЕННЯ КОРАБЛІВ", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))

        # Поле
        self.draw_board(screen, self.player_board, BOARD_OFFSET_X, BOARD_OFFSET_Y)

        # Підказки
        msg = FONT_MEDIUM.render(self.message, True, (255, 255, 200))
        screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 650))

    def draw_board(self, screen, board, offset_x, offset_y):
        # Вода
        pygame.draw.rect(screen, COLOR_WATER,
                        (offset_x, offset_y, BOARD_SIZE*CELL_SIZE, BOARD_SIZE*CELL_SIZE))

        # Сітка + кsdaasddsadasdasораблі
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                rect = pygame.Rect(offset_x + x*CELL_SIZE, offset_y + y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLOR_GRID, rect, 1)

                ship = board.grid[y][x]
                if ship:
                    color = COLOR_SHIP
                    pygame.draw.rect(screen, color, rect)

        # Hover
        if self.current_ship and self.hover_pos:
            hx, hy = self.hover_pos
            if 0 <= hx < BOARD_SIZE and 0 <= hy < BOARD_SIZE:
                for i in range(self.current_ship.length):
                    dx = 0 if self.vertical else i
                    dy = i if self.vertical else 0
                    rect = pygame.Rect(offset_x + (hx+dx)*CELL_SIZE,
                                     offset_y + (hy+dy)*CELL_SIZE,
                                     CELL_SIZE, CELL_SIZE)
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    s.fill(COLOR_HIGHLIGHT)
                    screen.blit(s, rect)