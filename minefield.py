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
    for y in range(size):
        row = []
        for x in range(size):
            row.append(Cell([y,x],0))
        minefield.append(row)
        
def generate_bombs(diff: int) -> None:
    """Determines number of bombs and assigns them to base field"""
    bombs = diff * 25
    for bomb in range(bombs):
        while True:
            randy=randint(0,size-1)
            randx=randint(0,size-1)
            if not minefield[randy][randx].is_mine:
                minefield[randy][randx].is_mine = True
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
    
    for y in range(size):
        for x in range(size):
            if minefield[y][x].is_mine:
                minefield[y][x].val=-1
            else:
                minefield[y][x].val=count_mines(y,x,extended)

def count_mines(y: int, x: int, extended: list) -> int:
    """Counts mines around a cell"""
    count=0
    y+=1
    x+=1
    for a in range(-1,2):
        for b in range(-1,2):
            if extended[y+a][x+b].is_mine:
                count+=1
    return count

"""================Debugging tools==============="""

def check_mines() -> None:
    """Debugging - Checks if the number of mines is correct"""
    count=0
    for y in range(size):
        for x in range(size):
            if minefield[y][x].is_mine:
                count+=1
                print(minefield[y][x].coord)
    print(count)

def print_field() -> None:
    """Debugging - Prints field"""
    for y in range(size):
        for x in range(size):
            if minefield[y][x].exposed:
                if minefield[y][x].is_mine:
                    print("*",end=" ")
                else:
                    print(minefield[y][x].val,end=" ")
            else:
                print("X",end=" ")            
        print()

            

   
"""=================Main code========================"""

def generate_minefield(diff: int=2) -> list:
    """Generates random minefield - 2D Array of Cell object type"""
    generate_field(diff)
    generate_bombs(diff)    
    allocate_val()
    print_field()
    #check_mines()

generate_minefield()