import arcade
import arcade.gui

from components.button import Button
from database.ConexionDB import ConexionBD
from setup import CUSTOM_FONT_PATH, SCOREBOARD_BG_PATH, TITLE_SCOREBOARD_PATH, WINDOW_HEIGHT, WINDOW_WIDTH, MENU_BUTTON_PATH, MENU_HOVER_BUTTON_PATH
from views.MainMenu import MainView

class ScoreboardView(arcade.View):
    def __init__(self):
        super().__init__()
        self.db = ConexionBD()
        self.ui_manager = arcade.gui.UIManager()
        self.background_image = None
        self.gameplay_font = arcade.load_font(CUSTOM_FONT_PATH)

        self.buttons = []
        self.selected_button_index = 0

        
    def setup(self):        
        self.background_image = arcade.load_texture(SCOREBOARD_BG_PATH)        
        main_layout = arcade.gui.UIBoxLayout(vertical=True)
        
        table_headers = arcade.gui.UIBoxLayout(vertical=False)
        for header_text in ["Nombre", "Puntos", "Duración total"]:
            table_headers.add(arcade.gui.UILabel(
                text=header_text, 
                width= 300 if header_text == "Nombre" else 150, 
                font_size=24,
                bold=True,
                text_align="center", 
                font_name=self.gameplay_font
            ))
        main_layout.add(table_headers)
        
        player_data_container = arcade.gui.UIBoxLayout(vertical=True)
        
        name, _, duration = range(3)
        
        for score in self.db.get_top_10_scores():
            row = arcade.gui.UIBoxLayout(vertical=False)
            for i in range(len(score)):
                item = arcade.gui.UILabel(
                    text=self._format_time(int(score[i])) if i == duration else str(score[i]),
                    font_size=24,  
                    width=300 if i == name else 150,
                    bold=True if i == name else False,                                                    
                ) 
                                 
                row.add(item)
                        
            player_data_container.add(row)
        main_layout.add(player_data_container)
                
        # back_button = arcade.gui.UIFlatButton(
        #     text="Atrás", width=120,     
        # )
        # back_button.on_click = self.on_back_button_click
        # main_layout.add(
        #     arcade.gui.UIAnchorWidget(child=back_button, anchor_x="center", anchor_y="bottom", align_y=-10)
        # )
        
        background_container = arcade.gui.UIWidget()
        background_container.add(arcade.gui.UIAnchorWidget(child=main_layout, anchor_x="center", anchor_y="center"))
        
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=background_container,
            )
        )
        
    def _format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background_image)
        title_image_x = WINDOW_WIDTH // 2
        title_image_y = WINDOW_HEIGHT - 100
        title_image_scale = 0.6  # You might need to adjust this if your title is too large
        arcade.draw_scaled_texture_rectangle(title_image_x, title_image_y, self.title_image, title_image_scale)
        for button in self.buttons:
            button.draw()
        self.ui_manager.draw()

    # def on_back_button_click(self, event):        
    #     from views.GameOver import GameOver
    #     game_over_view = GameOver()
    #     self.window.show_view(game_over_view)                 

    def on_show_view(self):
        self.title_image = arcade.load_texture(TITLE_SCOREBOARD_PATH)
        # Buttons
        scale = 0.3
        self.buttons.append(
            Button(MENU_BUTTON_PATH, MENU_HOVER_BUTTON_PATH, WINDOW_WIDTH // 5,
                   WINDOW_HEIGHT // 8, self.menu, scale=scale))
        self.setup()
        
    def on_hide_view(self):        
        self.ui_manager.disable()
        
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

    def menu(self):
        self.window.show_view(MainView())