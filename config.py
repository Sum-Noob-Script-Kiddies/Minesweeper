import pygame as pg
import pygame.freetype as freetype
freetype.init()

# Game Configurations
ROWS, COLS = 16, 16
BOMBS = 50

CELLSIZE = 25
GAP = 3

GAMEMODE = 0

# Constants

COLOR_DARK = pg.Color("#292831")
COLOR_DARK2 = pg.Color("#333f58")
COLOR_LIGHT = pg.Color("#fbbbad") 

FONT_PATH = "assets/fonts/the-bomb-sound.regular.ttf"
FONT_SIZE = 20
FONT = freetype.Font("assets/fonts/the-bomb-sound.regular.ttf", 20)

GAMESTART = pg.event.custom_type() 

# Event Listeners
listening_mouse_button = set()  # Listener ._on_mouse_button()