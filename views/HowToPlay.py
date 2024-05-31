import arcade

from setup import HOW_TO_PLAY_BG_PATH, WINDOW_HEIGHT, WINDOW_WIDTH
from views.MainMenu import MainView


class HowPlayView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)        
        self.howplay = arcade.load_texture(HOW_TO_PLAY_BG_PATH)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT, self.howplay)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())