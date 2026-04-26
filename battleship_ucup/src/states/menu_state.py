# src/states/menu_state.py
import pygame
from src.states.base_state import BaseState
from src.states.placement_state import PlacementState
from config import FONT_BIG, FONT_MEDIUM

class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.title = FONT_BIG.render("BATTLESHIP", True, (255, 215, 0))
        self.subtitle = FONT_MEDIUM.render("UCUP-2026 Game Jam", True, (200, 220, 255))
        self.start_text = FONT_MEDIUM.render("Натисни ПРОБІЛ щоб почати", True, (255, 255, 255))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.change_state(PlacementState(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.title, (screen.get_width()//2 - self.title.get_width()//2, 180))
        screen.blit(self.subtitle, (screen.get_width()//2 - self.subtitle.get_width()//2, 260))
        screen.blit(self.start_text, (screen.get_width()//2 - self.start_text.get_width()//2, 420))