from random import randint
import copy

ROWS, COLS = 16, 16
BOMBS = 50

class Cell():
    def __init__(self, coord, val, minefield, is_mine=False, is_flagged=False, exposed=False):
        self.coord = coord  # coord = (y, x) where top-left is 0,0
        self.val = val  # Number of bombs around this cell (None if is_mine)
        self.is_mine = is_mine  # Boolean
        self.is_flagged = is_flagged # Don't care for now
        self.exposed = exposed  # Sean will take care of this
        self.minefield = minefield

    def expose2(self): 
        """Expose this cell and other cells around it if 0 recursively"""
        if self.exposed:
            return 
        if self.is_mine:
            print("Lose")
        self.exposed = True
        if self.val == 0:
            y_range, x_range = (self.coord[0]-1, self.coord[0]+2), (self.coord[1]-1, self.coord[1]+2)
            y_range = max(y_range[0], 0), min(ROWS, y_range[1])
            x_range = max(x_range[0], 0), min(COLS, x_range[1])
            for i in range(y_range[0], y_range[1]):
                for j in range(x_range[0], x_range[1]):
                    self.minefield[i][j].expose2()


def generate_minefield(start_row: int, start_col: int) -> list[list[Cell]]:
    """Generates random minefield - 2D Array of Cell object type"""
    
    def generate_base() -> list[list[Cell]]:
        """Generates base field - 2D Array of Cell object type"""
        base = []
        for y in range(ROWS):
            row = []
            for x in range(COLS):
                row.append(Cell([y, x], 0, base))
            base.append(row)
        return base
        
    def generate_bombs(minefield) -> list[list[Cell]]:
        """Determines number of bombs and assigns them to base field"""
        bombs = BOMBS
        for _ in range(bombs):
            while True:
                randy = randint(0, ROWS-1)
                randx = randint(0, COLS-1)
                if not (minefield[randy][randx].is_mine or randy in blocked_rows or randx in blocked_cols):
                    #Ensures cell is not already a bomb, or in blacklisted 3x3 matrix based on start point
                    minefield[randy][randx].is_mine = True
                    break
        return minefield

    def allocate_val(minefield) -> list[list[Cell]]:
        """Allocates value of cell according to mines surrounding it using an extended field"""
        extended = copy.deepcopy(minefield)
        newtop=[]
        newbot=[]
        for i in range(COLS):
            newtop.append(Cell([-1, i], 0, extended))
            newbot.append(Cell([COLS, i], 0, extended))

        extended.insert(0, newtop)
        extended.append(newbot)

        for row in range(ROWS+2):
            extended[row].insert(0, Cell([row-1, -1], 0, extended))
            extended[row].append(Cell([row-1, ROWS], 0, extended))
        
        for y in range(ROWS):
            for x in range(COLS):
                if minefield[y][x].is_mine:
                    minefield[y][x].val = -1
                else:
                    minefield[y][x].val = count_mines(y, x, extended)
        return minefield

    def count_mines(y: int, x: int, extended: list) -> int:
        """Counts mines around a cell"""
        count = 0
        y += 1
        x += 1
        for a in range(-1, 2):
            for b in range(-1, 2):
                if extended[y+a][x+b].is_mine:
                    count += 1
        return count

    blocked_rows = list(range(start_row-1,start_row+1))
    blocked_cols = list(range(start_col-1,start_col+1))
    minefield = generate_base()
    minefield = generate_bombs(minefield)    
    minefield = allocate_val(minefield)
    # check_mines(minefield)
    return minefield

# ================Debugging tools===============

def print_field(minefield) -> None:
    """Debugging - Prints field"""
    for y in range(ROWS):
        for x in range(COLS):
            if not minefield[y][x].exposed:
                if minefield[y][x].is_mine:
                    print("*",end=" ")
                else:
                    print(minefield[y][x].val,end=" ")
            else:
                print("X",end=" ")            
        print()

minefield = generate_minefield(5,5)
print(minefield[5][5].is_mine)
print_field(minefield)