import arcade
import math

from setup import AGUA_SCALING, AGUA_SPRITE_PATH, ASPERSOR_SPAWN_SHOOT_DELAY, OBJECT_NAME_ENEMY_SPAWN, OBJECT_NAME_PROJECTILE

class Enemy(arcade.Sprite):
    def __init__(self, image_path, scaling, spawn_point):
        super().__init__(image_path, scaling)
         
        self.center_x, self.center_y = spawn_point
        self.time_since_spawn = 0
        
        self.is_active = False  # Tracks whether the enemy is currently present
        
        self.done = False # Tracks whether the enemy has been completed his movement
        self.respawn_time = 0
        

    def setup(self, cooldown):
        # Lo obtienes de los cooldown calculados aleatoriamente cada vez que se destruye el último        
        self.respawn_time = cooldown        

    def spawn(self, scene):        
        if not self.is_active and self.respawn_time == 0:
            self.is_active = True
            self.time_since_spawn = 0
            self.collidable = False  # Disable hitbox            
            
            scene.add_sprite(OBJECT_NAME_ENEMY_SPAWN, self)  # Add to sprite lists

    def update(self, delta_time, scene):
        
        if self.is_active:
            self.time_since_spawn += delta_time                    
                
        if not self.is_active:
            if self.respawn_time > 0:
                self.respawn_time -= delta_time            
            elif self.respawn_time <= 0:
                self.respawn_time = 0
                
            self.spawn(scene)
                                
        if self.is_active and self.done:
            self.is_active = False
            self.done = False
            self.kill()  # Remove from sprite lists

class Aspersor(Enemy):
    def __init__(self, image_path, scaling, spawn_point, projectile_speed):
        super().__init__(image_path, scaling, spawn_point)
        self.projectiles = arcade.SpriteList()        
        self.projectile_speed = projectile_speed
        self.existing_projectile = None
                

    def fire_projectile(self, scene):
        # Check if there are no existing projectiles and conditions are met
        if self.is_active and self.time_since_spawn >= ASPERSOR_SPAWN_SHOOT_DELAY and not self.projectiles:
            for angle in [-45, 45]:
                # Create a new projectile
                projectile = arcade.Sprite(AGUA_SPRITE_PATH, AGUA_SCALING)
                projectile.center_x = self.center_x
                projectile.center_y = self.center_y

                # Set its initial change_x and change_y
                radians = math.radians(angle)
                projectile.change_x = math.cos(radians) * self.projectile_speed
                projectile.change_y = math.sin(radians) * self.projectile_speed

                self.projectiles.append(projectile)
                scene.add_sprite(OBJECT_NAME_PROJECTILE, projectile)
        else:  
            # Move existing projectiles
            for sprite in self.projectiles:
                sprite.center_x += sprite.change_x
                sprite.center_y += sprite.change_y

                # # Remove if off-screen
                # if sprite.top < 0 or sprite.bottom > scene.get_size()[1] or \
                # sprite.left < 0 or sprite.right > scene.get_size()[0]:
                #     self.projectiles.remove(sprite)
                #     sprite.remove_from_sprite_lists()

    def update(self, delta_time, scene):
        super().update(delta_time, scene)
        
        self.fire_projectile(scene)

        # More extensive off-screen check
        if self.existing_projectile: # If there are projectiles
            screen_width = arcade.get_window().width
            screen_height = arcade.get_window().height
            for projectile in self.projectiles:
                if (projectile.bottom < 0 or projectile.top > screen_height or
                    projectile.left > screen_width or projectile.right < 0):
                    if not self.projectiles:
                        self.done = True

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

    def update(self, delta_time, scene):
        super().update(delta_time, scene)
        self.follow_trail()