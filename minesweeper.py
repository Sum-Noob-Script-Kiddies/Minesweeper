
ROWS, COLS = 16, 16

# Sean's Part
class Cell():
    def __init__(self, coord, val, is_mine=False, is_flagged=False, exposed=False):
        self.coord = coord  # coord = (y, x) where top-left is 0,0
        self.val = val  # Number of bombs around this cell (None if is_mine)
        self.is_mine = is_mine  # Boolean
        self.is_flagged = is_flagged # Don't care for now
        self.exposed = exposed  # Sean will take care of this
 
    def expose(self, minefield):
        # Sean will work on this
        # Expose this cell and other cells around it if 0
        pass


# Melvin's Part
# Create a ROWS x COLS (defined as 16x16 above) of Cell objects
# Below is some example code in case you're not sure how to instantiate the cells, feel free to delete
minefield = [[None]*COLS for _ in range(ROWS)]  # Creates a ROWS x COLS matrix of Nones
for row in range(ROWS):
    for col in range(COLS):
        minefield[row][col] = Cell((row, col), 5)   # This will make it such that every cell has a value of 5



