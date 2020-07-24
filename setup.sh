#!/usr/bin/env python3


def setup_ships(num = 1):

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
            print(s)
            n = n + 1

    if num == 0:
        ships = no_ship_group


    #for ship in ships:
    #    (ship_type, ship_char, ship_size) = ship
        #print(ship_type, ship_char, ship_size)

    return ships


setup_ships(4)
