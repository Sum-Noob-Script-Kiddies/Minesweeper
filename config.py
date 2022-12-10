import pygame as pg

ROWS, COLS = 16, 16
BOMBS = 50

CELLSIZE = 25
GAP = 3

COLOR_BG = pg.Color("#292831")
COLOR_BG2 = pg.Color("#333f58")

# Event Listener
listening_mouse_button = set()  # Listener ._on_mouse_button()