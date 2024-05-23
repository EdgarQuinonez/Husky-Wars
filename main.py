import arcade, random, math
from setup import BAD_COLLECTIBLE_RARE_DROP_RATE, BAD_COLLECTIBLE_RARE_PATH, BAD_COLLECTIBLE_RARE_POINTS, BAD_COLLECTIBLE_UNCOMMON_DROP_RATE, BAD_COLLECTIBLE_UNCOMMON_PATH, BAD_COLLECTIBLE_UNCOMMON_POINTS, GOOD_COLLECTIBLE_RARE_DROP_RATE, GOOD_COLLECTIBLE_RARE_PATH, GOOD_COLLECTIBLE_RARE_POINTS, GOOD_COLLECTIBLE_UNCOMMON_DROP_RATE, GOOD_COLLECTIBLE_UNCOMMON_PATH, GOOD_COLLECTIBLE_UNCOMMON_POINTS, LAYER_NAME_BACKGROUND, LAYER_NAME_METABACKGROUND, OBJECT_NAME_COLLECTIBLES, OBJECT_NAME_ENEMY_SPAWN, OBJECT_NAME_PLAYER_SPAWN, OBJECT_NAME_PROJECTILE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, TILE_SCALING, P1_STILL_PATH, P2_STILL_PATH, P1_START_X, P1_START_Y, P2_START_Y, P2_START_X, P1_SPEED, P2_SPEED, P1_KEYBINDINGS, P2_KEYBINDINGS, GRAVITY, P1_JUMP_SPEED, P2_JUMP_SPEED, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_COMMON_PATH, P1_SCORE_X, P1_SCORE_Y, P2_SCORE_X, P2_SCORE_Y, GOOD_COLLECTIBLE_COMMON_POINTS, BAD_COLLECTIBLE_COMMON_POINTS, BAD_COLLECTIBLE_COMMON_PATH, GOOD_COLLECTIBLE_COMMON_DROP_RATE, BAD_COLLECTIBLE_COMMON_DROP_RATE, TILE_SIZE, LAYER_NAME_PLATFORMS, RIGHT_FACING, LEFT_FACING, P1_ANIMATIONS_PATH, P2_ANIMATIONS_PATH, TILE_MAP_PATH
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
        
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

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
                "use_spatial_hash": True,
            }
        }

        
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        # self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING)
        self.collectible_layer = self.tile_map.object_lists[OBJECT_NAME_COLLECTIBLES]         

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        self.p1_sprite = Player("player1", 0, (P1_START_X, P1_START_Y), P1_STILL_PATH, P1_SPEED, P1_JUMP_SPEED, P1_KEYBINDINGS)
        self.p2_sprite = Player("player2", 0, (P2_START_X, P2_START_Y), P2_STILL_PATH, P2_SPEED, P2_JUMP_SPEED, P2_KEYBINDINGS)
        
        self.scene.add_sprite(OBJECT_NAME_PLAYER_SPAWN, self.p1_sprite)                        
        self.scene.add_sprite(OBJECT_NAME_PLAYER_SPAWN, self.p2_sprite)
        
        
        # Generate random collectibles function call
        self.collectible_list = arcade.SpriteList()
        self.generate_collectibles()
         # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

                    
        self.p1_sprite.setup(self.scene[LAYER_NAME_PLATFORMS], self.jump_sound, (P1_SCORE_X, P1_SCORE_Y), RIGHT_FACING, P1_ANIMATIONS_PATH)        
        self.p2_sprite.setup(self.scene[LAYER_NAME_PLATFORMS], self.jump_sound, (P2_SCORE_X, P2_SCORE_Y), LEFT_FACING, P2_ANIMATIONS_PATH)
        
        self.countdown = Countdown()
        self.countdown.start()
        self.countdown_text = f"{self.countdown.remaining_time}"
                
    
    def generate_collectibles(self):
        # Define possible collectible types
        collectible_types = ["Coin", "Trap"]                        
        # Iterate over spawn points and create collectibles
        for collectible_object in self.collectible_layer:
            cartesian = self.tile_map.get_cartesian(
                collectible_object.shape[0], collectible_object.shape[1]
            )
            print(collectible_object)
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
                    
                    # if collectible is not None:
                    #     collectible.setup(self.collect_coin_sound, (x, y))
                    
                        
                elif collectible_type == "Trap":
                
                    if random.random() < BAD_COLLECTIBLE_RARE_DROP_RATE:
                        collectible = Coin(BAD_COLLECTIBLE_RARE_PATH, COLLECTIBLE_SCALING, BAD_COLLECTIBLE_RARE_POINTS)
                    elif random.random() < BAD_COLLECTIBLE_UNCOMMON_DROP_RATE:
                        collectible = Coin(BAD_COLLECTIBLE_UNCOMMON_PATH, COLLECTIBLE_SCALING, BAD_COLLECTIBLE_UNCOMMON_POINTS)
                    elif random.random() <= BAD_COLLECTIBLE_COMMON_DROP_RATE:
                        collectible = Coin(BAD_COLLECTIBLE_COMMON_PATH, COLLECTIBLE_SCALING, BAD_COLLECTIBLE_COMMON_POINTS)
                        
                    # if collectible is not None:
                    #     collectible.setup(self.collect_coin_sound, (x, y))
                                
                # Only add to the lists if a collectible was created
                if collectible is not None:  
                    collectible.center_x = math.floor(
                        cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                    )
                    collectible.center_y = math.floor(
                        (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                    )
                    self.collectible_list.append(collectible)
                    self.scene.add_sprite(OBJECT_NAME_COLLECTIBLES, collectible)                        
        
    def match_duration_countdown(self):
        pass        
    
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
            # print("Regenerating collectibles")
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