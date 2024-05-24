import arcade

class Collectible(arcade.Sprite):
    def __init__(self, filename, scale, points):
        super().__init__(filename, scale)
        self.points = points
        self.collected = False
        
        self.center_x = None
        self.center_y = None
        self.collect_coin_sound = None
        
    def setup(self, collect_coin_sound):
        self.collect_coin_sound = collect_coin_sound    

    def collect(self, player):
        self.collected = True
        player.score += self.points
        arcade.play_sound(self.collect_coin_sound)
        

    def update(self):
        if self.collected:
            self.remove_from_sprite_lists()

class Coin(Collectible):
    def __init__(self, filename, scale, points):
        super().__init__(filename, scale, points)

class Trap(Collectible):
    def __init__(self, filename, scale, points, effect=None):
        super().__init__(filename, scale, points)
        self.effect = effect

class Powerup(Collectible):
    def __init__(self, filename, scale, points, effect=None, duration=10):
        super().__init__(filename, scale, points)
        self.effect = effect
        self.duration = duration