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
        

    def update(self):
        if self.collected:
            self.remove_from_sprite_lists()

class Coin(Collectible):
    def __init__(self, filename, scale, points):
        super().__init__(filename, scale, points)
        
    def collect(self, player):
        super().collect(player)
        player.score += self.points
        arcade.play_sound(self.collect_coin_sound)

class Trap(Collectible):
    def __init__(self, filename, scale, points):
        super().__init__(filename, scale, points)

        
    def collect(self, player):
        super().collect(player)
        player.take_damage(self.points)

class Powerup(Collectible):
    def __init__(self, filename, scale, points, time_increase):
        super().__init__(filename, scale, points)
        self.time_increase = time_increase
        self.power_up_sound = None
        
    def setup(self, power_up_sound):
        self.power_up_sound = power_up_sound
       
        
    def collect(self, player, countdown_ref):
        super().collect(player)
        player.score += self.points
        countdown_ref.increase_time(self.time_increase)
        arcade.play_sound(self.power_up_sound)

