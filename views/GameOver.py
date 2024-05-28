import arcade

from setup import GAME_OVER_BG_PATH, WINDOW_HEIGHT, WINDOW_WIDTH
from views.MainMenu import MainView


class GameOver(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        # Cargar la imagen de fondo
        self.fondo = arcade.load_texture(GAME_OVER_BG_PATH)
        #los sprites de los perros ya estan xd nomas ponlos ahi en medio y ya lo acomodo yo

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT, self.fondo)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())

