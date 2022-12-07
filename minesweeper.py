
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
        """Expose this cell and other cells around it if 0"""
        visiting = [self]
        if self.is_mine:
            print("Lose")
            return
        if not self.exposed:
            if self.val == 0:
                while visiting:
                    cur_cell = visiting.pop()
                    cur_cell.exposed = True
                    y,x = (cur_cell.coord[0]-1, cur_cell.coord[0]+2), (cur_cell.coord[1]-1, cur_cell.coord[1]+2)
                    if y[0] < 0:
                        y[0] = 0
                    if y[1] > ROWS:
                        y[1] = ROWS
                    if x[0] < 0:
                        x[0] = 0
                    if x[1] > COLS:
                        x[1] = COLS
                    for i in range(y[0], y[1]):
                        for j in range(x[0], x[1]):
                            if not minefield[i][j].exposed and minefield[i][j].val == 0:
                                visiting.append(minefield[i][j])
                            else:
                                minefield[i][j].exposed = True
            else:
                self.exposed = True

    def expose2(self, minefield):
        """Expose this cell and other cells around it if 0 recursively"""
        if self.exposed:
            return 
        if self.is_mine:
            print("Lose")
        self.exposed = True
        if self.val == 0:
            y, x = (self.coord[0]-1, self.coord[0]+2), (self.coord[1]-1, self.coord[1]+2)
            y = max(y[0],0), min(ROWS,y[1])
            x = max(x[0],0), min(COLS,x[1])
            for i in range(y[0], y[1]):
                for j in range(x[0], x[1]):
                    minefield[i][j].expose2()
        


# Melvin's Part
# Create a ROWS x COLS (defined as 16x16 above) of Cell objects
# Below is some example code in case you're not sure how to instantiate the cells, feel free to delete
minefield = [[None]*COLS for _ in range(ROWS)]  # Creates a ROWS x COLS matrix of Nones
for row in range(ROWS):
    for col in range(COLS):
        minefield[row][col] = Cell((row, col), 5)   # This will make it such that every cell has a value of 5



