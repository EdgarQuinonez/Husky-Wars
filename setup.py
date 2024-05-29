import arcade
import arcade.key
# Paths to image assets
P1_ANIMATIONS_PATH = "assets/character/p1"
P2_ANIMATIONS_PATH = "assets/character/p2"

MENU_BG_PATH = "assets/background_menu.png"
GAME_OVER_BG_PATH = "assets/game_over_bg.png"
TITLE_IMAGE_PATH = "assets/buttons/title.png"
JUGAR_BUTTON_PATH = "assets/buttons/jugar.png"
JUGAR_HOVER_BUTTON_PATH = "assets/buttons/jugar_hover.png"
OPCIONES_BUTTON_PATH = "assets/buttons/opciones.png"
OPCIONES_HOVER_BUTTON_PATH = "assets/buttons/opciones_hover.png"
COMO_BUTTON_PATH = "assets/buttons/como.png"
COMO_HOVER_BUTTON_PATH = "assets/buttons/como_hover.png"
SALIR_BUTTON_PATH = "assets/buttons/salir.png"
SALIR_HOVER_BUTTON_PATH = "assets/buttons/salir_hover.png"
DIFFICULTY_BUTTON_PATH = "assets/buttons/dificultad.png"


# Paths to sound assets
CLICK_SOUND_PATH = "assets/sounds/Button.mp3"
MENU_SOUNDTRACK_PATH = "assets/sounds/menu_soundtrack.mp3"

JUMP_SOUND_PATH = "assets/sounds/jump.wav"
FALLING_SOUND_PATH = "assets/sounds/fall.wav"
HURT_SOUND_PATH = "assets/sounds/hurt.wav"
COLLECTIBLE_SOUND_PATH = "assets/sounds/collectible.wav"
POWER_UP_SOUND_PATH = "assets/sounds/powerup.wav"
PROJECTILE_SOUND_PATH = "assets/sounds/projectile.wav"
FALL_SOUND_PATH = "assets/sounds/fall.wav"
GAME_OVER_SOUND_PATH = "assets/sounds/gameover.wav"
WATER_SOUND_PATH = "assets/sounds/water.wav"

GAMEPLAY_MUSIC_PATH = "assets/sounds/gameplay_music.mp3"

## P1
P1_STILL_PATH = f"{P1_ANIMATIONS_PATH}/idle.png"
P1_LOSER_PATH = f"{P1_ANIMATIONS_PATH}/loser.png"
P1_WINNER_PATH = f"{P1_ANIMATIONS_PATH}/winner.png"
## P2
P2_STILL_PATH = f"{P1_ANIMATIONS_PATH}/idle.png"
P2_LOSER_PATH = f"{P2_ANIMATIONS_PATH}/loser.png"
P2_WINNER_PATH = f"{P2_ANIMATIONS_PATH}/winner.png"
## Collectibles

COLLECTIBLE_SPAWN_COOLDOWN = 5
COLLECTIBLE_HARD_RESET_COOLDOWN = 10

### Good
GOOD_COLLECTIBLE_COMMON_PATH = "assets/collectibles/good/hueso_medio.png"
GOOD_COLLECTIBLE_UNCOMMON_PATH = "assets/collectibles/good/hueso.png"
GOOD_COLLECTIBLE_RARE_PATH = "assets/collectibles/good/hueso_oro.png"

# random < drop_rate -> spawn type
GOOD_COLLECTIBLE_COMMON_DROP_RATE = 0.75
GOOD_COLLECTIBLE_UNCOMMON_DROP_RATE = 0.5
GOOD_COLLECTIBLE_RARE_DROP_RATE = 0.25

# Points
GOOD_COLLECTIBLE_COMMON_POINTS = 2
GOOD_COLLECTIBLE_UNCOMMON_POINTS = 3
GOOD_COLLECTIBLE_RARE_POINTS = 5

### Bad
BAD_COLLECTIBLE_COMMON_PATH = "assets/collectibles/bad/aguacate.png"
BAD_COLLECTIBLE_UNCOMMON_PATH = "assets/collectibles/bad/champinion.png"
BAD_COLLECTIBLE_RARE_PATH = "assets/collectibles/bad/chocolate.png"

BAD_COLLECTIBLE_COMMON_DROP_RATE = 0.5
BAD_COLLECTIBLE_UNCOMMON_DROP_RATE = 0.25
BAD_COLLECTIBLE_RARE_DROP_RATE = 0.125

# Points
BAD_COLLECTIBLE_COMMON_POINTS = -3
BAD_COLLECTIBLE_UNCOMMON_POINTS = -5
BAD_COLLECTIBLE_RARE_POINTS = -10

ASPERSOR_SHOT_PENALIZATION_POINTS = -10
FRISBEE_PENALIZATION_POINTS = -20
FALLING_PENALIZATION_POINTS = -15

### Power Ups
POWER_UP_PATH = "assets/collectibles/power_ups/correa.png"

POWER_UP_DROP_RATE = 0.5
POWER_UP_COOLDOWN = 15
POWER_UP_POINTS = 20
POWER_UP_TIME_INCREASE = 10

## Enemies
ASPERSOR_SPRITE_PATH = "assets/enemies/aspersor.png"
AGUA_SPRITE_PATH = "assets/projectile/agua.png"
AGUA_SCALING = 0.125

FRISBEE_SPRITE_PATH = "assets/enemies/frisbee.png"
FRISBEE_SCALING = 0.2
FRISBEE_SPEED = 500
FRISBEE_DEBOUNCE_TIME = 0.75

ASPERSOR_PROJECTILE_SPEED = 5
ASPERSOR_SPAWN_SHOOT_DELAY = 2
# Scaling and positioning
CHARACTER_SCALING = 1.25
ASPERSOR_SCALING = 0.15
COLLECTIBLE_SCALING = 0.15

TILE_SIZE = 32

# CONSTANTS
GRAVITY = 1

# Window

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT

WINDOW_TITLE = "¡Husky Wars!"
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = int(1600 / ASPECT_RATIO)

TILE_WIDTH = 40
TILE_HEIGHT = 22

MAP_WIDTH = TILE_SIZE * TILE_WIDTH
MAP_HEIGHT = TILE_SIZE * TILE_HEIGHT

TILE_SCALING = WINDOW_WIDTH / MAP_WIDTH
SCALED_MAP_WIDTH = MAP_WIDTH * TILE_SCALING
SCALED_MAP_HEIGHT = MAP_HEIGHT * TILE_SCALING

LETTERBOX_HEIGHT = (WINDOW_HEIGHT - SCALED_MAP_HEIGHT) / 2

TILE_MAP_PATH = "assets/con-enemigos.tmj"

DIALOG_OVERLAY_WINDOW_MARGIN_X = 48
DIALOG_OVERLAY_WINDOW_MARGIN_Y = 56


SCREEN_TITLE = "¡Husky Wars!"

# Game States
GAME_STATE_MAIN_MENU = 0
GAME_STATE_GAMEPLAY = 1
GAME_STATE_GAME_OVER = 2
GAME_STATE_START_MATCH_COUNTDOWN = 3
GAME_STATE_LOADING = 4

# Difficulty
DIFFICULTY_REGULAR = 0
DIFFICULTY_HARD = 1

# Game State Variables
START_MATCH_COUNTDOWN_VALUE = 3

## Scores display
P1_SCORE_X = 10
P1_SCORE_Y = WINDOW_HEIGHT - (40 + LETTERBOX_HEIGHT)

P2_SCORE_X = WINDOW_WIDTH - 120
P2_SCORE_Y = WINDOW_HEIGHT - (40 + LETTERBOX_HEIGHT)


# Coordinates
P1_START_X = 64
P1_START_Y = 128

P2_START_X = 128
P2_START_Y = 128

# STATS
P1_SPEED = 5
P2_SPEED = 5

P1_JUMP_SPEED = 20
P2_JUMP_SPEED = 20


# Key bindings
P1_UP_KEY = arcade.key.W
P1_DOWN_KEY = arcade.key.S
P1_LEFT_KEY = arcade.key.A
P1_RIGHT_KEY = arcade.key.D

P1_KEYBINDINGS = {
    "up": P1_UP_KEY,
    "down": P1_DOWN_KEY,
    "left": P1_LEFT_KEY,
    "right": P1_RIGHT_KEY
}

P2_UP_KEY = arcade.key.UP
P2_DOWN_KEY = arcade.key.DOWN
P2_LEFT_KEY = arcade.key.LEFT
P2_RIGHT_KEY = arcade.key.RIGHT

P2_KEYBINDINGS = {
    "up": P2_UP_KEY,
    "down": P2_DOWN_KEY,
    "left": P2_LEFT_KEY,
    "right": P2_RIGHT_KEY
}


# Layers
LAYER_NAME_PLATFORMS = "platforms"
OBJECT_NAME_COLLECTIBLES = "collectible"
OBJECT_NAME_POWER_UP = "power_up"
LAYER_NAME_BACKGROUND = "background"
LAYER_NAME_METABACKGROUND = "Capa de patrones 3"
OBJECT_NAME_PLAYER_SPAWN = "player"
OBJECT_NAME_ENEMY_SPAWN = "enemy"
OBJECT_NAME_PROJECTILE = "projectile"
OBJECT_NAME_TRAILS = "trails"

# IDs
P1_ID = "player1"
P2_ID = "player2"

FRISBEE_ID_PREFIX = "frisbee"
ASPERSOR_ID_PREFIX = "aspersor"

OBJECT_PROJECTILE_ATTR = "frisbee_id"
OBJECT_ENEMY_ATTR = "enemy_id"

ASPERSOR_1_PROJECTILE_ID = "agua1"
ASPERSOR_2_PROJECTILE_ID = "agua2"
ASPERSOR_3_PROJECTILE_ID = "agua3"
ASPERSOR_4_PROJECTILE_ID = "agua4"

# Animations
RIGHT_FACING = 1
LEFT_FACING = 0

P1_INITIAL_FACING = RIGHT_FACING
P2_INITIAL_FACING = LEFT_FACING

HURT_TIMER_DURATION = 0.25

