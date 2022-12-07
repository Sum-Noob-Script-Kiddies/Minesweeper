import pygame as pg
from UI import Button
from config import *
import minesweeper

pg.init()

screen = pg.display.set_mode((960,540))
screen_rect = screen.get_rect()

screen.fill(COLOR_BG)

buttons = []

rows_n, cols_n = 16, 16
cell_size = 25
gap = 3

board = pg.Surface((cell_size*cols_n + gap*(cols_n-1), cell_size*rows_n + gap*(rows_n-1)))
board.fill(COLOR_BG2)
board_rect = board.get_rect(center=screen_rect.center)

for row in range(rows_n):
    for col in range(cols_n):
        rel_pos = ((cell_size+gap)*col, (cell_size+gap)*row)    # Relative position of the cell on the board
        buttons.append(Button(("assets/cell_idle.png", "assets/cell_hover.png"), rel_pos, on_surface=board, surface_abs_pos=board_rect.topleft))

while True:
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            for button in buttons:
                button.mouse_check(event.pos, event)

    for button in buttons:
        button.mouse_check(mouse)
        button.draw()
    
    screen.blit(board, board_rect)
    pg.display.update()

