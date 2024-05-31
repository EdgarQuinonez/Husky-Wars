import arcade

from setup import MENU_SOUNDTRACK_PATH


class Settings:
    __instance = None 

    def __init__(self):
        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:            
            Settings.__instance = self   

            self.music = arcade.load_sound(MENU_SOUNDTRACK_PATH)
            self.music_played = False
            if not self.music_played:
                self.music_player = self.music.play(volume=0.5, loop=True)           
                self.music_played = True                
            self.music_is_playing = True          

    @staticmethod
    def get_instance():
        if Settings.__instance is None:
            Settings()
        return Settings.__instance

    def toggle_music(self):
        
        if self.music_is_playing:
            self.music_player.pause()
            self.music_is_playing = False
        else:
            self.music_player.play()
            self.music_is_playing = True