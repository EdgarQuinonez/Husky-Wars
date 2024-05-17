import arcade
from setup import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, CHARACTER_SCALING, TILE_SCALING, P1_STILL_PATH, P1_START_X, P1_START_Y
from scripts.player import Player


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.wall_list = None
        self.player_list = None

        self.p1_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):

        """Set up the game here. Call this function to restart the game."""

        # Create the Sprite lists

        self.player_list = arcade.SpriteList()

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)            

        self.p1_sprite = Player("P1", 0, (P1_START_X, P1_START_Y), P1_STILL_PATH)


        self.player_list.append(self.p1_sprite)



        # Create the ground

        # This shows using a loop to place multiple sprites horizontally

        for x in range(0, 1250, 64):

            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)

            wall.center_x = x

            wall.center_y = 32

            self.wall_list.append(wall)



        # Put some crates on the ground

        # This shows using a coordinate list to place sprites

        coordinate_list = [[512, 96], [256, 96], [768, 96]]



        for coordinate in coordinate_list:

            # Add a crate on the ground

            wall = arcade.Sprite(

                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING

            )

            wall.position = coordinate

            self.wall_list.append(wall)


    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()


        # Draw our sprites

        self.wall_list.draw()

        self.player_list.draw()



def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()