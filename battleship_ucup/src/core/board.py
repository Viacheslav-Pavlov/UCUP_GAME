from src.core.ship import Ship
from config import BOARD_SIZE
from constants import SHIP_SET
import random

class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        self.reset()

    def reset(self):
        self.grid = [[None] * self.size for _ in range(self.size)]
        self.ships = []
        self.shots = set()
        self.hits = set()
        self.misses = set()

    def can_place_ship(self, ship, start_x, start_y, vertical):
        for i in range(ship.length):
            x = start_x + (0 if vertical else i)
            y = start_y + (i if vertical else 0)
            if not (0 <= x < self.size and 0 <= y < self.size):
                return False
            if self.grid[y][x] is not None:
                return False
        return True

    def place_ship(self, ship, start_x, start_y, vertical=True):
        if self.can_place_ship(ship, start_x, start_y, vertical):
            ship.place(start_x, start_y, vertical)
            for x, y in ship.positions:
                self.grid[y][x] = ship
            self.ships.append(ship)
            return True
        return False

    def auto_place_all(self):
        self.reset()
        for data in SHIP_SET:
            for _ in range(data["count"]):
                ship = Ship(data["length"], data["name"])
                placed = False
                for _ in range(100):
                    x = random.randint(0, self.size - 1)
                    y = random.randint(0, self.size - 1)
                    vertical = random.choice([True, False])
                    if self.place_ship(ship, x, y, vertical):
                        placed = True
                        break
                if not placed:
                    return False
        return True

    def shoot(self, x, y):
        if (x, y) in self.shots:
            return "already"
        self.shots.add((x, y))
        for ship in self.ships:
            if ship.hit(x, y):
                self.hits.add((x, y))
                return "sunk" if ship.is_sunk() else "hit"
        self.misses.add((x, y))
        return "miss"