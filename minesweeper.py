from config import *
import pygame as pg
import UI
from random import randint


class Cell():
    """A `Cell` is an object with a `CellButton` that user interacts with
    
    Attributes:
        coord (int, int): The (row, col) of the Cell with reference to it's `minefield`
        val (int): Number of bombs around this cell
        is_mine (bool): if this cell is a mine
        is_flagged (bool): if this cell is flagged
        self.is_exposed (bool): if this cell is exposed
        self.minefield (Minefield): the minefield that the Cell is in
        self.button (Button): The `Button` that is instantiated for this cell
    """
    def __init__(self, coord: tuple[int, int], val: int, minefield: "Minefield", cellstyle: UI.CellButtonStyle, is_mine=False, is_flagged=False, is_exposed=False):
        """Creates a `Cell` with a changeable `Button` associated to it"""
        self.coord = coord  # coord = (row, col) where top-left is 0,0
        self.val = val  # Number of bombs around this cell (None if is_mine)
        self.is_mine = is_mine  # Boolean
        self.is_flagged = is_flagged # Don't care for now
        self.is_exposed = is_exposed  # Sean will take care of this
        self.cellstyle = cellstyle
        self.minefield = minefield

        row, col = coord
        self.offset = ((CELLSIZE+GAP)*col, (CELLSIZE+GAP)*row)
        self.button = UI.Button(self.cellstyle.normal_button_imgs, self.offset, None,
            on_surface=self.minefield.board, surface_abs_pos=self.minefield.board_abs_pos)
        self.button_to_start()
        self.button.enable()

    # Setters / Getters
    def set_mine(self, is_mine: bool):
        """Setter for .is_mine"""
        self.is_mine = is_mine

    def set_val(self, val: int):
        """Setter for .val"""
        self.val = val

    def reset_cell(self):
        """Resets the Cell back and it's Button back to the start button"""
        self.val = -1
        self.is_mine = False
        self.is_flagged = False
        self.is_exposed = False
        self.button_to_start()
        self.button.enable()

    # Cell-Specific Methods
    def flag(self):
        """Toggles whether or not cell is flagged"""
        self.is_flagged = not self.is_flagged
        if self.is_flagged:
            self.minefield.remaining_bombs -= 1
        else: 
            self.minefield.remaining_bombs += 1
        self.update_button()

    def expose(self):
        """Expose this cell and `.expose_around()` if no mines around it"""
        if self.is_exposed or self.is_flagged:
            return

        self.is_exposed = True
        self.minefield.no_exposed += 1
        if self.val == 0:   # If cell is 0, we expose those around it
            self.expose_around()
        self.update_button()

        # Check Losing Condition
        if self.is_mine:
            print("Lose")
            pg.event.post(pg.event.Event(GAMEEND, {"won": False}))
            
        # Check Winning Condition
        elif self.minefield.check_win():
            print("Win")
            pg.event.post(pg.event.Event(GAMEEND, {"won": True}))

    def expose_around(self):    # Expose the cells around this cell
        """Exposes surrounding cells around this cell"""
        y_range, x_range = (self.coord[0]-1, self.coord[0]+2), (self.coord[1]-1, self.coord[1]+2)
        y_range = max(y_range[0], 0), min(ROWS, y_range[1])
        x_range = max(x_range[0], 0), min(COLS, x_range[1])
        for row in range(y_range[0], y_range[1]):
            for col in range(x_range[0], x_range[1]):
                    self.minefield.matrix[row][col].expose()
    
    def attempt_expose_around(self):
        flags = 0
        y_range, x_range = (self.coord[0]-1, self.coord[0]+2), (self.coord[1]-1, self.coord[1]+2)
        y_range = max(y_range[0], 0), min(ROWS, y_range[1])
        x_range = max(x_range[0], 0), min(COLS, x_range[1])
        for row in range(y_range[0], y_range[1]):
            for col in range(x_range[0], x_range[1]):
                if self.minefield.matrix[row][col].is_flagged:
                    flags += 1
        if flags == self.minefield.matrix[self.coord[0]][self.coord[1]].val and self.is_exposed:
            self.expose_around()

    def start_game(self, button):
        """Informs Minefield to start game, and exposes this cell after the game starts"""
        self.minefield.start_game(self.coord)   # Will get rid of all the "start buttons"
        if button == 1:
            self.expose()                           # This cell will be exposed
        elif button == 3:
            self.flag()

    # Button Changers
    def update_button(self):
        """Update the Cell's Button based on the Cell's current state"""
        self.button_to_normal()
        if self.is_exposed:
            self.button_to_revealed()
        elif self.is_flagged:
            self.button_to_flagged()

    def button_to_start(self):
        """Returns a new Button that generates a minefield when clicked"""
        self.button.set_imgs(self.cellstyle.normal_button_imgs)
        self.button.set_funcs({1: lambda _: self.start_game(1),         # All buttons start by being a "start game" button
                               3: lambda _: self.start_game(3)})        # Flags can be placed without starting game

    def button_to_normal(self):
        """Changes the Cell's Button to the Normal Button"""
        self.button.set_imgs(self.cellstyle.normal_button_imgs)
        self.button.set_funcs({1: lambda _:self.expose(), 3: lambda _: self.flag()})
    
    def button_to_flagged(self):
        """Changes the Cell's Button to the Flagged Button"""
        self.button.set_imgs(self.cellstyle.flag_button_imgs)
        self.button.set_funcs({3: lambda _: self.flag()})

    def button_to_revealed(self):
        """Changes the Cell's Button to the Revealed Button"""
        if self.is_mine:
            self.button.set_imgs(self.cellstyle.mine_button_imgs)
        else:
            self.button.set_imgs(self.cellstyle.num_buttons_imgs[self.val])
        self.button.set_funcs({1: lambda _:self.attempt_expose_around()})

class Minefield():
    """Minefield consists of `Cell`s which each contains a `Button`
    
    Attributes:
        board (pg.Surface): The Surface that the `CellButton`s are rendered on
        board_rect (pg.Rect)
        board_abs_pos (int, int): The top-left of `.board` relative to the game display
        matrix (list[list[Cell]]): The game 2D matrix of `Cell`s, each with a `CellButton`
    """
    def __init__(self, pos_centre: tuple[int, int], cellstyle: UI.CellButtonStyle, mode=1) -> None:
        """Creates the minefield filled with clickable `Cell`s"""
        self.board = pg.Surface((CELLSIZE*COLS + GAP*(COLS-1), CELLSIZE*ROWS + GAP*(ROWS-1)))
        self.board_rect = self.board.get_rect(center=pos_centre)
        self.board_abs_pos = self.board_rect.topleft
        self.is_suspended = False
        self.mode = mode
        self.matrix = [[None]*COLS for _ in range(ROWS)]
        for row in range(ROWS): # Create a matrix with -1 value Cells
            for col in range(COLS):
                self.matrix[row][col] = Cell((row, col), -1, self, cellstyle)   # Initialises with -1 default value
        
        self.no_exposed = 0
        self.remaining_bombs = BOMBS
    
    def reset_board(self):
        self.no_exposed = 0
        self.remaining_bombs = BOMBS
        for cells in self.matrix:
            for cell in cells:
                cell.reset_cell()

    def fill_matrix(self, start_coord: tuple[int, int], mode: int) -> None:
        """Fills the game matrix with new values and mines"""
        int_matrix = self.generate_int_matrix(start_coord, mode)
        for row in range(ROWS):
            for col in range(COLS):
                val = int_matrix[row][col]
                if val == -1:
                    self.matrix[row][col].set_mine(True)
                else:
                    self.matrix[row][col].set_val(val)

    def start_game(self, start_coord: tuple[int, int]) -> None:
        """Change the state of cell button from a "start button" to their appropriate button + Posts a GAMESTART event"""
        self.fill_matrix(start_coord, self.mode)
        for row in self.matrix:
            for cell in row:
                cell.update_button()
        pg.event.post(pg.event.Event(GAMESTART))   # Sends a GAMESTART event to be handled in main.py

    def suspend(self) -> None:
        """Disable all Buttons"""
        for row in self.matrix:
            for cell in row:
                cell.button.disable()
        self.is_suspended = True
    
    def resume(self) -> None:
        """Enable all Buttons"""
        for row in self.matrix:
            for cell in row:
                cell.button.enable()
        self.is_suspended = False
    
    def check_win(self) -> bool:
        """Winning condition"""
        for row in self.matrix:
            for cell in row:
                if not cell.is_exposed and not cell.is_mine:
                    return False
        return True

    @staticmethod
    def generate_int_matrix(start_coord: tuple[int, int], mode: int) -> list[list[int]]:
        """Generates random minefield - 2D Array of Cell object type

            Args:
                start_row: starting y-coordinate
                start_col: starting x-coordinate
                mode:
                    0 - (Are you cheating?): Ensures 1st cell is always a "0"
                    1 - (Standard): Ensures 1st cell is minimally an integer """

        def generate_bombs(int_matrix: list[list[int]], blocked_rows: list, blocked_cols: list, mode: int) -> list[list[int]]:
            """Determines number of bombs and assigns them to base matrix"""
            bombs = BOMBS
            for _ in range(bombs):
                while True:
                    randy = randint(0, ROWS-1)
                    randx = randint(0, COLS-1)
                    if mode == 1:
                        # Ensures cell is some integer - Not a bomb
                        if not int_matrix[randy][randx] == -1 and not (randy == blocked_rows[1] and randx == blocked_cols[1]):
                            int_matrix[randy][randx] = -1
                            break
                    if mode == 0:
                        # Ensures cell is a "0"
                        if not int_matrix[randy][randx] == -1 and not (randy in blocked_rows and randx in blocked_cols):
                            # Ensures cell is not already a bomb
                            int_matrix[randy][randx] = -1
                            break

        def allocate_val(int_matrix) -> list[list[int]]:
            """Allocates value of cell according to mines surrounding it using an extended field"""
            extended = [[0]*(COLS+2)]
            for row in range(ROWS):
                extended.append([0] + int_matrix[row] + [0])
            extended.append([0]*(COLS+2))

            for y in range(1, ROWS+1):
                for x in range(1, COLS+1):
                    if extended[y][x] != -1:
                        int_matrix[y-1][x-1] = count_mines(y, x, extended)

        def count_mines(y: int, x: int, extended: list) -> int:
            """Counts mines around a centre cell"""
            count = 0
            for a in range(-1, 2):
                for b in range(-1, 2):
                    if extended[y+a][x+b] == -1:
                        count += 1
            return count

        int_matrix = [[0]*COLS for _ in range(ROWS)]
        start_row, start_col = start_coord
        generate_bombs(int_matrix, list(range(start_row-1,start_row+2)), list(range(start_col-1,start_col+2)), mode)    
        allocate_val(int_matrix)
        
        return int_matrix
    
    def draw_board(self):
        """Renders the Cell's Buttons onto the minefield's `.board`"""
        self.board.fill(COLOR_DARK2)
        for row in self.matrix:
            for cell in row:
                cell.button.draw()

class Game():
    pass

# ================Debugging tools===============

def print_field(minefield: list[list[Cell]]) -> None:
    """Debugging - Prints field"""
    for y in range(ROWS):
        for x in range(COLS):
            if minefield[y][x].is_exposed:
                # "not" added in for debugging
                if minefield[y][x].is_mine:
                    print("*",end=" ")
                else:
                    print(minefield[y][x].val,end=" ")
            else:
                print("X",end=" ")            
        print()
