# src/states/menu_state.py
import pygame
from src.states.base_state import BaseState
from config import COLOR_BG, SCREEN_WIDTH


class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)

        # Створюємо шрифти тут, щоб точно уникнути None
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.medium_font = pygame.font.SysFont("Arial", 32)

        self.options = [
            "1. Одиночна гра (проти AI)",
            "2. Hotseat (два гравці на одному ПК)",
            "3. Створити гру (Host)",
            "4. Підключитися до гри (Join)"
        ]
        self.selected = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                from src.states.placement_state import PlacementState
                self.game.change_state(PlacementState(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BG)

        # Заголовок
        title = self.big_font.render("BATTLESHIP", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        subtitle = self.medium_font.render("UCUP-2026 Game Jam", True, (200, 220, 255))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 180))

        # Меню
        for i, option in enumerate(self.options):
            color = (255, 255, 100) if i == self.selected else (200, 200, 200)
            text = self.medium_font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 280 + i * 55))

        hint = self.medium_font.render("↑ ↓ — вибір    ENTER — почати", True, (150, 150, 150))
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 620))