import arcade

class Collectible(arcade.Sprite):
    def __init__(self, filename, scale, points, rarity, drop_rate):
        super().__init__(filename, scale)
        self.points = points
        self.rarity = rarity
        self.drop_rate = drop_rate
        self.collected = False

    def collect(self):
        self.collected = True
        # Additional actions when collected (e.g., play sound)

    def update(self):
        if self.collected:
            self.remove_from_sprite_lists()

class Coin(Collectible):
    def __init__(self, filename, scale=1, points=10, rarity="common", drop_rate=0.75):
        super().__init__(filename, scale, points, rarity, drop_rate)

class Trap(Collectible):
    def __init__(self, filename, scale=1, points=-10, rarity="common", drop_rate=0.75, effect=None):
        super().__init__(filename, scale, points, rarity, drop_rate)
        self.effect = effect

class Powerup(Collectible):
    def __init__(self, filename, scale=1, points=50, rarity="rare", drop_rate=0.25, effect=None, duration=10):
        super().__init__(filename, scale, points, rarity, drop_rate)
        self.effect = effect
        self.duration = duration