import arcade

from setup import WINDOW_HEIGHT, WINDOW_WIDTH, BG_EXTRA_PATH, TITLE_OPTIONS_PATH, SI_BUTTON_PATH, SI_HOVER_BUTTON_PATH, SUBTITLE_MUSIC_PATH, NO_BUTTON_PATH, NO_HOVER_BUTTON_PATH
from views.MainMenu import MainView
from components.button import Button
from settings import Settings

settings = Settings.get_instance()




class OptionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.is_music_playing = settings.music_is_playing 
        print(self.is_music_playing)       
        
        self.buttons = []
        self.selected_button_index = 0 
        self.max_button_width = 0 

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.background = arcade.load_texture(BG_EXTRA_PATH)
        # Cargar la imagen del título
        self.title_image = arcade.load_texture(TITLE_OPTIONS_PATH)
        self.second_title_image = arcade.load_texture(SUBTITLE_MUSIC_PATH)

        if self.is_music_playing:
            # Crear botones de menú
            scale = 0.35
            self.buttons.append(Button(NO_BUTTON_PATH, NO_HOVER_BUTTON_PATH, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 600,
                                        self.music_action, scale=scale))

            # Calcular el ancho máximo de los botones
            self.max_button_width = max(button.width for button in self.buttons)

            # Establecer el ancho de todos los botones con el ancho máximo
            for button in self.buttons:
                button.width = self.max_button_width

            # Seleccionar el primer botón
            self.buttons[self.selected_button_index].select()
            
        else:
                    
            # Crear botones de menú
            scale = 0.35
                    
            self.buttons.append(Button(SI_BUTTON_PATH, SI_HOVER_BUTTON_PATH, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 600,
                                            self.music_action, scale=scale))

            # Calcular el ancho máximo de los botones
            self.max_button_width = max(button.width for button in self.buttons)

            # Establecer el ancho de todos los botones con el ancho máximo
            for button in self.buttons:
                button.width = self.max_button_width

            # Seleccionar el primer botón
            self.buttons[self.selected_button_index].select()
            
    def update_button_appearance(self):
        if self.is_music_playing:
            self.buttons[0] = Button(NO_BUTTON_PATH, NO_HOVER_BUTTON_PATH, 
                                    WINDOW_WIDTH // 2, WINDOW_HEIGHT - 600,
                                    self.music_action, scale=0.35)
        else:
            self.buttons[0] = Button(SI_BUTTON_PATH, SI_HOVER_BUTTON_PATH, 
                                    WINDOW_WIDTH // 2, WINDOW_HEIGHT - 600,
                                    self.music_action, scale=0.35)

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
        title_image_y = WINDOW_HEIGHT - 200
        title_image_scale = 0.8  # You might need to adjust this if your title is too large
        arcade.draw_scaled_texture_rectangle(title_image_x, title_image_y, self.title_image, title_image_scale)

        subtitle_image_x = WINDOW_WIDTH // 2
        subtitle_image_y = WINDOW_HEIGHT - 400
        subtitle_image_scale = 0.5  # You might need to adjust this if your title is too large
        arcade.draw_scaled_texture_rectangle(subtitle_image_x, subtitle_image_y, self.second_title_image, subtitle_image_scale)

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
                self.buttons[self.selected_button_index].deselect()
                self.selected_button_index = index
                self.buttons[self.selected_button_index].select()

                
                button.action()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())

    def music_action(self):
        self.is_music_playing = not self.is_music_playing
        settings.toggle_music()
        self.update_button_appearance() 
