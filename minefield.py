import pygame as pg
from random import randint
import copy 
class Cell():
    def __init__(self, coord, val, is_mine=False, is_flagged=False, exposed=False):
        self.coord = coord  # coord = (y, x) where top-left is 0,0
        self.val = val  # Number of bombs around this cell (None if is_mine)
        self.is_mine = is_mine  # Boolean
        self.is_flagged = is_flagged # Don't care for now
        self.exposed = exposed  # Sean will take care of this

def generate_field(diff: int) -> None:
    """Generates base field - 2D Array of Cell object type"""
    global size, minefield
    size = 8*diff
    minefield = []
    for x in range(size):
        row = []
        for y in range(size):
            row.append(Cell([x,y],0))
        minefield.append(row)
        
def generate_bombs(diff: int) -> None:
    """Determines number of bombs and assigns them to base field"""
    bombs = diff * 25
    for bomb in range(bombs):
        while True:
            randx=randint(0,size-1)
            randy=randint(0,size-1)
            if not minefield[randx][randy].is_mine:
                minefield[randx][randy].is_mine = True
                break

def allocate_val() -> None:
    """Allocates value of cell according to mines surrounding it using an extended field"""
    extended = copy.deepcopy(minefield)
    newtop=[]
    newbot=[]
    for i in range(size):
        newtop.append(Cell([-1,i],0))
        newbot.append(Cell([16,i],0))

    extended.insert(0,newtop)
    extended.append(newbot)

    for row in range(size+2):
        extended[row].insert(0,Cell([row-1,-1],0))
        extended[row].append(Cell([row-1,16],0))
    
    for x in range(size):
        for y in range(size):
            if minefield[x][y].is_mine:
                minefield[x][y].val=-1
            else:
                minefield[x][y].val=count_mines(x,y,extended)

def count_mines(x: int, y: int, extended: list) -> int:
    """Counts mines around a cell"""
    count=0
    x+=1
    y+=1
    for a in range(-1,2):
        for b in range(-1,2):
            if extended[x+a][y+b].is_mine:
                count+=1
    return count

"""================Debugging tools==============="""

def check_mines() -> None:
    """Debugging - Checks if the number of mines is correct"""
    count=0
    for x in range(size):
        for y in range(size):
            if minefield[x][y].is_mine:
                count+=1
                print(minefield[x][y].coord)
    print(count)

def check_field() -> None:
    """Debugging - Checks field"""
    for x in range(size):
        for y in range(size):
            print(minefield[x][y].coord, minefield[x][y].is_mine, minefield[x][y].val)
   
"""=================Main code========================"""

def generate_minefield(diff: int=2) -> list:
    """Generates random minefield - 2D Array of Cell object type"""
    generate_field(diff)
    generate_bombs(diff)    
    allocate_val()
    check_field()
    check_mines()

generate_minefield()