import arcade

from setup import ASPECT_RATIO
from views.MainMenu import MainView


SCREEN_WIDTH, _ = arcade.window_commands.get_display_size()
SCREEN_HEIGHT = int(SCREEN_WIDTH / ASPECT_RATIO)

SCREEN_TITLE = "¡Husky Wars!"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
    main_view = MainView()
    window.show_view(main_view)
    
    arcade.window_commands.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    arcade.run()

if __name__ == "__main__":
    main()
