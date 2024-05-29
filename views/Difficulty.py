import arcade

from components.button import Button
from setup import DIFFICULTY_HARD, DIFFICULTY_REGULAR, WINDOW_HEIGHT, WINDOW_WIDTH, TITLE_DIFF_PATH, BG_EXTRA_PATH
from views.Game import MyGame
from views.MainMenu import MainView


class DifficultyView(arcade.View):
    def __init__(self, player1_name, player2_name):
        super().__init__()
        
        self.player1_name = player1_name
        self.player2_name = player2_name
        
        self.buttons = []
        self.selected_button_index = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_TERRA_COTTA)

        # Cargar la imagen de fondo
        self.background = arcade.load_texture(BG_EXTRA_PATH)
        # Cargar la imagen del título
        self.title_image = arcade.load_texture(TITLE_DIFF_PATH)

        scale = 0.5
        self.buttons.append(
            Button("assets/buttons/normalbtn.png", "assets/buttons/normalbtn_hover.png", WINDOW_WIDTH - 1100,
                   WINDOW_HEIGHT // 2, self.normal, scale=scale))
        self.buttons.append(
            Button("assets/buttons/dificilbtn.png", "assets/buttons/dificilbtn_hover.png", WINDOW_WIDTH - 500,
                   WINDOW_HEIGHT // 2, self.dificil, scale=scale))

    def on_draw(self):
        arcade.start_render()

        # Calculate scaling factors to fit the content to the viewport
        scale_x = self.window.width / WINDOW_WIDTH
        scale_y = self.window.height / WINDOW_HEIGHT

        # Apply the scaling factors and set the viewport to cover the entire window
        # Apply scaling using set_viewport
        arcade.set_viewport(0, self.window.width / scale_x, 0, self.window.height / scale_y)

        # Draw background, title, and buttons with the scaling applied
        arcade.draw_lrwh_rectangle_textured(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, self.background)
        title_image_x = WINDOW_WIDTH // 2
        title_image_y = WINDOW_HEIGHT - 100
        title_image_scale = 0.6  # You might need to adjust this if your title is too large
        arcade.draw_scaled_texture_rectangle(title_image_x, title_image_y, self.title_image, title_image_scale)
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
        game_view = MyGame(player1_name=self.player1_name, player2_name=self.player2_name)
        game_view.setup(DIFFICULTY_REGULAR)
        self.window.show_view(game_view)

    def dificil(self):
        #self.click_sound.play()
        game_view = MyGame(player1_name=self.player1_name, player2_name=self.player2_name)
        game_view.setup(DIFFICULTY_HARD)
        self.window.show_view(game_view)
