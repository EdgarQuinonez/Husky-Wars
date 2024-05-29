import arcade
import arcade.gui

from database.ConexionDB import ConexionBD
from setup import CUSTOM_FONT_PATH, SCOREBOARD_BG_PATH

class ScoreboardView(arcade.View):
    def __init__(self):
        super().__init__()
        self.db = ConexionBD()
        self.ui_manager = arcade.gui.UIManager()
        self.background_image = None
        self.gameplay_font = arcade.load_font(CUSTOM_FONT_PATH)
        

    def setup(self):
        arcade.set_background_color(arcade.csscolor.DARK_VIOLET)
        self.background_image = arcade.load_texture(SCOREBOARD_BG_PATH)

        # Main Layout
        main_layout = arcade.gui.UIBoxLayout(vertical=True)

        # Title
        title_label = arcade.gui.UILabel(
            text="Scoreboard", 
            text_align="center", 
            font_size=24, 
            bold=True, 
            font_name=self.gameplay_font
        )
        main_layout.add(arcade.gui.UIAnchorWidget(child=title_label, anchor_x="center", anchor_y="top"))

        # Table Headers (with custom font)
        table_headers = arcade.gui.UIBoxLayout(vertical=False)
        for header_text in ["Nombre", "Puntos", "Duración total"]:
            table_headers.add(arcade.gui.UILabel(
                text=header_text, 
                width=150, 
                text_align="center", 
                font_name=self.gameplay_font
            ))
        main_layout.add(table_headers)

        # Player Data
        player_data_container = arcade.gui.UIBoxLayout(vertical=True)
        for score in self.db.get_top_10_scores():
            row = arcade.gui.UIBoxLayout(vertical=False)
            for item in score:  
                row.add(arcade.gui.UILabel(
                    text=str(item),  
                    width=150, 
                    text_align="left" if isinstance(item, str) else "right",
                    font_name=self.gameplay_font
                ))
            player_data_container.add(row)
        main_layout.add(player_data_container)
        
        # Back Button
        back_button = arcade.gui.UIFlatButton(
            text="Atrás", width=120,     
        )
        back_button.on_click = self.on_back_button_click
        main_layout.add(
            arcade.gui.UIAnchorWidget(child=back_button, anchor_x="center", anchor_y="bottom", align_y=-10)
        )

        # UI setup
        background_container = arcade.gui.UIWidget()
        background_container.add(arcade.gui.UIAnchorWidget(child=main_layout, anchor_x="center", anchor_y="center"))
        
        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=background_container,
            )
        )

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background_image)
        self.ui_manager.draw()

    def on_back_button_click(self, event):        
        from views.GameOver import GameOver
        game_over_view = GameOver()
        self.window.show_view(game_over_view)                 

    def on_show_view(self):
        self.setup()
        
    def on_hide_view(self):        
        self.ui_manager.disable()


if __name__ == "__main__":
    window = arcade.Window(title="Scoreboard Example", width=800, height=600)
    view = ScoreboardView()
    window.show_view(view)
    arcade.run()
