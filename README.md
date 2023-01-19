# Minesweeper
Our very first Pygame Project

## Updates
- Game Timer
- Bomb Counter
- Cells are now clickable
- Clicking on a 0-Cell will automatically expose the cells around
- Game Start Event when player clicks on a cell

## Current WIP
<!-- - Game Timer
    - Sean is working on this
    - As of now just get a nice working timer that starts when the program starts
    - We will implement starting only after clicking 1st cell later on -->

- `Cell`'s `.expose_around()` should **only expose unflagged cells**
    - This is to integrate with the pressing on revealed cell feature, where only unflagged cells are exposed
    - This will not negatively affect the expose_around() when the cell is 0
    - The idea is that if the player thinks there's a mine at a cell, we will not expose it for them even if they are wrong
        - We will decide on the behaviour since the classic minesweeper just removes the flag for the player instead
- Implement a `flags_around()` for `Cell` to return the number of flags around it
- Implement a `.attempt_expose_around()` in `Cell` that checks for the flags around and only call `.expose_around()` if the number of flags is correct
    - This will be called when the player clicks on an opened cell in an attempt to expose the cells around it

- Generate the minefield only after user clicks on the first cell
    - Ye Chuan can try to think of how to implement this
    - In our current implementation, having a clickable board implies already having generated the minefield (else the board wouldn't exist)
    - So one way is to create temporary minefield first, then after the player clicks we quickly generate another to replace this temporary minefield

## Future
- Game Over Screen + Handling
- Main Menu
- e.t.c.

