import arcade

from setup import WINDOW_HEIGHT, WINDOW_WIDTH
from views.MainMenu import MainView


class OptionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Opciones", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                         arcade.color.WHITE, font_size=24, anchor_x="center")
        # No necesitamos dibujar botones aquí, eso lo maneja la vista principal

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())
