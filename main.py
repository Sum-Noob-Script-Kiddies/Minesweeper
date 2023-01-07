from config import *
import pygame as pg
import UI
import minesweeper

pg.init()
screen = pg.display.set_mode((960,540))
screen_rect = screen.get_rect()

cellstyle = UI.CellButtonStyle(("assets/cell/idle.png", "assets/cell/hover.png"), "assets/cell/flag.png", "assets/cell/mine.png", "assets/cell/")
minefield = minesweeper.Minefield(screen_rect.center, cellstyle, mode=GAMEMODE)     # Creates a minefield with the given cellstyle and mode
game_ended = False

font = pg.font.Font("assets/fonts/Rare Game.otf", 32)
green = COLOR_LIGHT
cur_dur = 0

def start_timer():
    start_ticks = pg.time.get_ticks()
    return start_ticks


# Game Over Pop-Up Initialisation
gameover_popup = UI.PopUp(pg.Rect(0,0,200,300), COLOR_LIGHT)
gameover_popup.rect.centerx = (screen_rect.w+minefield.board_abs_pos[0]+minefield.board_rect.w)/2
gameover_popup.rect.centery = screen_rect.h/2
gameover_popup.set_border(COLOR_LIGHT2)
gameover_popup.add_button(("assets/btn_restart_idle.png", "assets/btn_restart_hover.png"), lambda _:restart_game(), (150, 0, 0 ,0))

def restart_game():
    global game_ended
    game_ended = False
    minefield.reset_board()
    gameover_popup.hide()

while True:
    for event in pg.event.get():    # Event Loop
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # Passes all mouse button up/down events too all listeners
        # Objecting in `listening_mouse_button` have listeners `._on_mouse_button()`
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            for listening in listening_mouse_button.copy():
                listening._on_mouse_button(event)
        if event.type == GAMEEND:
            if game_ended:  # Ignore duplicate GAMEEND events that occurs when multiple Cell's .expose posts the event
                continue
            if event.won:
                gameover_popup.set_text(UI.Text("You\nWin!", 60), bounding_margins=(0, 120, 0, 0))
            else:
                gameover_popup.set_text(UI.Text("Ya\nSuck!", 60), bounding_margins=(0, 120, 0, 0))
            game_ended = True
            minefield.suspend()
            gameover_popup.unhide()

    screen.fill(COLOR_DARK) # Render the screen's background
    minefield.draw_board()  # Render the cells onto the board

    gameover_popup.draw()
    screen.blit(minefield.board, minefield.board_rect)  # Render the board onto the screen

    pg.display.update()
