#!/usr/bin/env python3

""" This file contains the routines to setup the battleship game
    10. Decide on size of grid and number and sizes of ships.
    12. Initially default to 10x10 size
    14. Initially default number of ships/sizes as: one each of Carrier (5), Battleship (4),
        Cruiser(3), Submarine(3), Destroyer(2).
    20. Decide on number of shots (default to one) or one per unsunk ship or one per unhit grid
    22. Decide on smart or random shooting.
    30. Place ships (random or deliberately).
    40. Display setup.
"""

# Import statements
import random
from datetime import datetime


# Initialize random number generator for ship location and orientation
random.seed(datetime.now())


# Set default values
default_x = 20  # X axis (A through J)
default_y = 20  # Y axis (1 through 10) (top left grid is A-1, bottom right grid is J-10)
random_count = 1 # initial counter if shot generation is random


# Set constants
MAX_HEADING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAX_WIDTH = 26
MAX_HEIGHT = 26
EMPTY_CHAR = "."
NO_SHOT_CHAR = " "
MISS_CHAR = "X"  
MAX_SHIP_GROUPS = 100  # maximum number of ship groups that can be selected.  Relate to grid size \
                     #  since one ship group uses 17 grids ?
MAX_TIMEOUT = 100000  # Try to configure ships 100k times; else timeout ship placement and quit session


def create_column_headings(width = default_x):
    """ Print heading for every column in grid
    Traditionally game is ten columns wide with letters A through J from left to right
    Our grid has left-most column containing row number. Its heading is "_".

    Parameters:
    width: number of columns in grid
    max_heading: maximum width string of column heading characters
    j: counter

    Return: 
    heading: list of characters for each column heading
    """

    # top left space filling character is "_"
    # heading = ["_"]
    heading = ["__"] # Need two characters wide to handle row "10"
    
    j = 0
    while j < width:
        heading.append(MAX_HEADING[j])
        j = j + 1
    return heading


def set_grid_size(max_x, max_y):
    """ Create playing grid
    (Default values to setup "Classic" game size of 10x10 grid)

    Parameters:
    max_x: width of grid/ number of columns
    max_y: height of grid/ number of rows
    max_width: set maximum width

    Return: 
    (max_x, max_y): tuple of width and height of grid
    """

    # Check range of parameters, must be > 0 and < max
    if max_x > MAX_WIDTH:
        max_x = MAX_WIDTH

    if max_y > MAX_HEIGHT:
        max_y = MAX_HEIGHT

    return (max_x, max_y)


def create_initial_empty_grid(max_x, max_y, empty_char = EMPTY_CHAR):
    """ Create the initial grid
        With every row populated with default "EMPTY" character
        Return tuple with size of grid and grid of rows

        Parameters:
        max_x: width of grid
        max_y: height of grid
        empty_char: default character for all points in grid
        x: counter for width
        y: counter for height
        row: list of values for every row
        grid: list of rows

        Return:
        (max_x, max_y, grid): tuple with grid dimensions and all contents of grid
    """
    grid = [] # Initialize game grid
        
    grid.append(create_column_headings(max_x)) # first/top row of grid is column headings

    y =  1
    while y <= max_y:     # for every row
        row = [(f"{y:02d}")]    # initialize empty row with first character as row number, must be two characters wide
        x = 0
        while x < max_x:  
            row.append(empty_char)  # create row of all default values
            x = x + 1
        grid.append(row) # Add latest row to grid
        y = y + 1
    #print_grid(max_x, max_y, grid)
    return (max_x, max_y, grid)


def print_grid(max_x, max_y, grid):
    """ Print the grid 

        Parameters:
        max_x: width of grid
        max_y: height of grid
        x: counter for width
        y: counter for height
        row: list of values for every row
        grid: list of rows

        Return:
        nothing
    """
    y = 0               # first row is the column heading
    while y <= max_y:
        print(grid[y])
        y = y + 1



def setup_ships(num = 1):
    """ Use default ship size and numbers to setup "Classic" game size
        Create tuple with unique ship type, character to place on grid, number of grid spots

        Parameters:
        num: number of five person ship groups; 0 = only one aircraft carrier; default = 1 meaning one five ship group
        ships: list of tuples in form of (ship type, grid character, number of grid spots)
        ship: counter for ships

        Return:
        ships
    """

    no_ship_group = [("aircraft carrier", "A", 5)]

    one_ship_group = [("aircraft carrier", "A", 5), ("battleship","B", 4), ("cruiser", "C", 3), \
                      ("submarine", "S", 3), ("destroyer", "D", 2)]

    """Loop through group and gather number of each ship type in descending size since larger
       ships are easier to place first
    """
    ships = []

    for s in one_ship_group:
        n = 0
        while n < num:
            ships.append(s)
            n = n + 1

    if num == 0:
        ships = no_ship_group


    #for ship in ships:
    #    (ship_type, ship_char, ship_size) = ship
        #print(ship_type, ship_char, ship_size)

    return ships


def generate_random_position(max_x, max_y):
    """ Return random number
        Top row ([0]) is reserved for column headings so range does not start with 1
        First column ([0]) is reserved for row numbers

        Parameters:
        max_x: width of grid
        max_y: height of grid
        num: random number
        x: modulo remainder of random number divided by width of grid + 1;
           so num=10 becomes x=1 aka "A" and y= 1
        y: floor of random number divided by width of grid;
           so num=109 becomes x=10 aka "J"  and y = 10

        Return:
        (x, y): tuple with random x, y co-ordinates
    """

    num = random.randint(max_x, max_x * (max_y + 1) - 1)
    x = num % max_x  + 1
    y = num // max_x
    return (x, y)


def generate_random_orientation():
    """return value of 1 through 4 inclusive
       where 1 = upward, 2 = downward, 3 = leftward, 4 = rightward

       Parameters:
       nothing passed in

       Return: 
       orientation: integer between 1 and 4 inclusive where
            1 = upward orientation
            2 = downward
            3 = leftward
            4 = rightward
    """
    orientation = random.randint(1,4)
    return orientation


def ship_overlap(max_x, max_y, grid, x, y, orientation, size, EMPTY_CHAR):
    """ Does ship overlap with an existing ship on the grid?

    Parameters:
    max_x: maximum row width
    max_y: maximum column height
    grid: list of rows 
    x: horizontal axis, left-most ship position is 1 since first column (x = 0) is row number
    y: vertical axis, top-most possible ship value is 1, top-most y=0 is column heading
    orientation: 
        Where = 1 is upwards aka "north" from random point (x,y)
        Where = 2 is downwards aka "south" from random point
        Where = 3 is leftward aka "west" from random point
        Where = 4 is rightward aka "east" from random point.
    size: number of grid spots for ship size
    EMPTY_CHAR: default character to be used for empty space

    Return:
    ship_overlap: boolean; True if grid spot already taken
    """
    
    ship_overlap = False
    if orientation == 1: # upward 
        while size > 0:
            if grid[y - size + 1][x] != EMPTY_CHAR:
                ship_overlap = True
                break
            size = size - 1
    elif orientation == 2: # downward
        while size > 0:
            if grid[y + size - 1][x] != EMPTY_CHAR:
                ship_overlap = True
                break
            size = size - 1
    elif orientation == 3: # left
        while size > 0:
            if grid[y][x - size + 1] != EMPTY_CHAR:
                ship_overlap = True
                break
            size = size - 1
    else: # (orientation == 4:) # right
        while size > 0:
            if grid[y][x + size - 1] != EMPTY_CHAR:
                ship_overlap = True
                break
            size = size - 1

    return ship_overlap


def does_ship_fit(max_x, max_y, grid, x, y, orientation, size, EMPTY_CHAR):
    """ Does ship fit on grid with this orientation at this location?

    Parameters:
    max_x: maximum row width
    max_y: maximum column height
    grid: list of rows 
    x: horizontal axis, left-most ship position is 1 since first column (x = 0) is row number
    y: vertical axis, top-most possible ship value is 1, top-most y=0 is column heading
    orientation: 
        Where = 1 is upwards aka "north" from random point (x,y)
        Where = 2 is downwards aka "south" from random point
        Where = 3 is leftward aka "west" from random point
        Where = 4 is rightward aka "east" from random point.
    size: number of grid spots for ship size

   Return:
   ship_fit: True or False     True if fits on grid, otherwise false
   """
    ship_fit = False
    if orientation == 1 and size <= y and not ship_overlap(max_x, max_y, grid, x, y, orientation, size, EMPTY_CHAR):
        ship_fit = True
    elif orientation == 2 and y + size <= max_y + 1 and not ship_overlap(max_x, max_y, grid, x, y, orientation, size, EMPTY_CHAR):
        ship_fit = True
    elif orientation == 3 and size <= x and not ship_overlap(max_x, max_y, grid, x, y, orientation, size, EMPTY_CHAR):
        ship_fit = True
    elif orientation == 4 and size + x <= max_x + 1 and not ship_overlap(max_x, max_y, grid, x, y, orientation, size, EMPTY_CHAR):
        ship_fit = True

    return ship_fit


def populate_grid(max_x, max_y, grid, x, y, orientation, size, char):
    """Change grid points from empty char to character for ship type

    Parameters:
    max_x: maximum row width
    max_y: maximum column height
    grid: list of rows
    x: horizontal axis, left-most ship position is 1 since first column (x = 0) is row number
    y: vertical axis, top-most possible ship value is 1, top-most y=0 is column heading
    orientation: 
        Where = 1 is upwards aka "north" from random point (x,y)
        Where = 2 is downwards aka "south" from random point
        Where = 3 is leftward aka "west" from random point
        Where = 4 is rightward aka "east" from random point.
    size: number of grid spots for ship size
    char: default character

   Return:
   grid: grid that now contains latest placed ship
   """
    ship_fit = False
    while size > 0:
        if orientation == 1: # upward 
            grid[y - size + 1][x] = char
            size = size - 1
        if orientation == 2: # downward
            grid[y + size - 1][x] = char
            size = size - 1
        if orientation == 3: # left
            grid[y][x - size + 1] = char
            size = size - 1
        if orientation == 4: # right
            grid[y][x + size - 1] = char
            size = size - 1
    return grid


def print_grid(max_x, max_y, grid):
    """ Print all rows

    Parameters:
        max_x: width of grid
        max_y: height of grid
        grid: list of rows
        row: counter

    Return:
        nothing
    """

    for row in grid:
        print(row)


def place_ships(max_x, max_y, grid, ships):
    """Place ships in order of largest to smallest - seems easiest.
       Generate random number which determines location
       Generate random number which determines orientation

    Parameters:
        max_x: width of grid
        max_y: height of grid
        grid: list of rows
        ships: tuple of (ship type, ship character, ship size)
        ship: counter for ships
        fit: boolean
        (x, y): tuple of random position
        orientation: 
            Where = 1 is upwards aka "north" from random point (x,y)
            Where = 2 is downwards aka "south" from random point
            Where = 3 is leftward aka "west" from random point
            Where = 4 is rightward aka "east" from random point.

    Return:
        grid
    """

    timeout_counter = 1
    timeout = False

    for ship in ships:
        (type, char, size) = ship
        fit = False
        while not fit and not timeout: 
            timeout_counter = timeout_counter + 1
            if timeout_counter > MAX_TIMEOUT:
                timeout = True
                print('SETUP TIMEOUT')

            (x, y) = generate_random_position(max_x, max_y)

            # generate random orientation for ship (up, down, left, right)
            orientation = generate_random_orientation()
   
            # Does this position and orientation fit on grid without overlapping another ship
            # If not, then generate new position and orientation and try again
            
            fit = does_ship_fit(max_x, max_y, grid, x, y, orientation, size, EMPTY_CHAR)

        populate_grid(max_x, max_y, grid, x, y, orientation, size, char)

    # All ships placed so print grid now
    # print_grid(max_x, max_y, grid)
    return (grid, timeout)


