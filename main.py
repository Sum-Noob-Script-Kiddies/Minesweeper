from config import *
import pygame as pg
import UI
import minesweeper

pg.init()

screen = pg.display.set_mode((960,540))
screen_rect = screen.get_rect()

cellstyle = UI.CellButtonStyle(("assets/cell/idle.png", "assets/cell/hover.png"), "assets/cell/flag.png", "assets/cell/mine.png", "assets/cell/")
minefield = minesweeper.Minefield(screen_rect.center, cellstyle, mode=GAMEMODE)     # Creates a minefield with the given cellstyle and mode

font = pg.font.Font('Rare Game.otf', 32)
green = (0, 255, 0)
cur_dur = 0

while True: 
    for event in pg.event.get():    # Event Loop
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # Passes all mouse button up/down events too all listeners
        # Objecting in `listening_mouse_button` have listeners `._on_mouse_button()`
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            for listening in listening_mouse_button:
                listening._on_mouse_button(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                minefield.toggle_pause()

    screen.fill(COLOR_DARK)   # Render the screen's background
    minefield.draw_board()  # Render the cells onto the board
    screen.blit(minefield.board, minefield.board_rect)  # Render the board onto the screen
    
    if cur_dur < 1000:
        cur_dur = pg.time.get_ticks()//1000
    text = font.render(str(cur_dur), True, green)
    textRect = text.get_rect()
    textRect.center = (100, 100)
    screen.blit(text, textRect)

    pg.display.update()
