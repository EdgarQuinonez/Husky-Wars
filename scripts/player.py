import arcade
from setup import CHARACTER_SCALING

class Player(arcade.Sprite):
    def __init__(self, name, score, initial_position, image_path):
        [x, y] = initial_position        
        super().__init__(filename=image_path, scale=CHARACTER_SCALING)
        self.center_x = x
        self.center_y = y
        self.name = name
        self.score = score        
                
        
    def play(self):        
        pass
        
    def __str__(self):
        return f"Player: {self.name}"