import arcade
import arcade.key
import arcade.key
from setup import CHARACTER_SCALING, GRAVITY, LEFT_FACING, RIGHT_FACING

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

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
        
        self.character_face_direction = None
        self.physics_engine: arcade.PhysicsEnginePlatformer = None
        self.jump_sound = None
        self.pressed_keys = set()
        self.score_x = None
        self.score_y = None
        self.animations_main_path = None
        
        
        # Animations
        
        self.animation_timer = 0  
        self.debounce_time = 0.1 
        
        self.cur_texture = 0
        
        self.is_jumping = False
        self.is_walking = False
        
        self.idle_texture_pair = None        
                            
        # Load textures for walking
        self.walk_textures = []
        self.jump_textures = []
        self.fall_textures = []

                
    
    def setup(self, walls, jump_sound, score_position, face_direction, animations_path):
        x,y = score_position
        self.physics_engine = arcade.PhysicsEnginePlatformer(self, walls, GRAVITY)
        self.jump_sound = jump_sound
        self.score_x = x
        self.score_y = y
        self.character_face_direction = face_direction
        self.animations_main_path = animations_path
        
        self.idle_texture_pair = load_texture_pair(f"{self.animations_main_path}/idle.png")        
        
        # Load walk textures
        for i in range(6):
            texture = load_texture_pair(f"{self.animations_main_path}/walk_{i}.png")
            self.walk_textures.append(texture)
            
        # Load jump textures
        for i in range(3):
            texture = load_texture_pair(f"{self.animations_main_path}/jump_{i}.png")
            self.jump_textures.append(texture)
            
        # Load fall textures
        for i in range(4):
            texture = load_texture_pair(f"{self.animations_main_path}/fall_{i}.png")
            self.fall_textures.append(texture)
        
            
        # Set the initial texture
        self.texture = self.idle_texture_pair[self.character_face_direction]
        self.hit_box = self.texture.hit_box_points
        
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
            
    def update_animation(self, delta_time: float = 1 / 60):
        # Update the animation timer
        self.animation_timer += delta_time


        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
                        

        if self.animation_timer >= self.debounce_time:
            # Reset the timer and update the current texture
            self.animation_timer = 0            
            # Determine animation based on current state
            if self.change_y > 0:
                self.cur_texture = (self.cur_texture + 1) % len(self.jump_textures)
                self.texture = self.jump_textures[self.cur_texture][self.character_face_direction]
            elif self.change_y < 0 and self.physics_engine.can_jump():
                self.cur_texture = (self.cur_texture + 1) % len(self.fall_textures)
                self.texture = self.fall_textures[self.cur_texture][self.character_face_direction]
            elif self.change_x == 0:
                self.cur_texture = 0 
                self.texture = self.idle_texture_pair[self.character_face_direction]
            elif self.change_x != 0:
                self.cur_texture = (self.cur_texture + 1) % len(self.walk_textures)
                self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

    
    def update(self):
        self.move()
        self.physics_engine.update()
        self.update_animation()      