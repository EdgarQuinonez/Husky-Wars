import arcade
import arcade.key
import arcade.key
from setup import CHARACTER_SCALING, FALLING_PENALIZATION_POINTS, GRAVITY, HURT_TIMER_DURATION, LEFT_FACING, RIGHT_FACING, SCORE_COLOR, SCORE_PIXEL_SIZE, SCORE_SPRITE_SCALE

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class Player(arcade.Sprite):
    def __init__(self, image_path):      
        super().__init__(filename=image_path, scale=CHARACTER_SCALING)        
             
        self.character_face_direction = None
        self.physics_engine: arcade.PhysicsEnginePlatformer = None
        self.name = None
        self.keybindings = None
        self.score = 0
        self.score_text = "Score: 0"
        self.jump_speed = None
        self.speed = None        
        self.jump_sound = None
        self.pressed_keys = set()
        self.score_x = None
        self.score_y = None
        self.animations_main_path = None
        self.hurt_sound = None
        self.respawn_timer = 0  
        self.respawn_delay = 3  # seconds
        
        
        # Animations
        
        self.animation_timer = 0  
        self.debounce_time = 0.1 
        self.hurt_timer = 0  # Timer for hurt state
        
        self.cur_texture = 0
        
        self.is_jumping = False
        self.is_walking = False
        
        self.idle_texture_pair = None
        self.falling_sound_played = False        
                            
        # Load textures for walking
        self.hurt_textures = []
        self.walk_textures = []
        self.jump_textures = []
        self.fall_textures = []

                
    
    def setup(self, walls, jump_sound, score_position, face_direction, animations_path, score, name, jump_speed, speed, keybindings, spawn_position, hurt_sound, falling_sound, score_sprite, score_sprite_position):        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self, walls, GRAVITY)
        self.jump_sound = jump_sound
        self.score_x, self.score_y = score_position        
        self.character_face_direction = face_direction
        self.animations_main_path = animations_path
        self.score = score
        self.name = name
        self.jump_speed = jump_speed
        self.speed = speed
        self.keybindings = keybindings
        self.spawn_position = spawn_position
        self.center_x, self.center_y = spawn_position
        self.hurt_sound = hurt_sound
        self.falling_sound = falling_sound
        self.idle_texture_pair = load_texture_pair(f"{self.animations_main_path}/idle.png")        
        self.score_sprite = arcade.Sprite(score_sprite, SCORE_SPRITE_SCALE)
        self.score_sprite_x, self.score_sprite_y = score_sprite_position
        
        
        # Load hurt textures
        for i in range(6):
            texture = load_texture_pair(f"{self.animations_main_path}/hurt_{i}.png")
            self.hurt_textures.append(texture)
        
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
        self.score_sprite.center_x = self.score_sprite_x
        self.score_sprite.center_y = self.score_sprite_y
        self.score_sprite.draw()
        
        score_text = f"{self.score}"
        arcade.draw_text(
            score_text,
            self.score_x,
            self.score_y,
            SCORE_COLOR,
            SCORE_PIXEL_SIZE,
            bold=True,
        )
    
    def move(self):
        if self.keybindings["up"] in self.pressed_keys:
            if self.physics_engine.can_jump():
                self.change_y = self.jump_speed 
                arcade.play_sound(self.jump_sound)           
        # elif self.keybindings["down"] in self.pressed_keys:
        #     self.change_y = -self.speed        
        if self.keybindings["right"] in self.pressed_keys:
            self.change_x = self.speed
        elif self.keybindings["left"] in self.pressed_keys:
            self.change_x = -self.speed
        else:
            self.change_x = 0
            
    def respawn(self):
        # Reset position to spawn point
        self.center_x, self.center_y = self.spawn_position
        
        # Diminish score (adjust points as needed)
        self.score += FALLING_PENALIZATION_POINTS
        self.score_text = f"Score: {self.score}"
        
        # Reset the timer and any falling-related state
        self.falling_sound_played = False
        self.respawn_timer = 0
        self.change_y = 0  # Stop any residual falling motion
            
    def take_damage(self, penalization_points):
        if self.hurt_timer <= 0:  # Check if not already hurt
            arcade.play_sound(self.hurt_sound)  # Play the hurt sound
            self.score += penalization_points  # Decrease the score
            self.score_text = f"Score: {self.score}"             
            self.hurt_timer = HURT_TIMER_DURATION  # Set hurt duration (adjust as needed)
            
    def update_animation(self, delta_time: float = 1 / 60):
        # Update the animation timer
        self.animation_timer += delta_time

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        
        # Determine animation based on current state
        if self.hurt_timer > 0:
            self.cur_texture = (self.cur_texture + 1) % len(self.hurt_textures)
            self.texture = self.hurt_textures[self.cur_texture][self.character_face_direction]
            self.hurt_timer -= delta_time # Decrement timer based on frame rate
            if self.hurt_timer <= 0:
                self.texture = self.idle_texture_pair[self.character_face_direction]  # Reset to idle texture                               
        
        if self.animation_timer >= self.debounce_time:
            # Reset the timer and update the current texture
            self.animation_timer = 0            
                                                    
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
    
    def player_fell(self, delta_time):
        if self.center_y < -50 and self.change_y < 0: 
            if not self.falling_sound_played:
                arcade.play_sound(self.falling_sound)
                self.falling_sound_played = True
            self.respawn_timer += delta_time
            if self.respawn_timer >= self.respawn_delay:
                self.respawn()  
    
    def update(self, delta_time: float = 1 / 60):
        self.move()
        self.physics_engine.update()
        self.update_animation()
        self.player_fell(delta_time)
        
        if self.score < 0:
            self.score = 0
             