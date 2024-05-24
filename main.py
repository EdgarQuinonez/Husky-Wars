import arcade, random, math
from scripts.enemy import Aspersor
from setup import ASPERSOR_1_ID, ASPERSOR_2_ID, ASPERSOR_3_ID, ASPERSOR_4_ID, ASPERSOR_PROJECTILE_SPEED, ASPERSOR_SCALING, ASPERSOR_SPRITE_PATH, BAD_COLLECTIBLE_RARE_DROP_RATE, BAD_COLLECTIBLE_RARE_PATH, BAD_COLLECTIBLE_RARE_POINTS, BAD_COLLECTIBLE_UNCOMMON_DROP_RATE, BAD_COLLECTIBLE_UNCOMMON_PATH, BAD_COLLECTIBLE_UNCOMMON_POINTS, COLLECTIBLE_SOUND_PATH, FRISBEE_1_ID, FRISBEE_2_ID, GOOD_COLLECTIBLE_RARE_DROP_RATE, GOOD_COLLECTIBLE_RARE_PATH, GOOD_COLLECTIBLE_RARE_POINTS, GOOD_COLLECTIBLE_UNCOMMON_DROP_RATE, GOOD_COLLECTIBLE_UNCOMMON_PATH, GOOD_COLLECTIBLE_UNCOMMON_POINTS, HURT_SOUND_PATH, JUMP_SOUND_PATH, LAYER_NAME_BACKGROUND, LAYER_NAME_METABACKGROUND, OBJECT_ENEMY_ATTR, OBJECT_NAME_COLLECTIBLES, OBJECT_NAME_ENEMY_SPAWN, OBJECT_NAME_PLAYER_SPAWN, OBJECT_NAME_PROJECTILE, P1_ID, P2_ID, PROJECTILE_SOUND_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, TILE_SCALING, P1_STILL_PATH, P2_STILL_PATH, P1_START_X, P1_START_Y, P2_START_Y, P2_START_X, P1_SPEED, P2_SPEED, P1_KEYBINDINGS, P2_KEYBINDINGS, GRAVITY, P1_JUMP_SPEED, P2_JUMP_SPEED, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_COMMON_PATH, P1_SCORE_X, P1_SCORE_Y, P2_SCORE_X, P2_SCORE_Y, GOOD_COLLECTIBLE_COMMON_POINTS, BAD_COLLECTIBLE_COMMON_POINTS, BAD_COLLECTIBLE_COMMON_PATH, GOOD_COLLECTIBLE_COMMON_DROP_RATE, BAD_COLLECTIBLE_COMMON_DROP_RATE, TILE_SIZE, LAYER_NAME_PLATFORMS, RIGHT_FACING, LEFT_FACING, P1_ANIMATIONS_PATH, P2_ANIMATIONS_PATH, TILE_MAP_PATH, WATER_SOUND_PATH
from scripts.player import Player
from scripts.collectible import Coin, Trap, Powerup
from scripts.countdown import Countdown


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.tile_map = None
        self.collectible_layer = None
        self.scene = None
        self.p1_sprite = None
        self.p2_sprite = None
        self.countdown = None
        self.countdown_text = None
        
        self.collectible_sound = arcade.load_sound(COLLECTIBLE_SOUND_PATH)
        self.jump_sound = arcade.load_sound(JUMP_SOUND_PATH)
        self.water_sound = arcade.load_sound(WATER_SOUND_PATH)
        self.projectile_sound = arcade.load_sound(PROJECTILE_SOUND_PATH)
        self.hurt_sound = arcade.load_sound(HURT_SOUND_PATH)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        self.scene = arcade.Scene()
        
        map_name = TILE_MAP_PATH
        
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            OBJECT_NAME_COLLECTIBLES: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_BACKGROUND: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_METABACKGROUND: {
                "use_spatial_hash": True,
            },
            OBJECT_NAME_PLAYER_SPAWN: {
                "use_spatial_hash": True,
            },
            OBJECT_NAME_ENEMY_SPAWN: {
                "use_spatial_hash": True,
            },
            OBJECT_NAME_PROJECTILE: {
                "use_spatial_hash": False,
            }
        }

        
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.collectible_layer = self.tile_map.object_lists[OBJECT_NAME_COLLECTIBLES]         
        self.player_spawn_objs = self.tile_map.object_lists[OBJECT_NAME_PLAYER_SPAWN]
        self.enemy_spawn_objs = self.tile_map.object_lists[OBJECT_NAME_ENEMY_SPAWN]

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        platforms_layer = self.scene[LAYER_NAME_PLATFORMS]
        p1_spawn = self.get_player_spawn_point(P1_ID)
        p2_spawn = self.get_player_spawn_point(P2_ID)
                
        self.p1_sprite = Player(P1_STILL_PATH)
        self.p2_sprite = Player(P2_STILL_PATH)
        
        self.p1_sprite.setup(platforms_layer, self.jump_sound, (P1_SCORE_X, P1_SCORE_Y), RIGHT_FACING, P1_ANIMATIONS_PATH, 0, "Player 1", P1_JUMP_SPEED, P1_SPEED, P1_KEYBINDINGS, p1_spawn, self.hurt_sound)        
        self.p2_sprite.setup(platforms_layer, self.jump_sound, (P2_SCORE_X, P2_SCORE_Y), LEFT_FACING, P2_ANIMATIONS_PATH, 0, "Player 2", P2_JUMP_SPEED, P2_SPEED, P2_KEYBINDINGS, p2_spawn, self.hurt_sound)        
        
        self.scene.add_sprite(OBJECT_NAME_PLAYER_SPAWN, self.p1_sprite)                        
        self.scene.add_sprite(OBJECT_NAME_PLAYER_SPAWN, self.p2_sprite)
                
        # Generate random collectibles function call
        self.collectible_list = arcade.SpriteList()
        self.generate_collectibles()                          
        
        self.countdown = Countdown()
        self.countdown.start()
        self.countdown_text = f"{self.countdown.remaining_time}"
        
        # Enemies setup
        self.aspersores_ids = [ASPERSOR_1_ID, ASPERSOR_2_ID, ASPERSOR_3_ID, ASPERSOR_4_ID]
        self.frisbee_ids = [FRISBEE_1_ID, FRISBEE_2_ID]
        
        # Create enemies instances
        self.enemies = arcade.SpriteList()
        self.projectiles = arcade.SpriteList()
        
        self.aspersores_objs = {}
        
        # Set up aspersores        
        for aspersor_id in self.aspersores_ids:            
            self.aspersores_objs[aspersor_id] = Aspersor(ASPERSOR_SPRITE_PATH, ASPERSOR_SCALING, self.get_enemy_spawn_point(aspersor_id),  ASPERSOR_PROJECTILE_SPEED)                                    
            self.aspersores_objs[aspersor_id].setup(self.scene, self.water_sound)                        
    
    def get_player_spawn_point(self, player_id):                
        for spawn in self.player_spawn_objs:
            if spawn.properties["player_id"] == player_id:
                cartesian = self.tile_map.get_cartesian(spawn.shape[0], spawn.shape[1])
                center_x = math.floor(
                        cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                    )
                center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                )
                
                return (center_x, center_y)                
                    
    def generate_collectibles(self):
        # Define possible collectible types
        collectible_types = ["Coin", "Trap"]                       
        # Iterate over spawn points and create collectibles
        for collectible_object in self.collectible_layer:
            cartesian = self.tile_map.get_cartesian(
                collectible_object.shape[0], collectible_object.shape[1]
            )            
            collectible = None                        
            # Check for existing collectibles at this position
            existing_collectible = None
    

            # If no existing collectible found, spawn a new one
            for sprite in self.collectible_list:
                if sprite.center_x == math.floor(
                    cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                ) and sprite.center_y == math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                ):
                    existing_collectible = sprite
                    break
                
            if existing_collectible is None: 
                    
                collectible_type = random.choice(collectible_types)  # Randomly choose the type
                
                if collectible_type == "Coin":
                    
                    if random.random() < GOOD_COLLECTIBLE_RARE_DROP_RATE:
                        collectible = Coin(GOOD_COLLECTIBLE_RARE_PATH, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_RARE_POINTS)
                    elif random.random() < GOOD_COLLECTIBLE_UNCOMMON_DROP_RATE:
                        collectible = Coin(GOOD_COLLECTIBLE_UNCOMMON_PATH, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_UNCOMMON_POINTS)
                    elif random.random() <= GOOD_COLLECTIBLE_COMMON_DROP_RATE:
                        collectible = Coin(GOOD_COLLECTIBLE_COMMON_PATH, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_COMMON_POINTS)
                        
                    
                    
                        
                elif collectible_type == "Trap":
                
                    if random.random() < BAD_COLLECTIBLE_RARE_DROP_RATE:
                        collectible = Trap(BAD_COLLECTIBLE_RARE_PATH, COLLECTIBLE_SCALING, BAD_COLLECTIBLE_RARE_POINTS)
                    elif random.random() < BAD_COLLECTIBLE_UNCOMMON_DROP_RATE:
                        collectible = Trap(BAD_COLLECTIBLE_UNCOMMON_PATH, COLLECTIBLE_SCALING, BAD_COLLECTIBLE_UNCOMMON_POINTS)
                    elif random.random() <= BAD_COLLECTIBLE_COMMON_DROP_RATE:
                        collectible = Trap(BAD_COLLECTIBLE_COMMON_PATH, COLLECTIBLE_SCALING, BAD_COLLECTIBLE_COMMON_POINTS)
                    

                                                                   
                # Only add to the lists if a collectible was created
                if collectible is not None:  
                    collectible.center_x = math.floor(
                        cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                    )
                    collectible.center_y = math.floor(
                        (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                    )
                    
                    if collectible_type == "Coin":
                        collectible.setup(self.collectible_sound)
                    elif collectible_type == "Trap":
                        collectible.setup(self.hurt_sound)
    
                    self.collectible_list.append(collectible)
                    self.scene.add_sprite(OBJECT_NAME_COLLECTIBLES, collectible) # Creating new layer with collectibles and adding each sprite.
                    
    def get_enemy_spawn_point(self, enemy_id):        
        for spawn in self.enemy_spawn_objs:            
            if spawn.properties["enemy_id"] == enemy_id:
                cartesian = self.tile_map.get_cartesian(spawn.shape[0], spawn.shape[1])
                center_x = math.floor(
                        cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                    )
                center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                )
                
                return (center_x, center_y)
    
    def spawn_enemies(self, delta_time):
        for aspersor in self.aspersores_objs.values():
            
            aspersor.update(delta_time)
        

                                                                                                   
    def on_draw(self):
        """Render the screen."""        
        self.clear()        
            
        self.scene.draw()        
        self.p1_sprite.draw_gui()
        self.p2_sprite.draw_gui()
        arcade.draw_text(
            self.countdown_text,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 30,
            arcade.csscolor.WHITE,
            30,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):
        self.p1_sprite.on_key_press(key, modifiers)
        self.p2_sprite.on_key_press(key, modifiers)
                    
        
    def on_key_release(self, key, modifiers):
        self.p1_sprite.on_key_release(key, modifiers)
        self.p2_sprite.on_key_release(key, modifiers)
            
    def on_update(self, delta_time: float):
        self.p1_sprite.update()
        self.p2_sprite.update()
        
        # Check collectible spawn cooldown to regenerate collectibles
        if self.countdown.remaining_time % 5 == 0:            
            self.generate_collectibles()
        
                
        # Separate collision checks
        player1_coin_hit_list = arcade.check_for_collision_with_list(self.p1_sprite, self.scene[OBJECT_NAME_COLLECTIBLES])
        player2_coin_hit_list = arcade.check_for_collision_with_list(self.p2_sprite, self.scene[OBJECT_NAME_COLLECTIBLES])

        for coin in player1_coin_hit_list:
            coin.collect(self.p1_sprite)  # Update only Player 1's score
            coin.update()

        for coin in player2_coin_hit_list:
            coin.collect(self.p2_sprite)  # Update only Player 2's score
            coin.update()
        
        self.spawn_enemies(delta_time)
        
        # Countdown Check and Match Reset
        self.countdown_text = f"{self.countdown.remaining_time}"
        if self.countdown.remaining_time <= 0:
            self.setup()  # Reset the game when the countdown reaches 0


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()