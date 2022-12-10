from config import *
import pygame as pg
import UI
from random import randint

ROWS, COLS = 16, 16
BOMBS = 50

class Cell():
    """A `Cell` is an object with a `CellButton` that user interacts with
    
    Attributes:
        coord (int, int): The (row, col) of the Cell with reference to it's `minefield`
        val (int): Number of bombs around this cell
        is_mine (bool): if this cell is a mine
        is_flagged (bool): if this cell is flagged
        self.is_exposed (bool): if this cell is exposed
        self.minefield (Minefield): the minefield that the Cell is in
        self.button (CellButton): The `CellButton` that is instantiated for this cell
    """
    def __init__(self, coord, val, minefield, cellstyle, is_mine=False, is_flagged=False, exposed=False):
        """Creates a `Cell` and instantiate the `CellButton` associated to it"""
        self.coord = coord  # coord = (row, col) where top-left is 0,0
        self.val = val  # Number of bombs around this cell (None if is_mine)
        self.is_mine = is_mine  # Boolean
        self.is_flagged = is_flagged # Don't care for now
        self.is_exposed = exposed  # Sean will take care of this
        self.minefield = minefield
        self.button = UI.CellButton(self, cellstyle)

        listening_mouse_button.add(self.button)

    def expose(self): 
        """Expose this cell and `.expose_around()` if no mines around it"""
        if self.is_exposed:
            return 
        if self.is_mine:
            print("Lose")
        self.is_exposed = True
        if self.val == 0:   # If cell is 0, we expose those around it
            self.expose_around()

    def expose_around(self):    # Expose the cells around this cell
        """Exposes surrounding cells around this cell"""
        y_range, x_range = (self.coord[0]-1, self.coord[0]+2), (self.coord[1]-1, self.coord[1]+2)
        y_range = max(y_range[0], 0), min(ROWS, y_range[1])
        x_range = max(x_range[0], 0), min(COLS, x_range[1])
        for i in range(y_range[0], y_range[1]):
            for j in range(x_range[0], x_range[1]):
                self.minefield[i][j].expose()

class Minefield():
    """Minefield consists of `Cell`s which each has a `CellButton`
    
    Attributes:
        board (pg.Surface): The Surface that the `CellButton`s are rendered on
        board_rect (pg.Rect)
        board_abs_pos (int, int): The top-left of `.board` relative to the game display
        matrix (list[list[Cell]]): The game 2D matrix of `Cell`s, each with a `CellButton`
    """
    def __init__(self, pos_centre, cellstyle, mode=1):
        self.board = pg.Surface((CELLSIZE*COLS + GAP*(COLS-1), CELLSIZE*ROWS + GAP*(ROWS-1)))
        self.board_rect = self.board.get_rect(center=pos_centre)
        self.board_abs_pos = self.board_rect.topleft
        int_matrix = self.generate_int_matrix(5, 5, mode)
        self.matrix = [[None]*COLS for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                val = int_matrix[row][col]
                if val == -1:
                    self.matrix[row][col] = Cell((row, col), -1, self, cellstyle, is_mine=True)
                else:
                    self.matrix[row][col] = Cell((row, col), val, self, cellstyle, is_mine=False)

    @staticmethod
    def generate_int_matrix(start_row: int, start_col: int, mode: int) -> list[list[int]]:
        """Generates random minefield - 2D Array of Cell object type

            Parameters:
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
                        #Ensures cell is some integer - Not a bomb
                        if not int_matrix[randy][randx] == -1 and not (randy == blocked_rows[1] and randx == blocked_cols[1]):
                            int_matrix[randy][randx] = -1
                            break
                    if mode == 0:
                        #Ensures cell is a "0"
                        if not int_matrix[randy][randx] == -1 and not (randy in blocked_rows and randx in blocked_cols):
                            #Ensures cell is not already a bomb
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
        generate_bombs(int_matrix, list(range(start_row-1,start_row+2)), list(range(start_col-1,start_col+2)), mode)    
        allocate_val(int_matrix)
        return int_matrix
    
    def draw_board(self):
        """Renders the Cell's Buttons onto the minefield's `.board`"""
        self.board.fill(COLOR_BG2)
        for row in self.matrix:
            for cell in row:
                cell.button.draw()


# ================Debugging tools===============

def print_field(minefield) -> None:
    """Debugging - Prints field"""
    for y in range(ROWS):
        for x in range(COLS):
            if not minefield[y][x].exposed:
                # "not" added in for debugging
                if minefield[y][x].is_mine:
                    print("*",end=" ")
                else:
                    print(minefield[y][x].val,end=" ")
            else:
                print("X",end=" ")            
        print()
