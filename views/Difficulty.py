import arcade

from components.button import Button
from setup import DIFFICULTY_HARD, DIFFICULTY_REGULAR, WINDOW_HEIGHT, WINDOW_WIDTH
from views.Game import MyGame
from views.MainMenu import MainView


class DifficultyView(arcade.View):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.selected_button_index = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_TERRA_COTTA)
        scale = 0.5
        self.buttons.append(
            Button("assets/buttons/normalbtn.png", "assets/buttons/normalbtn_hover.png", WINDOW_WIDTH - 1300,
                   WINDOW_HEIGHT // 2, self.normal, scale=scale))
        self.buttons.append(
            Button("assets/buttons/dificilbtn.png", "assets/buttons/dificilbtn_hover.png", WINDOW_WIDTH - 600,
                   WINDOW_HEIGHT // 2, self.dificil, scale=scale))

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Dificultades", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50,
                         arcade.color.WHITE, font_size=24, anchor_x="center")
        for button in self.buttons:
            button.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())
        elif key == arcade.key.UP:
            self.buttons[self.selected_button_index].deselect()  # Deseleccionar el botón actual
            self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
            self.buttons[self.selected_button_index].select()  # Seleccionar el nuevo botón
        elif key == arcade.key.DOWN:
            self.buttons[self.selected_button_index].deselect()  # Deseleccionar el botón actual
            self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
            self.buttons[self.selected_button_index].select()  # Seleccionar el nuevo botón
        elif key == arcade.key.SPACE:
            self.buttons[self.selected_button_index].action()

    def on_mouse_motion(self, x, y, dx, dy):
        for index, button in enumerate(self.buttons):
            if button.check_mouse_hover(x, y):
                self.buttons[self.selected_button_index].deselect()  # Deseleccionar el botón actual
                self.selected_button_index = index
                self.buttons[self.selected_button_index].select()  # Seleccionar el nuevo botón

    def on_mouse_press(self, x, y, button, modifiers):
        for index, button in enumerate(self.buttons):
            if button.check_mouse_hover(x, y):
                self.buttons[self.selected_button_index].deselect()  # Deseleccionar el botón actual
                self.selected_button_index = index
                self.buttons[self.selected_button_index].select()  # Seleccionar el nuevo botón
                button.action()

    def normal(self):
        game_view = MyGame()
        game_view.setup(DIFFICULTY_REGULAR)
        self.window.show_view(game_view)

    def dificil(self):
        #self.click_sound.play()
        game_view = MyGame()
        game_view.setup(DIFFICULTY_HARD)
        self.window.show_view(game_view)
