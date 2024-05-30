import arcade
import arcade.gui

from database.ConexionDB import ConexionBD
from setup import CUSTOM_FONT_PATH, SCOREBOARD_BG_PATH
from views.MainMenu import MainView

class ScoreboardView(arcade.View):
    def __init__(self):
        super().__init__()
        self.db = ConexionBD()
        self.ui_manager = arcade.gui.UIManager()
        self.background_image = None
        self.gameplay_font = arcade.load_font(CUSTOM_FONT_PATH)
        
    def setup(self):        
        self.background_image = arcade.load_texture(SCOREBOARD_BG_PATH)        
        main_layout = arcade.gui.UIBoxLayout(vertical=True)
        
        title_label = arcade.gui.UILabel(
            text="Scoreboard",                        
            font_size=64, 
            bold=True, 
            font_name=self.gameplay_font
        )
        main_layout.add(arcade.gui.UIAnchorWidget(child=title_label, anchor_x="center", anchor_y="top"))
        
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
        self.ui_manager.draw()

    # def on_back_button_click(self, event):        
    #     from views.GameOver import GameOver
    #     game_over_view = GameOver()
    #     self.window.show_view(game_over_view)                 

    def on_show_view(self):
        self.setup()
        
    def on_hide_view(self):        
        self.ui_manager.disable()
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())