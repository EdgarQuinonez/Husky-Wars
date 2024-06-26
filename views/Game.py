from datetime import datetime
import time
import arcade, random, math
from database.ConexionDB import ConexionBD
from scripts.enemy import Aspersor, Frisbee
from setup import ASPERSOR_ID_PREFIX, ASPERSOR_PROJECTILE_SPEED, ASPERSOR_SCALING, ASPERSOR_SPRITE_PATH, BAD_COLLECTIBLE_RARE_DROP_RATE, BAD_COLLECTIBLE_RARE_PATH, BAD_COLLECTIBLE_RARE_POINTS, BAD_COLLECTIBLE_UNCOMMON_DROP_RATE, BAD_COLLECTIBLE_UNCOMMON_PATH, BAD_COLLECTIBLE_UNCOMMON_POINTS, COLLECTIBLE_HARD_RESET_COOLDOWN, COLLECTIBLE_SOUND_PATH, COLLECTIBLE_SPAWN_COOLDOWN, COUNTDOWN_BG_SCALE, COUNTDOWN_BG_X, COUNTDOWN_BG_Y, COUNTDOWN_DECORATION_HARD, COUNTDOWN_DECORATION_REGULAR, COUNTDOWN_TEXT_COLOR, COUNTDOWN_TEXT_PIXEL_SIZE, COUNTDOWN_TEXT_X, COUNTDOWN_TEXT_Y, DIFFICULTY_HARD, DIFFICULTY_REGULAR, FALLING_SOUND_PATH, FRISBEE_ID_PREFIX, FRISBEE_SCALING, FRISBEE_SPEED, FRISBEE_SPRITE_PATH, GAME_OVER_SOUND_PATH, GAME_STATE_GAME_OVER, GAME_STATE_GAMEPLAY, GAME_STATE_START_MATCH_COUNTDOWN, GOOD_COLLECTIBLE_RARE_DROP_RATE, GOOD_COLLECTIBLE_RARE_PATH, GOOD_COLLECTIBLE_RARE_POINTS, GOOD_COLLECTIBLE_UNCOMMON_DROP_RATE, GOOD_COLLECTIBLE_UNCOMMON_PATH, GOOD_COLLECTIBLE_UNCOMMON_POINTS, HURT_SOUND_PATH, JUMP_SOUND_PATH, LAYER_NAME_BACKGROUND, LAYER_NAME_METABACKGROUND, LETTERBOX_HEIGHT, OBJECT_ENEMY_ATTR, OBJECT_NAME_COLLECTIBLES, OBJECT_NAME_ENEMY_SPAWN, OBJECT_NAME_PLAYER_SPAWN, OBJECT_NAME_POWER_UP, OBJECT_NAME_PROJECTILE, OBJECT_NAME_TRAILS, P1_ID, P1_SCORE_SPRITE_PATH, P1_SCORE_SPRITE_X, P1_SCORE_SPRITE_Y, P2_ID, P2_SCORE_SPRITE_PATH, P2_SCORE_SPRITE_X, P2_SCORE_SPRITE_Y, POWER_UP_COOLDOWN, POWER_UP_DROP_RATE, POWER_UP_PATH, POWER_UP_POINTS, POWER_UP_SOUND_PATH, POWER_UP_TIME_INCREASE, PROJECTILE_SOUND_PATH, SKY_COLOR, START_COUNTDOWN_ANIMATION_PATH, TITLE_GAMEOVER_PATH, WINDOW_WIDTH, WINDOW_HEIGHT, SCREEN_TITLE, START_MATCH_COUNTDOWN_VALUE, TILE_SCALING, P1_STILL_PATH, P2_STILL_PATH, P1_SPEED, P2_SPEED, P1_KEYBINDINGS, P2_KEYBINDINGS, P1_JUMP_SPEED, P2_JUMP_SPEED, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_COMMON_PATH, P1_SCORE_X, P1_SCORE_Y, P2_SCORE_X, P2_SCORE_Y, GOOD_COLLECTIBLE_COMMON_POINTS, BAD_COLLECTIBLE_COMMON_POINTS, BAD_COLLECTIBLE_COMMON_PATH, GOOD_COLLECTIBLE_COMMON_DROP_RATE, BAD_COLLECTIBLE_COMMON_DROP_RATE, LAYER_NAME_PLATFORMS, RIGHT_FACING, LEFT_FACING, P1_ANIMATIONS_PATH, P2_ANIMATIONS_PATH, TILE_MAP_PATH, WATER_SOUND_PATH
from scripts.player import Player
from scripts.collectible import Coin, Trap, Powerup
from scripts.countdown import Countdown
from views.GameOver import GameOver

class MyGame(arcade.View):
    def __init__(self, player1_name, player2_name):
        super().__init__()
        
        self.player1_name = player1_name
        self.player2_name = player2_name
        
        self.tile_map = None
        self.collectible_layer = None
        self.scene = None
        self.p1_sprite = None
        self.p2_sprite = None
        self.game_over_text_sprite = None
        self.game_over_sound = None 
        self.countdown = None
        self.countdown_text = None
        self.start_countdown = None
        self.start_countdown_text = None
        self.time_since_power_up_spawn = None
        self.time_since_collectibles_refresh = None
        self.time_since_collectibles_hard_reset = None
        self.collectible_hard_reset_needed = False
        self.collectible_refresh_needed = False
        self.GAME_DIFFICULTY = None
        self.GAME_STATE = None        
        
        self.db = ConexionBD()
        
        self.collectible_sound = arcade.load_sound(COLLECTIBLE_SOUND_PATH)
        self.power_up_sound = arcade.load_sound(POWER_UP_SOUND_PATH)
        self.jump_sound = arcade.load_sound(JUMP_SOUND_PATH)
        self.falling_sound = arcade.load_sound(FALLING_SOUND_PATH)
        self.water_sound = arcade.load_sound(WATER_SOUND_PATH)
        self.projectile_sound = arcade.load_sound(PROJECTILE_SOUND_PATH)
        self.hurt_sound = arcade.load_sound(HURT_SOUND_PATH)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self, difficulty):
        """Set up the game here. Call this function to restart the game."""
        
        self.scene = arcade.Scene()   
        self.game_over_text_sprite = arcade.Sprite(TITLE_GAMEOVER_PATH, 1)
        self.game_over_sound = arcade.load_sound(GAME_OVER_SOUND_PATH)
                   
        self.time_since_power_up_spawn = 0
        self.time_since_collectibles_refresh = COLLECTIBLE_SPAWN_COOLDOWN
        self.time_since_collectibles_hard_reset = COLLECTIBLE_HARD_RESET_COOLDOWN
        
        map_name = TILE_MAP_PATH
        
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            OBJECT_NAME_COLLECTIBLES: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_BACKGROUND: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_METABACKGROUND: {
                "use_spatial_hash": True,
            },
            OBJECT_NAME_PLAYER_SPAWN: {
                "use_spatial_hash": True,
            },
            OBJECT_NAME_ENEMY_SPAWN: {
                "use_spatial_hash": True,
            },
            OBJECT_NAME_PROJECTILE: {
                "use_spatial_hash": False,
            }
        }

        
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.collectible_layer = self.tile_map.object_lists[OBJECT_NAME_COLLECTIBLES]         
        self.player_spawn_objs = self.tile_map.object_lists[OBJECT_NAME_PLAYER_SPAWN]
        self.enemy_spawn_objs = self.tile_map.object_lists[OBJECT_NAME_ENEMY_SPAWN]
        self.power_up_spawn_objs = self.tile_map.object_lists[OBJECT_NAME_POWER_UP]
        self.trails_objs = self.tile_map.object_lists[OBJECT_NAME_TRAILS]                

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        # self.center_tile_map()
        
        platforms_layer = self.scene[LAYER_NAME_PLATFORMS]
        p1_spawn = self.get_player_spawn_point(P1_ID)
        p2_spawn = self.get_player_spawn_point(P2_ID)
                
        self.p1_sprite = Player(P1_STILL_PATH)
        self.p2_sprite = Player(P2_STILL_PATH)
        
        self.p1_sprite.setup(platforms_layer, self.jump_sound, (P1_SCORE_X, P1_SCORE_Y), RIGHT_FACING, P1_ANIMATIONS_PATH, 0, self.player1_name, P1_JUMP_SPEED, P1_SPEED, P1_KEYBINDINGS, p1_spawn, self.hurt_sound, self.falling_sound, P1_SCORE_SPRITE_PATH, (P1_SCORE_SPRITE_X, P1_SCORE_SPRITE_Y))        
        self.p2_sprite.setup(platforms_layer, self.jump_sound, (P2_SCORE_X, P2_SCORE_Y), LEFT_FACING, P2_ANIMATIONS_PATH, 0, self.player2_name, P2_JUMP_SPEED, P2_SPEED, P2_KEYBINDINGS, p2_spawn, self.hurt_sound, self.falling_sound, P2_SCORE_SPRITE_PATH, (P2_SCORE_SPRITE_X, P2_SCORE_SPRITE_Y))        
        
        self.scene.add_sprite(OBJECT_NAME_PLAYER_SPAWN, self.p1_sprite)                        
        self.scene.add_sprite(OBJECT_NAME_PLAYER_SPAWN, self.p2_sprite)
                
        # Generate random collectibles function call
        self.collectible_list = arcade.SpriteList()
        self.power_up_list = arcade.SpriteList()
        
        self.scene.add_sprite_list(OBJECT_NAME_COLLECTIBLES, self.collectible_list)
        self.scene.add_sprite_list(OBJECT_NAME_POWER_UP, self.power_up_list)
        self.generate_collectibles()                          
                
        
        self.GAME_DIFFICULTY = difficulty
        
        self.setup_countdown_gui()      
        
        self.GAME_STATE = GAME_STATE_START_MATCH_COUNTDOWN              
        self.start_countdown = Countdown(START_MATCH_COUNTDOWN_VALUE)
        self.start_countdown_text = str(START_MATCH_COUNTDOWN_VALUE)
        self.start_countdown.start()

        # Enemies setup
        self.aspersores_ids = [obj.properties[OBJECT_ENEMY_ATTR] for obj in self.enemy_spawn_objs if obj.properties[OBJECT_ENEMY_ATTR][:len(ASPERSOR_ID_PREFIX)] == ASPERSOR_ID_PREFIX]
        self.fribees_ids = [obj.properties[OBJECT_ENEMY_ATTR] for obj in self.enemy_spawn_objs if obj.properties[OBJECT_ENEMY_ATTR][:len(FRISBEE_ID_PREFIX)] == FRISBEE_ID_PREFIX]
        
        self.aspersores_objs = {}
        self.frisbees_objs = {}
        
        # Set up aspersores        
        for aspersor_id in self.aspersores_ids:            
            self.aspersores_objs[aspersor_id] = Aspersor(ASPERSOR_SPRITE_PATH, ASPERSOR_SCALING, self.get_enemy_spawn_point(aspersor_id),  ASPERSOR_PROJECTILE_SPEED)                                    
            self.aspersores_objs[aspersor_id].setup(self.scene, self.water_sound)                        
            
        for frisbee_id in self.fribees_ids:
            self.frisbees_objs[frisbee_id] = Frisbee(FRISBEE_SPRITE_PATH, FRISBEE_SCALING, self.get_enemy_spawn_point(frisbee_id), FRISBEE_SPEED, self.get_frisbee_trail(frisbee_id), frisbee_id)
            self.frisbees_objs[frisbee_id].setup(self.scene, self.water_sound, self.projectile_sound)
    
    def setup_countdown_gui(self):
        self.countdown_bg = None
        if self.GAME_DIFFICULTY == DIFFICULTY_HARD:
            self.countdown_bg = arcade.Sprite(COUNTDOWN_DECORATION_HARD, COUNTDOWN_BG_SCALE)
        elif self.GAME_DIFFICULTY == DIFFICULTY_REGULAR:
            self.countdown_bg = arcade.Sprite(COUNTDOWN_DECORATION_REGULAR, COUNTDOWN_BG_SCALE)
            
        self.countdown_bg.center_x = COUNTDOWN_BG_X
        self.countdown_bg.center_y = COUNTDOWN_BG_Y
        
        self.countdown_text = "01:00"        

                    
    def get_player_spawn_point(self, player_id):                
        for spawn in self.player_spawn_objs:
            if spawn.properties["player_id"] == player_id:
                cartesian = self.tile_map.get_cartesian(spawn.shape[0], spawn.shape[1])
                center_x = math.floor(
                        cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                    )
                center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                )
                
                return (center_x, center_y)                
                    
    def generate_collectibles(self, delta_time: float = 1/160):
        # Define possible collectible types
        collectible_types = ["Coin", "Trap"]
        # Time tracking for collectibles and power-ups
        self.time_since_collectibles_refresh += delta_time
        self.time_since_collectibles_hard_reset += delta_time
        
        # Collectible hard reset
        if self.time_since_collectibles_hard_reset >= COLLECTIBLE_HARD_RESET_COOLDOWN and self.collectible_refresh_needed == False:
            self.time_since_collectibles_hard_reset = 0  # Reset the timer
            # Remove all existing collectibles from the scene and list
            for collectible in self.collectible_list:
                collectible.remove_from_sprite_lists()
            self.collectible_list = []  # Clear the list
            
            self.collectible_hard_reset_needed = True  # Flag that a hard reset is needed
            
        # Collectible refresh (only if enough time has passed since the last refresh)
        elif self.time_since_collectibles_refresh >= COLLECTIBLE_SPAWN_COOLDOWN and self.collectible_hard_reset_needed == False:
            self.time_since_collectibles_refresh = 0  # Reset the timer
            
            self.collectible_refresh_needed = True  # Flag that a refresh is needed
            
        # Iterate over spawn points and create collectibles
        if self.collectible_refresh_needed or self.collectible_hard_reset_needed:
            for collectible_object in self.collectible_layer:
                    cartesian = self.tile_map.get_cartesian(
                        collectible_object.shape[0], collectible_object.shape[1]
                    )            
                    collectible = None                        
                    # Check for existing collectibles at this position
                    existing_collectible = None
            

                    # If no existing collectible found, spawn a new one
                    for sprite in self.collectible_list:
                        if sprite.center_x == math.floor(
                            cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                        ) and sprite.center_y == math.floor(
                            (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                        ):
                            existing_collectible = sprite
                            break
                        
                    if existing_collectible is None: 
                            
                        collectible_type = random.choice(collectible_types)  # Randomly choose the type
                        
                        if collectible_type == "Coin":
                            
                            if random.random() < GOOD_COLLECTIBLE_RARE_DROP_RATE:
                                collectible = Coin(GOOD_COLLECTIBLE_RARE_PATH, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_RARE_POINTS)
                            elif random.random() < GOOD_COLLECTIBLE_UNCOMMON_DROP_RATE:
                                collectible = Coin(GOOD_COLLECTIBLE_UNCOMMON_PATH, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_UNCOMMON_POINTS)
                            elif random.random() <= GOOD_COLLECTIBLE_COMMON_DROP_RATE:
                                collectible = Coin(GOOD_COLLECTIBLE_COMMON_PATH, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_COMMON_POINTS)
                                
                            
                            
                                
                        elif collectible_type == "Trap":
                        
                            if random.random() < BAD_COLLECTIBLE_RARE_DROP_RATE:
                                collectible = Trap(BAD_COLLECTIBLE_RARE_PATH, COLLECTIBLE_SCALING, BAD_COLLECTIBLE_RARE_POINTS)
                            elif random.random() < BAD_COLLECTIBLE_UNCOMMON_DROP_RATE:
                                collectible = Trap(BAD_COLLECTIBLE_UNCOMMON_PATH, COLLECTIBLE_SCALING, BAD_COLLECTIBLE_UNCOMMON_POINTS)
                            elif random.random() <= BAD_COLLECTIBLE_COMMON_DROP_RATE:
                                collectible = Trap(BAD_COLLECTIBLE_COMMON_PATH, COLLECTIBLE_SCALING, BAD_COLLECTIBLE_COMMON_POINTS)
                            

                                                                        
                        # Only add to the lists if a collectible was created
                        if collectible is not None:  
                            collectible.center_x = math.floor(
                                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                            )
                            collectible.center_y = math.floor(
                                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                            )
                            
                            if collectible_type == "Coin":
                                collectible.setup(self.collectible_sound)
                            elif collectible_type == "Trap":
                                collectible.setup(self.hurt_sound)
            
                            self.collectible_list.append(collectible)
                            self.scene.add_sprite(OBJECT_NAME_COLLECTIBLES, collectible) # Creating new layer with collectibles and adding each sprite.
            self.collectible_refresh_needed = False  # Reset the flag
            self.collectible_hard_reset_needed = False  # Reset the flag        
        
        for power_up_object in self.power_up_spawn_objs:
            cartesian = self.tile_map.get_cartesian(
                power_up_object.shape[0], power_up_object.shape[1]
            )
            power_up = None                        
            # Check for existing power_ups at this position
            existing_power_up = None    

            # If no existing power_up found, spawn a new one
            for sprite in self.power_up_list:
                if sprite.center_x == math.floor(
                    cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                ) and sprite.center_y == math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                ):
                    existing_power_up = sprite
                    break
                               
            if existing_power_up is None:
                self.time_since_power_up_spawn += delta_time                
                if random.random() <= POWER_UP_DROP_RATE and self.time_since_power_up_spawn >= POWER_UP_COOLDOWN:
                    self.time_since_power_up_spawn = 0
                    power_up = Powerup(POWER_UP_PATH, COLLECTIBLE_SCALING, POWER_UP_POINTS, POWER_UP_TIME_INCREASE)
                    power_up.center_x = math.floor(
                        cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                    )
                    power_up.center_y = math.floor(
                        (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                    )
                    power_up.setup(self.power_up_sound)
                    self.power_up_list.append(power_up)
                    self.scene.add_sprite(OBJECT_NAME_POWER_UP, power_up)
                                    
    def get_enemy_spawn_point(self, enemy_id):        
        for spawn in self.enemy_spawn_objs:            
            if spawn.properties["enemy_id"] == enemy_id:
                cartesian = self.tile_map.get_cartesian(spawn.shape[0], spawn.shape[1])
                center_x = math.floor(
                        cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                    )
                center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                )
                
                return (center_x, center_y)
            
    def get_frisbee_trail(self, frisbee_id):
        for trail in self.trails_objs:
            if trail.properties["id"] == frisbee_id:
                cartesian_trail = []
                for point in trail.shape:
                    cartesian = self.tile_map.get_cartesian(point[0], point[1])
                    center_x = math.floor(
                        cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                    )
                    center_y = math.floor(
                        (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                    )
                    cartesian_trail.append((center_x, center_y))
                return cartesian_trail
                
        return None
    
    def spawn_enemies(self, delta_time):
        for aspersor in self.aspersores_objs.values():            
            aspersor.update(delta_time)
            
        for frisbee in self.frisbees_objs.values():
            frisbee.update(delta_time)
                                                                                                           
    def on_draw(self):                        
        self.window.background_color = SKY_COLOR                                
        self.clear()
                
        scale_x = self.window.width / WINDOW_WIDTH
        scale_y = self.window.height / WINDOW_HEIGHT
        
        arcade.set_viewport(0, self.window.width / scale_x, 0, self.window.height / scale_y)
            
        self.scene.draw()
        self.countdown_bg.draw()        
        self.p1_sprite.draw_gui()
        self.p2_sprite.draw_gui()
        
        arcade.draw_text(
            self.countdown_text,
            COUNTDOWN_TEXT_X,
            COUNTDOWN_TEXT_Y,
            COUNTDOWN_TEXT_COLOR,
            COUNTDOWN_TEXT_PIXEL_SIZE,
            anchor_x="center",
            bold=True,
        )
        
        if self.GAME_STATE == GAME_STATE_START_MATCH_COUNTDOWN:
            countdown_number_sprites = []  

            for i in range(3, 0, -1):
                texture = arcade.load_texture(f"{START_COUNTDOWN_ANIMATION_PATH}/{i}.png")
                sprite = arcade.Sprite(scale=0.5)  
                sprite.texture = texture  
                countdown_number_sprites.append(sprite)

            remaining_time = self.start_countdown.remaining_time
            countdown_index = 3 - int(remaining_time)
            if 0 <= countdown_index < len(countdown_number_sprites):  
                current_sprite = countdown_number_sprites[countdown_index]

                current_sprite.center_x = WINDOW_WIDTH // 2
                current_sprite.center_y = WINDOW_HEIGHT // 2
                current_sprite.draw()
                    
                                                              
    def on_key_press(self, key, modifiers):
        self.p1_sprite.on_key_press(key, modifiers)
        self.p2_sprite.on_key_press(key, modifiers)
                            
    def on_key_release(self, key, modifiers):
        self.p1_sprite.on_key_release(key, modifiers)
        self.p2_sprite.on_key_release(key, modifiers)
    
    def on_game_over(self):        
        if self.GAME_STATE == GAME_STATE_GAME_OVER:
            arcade.play_sound(self.game_over_sound)            
            self.db.add_match_score(self.p1_sprite.name, self.GAME_DIFFICULTY, self.countdown.get_complete_match_duration(), self.p1_sprite.score, datetime.now())
            self.db.add_match_score(self.p2_sprite.name, self.GAME_DIFFICULTY, self.countdown.get_complete_match_duration(), self.p2_sprite.score, datetime.now())                                                                         
            self.game_over_view = GameOver(self.p1_sprite.score, self.p2_sprite.score, self.player1_name, self.player2_name, self.GAME_DIFFICULTY)
            self.window.show_view(self.game_over_view)
            
    def on_update(self, delta_time: float):        
        if self.GAME_STATE == GAME_STATE_START_MATCH_COUNTDOWN:
            self.start_countdown_text = str(self.start_countdown.remaining_time)
            if self.start_countdown.remaining_time <= 0:
                self.start_countdown.stop()
                self.GAME_STATE = GAME_STATE_GAMEPLAY
                self.countdown = Countdown()
                self.countdown.start()
                self.start_countdown_text = ""
            else:
                return  # Skip game updates during countdown
        
        if self.GAME_STATE == GAME_STATE_GAMEPLAY:   
            self.p1_sprite.update()
            self.p2_sprite.update()
            
            self.generate_collectibles(delta_time)
                                    
            # Separate collision checks
            player1_coin_hit_list = arcade.check_for_collision_with_list(self.p1_sprite, self.scene[OBJECT_NAME_COLLECTIBLES])
            player2_coin_hit_list = arcade.check_for_collision_with_list(self.p2_sprite, self.scene[OBJECT_NAME_COLLECTIBLES])
            
            p1_power_up_hit_list = arcade.check_for_collision_with_list(self.p1_sprite, self.scene[OBJECT_NAME_POWER_UP])
            p2_power_up_hit_list = arcade.check_for_collision_with_list(self.p2_sprite, self.scene[OBJECT_NAME_POWER_UP])

            for coin in player1_coin_hit_list:
                coin.collect(self.p1_sprite)  # Update only Player 1's score
                coin.update()

            for coin in player2_coin_hit_list:
                coin.collect(self.p2_sprite)  # Update only Player 2's score
                coin.update()
                
            for power_up in p1_power_up_hit_list:
                power_up.collect(self.p1_sprite, self.countdown)
                power_up.update()
                
            for power_up in p2_power_up_hit_list:
                power_up.collect(self.p2_sprite, self.countdown)
                power_up.update()
                
                
            if self.GAME_DIFFICULTY == DIFFICULTY_HARD:
                self.spawn_enemies(delta_time)
            
            # Countdown Check and Match Reset
            self.countdown_text = f"{self.countdown.remaining_time_string}"
            # Game Over
            if self.countdown.remaining_time <= 0:                
                self.GAME_STATE = GAME_STATE_GAME_OVER                                                                                               
                self.on_game_over()
                self.countdown.stop()
                