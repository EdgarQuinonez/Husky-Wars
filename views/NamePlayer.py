import arcade
import arcade.gui

from database.ConexionDB import ConexionBD
from views.Difficulty import DifficultyView
from views.MainMenu import MainView


class NamePlayerView(arcade.View):
    def __init__(self):
        super().__init__()
        self.db = ConexionBD()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        self.label = arcade.gui.UILabel(text="Enter names for Player 1 and Player 2",
                                        font_size=24,
                                        text_color=arcade.color.WHITE,
                                        anchor_x="center")
        self.v_box.add(self.label.with_space_around(bottom=20))

        self.player1_input = arcade.gui.UIInputText(text="", width=200)
        self.player2_input = arcade.gui.UIInputText(text="", width=200)

        self.v_box.add(self.player1_input.with_space_around(bottom=20))
        self.v_box.add(self.player2_input.with_space_around(bottom=20))

        self.confirm_button = arcade.gui.UIFlatButton(text="Confirm", width=200)
        self.confirm_button.on_click = self.on_click_confirm
        self.v_box.add(self.confirm_button.with_space_around(bottom=20))

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_TERRA_COTTA)

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()

    def on_click_confirm(self, event):
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
