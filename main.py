import arcade

from setup import WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from views.MainMenu import MainView


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, fullscreen=False)
    main_view = MainView()
    window.show_view(main_view)
    
    arcade.window_commands.set_viewport(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    arcade.run()

if __name__ == "__main__":
    main()
