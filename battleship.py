#!/usr/bin/env python3

""" Sections of the program are:
    10. Decide on size of grid and number and sizes of ships.
    12. Initially default to 10x10 size 
    14. Initially default number of ships/sizes as: one each of Carrier (5), Battleship (4), 
        Cruiser(3), Submarine(3), Destroyer(2).
    20. Decide on number of shots (default to one) or one per unsunk ship or one per unhit grid space
    22. Decide on smart or random shooting.
    30. Place ships (random or deliberately).
    40. Display setup.
    100. Start game.
    200. Start displaying statistics.
    300. Update display with every shot.
    1000. Add ability to: save game mid-session, 
"""

# Import statements
import os


# Set default values
default_x = 10  # X axis (A through J)
default_y = 10  # Y axis (1 through 10) (top left grid point is A-1, bottom right grid point is J-10)
biggest_ship = 5
big_ship = 4
medium_ship_1 = 3
medium_ship_2 = 3
smallest_ship = 2

def print_column_heading():
    col = "ABCDEFGHIJ"
    heading =[0]
    for j in col:
        heading.append(j)
    print(heading)


def setup_grid():
    """ Use default values to setup "Classic" game size of 10x10 grid"""
    max_x = default_x
    max_y = default_y

    print_column_heading()
    y = 1
    while y <= max_y:
        row = [y]           # first value in row is row number (1 to max_y)
        x = 1
        while x <= max_x:
            row.append("O")
            x = x + 1
        print(row)    
        y = y + 1
    pass

def setup_ships():
    """ Use default ship size and numbers to setup "Classic" game size"""
    ships = []
    pass


def main():
    setup_grid()
    setup_ships()


main()
