#!/usr/bin/env python3

""" Sections of the program are:
    100. Start game.
    120. Random shots
    140. Display shots
    200. Start displaying statistics.
    300. Update display with every shot.
    1000. Add ability to: save game mid-session,
"""

# Import statements
from setup_battleship import *
import sys


def find_available_spot(max_x, max_y, shot_grid):
    """Find location on grid to shoot
       Return that grid location

       Parameters:
       max_x:
       max_y:
       shot_grid: 

       Return:
       (x, y): shot location
    """
    game_over = False

    last_spot =  max_x * (max_y + 1) - 1
    spot = max_x 
    
    while spot <= last_spot:
        x = spot % max_x + 1
        y = spot // max_x 
        
        if x == max_x and y == max_y:
            game_over = True

        if shot_grid[y][x] == NO_SHOT_CHAR:
            break  # this is empty spot so return this value
        else:
            spot = spot + 1
            #print(shot_grid[y][x], x, y)

    return (x, y)


def find_random_even_spot(max_x, max_y, shot_grid, count):
    valid_choice = False
    while not valid_choice:
        (x, y) = generate_random_position(max_x, max_y)
     
        if shot_grid[y][x] == NO_SHOT_CHAR:
            if count <= max_x * max_y / 2 and (x+y) % 2 == 0:
                valid_choice = True
            elif count > max_x * max_y / 2: #After all even spots taken, then guess randomly
                valid_choice = True

    return (x, y, count)


def find_random_odd_spot(max_x, max_y, shot_grid, count):
    valid_choice = False
    while not valid_choice:
        (x, y) = generate_random_position(max_x, max_y)
     
        if shot_grid[y][x] == NO_SHOT_CHAR: 
            if count <= max_x * max_y / 2 and (x+y) % 2 == 1:
                valid_choice = True
            elif count > max_x * max_y / 2: #After all odd spots taken, then guess randomly
                valid_choice = True

    return (x, y, count)


def find_smart_random_spot(max_x, max_y, shot_grid, count):
    """When random shot hits ship, next shot should try to hit same ship
       by either being above or below or on either side of hit
       Try next shot above the hit, and if miss then move clockwise and try again
       If next shot also hits, then jump to opposite side.
    """
    
    # Try with just single ship
    valid_choice = False

    while not valid_choice:
        (x, y) = generate_random_position(max_x, max_y)
     
        if shot_grid[y][x] == NO_SHOT_CHAR:
            valid_choice = True

    return (x, y, count)


def find_random_spot(max_x, max_y, shot_grid, count):
    valid_choice = False

    while not valid_choice:
        (x, y) = generate_random_position(max_x, max_y)
     
        if shot_grid[y][x] == NO_SHOT_CHAR:
            valid_choice = True

    return (x, y, count)


def determine_hit_or_miss(x, y, ship_grid, shot_grid):
    if ship_grid[y][x] == EMPTY_CHAR:
        hit = False  # miss
    else:
        hit = True
    return hit


def all_ships_sunk(max_x, max_y, ship_grid, shot_grid, count):
    """Determine if all ships have been sunk
       Return boolean True or False

       Parameters:
       max_x:
       max_y:
       shot_grid: 

       Return:
       all_sunk: boolean
    """
    all_sunk = True

    last_spot =  max_x * (max_y + 1) - 1
    spot = max_x 
    
    while spot <= last_spot:
        x = spot % max_x + 1
        y = spot // max_x 
        
        if ship_grid[y][x] != EMPTY_CHAR and shot_grid[y][x] == NO_SHOT_CHAR:
            all_sunk = False # some ship spots have not been targetted yet
            break  
        else:
            spot = spot + 1
    #print("ALL SUNK=", all_sunk, "COUNT =", count)
    return all_sunk

 

def is_game_over(max_x, max_y, shot_pattern, count):
    """
    game_over = False
    count = count + 1  # increment shot counter

    if count >= max_x * max_y and shot_pattern == "top_left_to_bottom_right": 
        game_over = True  # if shot count exceeds number of grid spots then game is over
    elif count >= max_x * max_y and shot_pattern == "random":
        game_over = True  # if shot count exceeds number of grid spots then game is over
    elif count >= max_x * max_y / 2 and shot_pattern == "random_odd":
        game_over = True
    elif count >= max_x * max_y / 2 and shot_pattern == "random_even":
        game_over = True
    else:
        pass

    return(game_over, count)
    """
 
    """ Move logic to new function 'all_ships_sunk'
    See if all ships have been sunk. If yes then game is over
    """

def choose_shot(max_x, max_y, shot_grid, shot_pattern, count):
    """Select location on grid to shoot
       Return that grid location

       Parameters:
       max_x:
       max_y:
       shot_grid: 
       shot_pattern: 
       count: 

       Return:
       (x, y, game_over, count) = location of shot and boolean game over
    """
    count = count + 1

    if shot_pattern == "top_left_to_bottom_right":
        (x, y) = find_available_spot(max_x, max_y, shot_grid)
    elif shot_pattern == "random":
        (x, y, count) = find_random_spot(max_x, max_y, shot_grid, count)
    elif shot_pattern == "random_odd":
        (x, y, count) = find_random_odd_spot(max_x, max_y, shot_grid, count)
    elif shot_pattern == "random_even":
        (x, y, count) = find_random_even_spot(max_x, max_y, shot_grid, count)
    elif shot_pattern == "smart_random":
        (x, y, count) = find_smart_random_spot(max_x, max_y, shot_grid, count)

    else:
        print(shot_pattern)
        (x, y) = generate_random_position(max_x, max_y)

    return (x, y, count)


def play_game(max_x, max_y, ship_grid, shot_grid, shot_pattern, count):
    """Generate shot location and track results on shot_grid.
       If shot hits then get another free shot?
       Concentrate on damaged ship or keep shooting randomly?
       Continue until game ends.

       Parameters:
       max_x: width of grid
       max_y: height of grid
       ship_grid: grid with placed ships
       shot_grid: grid tracking shots and results (miss or hit)
       shot_pattern: how shots are determined
           Possible values are: 
               "top_left_to_bottom_right": first shot is top left and last shot is bottom right
               "random": shots selected randomly
               "random-even": sum of row number and column number add to even number
               "random-odd": sum of row number and column number add to odd number
               "manual": manually selected by player
       count: if "random" need to count how many turns have been taken

       Return:
       game_over: boolean
    """

    # (game_over, count) = is_game_over(max_x, max_y, shot_pattern, count)

    (x, y, count) = choose_shot(max_x, max_y, shot_grid, shot_pattern, count)
    
    hit = determine_hit_or_miss(x, y, ship_grid, shot_grid)
    if hit:
        shot_grid[y][x] = ship_grid[y][x] #update shot grid to show hit ship character
    else:
        shot_grid[y][x] = MISS_CHAR #update shot grid to show a miss

    return count


def show_help():
    """List all help for this program
    with explanation of expected values and order of arguments

    Parameters: none
    """
    print("First parameter is 'num=' followed by 0 through 4 inclusive for number of ship groups")
    print("Second parameter is 'pattern=' followed by possible values of 'random' or 'random_even' or 'random_odd'")
    print("For example, 'battleship.py num=2 pattern=random'")
    print("")


def handle_args(args): 
    """Handle arguments if any
    Check if "--h" or "-help" or "-h" or "--help" are included then display Help options and exit

    Arguments format is:
    "x=A" where A is width of grid (defaults to 10)
    "y=B" where B is the height of the grid (defaults to 10)
    "num=X" for X number of ship groups
    "pattern=Y" for shot_pattern Y is "random" or "random_even" or "random"odd" or "top_left_to_bottom_right" etc


    Parameters:
    args: full command line contents
    """
    game_over = False
    n = 1  # set default in case ask for help
    p = "random" # set defaults in case ask for help

    print("CLI=", args[:])

    if "--h" in args or "-help" in args or "-h" in args or "--help" in args:
        game_over = True
        show_help()

    else:
        for arg in args:
            if "x=" in arg:
                val = arg.split('=')   #split value to get string following the '=' sign
                x = int(val[1])

            if "y=" in arg:
                val2 = arg.split('=')   #split value to get string following the '=' sign
                y = int(val2[1])

            if "num=" in arg:
                val3 = arg.split('=')   #split value to get number following the '=' sign
                n = int(val3[1])

                if n > MAX_SHIP_GROUPS:
                    n = MAX_SHIP_GROUPS

            if "pattern=" in arg:
                val4 = arg.split('=')   #split value to get string following the '=' sign
                p = val4[1]

    return (game_over, x, y, n, p)



def main():
    game_over = False
    count = 0  # initialize number of shots taken
    (game_over, x, y, n, p) = handle_args(sys.argv)   # handle command line arguments
    shot_pattern = p
    print("SHOT_PATTERN=", shot_pattern)

    if game_over == False:
        # Set grid size and place ships on grid
        (max_x, max_y) = set_grid_size(x, y)
        (max_x, max_y, empty_grid) = create_initial_empty_grid(max_x, max_y, EMPTY_CHAR)
        ships = setup_ships(n)
        ship_grid = place_ships(max_x, max_y, empty_grid, ships)
        print_grid(max_x, max_y, ship_grid)
        print("")    # blank line after ship grid
        (max_x, max_y, shot_grid) = create_initial_empty_grid(max_x, max_y, NO_SHOT_CHAR)
        #print_grid(max_x, max_y, shot_grid)  #print empty shot grid

    # Start playing game 
    while not game_over:
        count = play_game(max_x, max_y, ship_grid, shot_grid, shot_pattern, count)
        game_over = all_ships_sunk(max_x, max_y, ship_grid, shot_grid, count)
        # print_grid(max_x, max_y, shot_grid)

    # if game was played (not "--h" in command line)
    if count > 0:
        print_grid(max_x, max_y, shot_grid)
        print("")

    print(shot_pattern,"     ", "GAME OVER","     "," SHIP GROUPS=", n, "    ", "COUNT=", count)

if __name__ == "__main__":
    main()
