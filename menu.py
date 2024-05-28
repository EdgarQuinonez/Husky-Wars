import arcade
from time import sleep
import arcade, random, math
from database.ConexionDB import ConexionBD
from scripts.enemy import Aspersor, Frisbee
from setup import ASPECT_RATIO, ASPERSOR_ID_PREFIX, ASPERSOR_PROJECTILE_SPEED, ASPERSOR_SCALING, ASPERSOR_SPRITE_PATH, BAD_COLLECTIBLE_RARE_DROP_RATE, BAD_COLLECTIBLE_RARE_PATH, BAD_COLLECTIBLE_RARE_POINTS, BAD_COLLECTIBLE_UNCOMMON_DROP_RATE, BAD_COLLECTIBLE_UNCOMMON_PATH, BAD_COLLECTIBLE_UNCOMMON_POINTS, COLLECTIBLE_HARD_RESET_COOLDOWN, COLLECTIBLE_SOUND_PATH, COLLECTIBLE_SPAWN_COOLDOWN, FALLING_SOUND_PATH, FRISBEE_ID_PREFIX, FRISBEE_SCALING, FRISBEE_SPEED, FRISBEE_SPRITE_PATH, GAME_STATE_GAME_OVER, GAME_STATE_GAMEPLAY, GAME_STATE_START_MATCH_COUNTDOWN, GOOD_COLLECTIBLE_RARE_DROP_RATE, GOOD_COLLECTIBLE_RARE_PATH, GOOD_COLLECTIBLE_RARE_POINTS, GOOD_COLLECTIBLE_UNCOMMON_DROP_RATE, GOOD_COLLECTIBLE_UNCOMMON_PATH, GOOD_COLLECTIBLE_UNCOMMON_POINTS, HURT_SOUND_PATH, JUMP_SOUND_PATH, LAYER_NAME_BACKGROUND, LAYER_NAME_METABACKGROUND, OBJECT_ENEMY_ATTR, OBJECT_NAME_COLLECTIBLES, OBJECT_NAME_ENEMY_SPAWN, OBJECT_NAME_PLAYER_SPAWN, OBJECT_NAME_POWER_UP, OBJECT_NAME_PROJECTILE, OBJECT_NAME_TRAILS, P1_ID, P2_ID, POWER_UP_COOLDOWN, POWER_UP_DROP_RATE, POWER_UP_PATH, POWER_UP_POINTS, POWER_UP_SOUND_PATH, POWER_UP_TIME_INCREASE, PROJECTILE_SOUND_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, START_MATCH_COUNTDOWN_VALUE, TILE_SCALING, P1_STILL_PATH, P2_STILL_PATH, P1_SPEED, P2_SPEED, P1_KEYBINDINGS, P2_KEYBINDINGS, P1_JUMP_SPEED, P2_JUMP_SPEED, COLLECTIBLE_SCALING, GOOD_COLLECTIBLE_COMMON_PATH, P1_SCORE_X, P1_SCORE_Y, P2_SCORE_X, P2_SCORE_Y, GOOD_COLLECTIBLE_COMMON_POINTS, BAD_COLLECTIBLE_COMMON_POINTS, BAD_COLLECTIBLE_COMMON_PATH, GOOD_COLLECTIBLE_COMMON_DROP_RATE, BAD_COLLECTIBLE_COMMON_DROP_RATE, LAYER_NAME_PLATFORMS, RIGHT_FACING, LEFT_FACING, P1_ANIMATIONS_PATH, P2_ANIMATIONS_PATH, TILE_MAP_PATH, WATER_SOUND_PATH
from scripts.player import Player
from scripts.collectible import Coin, Trap, Powerup
from scripts.countdown import Countdown

# Tamaño de la ventana
SCREEN_WIDTH, _ = arcade.window_commands.get_display_size()
SCREEN_HEIGHT = round(SCREEN_WIDTH * ASPECT_RATIO)

SCREEN_TITLE = "¡Husky Wars!"


class Button:
    def __init__(self, image_path, hover_image_path, x, y, action, scale = 1.0):
        self.image = arcade.load_texture(image_path)
        self.hover_image = arcade.load_texture(hover_image_path)
        self.current_image = self.image
        self.x = x
        self.y = y
        self.action = action
        self.scale = scale
        self.width = self.image.width * self.scale
        self.height = self.image.height * self.scale

    def draw(self):
        # Draw the image with a tint if hovered or selected
        arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.current_image)

    def check_mouse_hover(self, x, y):
        if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y < self.y + self.height / 2:
            self.current_image = self.hover_image
            return True
        else:
            self.current_image = self.image
            return False

    def select(self):
        self.current_image = self.hover_image

    def deselect(self):
        self.current_image = self.image


class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_view = None
        self.background = None
        self.buttons = []
        self.selected_button_index = 0  # Índice del botón seleccionado
        self.max_button_width = 0  # Ancho máximo de los botones

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        # Cargar la imagen de fondo
        self.background = arcade.load_texture("background_menu.png")
        # Cargar la imagen del título
        self.title_image = arcade.load_texture("assets/buttons/title.png")
        # Crear botones de menú
        scale = 0.5
        self.buttons.append(Button("assets/buttons/jugar.png", "assets/buttons/jugar_hover.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 500, self.on_click_play, scale=scale))
        self.buttons.append(Button("assets/buttons/opciones.png", "assets/buttons/opciones_hover.png", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 650, self.on_click_options, scale=scale))
        self.buttons.append(Button("assets/buttons/como.png", "assets/buttons/como_hover.png",SCREEN_WIDTH // 2, SCREEN_HEIGHT - 800, self.on_click_how_to_play, scale=scale))
        self.buttons.append(Button("assets/buttons/salir.png", "assets/buttons/salir_hover.png",SCREEN_WIDTH // 2, SCREEN_HEIGHT - 950, self.on_click_exit, scale=scale))
        # Calcular el ancho máximo de los botones
        self.max_button_width = max(button.width for button in self.buttons)
        # Establecer el ancho de todos los botones con el ancho máximo
        for button in self.buttons:
            button.width = self.max_button_width
        # Seleccionar el primer botón
        self.buttons[self.selected_button_index].select()
        # Reproducir música de fondo
        #soundtrack = arcade.Sound("menu_soundtrack.mp3", streaming=True)
        #soundtrack.play(volume=0.5, loop=True)
        self.click_sound = arcade.Sound("Button.mp3")

    def on_draw(self):
        arcade.start_render()
        # Dibujar la imagen de fondo

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        # Dibujar la imagen del título
        title_image_x = SCREEN_WIDTH // 2
        title_image_y = SCREEN_HEIGHT - 200
        title_image_scale = 1  # Ajusta la escala de la imagen del título si es necesario
        arcade.draw_scaled_texture_rectangle(title_image_x, title_image_y, self.title_image, title_image_scale)
        # Dibujar los botones
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
                self.buttons[self.selected_button_index].deselect()  # Deseleccionar el botón actual
                self.selected_button_index = index
                self.buttons[self.selected_button_index].select()  # Seleccionar el nuevo botón
                button.action()

    def on_click_play(self):
        self.click_sound.play()
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)

    def on_click_options(self):
        self.option_view = OptionView()  # Cambia a la vista del menú
        self.window.show_view(self.option_view)
        self.click_sound.play()

    def on_click_how_to_play(self):
        self.hplay_view = HowPlayView()  # Cambia a la vista del menú
        self.window.show_view(self.hplay_view)
        self.click_sound.play()

    def on_click_exit(self):
        arcade.close_window()

    def close(self):
        # Liberar recursos o realizar cualquier limpieza necesaria
        # Por ejemplo, puedes cerrar conexiones a bases de datos, liberar texturas cargadas, etc.

        # Cerrar la ventana actual
        arcade.close_window()

class OptionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Opciones", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50,
                         arcade.color.WHITE, font_size=24, anchor_x="center")
        # No necesitamos dibujar botones aquí, eso lo maneja la vista principal

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())

class HowPlayView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        # Cargar la imagen de fondo
        self.howplay = arcade.load_texture("assets/buttons/how_play.jpg")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.howplay)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MainView())


class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()  # Inicializar arcade.View sin parámetros
        self.window = arcade.get_window()  # Obtener la ventana actual

        self.tile_map = None
        self.collectible_layer = None
        self.scene = None
        self.p1_sprite = None
        self.p2_sprite = None
        self.countdown = None
        self.countdown_text = None
        self.start_countdown = None
        self.start_countdown_text = None
        self.time_since_power_up_spawn = None
        self.time_since_collectibles_refresh = None
        self.time_since_collectibles_hard_reset = None
        self.collectible_hard_reset_needed = False
        self.collectible_refresh_needed = False
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

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        self.scene = arcade.Scene()
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

        platforms_layer = self.scene[LAYER_NAME_PLATFORMS]
        p1_spawn = self.get_player_spawn_point(P1_ID)
        p2_spawn = self.get_player_spawn_point(P2_ID)

        self.p1_sprite = Player(P1_STILL_PATH)
        self.p2_sprite = Player(P2_STILL_PATH)

        self.p1_sprite.setup(platforms_layer, self.jump_sound, (P1_SCORE_X, P1_SCORE_Y), RIGHT_FACING,
                             P1_ANIMATIONS_PATH, 0, "Player 1", P1_JUMP_SPEED, P1_SPEED, P1_KEYBINDINGS, p1_spawn,
                             self.hurt_sound, self.falling_sound)
        self.p2_sprite.setup(platforms_layer, self.jump_sound, (P2_SCORE_X, P2_SCORE_Y), LEFT_FACING,
                             P2_ANIMATIONS_PATH, 0, "Player 2", P2_JUMP_SPEED, P2_SPEED, P2_KEYBINDINGS, p2_spawn,
                             self.hurt_sound, self.falling_sound)

        self.scene.add_sprite(OBJECT_NAME_PLAYER_SPAWN, self.p1_sprite)
        self.scene.add_sprite(OBJECT_NAME_PLAYER_SPAWN, self.p2_sprite)

        # Generate random collectibles function call
        self.collectible_list = arcade.SpriteList()
        self.power_up_list = arcade.SpriteList()

        self.scene.add_sprite_list(OBJECT_NAME_COLLECTIBLES, self.collectible_list)
        self.scene.add_sprite_list(OBJECT_NAME_POWER_UP, self.power_up_list)
        self.generate_collectibles()

        self.countdown_text = "60"

        self.GAME_STATE = GAME_STATE_START_MATCH_COUNTDOWN
        self.start_countdown = Countdown(START_MATCH_COUNTDOWN_VALUE)
        self.start_countdown_text = str(START_MATCH_COUNTDOWN_VALUE)
        self.start_countdown.start()

        # Enemies setup
        self.aspersores_ids = [obj.properties[OBJECT_ENEMY_ATTR] for obj in self.enemy_spawn_objs if
                               obj.properties[OBJECT_ENEMY_ATTR][:len(ASPERSOR_ID_PREFIX)] == ASPERSOR_ID_PREFIX]
        self.fribees_ids = [obj.properties[OBJECT_ENEMY_ATTR] for obj in self.enemy_spawn_objs if
                            obj.properties[OBJECT_ENEMY_ATTR][:len(FRISBEE_ID_PREFIX)] == FRISBEE_ID_PREFIX]

        self.aspersores_objs = {}
        self.frisbees_objs = {}

        # Set up aspersores
        for aspersor_id in self.aspersores_ids:
            self.aspersores_objs[aspersor_id] = Aspersor(ASPERSOR_SPRITE_PATH, ASPERSOR_SCALING,
                                                         self.get_enemy_spawn_point(aspersor_id),
                                                         ASPERSOR_PROJECTILE_SPEED)
            self.aspersores_objs[aspersor_id].setup(self.scene, self.water_sound)

        for frisbee_id in self.fribees_ids:
            self.frisbees_objs[frisbee_id] = Frisbee(FRISBEE_SPRITE_PATH, FRISBEE_SCALING,
                                                     self.get_enemy_spawn_point(frisbee_id), FRISBEE_SPEED,
                                                     self.get_frisbee_trail(frisbee_id), frisbee_id)
            self.frisbees_objs[frisbee_id].setup(self.scene, self.water_sound, self.projectile_sound)

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

    def generate_collectibles(self, delta_time: float = 1 / 160):
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
                            collectible = Coin(GOOD_COLLECTIBLE_RARE_PATH, COLLECTIBLE_SCALING,
                                               GOOD_COLLECTIBLE_RARE_POINTS)
                        elif random.random() < GOOD_COLLECTIBLE_UNCOMMON_DROP_RATE:
                            collectible = Coin(GOOD_COLLECTIBLE_UNCOMMON_PATH, COLLECTIBLE_SCALING,
                                               GOOD_COLLECTIBLE_UNCOMMON_POINTS)
                        elif random.random() <= GOOD_COLLECTIBLE_COMMON_DROP_RATE:
                            collectible = Coin(GOOD_COLLECTIBLE_COMMON_PATH, COLLECTIBLE_SCALING,
                                               GOOD_COLLECTIBLE_COMMON_POINTS)




                    elif collectible_type == "Trap":

                        if random.random() < BAD_COLLECTIBLE_RARE_DROP_RATE:
                            collectible = Trap(BAD_COLLECTIBLE_RARE_PATH, COLLECTIBLE_SCALING,
                                               BAD_COLLECTIBLE_RARE_POINTS)
                        elif random.random() < BAD_COLLECTIBLE_UNCOMMON_DROP_RATE:
                            collectible = Trap(BAD_COLLECTIBLE_UNCOMMON_PATH, COLLECTIBLE_SCALING,
                                               BAD_COLLECTIBLE_UNCOMMON_POINTS)
                        elif random.random() <= BAD_COLLECTIBLE_COMMON_DROP_RATE:
                            collectible = Trap(BAD_COLLECTIBLE_COMMON_PATH, COLLECTIBLE_SCALING,
                                               BAD_COLLECTIBLE_COMMON_POINTS)

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
                        self.scene.add_sprite(OBJECT_NAME_COLLECTIBLES,
                                              collectible)  # Creating new layer with collectibles and adding each sprite.
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
        """Render the screen."""
        self.clear()

        self.scene.draw()
        self.p1_sprite.draw_gui()
        self.p2_sprite.draw_gui()
        arcade.draw_text(
            self.countdown_text,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 30,
            arcade.csscolor.WHITE,
            30,
            anchor_x="center",
        )

        if self.GAME_STATE == GAME_STATE_START_MATCH_COUNTDOWN:
            arcade.draw_text(
                self.start_countdown_text,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.csscolor.WHITE,
                30,
                anchor_x="center",
            )

    def on_key_press(self, key, modifiers):
        self.p1_sprite.on_key_press(key, modifiers)
        self.p2_sprite.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.p1_sprite.on_key_release(key, modifiers)
        self.p2_sprite.on_key_release(key, modifiers)

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
            player1_coin_hit_list = arcade.check_for_collision_with_list(self.p1_sprite,
                                                                         self.scene[OBJECT_NAME_COLLECTIBLES])
            player2_coin_hit_list = arcade.check_for_collision_with_list(self.p2_sprite,
                                                                         self.scene[OBJECT_NAME_COLLECTIBLES])

            p1_power_up_hit_list = arcade.check_for_collision_with_list(self.p1_sprite,
                                                                        self.scene[OBJECT_NAME_POWER_UP])
            p2_power_up_hit_list = arcade.check_for_collision_with_list(self.p2_sprite,
                                                                        self.scene[OBJECT_NAME_POWER_UP])

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

            self.spawn_enemies(delta_time)

            # Countdown Check and Match Reset
            self.countdown_text = f"{self.countdown.remaining_time}"
            # Game Over
            if self.countdown.remaining_time <= 0:
                # Open game over view (winner/loser total score, scoreboard and play again buttons)
                # self.GAME_STATE = GAME_STATE_GAME_OVER
                self.setup()  # Reset the game when the countdown reaches 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()

if __name__ == "__main__":
    main()
