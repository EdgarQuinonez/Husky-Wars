import arcade
import arcade.key
# Paths to image assets

## P1
P1_STILL_PATH = "assets/character/p1_still.png"

## P2
P2_STILL_PATH = "assets/character/p2_still.png"

## Collectibles

### Good
GOOD_COLLECTIBLE_COMMON_PATH = "assets/collectibles/good/hueso_medio.png"
GOOD_COLLECTIBLE_UNCOMMON_PATH = "assets/collectibles/good/hueso.png"
GOOD_COLLECTIBLE_RARE_PATH = "assets/collectibles/good/hueso_oro.png"

### Bad
BAD_COLLECTIBLE_COMMON_PATH = "assets/collectibles/bad/aguacate.png"
BAD_COLLECTIBLE_UNCOMMON_PATH = "assets/collectibles/bad/champinion.png"
BAD_COLLECTIBLE_RARE_PATH = "assets/collectibles/bad/chocolate.png"

### Power Ups
POWER_UPS_COLLECTIBLE_COMMON_PATH = "assets/collectibles/power_ups/correa.png"

## Enemies
ENEMY_1_PATH = "assets/enemies/aspersor.png"
ENEMY_2_PATH = "assets/enemies/frisbee.png"

# Scaling and positioning
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# Window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Husky Wars!"


# Coordinates
P1_START_X = 64
P1_START_Y = 128

P2_START_X = 128
P2_START_Y = 128

# STATS
P1_SPEED = 5
P2_SPEED = 5


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



# Drop Rates
