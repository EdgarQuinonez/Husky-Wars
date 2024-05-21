import arcade
from setup import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, CHARACTER_SCALING, TILE_SCALING, P1_STILL_PATH, P2_STILL_PATH, P1_START_X, P1_START_Y, P2_START_Y, P2_START_X, P1_SPEED, P2_SPEED, P1_KEYBINDINGS, P2_KEYBINDINGS, GRAVITY, P1_JUMP_SPEED, P2_JUMP_SPEED, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_COMMON_PATH
from scripts.player import Player
from scripts.collectible import Coin, Powerup


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.scene = None
        self.p1_sprite = None
        self.p2_sprite = None
        
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        
        self.scene = arcade.Scene()
        
        self.p1_sprite = Player("P1", 0, (P1_START_X, P1_START_Y), P1_STILL_PATH, P1_SPEED, P1_JUMP_SPEED, P1_KEYBINDINGS)
        self.p2_sprite = Player("P2", 0, (P2_START_X, P2_START_Y), P2_STILL_PATH, P2_SPEED, P2_JUMP_SPEED, P2_KEYBINDINGS)
        
        self.scene.add_sprite("Player", self.p1_sprite)                        
        self.scene.add_sprite("Player", self.p2_sprite)                        
                           
        # Tile generation
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)
        
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        # Crate generation
        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
            
        # Static good collectible spawning
        for x in range(128, 1250, 256):
            collectible = Coin(GOOD_COLLECTIBLE_COMMON_PATH, COLLECTIBLE_SCALING, 10, "common", 0.75)
            collectible.center_x = x
            collectible.center_y = 96
            self.scene.add_sprite("Coins", collectible)
            
        # Physics engine setup
        self.p1_sprite.setup(self.scene["Walls"], self.jump_sound)        
        self.p2_sprite.setup(self.scene["Walls"], self.jump_sound)        



    def on_draw(self):
        """Render the screen."""        
        self.clear()        
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        self.p1_sprite.on_key_press(key, modifiers)
        self.p2_sprite.on_key_press(key, modifiers)
                    
        
    def on_key_release(self, key, modifiers):
        self.p1_sprite.on_key_release(key, modifiers)
        self.p2_sprite.on_key_release(key, modifiers)
            
    def on_update(self, delta_time: float):
        self.p1_sprite.update()
        self.p2_sprite.update()
                
        # Combined collision check
        coin_hit_list = arcade.check_for_collision_with_list(self.p1_sprite, self.scene["Coins"])
        coin_hit_list.extend(arcade.check_for_collision_with_list(self.p2_sprite, self.scene["Coins"]))
        
        for coin in coin_hit_list:            
            coin.remove_from_sprite_lists()            
            arcade.play_sound(self.collect_coin_sound)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()