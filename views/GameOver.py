import arcade
import arcade.gui

from setup import DIALOG_OVERLAY_WINDOW_MARGIN_X, DIALOG_OVERLAY_WINDOW_MARGIN_Y, GAME_OVER_BG_PATH, P1_ID, P1_LOSER_PATH, P1_WINNER_PATH, P2_ID, P2_LOSER_PATH, P2_WINNER_PATH, WINDOW_HEIGHT, WINDOW_WIDTH
from views.MainMenu import MainView
from views.Scoreboard import ScoreboardView


class GameOver(arcade.View):
    
    def __init__(self, p1_score, p2_score):
        super().__init__()
        self.p1_score = p1_score
        self.p2_score = p2_score
        
        self.p1_sprite = None
        self.p2_sprite = None
        
        self.scoreboard_view = ScoreboardView()
        
    def setup(self):        
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        
        # Create a button and add it to the UI manager
        button = arcade.gui.UIFlatButton(text="Show Scoreboard", width=200)
        self.ui_manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="bottom",
            child=button)
        )

        # Assign the button's on_click method
        button.on_click = self.show_scoreboard
        
    
    def determine_winner(self, p1_score, p2_score):
        if p1_score > p2_score:
            return P1_ID
        elif p2_score > p1_score:
            return P2_ID
        else:
            return "tie"
    
    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        # self.fondo = arcade.load_texture(GAME_OVER_BG_PATH, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH - (DIALOG_OVERLAY_WINDOW_MARGIN_X // 2), WINDOW_HEIGHT - (DIALOG_OVERLAY_WINDOW_MARGIN_Y // 2))
        self.fondo = arcade.load_texture(GAME_OVER_BG_PATH)

        winner = self.determine_winner(self.p1_score, self.p2_score)
        
        if winner == P1_ID:
            self.p1_sprite = arcade.Sprite(P1_WINNER_PATH, scale=0.5)
            self.p2_sprite = arcade.Sprite(P2_LOSER_PATH, scale=0.5)
        elif winner == P2_ID:
            self.p1_sprite = arcade.Sprite(P1_LOSER_PATH, scale=0.5)
            self.p2_sprite = arcade.Sprite(P2_WINNER_PATH, scale=0.5)
        else:  # Tie
            self.p1_sprite = arcade.Sprite(P1_WINNER_PATH, scale=0.5)
            self.p2_sprite = arcade.Sprite(P2_WINNER_PATH, scale=0.5)

        # Position the sprites (adjust as needed)
        self.p1_sprite.center_x = WINDOW_WIDTH // 4
        self.p1_sprite.center_y = WINDOW_HEIGHT // 2
        self.p2_sprite.center_x = 3 * WINDOW_WIDTH // 4
        self.p2_sprite.center_y = WINDOW_HEIGHT // 2

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT, self.fondo)
                 
        if self.p1_sprite:
            self.p1_sprite.draw()
        if self.p2_sprite:
            self.p2_sprite.draw()
            
        self.ui_manager.draw()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())
            
    def show_scoreboard(self, event):
        # Switch to the scoreboard view
        self.window.show_view(self.scoreboard_view)

