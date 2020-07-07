#!/usr/bin/env python3

""" Sections of the program are:
    10. Decide on size of grid and number and sizes of ships.
    12. Initially default to 10x10 size
    14. Initially default number of ships/sizes as: one each of Carrier (5), Battleship (4),
        Cruiser(3), Submarine(3), Destroyer(2).
    20. Decide on number of shots (default to one) or one per unsunk ship or one per unhit grid
    22. Decide on smart or random shooting.
    30. Place ships (random or deliberately).
    40. Display setup.
    100. Start game.
    200. Start displaying statistics.
    300. Update display with every shot.
    1000. Add ability to: save game mid-session,
"""

# Import statements
import random
from datetime import datetime


# Initialize random number generator for ship location and orientation
random.seed(datetime.now())


# Set default values
default_x = 10  # X axis (A through J)
default_y = 10  # Y axis (1 through 10) (top left grid is A-1, bottom right grid is J-10)


def print_column_headings(width = default_x):
    """ Print heading for every column in grid
    Traditionally game is ten columnx wide with letters A through J from left to right

    Parameters:
    width: number of columns in grid
    heading: value to be printed
    Return: nothing
    """
    col = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    heading = [0]
    j = 0
    while j < width:
        heading.append(col[j])
        j = j + 1
    print(heading)


def setup_grid():
    """ Create playing grid
    Default values to setup "Classic" game size of 10x10 grid
    """
    max_x = default_x
    max_y = default_y
    return (max_x, max_y)

def print_empty_grid(max_x, max_y):
    print_column_headings()
    y = 0
    row = []
    while y < max_y:
        r = [y]           # first value in row is row number (0 to max_y - 1)
        x = 1
        while x <= max_x:
            r.append("O")
            x = x + 1
        row.append(r)
        print(row[y])    
        y = y + 1
    return row

def setup_ships():
    """ Use default ship size and numbers to setup "Classic" game size
        Create tuple with unique ship type, character to place on grid, number of grid spots
    """
    ships = [("aircraft carrier", "A", 5), ("battleship","B", 4), ("cruiser", "C", 3), \
            ("submarine", "S", 3), ("destroyer", "D", 2)]
    for ship in ships:
        (a, b, c) = ship
        print(a, b, c)
    return ships


def generate_random_position(max_x, max_y):
    num = random.randint(1, max_x * max_y)
    x = num % max_x
    y = num // max_x
    print(" ")
    print(num, "translates to x=", x, "and y=", y)
    return (x, y)


def generate_random_orientation():
    """return value of 1 through 4 inclusive
       where 1 = up, 2 = down, 3 = left, 4 = right
       if that does not fit then try the next orientation
    """
    orient = random.randint(1,4)
    return orient


def does_it_fit(x, y, max_x, max_y, orientation, size):
    """ Does ship fit on grid with this orientation at this location?

    Parameters:
    x: horizontal axis, value between 0 and max_x, left-most position = 0
    y: vertical axis, value between 0 and max_y, top-most position = 0
    max_x: maximum row width
    max_y: maximum column height
    orientation: 
        Where = 1 is upwards aka "north" from random point (x,y)
        Where = 2 is downwards aka "south" from random point
        Where = 3 is leftward aka "west" from random point
        Where = 4 is rightward aka "east" from random point.

   Return:
   fit: True or False     True if fits on grid, otherwise false
   """
    fit = False
    if orientation == 1 and size <= y:
        fit = True
    if orientation == 2 and y + size <= max_y:
        fit = True
    if orientation == 3 and size <= max_x:
        fit = True
    if orientation == 4 and size + x <= max_x:
        fit = True
    return fit



def populate_grid(x, y, orient, size, char, row):
    """Change grid points from empty ("0") to char for ship
    """
    while size > 0:
        if orient == 1: # upward 
            row[y - size][x] = char
            size = size - 1
        if orient == 2: # downward
            row[y + size][x] = char
            size = size - 1
        if orient == 3: # left
            row[y][x - size] = char
            size = size - 1
        if orient == 4: # right
            row[y][x + size] = char
            size = size - 1


def print_grid(max_x, max_y, row):
    """ Print all rows now that they are populated"""
    for r in row:
        print(r)


def place_ships(max_x, max_y, ships, row):
    """Place ships in order of largest to smallest - seems easiest.
       Generate random number which determines location
    """
    for ship in ships:
        (type, char, size) = ship
        fit = False
        while not fit:
            (x, y) = generate_random_position(max_x, max_y)

            # choose random orientation for ship (up, down, left, right)
            orient = generate_random_orientation()

            # Does this position and orientation fit on grid?
            fit = does_it_fit(x, y, max_x, max_y, orient, size)
            print("FIT=",fit, "ORIENT=",orient,"SIZE=", size)

        populate_grid(x, y, orient, size, char, row)

        print_column_headings()
        print_grid(max_x, max_y, row)

def main():
    (x, y) = setup_grid()
    row = print_empty_grid(x, y)
    ships = setup_ships()
    place_ships(x, y, ships, row)


if __name__ == "__main__":
    main()
