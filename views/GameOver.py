import arcade
import arcade.gui

from setup import DIALOG_OVERLAY_WINDOW_MARGIN_X, DIALOG_OVERLAY_WINDOW_MARGIN_Y, GAME_OVER_BG_PATH, P1_ID, P1_LOSER_PATH, P1_WINNER_PATH, P2_ID, P2_LOSER_PATH, P2_WINNER_PATH, WINDOW_HEIGHT, WINDOW_WIDTH, TITLE_GAMEOVER_PATH, MENU_BUTTON_PATH, MENU_HOVER_BUTTON_PATH, RESTART_BUTTON_PATH, RESTART_HOVER_BUTTON_PATH, SCOREBOARD_BUTTON_PATH, SCOREBOARD_HOVER_BUTTON_PATH
from views.MainMenu import MainView
from views.Scoreboard import ScoreboardView
from components.button import Button


class GameOver(arcade.View):
    
    def __init__(self, p1_score, p2_score):
        super().__init__()
        self.p1_score = p1_score
        self.p2_score = p2_score
        
        self.p1_sprite = None
        self.p2_sprite = None
        
        self.scoreboard_view = ScoreboardView()

        self.buttons = []
        self.selected_button_index = 0
        
    def setup(self):        
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        
    
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

        self.title_image = arcade.load_texture(TITLE_GAMEOVER_PATH)

        # Buttons
        scale = 0.3
        self.buttons.append(
            Button(MENU_BUTTON_PATH, MENU_HOVER_BUTTON_PATH, WINDOW_WIDTH // 5,
                   WINDOW_HEIGHT // 8, self.menu, scale=scale))
        self.buttons.append(
            Button(RESTART_BUTTON_PATH, RESTART_HOVER_BUTTON_PATH, WINDOW_WIDTH // 2,
                   WINDOW_HEIGHT // 8, self.restart, scale=scale))
        self.buttons.append(
            Button(SCOREBOARD_BUTTON_PATH, SCOREBOARD_HOVER_BUTTON_PATH, WINDOW_WIDTH - 300,
                   WINDOW_HEIGHT // 8, self.show_scoreboard, scale=scale))



    def on_draw(self):
        arcade.start_render()

        # Calculate scaling factors to fit the content to the viewport
        scale_x = self.window.width / WINDOW_WIDTH
        scale_y = self.window.height / WINDOW_HEIGHT

        # Apply the scaling factors and set the viewport to cover the entire window
        # Apply scaling using set_viewport
        arcade.set_viewport(0, self.window.width / scale_x, 0, self.window.height / scale_y)

        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT, self.fondo)
                 
        title_image_x = WINDOW_WIDTH // 2
        title_image_y = WINDOW_HEIGHT - 100
        title_image_scale = 0.6  # You might need to adjust this if your title is too large
        arcade.draw_scaled_texture_rectangle(title_image_x, title_image_y, self.title_image, title_image_scale)
        for button in self.buttons:
            button.draw()

        if self.p1_sprite:
            self.p1_sprite.draw()
        if self.p2_sprite:
            self.p2_sprite.draw()
            
        self.ui_manager.draw()


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
            
    def show_scoreboard(self):
        # Switch to the scoreboard view
        self.window.show_view(self.scoreboard_view)

    def menu(self):
        self.window.show_view(MainView())

    def restart(self):
        pass
