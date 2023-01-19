from config import *
import pygame as pg
# import numpy as np
import UI
import minesweeper

pg.init()
pg.display.set_caption('Minesweeper')
screen = pg.display.set_mode((960,540))
screen_rect = screen.get_rect()

# push minesweeper board down 
screen_rect.center = (screen_rect.center[0], screen_rect.center[1]+10)

cellstyle = UI.CellButtonStyle(("assets/cell/idle.png", "assets/cell/hover.png"), "assets/cell/flag.png", "assets/cell/mine.png", "assets/cell/")
minefield = minesweeper.Minefield(screen_rect.center, cellstyle, mode=GAMEMODE)     # Creates a minefield with the given cellstyle and mode
game_ended = False
game_start = False
start_tick = pg.time.get_ticks()

font = pg.font.Font("assets/fonts/Rare Game.otf", 32)

# Game Over Pop-Up Initialisation
gameover_popup = UI.PopUp(pg.Rect(0,0,200,300), COLOR_LIGHT)
gameover_popup.rect.centerx = (screen_rect.w+minefield.board_abs_pos[0]+minefield.board_rect.w)/2
gameover_popup.rect.centery = screen_rect.h/2
gameover_popup.set_border(COLOR_LIGHT2)
gameover_popup.add_button(("assets/btn_restart_idle.png", "assets/btn_restart_hover.png"), lambda _:restart_game(), (150, 0, 0 ,0))

def restart_game():
    global game_ended
    global game_start
    game_ended = False
    game_start = False
    minefield.reset_board()
    gameover_popup.hide()

while True:
    for event in pg.event.get():    # Event Loop                        
        if event.type == GAMESTART:
            start_tick = pg.time.get_ticks()
            game_start = True
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
                end_tick = pg.time.get_ticks()
                gameover_popup.set_text(UI.Text(" Ya\nSuck!", 60), bounding_margins=(0, 120, 0, 0))
                # # what about using numpy?
                # cells = list(np.hstack(minefield.matrix))
                # for cell in cells:
                #     if cell.is_mine and not cell.is_flagged:
                #         cell.expose()
                #     if not cell.is_mine and cell.is_flagged:
                #         cell.button.set_imgs("assets/cell/flag_wrong.png")

                for cells in minefield.matrix:
                    for cell in cells:
                        if cell.is_mine and not cell.is_flagged:
                            cell.expose()
                        if not cell.is_mine and cell.is_flagged:
                            cell.button.set_imgs("assets/cell/flag_wrong.png")
            game_ended = True
            minefield.suspend()
            gameover_popup.unhide()

    screen.fill(COLOR_DARK) # Render the screen's background
    minefield.draw_board()  # Render the cells onto the board

    gameover_popup.draw()

    if game_ended:
        text = font.render(str(int((end_tick - start_tick) / 1000)), True, COLOR_LIGHT)
    elif not game_start:
        text = font.render('0', True, COLOR_LIGHT)
    else:
        text = font.render(str(int((pg.time.get_ticks() - start_tick) / 1000)), True, COLOR_LIGHT)
        
    textRect = text.get_rect() 
    textRect.centery = 30
    textRect.left = screen_rect.center[0] - minefield.board.get_width()/2 # Render the timer at the left edge of the board

    bomb_text = font.render(str(minefield.remaining_bombs), True, COLOR_LIGHT)
    bombRect = bomb_text.get_rect()
    bombRect.centery =  30
    bombRect.right = screen_rect.center[0] + minefield.board.get_width()/2 # Render the bomb counter at the right edge of the board

    screen.blit(bomb_text, bombRect) # Render the bomb counter before the board
    screen.blit(text, textRect) # Render the timer before the board
    screen.blit(minefield.board, minefield.board_rect)  # Render the board onto the screen

    pg.display.update()
