import arcade
import arcade.key
import arcade.key
from setup import CHARACTER_SCALING, GRAVITY

class Player(arcade.Sprite):
    def __init__(self, name, score, initial_position, image_path, speed, jump_speed, keybindings):
        [x, y] = initial_position        
        super().__init__(filename=image_path, scale=CHARACTER_SCALING)        
        self.center_x = x
        self.center_y = y
        self.name = name
        self.score = score
        self.jump_speed = jump_speed
        self.speed = speed
        self.keybindings = keybindings
        self.score_text = "Score: 0"
        
        self.physics_engine: arcade.PhysicsEnginePlatformer = None
        self.jump_sound = None
        self.pressed_keys = set()
        self.score_x = None
        self.score_y = None
                
    
    def setup(self, walls, jump_sound, score_position):
        x,y = score_position
        self.physics_engine = arcade.PhysicsEnginePlatformer(self, walls, GRAVITY)
        self.jump_sound = jump_sound
        self.score_x = x
        self.score_y = y
        
    def on_key_press(self, key, modifiers):             
        if key in self.keybindings.values():            
            self.pressed_keys.add(key)
        
    def on_key_release(self, key, modifiers):
        if key in self.keybindings.values():
            self.pressed_keys.discard(key)
            
    def draw_gui(self):
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            self.score_x,
            self.score_y,
            arcade.csscolor.WHITE,
            18,
        )
    
    def move(self):
        if self.keybindings["up"] in self.pressed_keys:
            if self.physics_engine.can_jump():
                self.change_y = self.jump_speed 
                arcade.play_sound(self.jump_sound)           
        elif self.keybindings["down"] in self.pressed_keys:
            self.change_y = -self.speed
        
        if self.keybindings["right"] in self.pressed_keys:
            self.change_x = self.speed
        elif self.keybindings["left"] in self.pressed_keys:
            self.change_x = -self.speed
        else:
            self.change_x = 0

    
    def update(self):
        self.move()
        self.physics_engine.update()      