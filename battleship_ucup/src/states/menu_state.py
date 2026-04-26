# src/states/menu_state.py
import pygame
from src.states.base_state import BaseState
from config import FONT_BIG, FONT_MEDIUM


class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)

        if FONT_BIG is None:
            # Аварійний варіант, якщо шрифти не встигли ініціалізуватися
            print("ПОМИЛКА: Шрифти не ініціалізовано! Використовуємо тимчасовий шрифт.")
            temp_font = pygame.font.SysFont("Arial", 48, bold=True)
            self.title = temp_font.render("BATTLESHIP", True, (255, 215, 0))
            self.subtitle = pygame.font.SysFont("Arial", 32).render("UCUP-2026 Game Jam", True, (200, 220, 255))
            self.start_text = pygame.font.SysFont("Arial", 28).render("Натисни ПРОБІЛ щоб почати", True,
                                                                      (255, 255, 255))
        else:
            self.title = FONT_BIG.render("BATTLESHIP", True, (255, 215, 0))
            self.subtitle = FONT_MEDIUM.render("UCUP-2026 Game Jam", True, (200, 220, 255))
            self.start_text = FONT_MEDIUM.render("Натисни ПРОБІЛ щоб почати", True, (255, 255, 255))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            from src.states.placement_state import PlacementState
            self.game.change_state(PlacementState(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((10, 25, 45))

        screen.blit(self.title, (screen.get_width() // 2 - self.title.get_width() // 2, 180))
        screen.blit(self.subtitle, (screen.get_width() // 2 - self.subtitle.get_width() // 2, 260))
        screen.blit(self.start_text, (screen.get_width() // 2 - self.start_text.get_width() // 2, 420))