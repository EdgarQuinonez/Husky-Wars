import arcade

from components.button import Button
from setup import CLICK_SOUND_PATH, COMO_BUTTON_PATH, COMO_HOVER_BUTTON_PATH, JUGAR_BUTTON_PATH, JUGAR_HOVER_BUTTON_PATH, MENU_BG_PATH, OPCIONES_BUTTON_PATH, OPCIONES_HOVER_BUTTON_PATH, SALIR_BUTTON_PATH, SALIR_HOVER_BUTTON_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE_IMAGE_PATH
from views.Game import MyGame



class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_view = None
        self.background = None
        self.buttons = []
        self.selected_button_index = 0  # Índice del botón seleccionado
        self.max_button_width = 0  # Ancho máximo de los botones

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Cargar la imagen de fondo
        self.background = arcade.load_texture(MENU_BG_PATH)

        # Cargar la imagen del título
        self.title_image = arcade.load_texture(TITLE_IMAGE_PATH)

        # Crear botones de menú
        scale = 0.5
        self.buttons.append(Button(JUGAR_BUTTON_PATH, JUGAR_HOVER_BUTTON_PATH, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 500, self.on_click_play, scale=scale))
        self.buttons.append(Button(OPCIONES_BUTTON_PATH, OPCIONES_HOVER_BUTTON_PATH, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 650, self.on_click_options, scale=scale))
        self.buttons.append(Button(COMO_BUTTON_PATH, COMO_HOVER_BUTTON_PATH, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 800, self.on_click_how_to_play, scale=scale))
        self.buttons.append(Button(SALIR_BUTTON_PATH, SALIR_HOVER_BUTTON_PATH, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 950, self.on_click_exit, scale=scale))

        # Calcular el ancho máximo de los botones
        self.max_button_width = max(button.width for button in self.buttons)

        # Establecer el ancho de todos los botones con el ancho máximo
        for button in self.buttons:
            button.width = self.max_button_width

        # Seleccionar el primer botón
        self.buttons[self.selected_button_index].select()

        # Reproducir música de fondo
        #soundtrack = arcade.Sound("menu_soundtrack.mp3", streaming=True)
        #soundtrack.play(volume=0.5, loop=True)

        self.click_sound = arcade.Sound(CLICK_SOUND_PATH)

    def on_draw(self):
        arcade.start_render()

        # Calculate scaling factors to fit the content to the viewport
        scale_x = self.window.width / SCREEN_WIDTH
        scale_y = self.window.height / SCREEN_HEIGHT

        # Apply the scaling factors and set the viewport to cover the entire window
        # Apply scaling using set_viewport
        arcade.set_viewport(0, self.window.width / scale_x, 0, self.window.height / scale_y)  
     
        # Draw background, title, and buttons with the scaling applied
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        
        title_image_x = SCREEN_WIDTH // 2
        title_image_y = SCREEN_HEIGHT - 200
        title_image_scale = 1  # You might need to adjust this if your title is too large
        arcade.draw_scaled_texture_rectangle(title_image_x, title_image_y, self.title_image, title_image_scale)

        for button in self.buttons:
            button.draw()

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

    def on_click_play(self):
        self.click_sound.play()
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)

    def on_click_options(self):
        from views.OptionsMenu import OptionView
        self.option_view = OptionView()  # Cambia a la vista del menú
        self.window.show_view(self.option_view)
        self.click_sound.play()

    def on_click_how_to_play(self):
        from views.HowToPlay import HowPlayView
        
        self.hplay_view = HowPlayView()  # Cambia a la vista del menú
        self.window.show_view(self.hplay_view)
        self.click_sound.play()

    def on_click_exit(self):
        arcade.close_window()

    def close(self):
        # Liberar recursos o realizar cualquier limpieza necesaria
        # Por ejemplo, puedes cerrar conexiones a bases de datos, liberar texturas cargadas, etc.

        # Cerrar la ventana actual
        arcade.close_window()
