import arcade
from setup import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, CHARACTER_SCALING, TILE_SCALING, P1_STILL_PATH, P2_STILL_PATH, P1_START_X, P1_START_Y, P2_START_Y, P2_START_X, P1_SPEED, P2_SPEED, P1_KEYBINDINGS, P2_KEYBINDINGS
from scripts.player import Player


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.scene = None
        self.p1_sprite = None
        self.p1_physics_engine = None
        self.p2_physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):

        """Set up the game here. Call this function to restart the game."""
        
        self.scene = arcade.Scene()
        
        self.p1_sprite = Player("P1", 0, (P1_START_X, P1_START_Y), P1_STILL_PATH, P1_SPEED, P1_KEYBINDINGS)
        self.p2_sprite = Player("P2", 0, (P2_START_X, P2_START_Y), P2_STILL_PATH, P2_SPEED, P2_KEYBINDINGS)
        self.p1_keys_pressed = set()
        self.p2_keys_pressed = set()
        
        self.scene.add_sprite("Player", self.p1_sprite)
                   

        for x in range(0, 1250, 64):

            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)

            wall.center_x = x

            wall.center_y = 32

            self.scene.add_sprite("Walls", wall)
        
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:

            # Add a crate on the ground

            wall = arcade.Sprite(

                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING

            )

            wall.position = coordinate

            self.scene.add_sprite("Walls", wall)
            
        self.p1_physics_engine = arcade.PhysicsEngineSimple(self.p1_sprite, self.scene.get_sprite_list("Walls"))            
        self.p2_physics_engine = arcade.PhysicsEngineSimple(self.p2_sprite, self.scene.get_sprite_list("Walls"))



    def on_draw(self):
        """Render the screen."""
        # Clear the screen to the background color
        self.clear()
        # Draw our sprites
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        if key in (P1_KEYBINDINGS["up"], P1_KEYBINDINGS["left"], P1_KEYBINDINGS["down"], P1_KEYBINDINGS["right"]):
            self.p1_keys_pressed.add(key)
        if key in (P2_KEYBINDINGS["up"], P2_KEYBINDINGS["left"], P2_KEYBINDINGS["down"], P2_KEYBINDINGS["right"]):
            self.p2_keys_pressed.add(key)
            
        print(self.p1_keys_pressed)
        
    def on_key_release(self, key, modifiers):
        if key in (P1_KEYBINDINGS["up"], P1_KEYBINDINGS["left"], P1_KEYBINDINGS["down"], P1_KEYBINDINGS["right"]):
            self.p1_keys_pressed.discard(key)
        if key in (P2_KEYBINDINGS["up"], P2_KEYBINDINGS["left"], P2_KEYBINDINGS["down"], P2_KEYBINDINGS["right"]):
            self.p2_keys_pressed.discard(key)
            
    def on_update(self, delta_time: float):
        if P1_KEYBINDINGS["up"] in self.p1_keys_pressed and P1_KEYBINDINGS["down"] not in self.p1_keys_pressed:
            self.p1_sprite.change_y = self.p1_sprite.speed
        elif P1_KEYBINDINGS["down"] in self.p1_keys_pressed and P1_KEYBINDINGS["up"] not in self.p1_keys_pressed:
            self.p1_sprite.change_y = -self.p1_sprite.speed
        
        if P1_KEYBINDINGS["right"] in self.p1_keys_pressed and P1_KEYBINDINGS["left"] not in self.p1_keys_pressed:
            self.p1_sprite.change_x = self.p1_sprite.speed
        elif P1_KEYBINDINGS["left"] in self.p1_keys_pressed and P1_KEYBINDINGS["right"] not in self.p1_keys_pressed:
            self.p1_sprite.change_x = -self.p1_sprite.speed
    
        if P2_KEYBINDINGS["up"] in self.p1_keys_pressed and P2_KEYBINDINGS["down"] not in self.p1_keys_pressed:
            self.p2_sprite.change_y = self.p2_sprite.speed
        elif P2_KEYBINDINGS["down"] in self.p2_keys_pressed and P2_KEYBINDINGS["up"] not in self.p2_keys_pressed:
            self.p2_sprite.change_y = -self.p2_sprite.speed
        
        if P2_KEYBINDINGS["right"] in self.p2_keys_pressed and P2_KEYBINDINGS["left"] not in self.p2_keys_pressed:
            self.p2_sprite.change_x = self.p2_sprite.speed
        elif P2_KEYBINDINGS["left"] in self.p2_keys_pressed and P2_KEYBINDINGS["right"] not in self.p2_keys_pressed:
            self.p2_sprite.change_x = -self.p2_sprite.speed
                        
        self.p1_physics_engine.update()
        self.p2_physics_engine.update()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()