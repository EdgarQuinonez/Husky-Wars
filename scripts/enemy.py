import arcade
import math
import random

from setup import AGUA_SCALING, AGUA_SPRITE_PATH, ASPERSOR_SHOT_PENALIZATION_POINTS, ASPERSOR_SPAWN_SHOOT_DELAY, FRISBEE_DEBOUNCE_TIME, FRISBEE_PENALIZATION_POINTS, OBJECT_NAME_ENEMY_SPAWN, OBJECT_NAME_PLAYER_SPAWN, OBJECT_NAME_PROJECTILE

class Enemy(arcade.Sprite):
    def __init__(self, image_path, scaling, spawn_point):
        super().__init__(image_path, scaling)
         
        self.center_x, self.center_y = spawn_point
        self.time_since_spawn = 0
        
        self.is_active = False  # Tracks whether the enemy is currently present
        
        self.done = False # Tracks whether the enemy has been completed his movement
        
        self.scene = None
        self.water_sound = None
        self.spawn_sound_played = True
        
        self.respawn_time = 0
        

    def setup(self, scene, water_sound):        
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
            self.spawn_sound_played = False         
            
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
                hit_list = arcade.check_for_collision_with_list(projectile, player_list)
                
                if hit_list:
                    projectile.remove_from_sprite_lists()  # Remove the projectile                    
                    for player in hit_list:
                        player.take_damage(ASPERSOR_SHOT_PENALIZATION_POINTS)
                
    def update(self, delta_time):
        super().update(delta_time)
        
        self.fire_projectile()
        
        if self.existing_projectile: # If there are projectiles
            screen_width = arcade.get_window().width
            screen_height = arcade.get_window().height
            for projectile in self.projectiles:
                if (projectile.bottom < 0 or projectile.top > screen_height or
                    projectile.left > screen_width or projectile.right < 0):
                    projectile.kill()                                        
                    
class Frisbee(Enemy):
    def __init__(self, image_path, scaling, spawn_point, speed, trail, id): 
        super().__init__(image_path, scaling, spawn_point)
        self.trail = trail  # Pass the trail directly
        self.speed = speed
        self.id = id
        
        self.projectile_sound = None
        self.current_waypoint = 0  # Track the current waypoint index
        self.harmless_timer = 0 

    def setup(self, scene, water_sound, projectile_sound):
        super().setup(scene, water_sound)
        self.projectile_sound = projectile_sound
        
    def spawn(self):
        super().spawn()
        if not self.spawn_sound_played:            
            self.spawn_sound_played = True
            arcade.play_sound(self.projectile_sound)
        
    
    def follow_trail(self, delta_time: float = 1 / 60):
        if self.is_active and self.current_waypoint < len(self.trail):            
            target_x, target_y = self.trail[self.current_waypoint]
            
    
            dx = (target_x - self.center_x) 
            dy = (target_y - self.center_y)
                  
            distance = math.hypot(dx, dy)
            
            if distance <= self.speed * delta_time:  
                self.current_waypoint += 1
                if self.current_waypoint >= len(self.trail):
                    self.done = True
                    self.current_waypoint = 0
            else:
                self.change_x = dx / distance * self.speed 
                self.change_y = dy / distance * self.speed
                self.center_x += self.change_x * delta_time
                self.center_y += self.change_y * delta_time
         
                                
            player_list = self.scene.get_sprite_list(OBJECT_NAME_PLAYER_SPAWN)                    
            hit_list = arcade.check_for_collision_with_list(self, player_list)
                
            # Harmless Period
            if self.harmless_timer > 0:
                self.harmless_timer -= delta_time
            else:  # Harmless period is over or not started
                if hit_list: 
                    for player in hit_list:
                        player.take_damage(FRISBEE_PENALIZATION_POINTS)
                    self.harmless_timer = FRISBEE_DEBOUNCE_TIME
                
            
                    
    def update(self, delta_time):
        super().update(delta_time)
        self.follow_trail()