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


# Initialize random number generator
random.seed(datetime.now())


# Set default values
default_x = 10  # X axis (A through J)
default_y = 10  # Y axis (1 through 10) (top left grid is A-1, bottom right grid is J-10)


def print_column_heading():
    col = "ABCDEFGHIJ"
    heading = [0]
    for j in col:
        heading.append(j)
    print(heading)


def setup_grid():
    """ Use default values to setup "Classic" game size of 10x10 grid"""
    max_x = default_x
    max_y = default_y
    return (max_x, max_y)

def print_empty_grid(max_x, max_y):
    print_column_heading()
    y = 0
    while y < max_y:
        row = [y]           # first value in row is row number (0 to max_y - 1)
        x = 1
        while x <= max_x:
            row.append("O")
            x = x + 1
        print(row)    
        y = y + 1

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
    print(num, "translates to x=", x, "and y=", y)
    return (x, y)


def generate_random_orientation():
    """return value of 1 through 4 inclusive
       where 1 = up, 2 = down, 3 = left, 4 = right
       if that does not fit then try the next orientation
    """
    orient = random.randint(1,4)
    return orient


def does_it_fit_on_grid(x, y, max_x, max_y, orient, size):
    # does it fully fit on grid?
    count = 4
    fit = False
    while not fit and count > 0:
        if orient == 1: # see if ship fits with upward orientation
            if y >= size: 
                fit = True
                return (fit, orient) # fits 
            else:
                orient = orient + 1 # try next orientation
                count = count - 1

        if orient == 2: # does it fit with downward orientation
            if y + size <= max_y:
                fit = True
                return (fit, orient) # fits 
            else:
                orient = orient + 1 # try next orientation
                count = count - 1

        if orient == 3: # does it fit with left orientation
            if x >= size:
                fit = True
                return (fit, orient) # fits 
            else:
                orient = orient + 1 # try next orientation
                count = count - 1
    
        if orient == 4: # does it fit with right orientation
            if x + size <= max_x:
                fit = True
                return (fit, orient) # fits 
            else:
                orient = 1 # try first orientation
                count = count - 1


def populate_grid(x, y, orient, size, char):
    pass


def place_ships(max_x, max_y, ships):
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

            # see which orientation fits on grid
            (fit, orient) = does_it_fit_on_grid(x, y, max_x, max_y, orient, size)

        populate_grid(x, y, orient, size, char)

def main():
    (x, y) = setup_grid()
    print_empty_grid(x, y)
    ships = setup_ships()
    place_ships(x, y, ships)


if __name__ == "__main__":
    main()
