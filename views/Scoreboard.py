import arcade
import arcade.gui

from database.ConexionDB import ConexionBD

class ScoreboardView(arcade.View):
    def __init__(self):
        super().__init__()
        self.db = ConexionBD()
        self.ui_manager = arcade.gui.UIManager()  # For UI elements        

   
    def setup(self):
        main_layout = arcade.gui.UIBoxLayout(vertical=True)

        # Title
        title = arcade.gui.UILabel(text="Scoreboard", text_align="center", font_size=24, bold=True)
        main_layout.add(
            arcade.gui.UIAnchorWidget(child=title, anchor_x="center", anchor_y="top")
        )

        # Table headers
        table_headers = arcade.gui.UIBoxLayout(vertical=False)
        table_headers.add(arcade.gui.UILabel(text="Nombre", width=150, text_align="center"))
        table_headers.add(arcade.gui.UILabel(text="Puntos", width=100, text_align="center"))
        main_layout.add(table_headers)

        # Container for player data (no scrolling)
        player_data_container = arcade.gui.UIBoxLayout(vertical=True)
        main_layout.add(player_data_container)

        top_10_scores = self.db.get_top_10_scores()
        
        # Player rows
        for score in top_10_scores:
            row = arcade.gui.UIBoxLayout(vertical=False)
            row.add(arcade.gui.UILabel(text=score[0], width=150, text_align="left"))  # Score[0] should be name
            row.add(arcade.gui.UILabel(text=str(score[1]), width=100, text_align="right")) # Score[1] should be points
            player_data_container.add(row)

        self.ui_manager.add(main_layout) 
        
    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
        

    def on_show(self):
        self.setup()


if __name__ == "__main__":
    window = arcade.Window(title="Scoreboard Example", width=800, height=600)
    view = ScoreboardView()
    window.show_view(view)
    arcade.run()
