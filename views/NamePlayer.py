import arcade
import arcade.gui

from database.ConexionDB import ConexionBD
from views.Difficulty import DifficultyView
from views.MainMenu import MainView
from components.button import Button
from setup import PLAYER_BG_PATH, WINDOW_WIDTH, WINDOW_HEIGHT, TITLE_NAME_PATH, CONTINUE_BUTTON_PATH, CONTINUE_HOVER_BUTTON_PATH

class NamePlayerView(arcade.View):
    def __init__(self):
        super().__init__()
        self.db = ConexionBD()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.buttons = []
        self.selected_button_index = 0  # Índice del botón seleccionado

        scale = 0.35
        self.buttons.append(Button(CONTINUE_BUTTON_PATH, CONTINUE_HOVER_BUTTON_PATH, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 700, self.on_click_confirm, scale=scale))
        # Calcular el ancho máximo de los botones
        self.max_button_width = max(button.width for button in self.buttons)

        # Establecer el ancho de todos los botones con el ancho máximo
        for button in self.buttons:
            button.width = self.max_button_width

        # Seleccionar el primer botón
        self.buttons[self.selected_button_index].select()

        self.v_box = arcade.gui.UIBoxLayout()

        self.lblp1 = arcade.gui.UILabel(
            text="",
            font_size=24,
            height=100,
            width=200,
            text_color=arcade.color.WHITE,
            anchor_x="left",
            anchor_y="center"
        )
        self.lblp2 = arcade.gui.UILabel(
            text="",
            font_size=24,
            height=100,
            width=200,
            text_color=arcade.color.WHITE,
            anchor_x="left",
            anchor_y="center"
        )
        self.v_box.add(self.lblp1.with_space_around(bottom=25))

        self.player1_input = arcade.gui.UIInputText(text="", width=200, text_color=(255,255,255), font_size=30)
        self.player2_input = arcade.gui.UIInputText(text="", width=200, text_color=(255,255,255), font_size=30)

        self.v_box.add(self.player1_input.with_space_around(bottom=20))
        self.v_box.add(self.lblp2.with_space_around(bottom=25))
        self.v_box.add(self.player2_input.with_space_around(bottom=20))

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE)  # Cambiar el fondo a azul
        self.background = arcade.load_texture(PLAYER_BG_PATH)
        self.title_image = arcade.load_texture(TITLE_NAME_PATH)

    def on_draw(self):
        arcade.start_render()
        scale_x = self.window.width / WINDOW_WIDTH
        scale_y = self.window.height / WINDOW_HEIGHT

        # Apply the scaling factors and set the viewport to cover the entire window
        # Apply scaling using set_viewport
        arcade.set_viewport(0, self.window.width / scale_x, 0, self.window.height / scale_y)

        # Draw background, title, and buttons with the scaling applied
        arcade.draw_lrwh_rectangle_textured(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, self.background)

        title_image_x = WINDOW_WIDTH // 2
        title_image_y = WINDOW_HEIGHT - 100
        title_image_scale = 1  # You might need to adjust this if your title is too large
        arcade.draw_scaled_texture_rectangle(title_image_x, title_image_y, self.title_image, title_image_scale)
        for button in self.buttons:
            button.draw()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.buttons[self.selected_button_index].deselect()  # Deseleccionar el botón actual
            self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
            self.buttons[self.selected_button_index].select()  # Seleccionar el nuevo botón
        elif key == arcade.key.DOWN:
            self.buttons[self.selected_button_index].deselect()  # Deseleccionar el botón actual
            self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
            self.buttons[self.selected_button_index].select()  # Seleccionar el nuevo botón
        elif key == arcade.key.SPACE:
            self.buttons[self.selected_button_index].action()
        elif key == arcade.key.ESCAPE:
            self.window.show_view(MainView())

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

    def on_click_confirm(self):
        player1_name = self.player1_input.text.strip()
        player2_name = self.player2_input.text.strip()
        
        p1_found = self.db.get_player_by_name(player1_name)
        p2_found = self.db.get_player_by_name(player2_name)
        
        if not player1_name or not player2_name:
            return
        
        if p1_found is None:
            self.db.insert_player(player1_name)
            
        if p2_found is None:
            self.db.insert_player(player2_name)
            
        # Aquí puedes agregar la lógica para cambiar a la siguiente vista o almacenar los nombres.
        self.dificult_view = DifficultyView(player1_name, player2_name)  # Cambia a la vista del menú
        self.window.show_view(self.dificult_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())

    def on_hide_view(self):
        self.manager.disable()