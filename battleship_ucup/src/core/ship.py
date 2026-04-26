class Ship:
    def __init__(self, length, name=""):
        self.length = length
        self.name = name
        self.positions = []
        self.hits = 0
        self.vertical = True

    def place(self, start_x, start_y, vertical=True):
        self.vertical = vertical
        self.positions = []
        for i in range(self.length):
            x = start_x + (0 if vertical else i)
            y = start_y + (i if vertical else 0)
            self.positions.append((x, y))

    def is_sunk(self):
        return self.hits >= self.length

    def hit(self, x, y):
        if (x, y) in self.positions:
            self.hits += 1
            return True
        return False