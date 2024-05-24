import arcade
import math
import random

from setup import AGUA_SCALING, AGUA_SPRITE_PATH, ASPERSOR_SHOT_PENALIZATION_POINTS, ASPERSOR_SPAWN_SHOOT_DELAY, OBJECT_NAME_ENEMY_SPAWN, OBJECT_NAME_PLAYER_SPAWN, OBJECT_NAME_PROJECTILE

class Enemy(arcade.Sprite):
    def __init__(self, image_path, scaling, spawn_point):
        super().__init__(image_path, scaling)
         
        self.center_x, self.center_y = spawn_point
        self.time_since_spawn = 0
        
        self.is_active = False  # Tracks whether the enemy is currently present
        
        self.done = False # Tracks whether the enemy has been completed his movement
        
        self.scene = None  # Reference to the scene object
        self.water_sound = None  # Reference to the water sound object
        self.respawn_time = 0
        

    def setup(self, scene, water_sound):
        # Lo obtienes de los cooldown calculados aleatoriamente cada vez que se destruye el último        
        self.scene = scene
        self.water_sound = water_sound
        self.respawn_time = self.get_cooldown() 

    def get_cooldown(self):
        return random.randint(8, 13)
        
    
    def spawn(self):        
        if not self.is_active and self.respawn_time == 0:
            self.is_active = True
            self.time_since_spawn = 0
            self.collidable = False  # Disable hitbox            
            
            self.scene.add_sprite(OBJECT_NAME_ENEMY_SPAWN, self)  # Add to sprite lists

    def update(self, delta_time):
        
        if self.is_active:
            self.time_since_spawn += delta_time                    
                
        if not self.is_active:
            if self.respawn_time > 0:
                self.respawn_time -= delta_time            
            elif self.respawn_time <= 0:
                self.respawn_time = 0            
            self.spawn()
                                
        if self.is_active and self.done:            
            self.is_active = False
            self.done = False
            self.has_shot = False        
            self.kill()  # Remove from sprite lists
            self.respawn_time = self.get_cooldown()  # Set the respawn time to a random value

class Aspersor(Enemy):
    def __init__(self, image_path, scaling, spawn_point, projectile_speed):
        super().__init__(image_path, scaling, spawn_point)
        self.projectiles = arcade.SpriteList()        
        self.projectile_speed = projectile_speed
        self.existing_projectile = False
        self.has_shot = False
                

    def fire_projectile(self):        
        if not any(self.projectiles):  # Empty sprite lists evaluate to False
            self.existing_projectile = False            
             # Has shot and projectiles have been destroyed
            if self.is_active and self.time_since_spawn >= ASPERSOR_SPAWN_SHOOT_DELAY and self.has_shot:  # Ensure enemy is still active
                self.done = True
                
        elif any(self.projectiles):
            self.existing_projectile = True
        
        # Hasn't shot yet
        if self.is_active and self.time_since_spawn >= ASPERSOR_SPAWN_SHOOT_DELAY and not self.existing_projectile and not self.done:
            self.has_shot = True
            arcade.play_sound(self.water_sound)  # Play the water sound
            for angle in [135, 45]:
                # Create a new projectile
                projectile = arcade.Sprite(AGUA_SPRITE_PATH, AGUA_SCALING)
                projectile.center_x = self.center_x
                projectile.center_y = self.center_y

                # Set its initial change_x and change_y
                radians = math.radians(angle)
                projectile.change_x = math.cos(radians) * self.projectile_speed
                projectile.change_y = math.sin(radians) * self.projectile_speed

                self.projectiles.append(projectile)
                self.scene.add_sprite(OBJECT_NAME_PROJECTILE, projectile)
        # Has shot and projectiles are still active                
        elif self.existing_projectile and self.is_active and not self.done:  
            # Move existing projectiles
            for sprite in self.projectiles:
                sprite.center_x += sprite.change_x
                sprite.center_y += sprite.change_y
                
                
        # Check for collisions only if projectiles exist and the enemy is active
        if self.existing_projectile and self.is_active and not self.done:
            player_list = self.scene.get_sprite_list(OBJECT_NAME_PLAYER_SPAWN)  # Get the player sprite list

            # Check each projectile for collision with any player sprite
            for projectile in self.projectiles:
                # Use the sprite list for efficient collision detection
                hit_list = arcade.check_for_collision_with_list(projectile, player_list)
                
                if hit_list:
                    projectile.remove_from_sprite_lists()  # Remove the projectile                    
                    for player in hit_list:
                        player.take_damage(ASPERSOR_SHOT_PENALIZATION_POINTS)  # Example method to handle player damage
                
    
        

    def update(self, delta_time):
        super().update(delta_time)
        
        self.fire_projectile()

        # More extensive off-screen check
        if self.existing_projectile: # If there are projectiles
            screen_width = arcade.get_window().width
            screen_height = arcade.get_window().height
            for projectile in self.projectiles:
                if (projectile.bottom < 0 or projectile.top > screen_height or
                    projectile.left > screen_width or projectile.right < 0):
                    projectile.kill()                                        
                    
    
                    
            

class Frisbee(Enemy):
    def __init__(self, image_path, scaling, spawn_point, speed):
        super().__init__(image_path, scaling, spawn_point)
        self.trail = []  # List to store the trail coordinates
        self.speed = speed  # Speed at which the enemy moves

    def follow_trail(self):
        # Implement logic to follow the trail created in Tiled
        if self.trail:
            target_x, target_y = self.trail[0]  # Get the next target coordinates
            self.change_x = target_x - self.center_x  # Calculate the change in x direction
            self.change_y = target_y - self.center_y  # Calculate the change in y direction
            distance = math.sqrt(self.change_x ** 2 + self.change_y ** 2)  # Calculate the distance to the target
            if distance > 0:
                self.change_x /= distance  # Normalize the change in x direction
                self.change_y /= distance  # Normalize the change in y direction
                self.change_x *= self.speed  # Scale the change in x direction by the projectile speed
                self.change_y *= self.speed  # Scale the change in y direction by the projectile speed

    def update(self, delta_time):
        super().update(delta_time)
        self.follow_trail()