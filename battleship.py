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
    """Select a spot for the shot where x + y is even so
       select every second spot on the diagonal so quickly cover half the grid
       If spot was chosen previously, must select another spot

       Parameters:
       max_x: width of grid
       max_y: height of grid
       shot_grid: record of shots already taken
       count: number of shots already taken

       Return:
       (x, y, count): tuple with shot locations x,y and updated count of shots taken
    """
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
    """Select a spot for the shot where x + y is odd so
       select every second spot on the diagonal so quickly cover half the grid
       If spot was chosen previously, must select another spot

       Parameters:
       max_x: width of grid
       max_y: height of grid
       shot_grid: record of shots already taken
       count: number of shots already taken

       Return:
       (x, y, count): tuple with shot locations x,y and updated count of shots taken

    """
    valid_choice = False
    while not valid_choice:
        (x, y) = generate_random_position(max_x, max_y)
     
        if shot_grid[y][x] == NO_SHOT_CHAR: 
            if count <= max_x * max_y / 2 and (x+y) % 2 == 1:
                valid_choice = True
            elif count > max_x * max_y / 2: #After all odd spots taken, then guess randomly
                valid_choice = True

    return (x, y, count)


def update_orientation(orient, current):
    """Determine the orientation(s) of the ship or ships adjacent to hit
       by checking all four spots adjacent to hit spot

       If orientation is already "both" it cannot change.
       If "none", set it to whatever has been discovered adjacent.
       If it is already "vertical" but adjacent horizontal exists then change to "both"
       If if is already "horizontal" but adjacent vertical exists then change to "both"

       Parameters:
       orient: existing orientation ("none", "vertical", "horizontal", "both")
       current: orientation of latest adjacent hit

       Return: 
       orient: updated orientation value
    """

    if orient != "both": # cannot add if state is "both"
        if orient == "none":
            orient = current    # set to current orientation
        elif orient == "vertical" and current =="horizontal":
            orient = "both"     # both orientations are possible
        elif orient == "horizontal" and current == "vertical":
            orient = "both"       # both orientations are possible
        fi
    fi

    return orient


def adjacent_hit(last_hit_xy, shot_grid):
    """Determine if an adjacent row or column exists and if there was a previous hit 
       adjacent to latest hit.

       That is a good indication that the same ship was hit so we
       can guess what orientation the ship has.

       There is a small chance that the adjacent hit is on a different ship so also
       need to handle that scenario.

       Parameters:
       last_hit_xy: (x, y) tuple with coordinates of last hit
       shot_grid: record of all previous shots

       Return:
       a_hit: boolean - True if there was an adjacent hit 
       orientation: "none", "vertical", "horizontal" or "both"
    """
    a_hit = False
    orient = "none"

    #Check if row above exists and was a hit
    if y >= 2:
        if shot_grid[x][y - 1] != (NO_SHOT_CHAR or MISS_CHAR):
            a_hit = True  # adjacent shot above is hit so ship orientation is vertical
            orient = update_orientation (orient, "vertical")

    # Check if column exists to right and was a hit
    if x <= 9:
        if shot_grid[x + 1][y] != (NO_SHOT_CHAR or MISS_CHAR):
            a_hit = True  # adjacent shot above is to right so ship orientation is horizontal
            orient = update_orientation (orient, "horizontal")

    #Check if row below exists and was a hit
    if y <= 9:
        if shot_grid[x][y + 1] != (NO_SHOT_CHAR or MISS_CHAR):
            a_hit = True  # adjacent shot below is hit so ship orientation is vertical
            orient = update_orientation (orient, "vertical")

    # Check if column exists to left and was a hit
    if x >= 2:
        if shot_grid[x - 1][y] != (NO_SHOT_CHAR or MISS_CHAR):
            a = True  # adjacent shot above is to left so ship orientation is horizontal
            orient = update_orientation (orient, "horizontal")

    return (a_hit, orient)


def try_to_sink_ship (last_hit_xy, shot_grid, count):
    """Since last shot hit ship and did not sink it, search for adjacent shots that have also hit.
       If those shots are found, determine the orientation of the ship and try on either side of the hits.
       If no adjacent hits, then start one row above in grid (if row exists) and then work clockwise.

       Parameters:
       last_hit_xy: tuple with (x, y) co-ordinates of hit on ship
       shot_grid: record of previous shots (so not overlap)
       count: count of total shots taken

       Return:
       (x, y, count): next shot to take and incremented count
    """

    (a_hit, orient) =  adjacent_hit(last_hit_xy, shot_grid)

    if a_hit == True:
        (x, y) = determine_next_smart_shot(last_hit_xy, shot_grid, orient)
    else:
        (x, y) = determine_next_smart_shot(last_hit_xy, shot_grid, orient)

    return (x, y)



def find_smart_random_spot(max_x, max_y, shot_grid, count, last_hit_xy, last_shot_xy):
    """Start game with random shots or after a ship sinks.
    
       When random shot hits ship, next shot should try to hit same ship
       by either being above or below or on either side of first hit.

       If there are already two hits side by side then the smart shot is to try to get third 
       and fourth etc hits along that (vertical or horizontal) line until the ship sinks.

       If just a single hit, there is no "best guess" at the next shot,  so start with shot 
       above and move clockwise and try again

       If next shot also hits, then figure out ship orientation and shot along that track.

       So unlike other random shot selections, this function needs to track last successful hit 
       so that next attempt can be based on that information.

       Several ways to record last hit: either x,y co-ordinates or mark that somehow on shot_grid.

       Parameters:
       max_x: width of grid
       max_y: height of grid
       shot_grid: record of shots already taken
       count: number of shots already taken
       last_hit_xy: x,y co-ordinates tuple of last hit
       last_shot_xy: x,y co-ordinates tuple of last shot

       Return:
       (x, y, count): tuple with shot locations x,y and updated count of shots taken
    """
    
    valid_choice = False

    while not valid_choice:
        if last_hit_xy == (0,0): # if no previous shots have hit then take random shot
            (x, y) = generate_random_position(max_x, max_y)  # take random shots when game starts or after a ship sinks
     
            if shot_grid[y][x] == NO_SHOT_CHAR:
                valid_choice = True
        else:
            (x, y) = try_to_sink_ship (last_hit_xy, shot_grid, count)

    print(x, y, count, "DEBUG_A")
    return (x, y, count)


def find_random_spot(max_x, max_y, shot_grid, count):
    """Select a random spot for the shot
       If spot was chosen previously, must select another spot

       Parameters:
       max_x: width of grid
       max_y: height of grid
       shot_grid: record of shots already taken
       count: number of shots already taken

       Return:
       (x, y, count): tuple with shot locations x,y and updated count of shots taken

    """
    valid_choice = False

    while not valid_choice:
        (x, y) = generate_random_position(max_x, max_y)
     
        if shot_grid[y][x] == NO_SHOT_CHAR:
            valid_choice = True

    return (x, y, count)


def determine_hit_or_miss(x, y, ship_grid, shot_grid):
    """Figure out if the shot landed in an empty spot
       or where a ship is located.

    Parameters:
       x: horizontal location of shot
       y: vertical location of shot
       ship_grid: grid with ship locations
       shot_grid: grid tracking shots

       Return: hit (boolean) whether shot is a hit (True) or a miss (False)
    """

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

def choose_shot(max_x, max_y, shot_grid, shot_pattern, count, last_hit_xy, last_shot_xy):
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
        (x, y, count) = find_smart_random_spot(max_x, max_y, shot_grid, count, last_hit_xy, last_shot_xy)

    else:
        print(shot_pattern)
        (x, y) = generate_random_position(max_x, max_y)

    return (x, y, count)


def play_game(max_x, max_y, ship_grid, shot_grid, shot_pattern, count, last_hit_xy, last_shot_xy):
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

    (x, y, count) = choose_shot(max_x, max_y, shot_grid, shot_pattern, count, last_hit_xy, last_shot_xy)
    
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
    print("All parameters are optional. ")
    print("Parameter to set grid width is 'x=' followed by number 5 through 26 inclusive")
    print("Parameter to set grid height is 'y=' followed by number 5 through 26 inclusive")
    print("One parameter is 'num=' followed by 0 through 4 inclusive for number of ship groups")
    print("Another parameter is 'pattern=' followed by possible values of 'random' or 'random_even' or 'random_odd'")
    print("For example, 'battleship.py x=20 y=15 num=2 pattern=random'")
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
        x=0
        y=0
        show_help()

    else:
        game_over = False # initialize
        x=10  # initialize optional variable
        y=10  # initialize optional variable
        n=1 # initialize optional variable
        p="random" # initialize optional variable
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
    max_x = 0
    max_y = 0
    count = 0  # initialize number of shots taken
    last_hit_xy = (0, 0) # initialize
    last_shot_xy = (0, 0)  # Initialize
    (game_over, x, y, n, p) = handle_args(sys.argv)   # handle command line arguments
    shot_pattern = p
    print("SHOT_PATTERN=", shot_pattern)

    if game_over == False:
        # Set grid size and place ships on grid
        (max_x, max_y) = set_grid_size(x, y)
        (max_x, max_y, empty_grid) = create_initial_empty_grid(max_x, max_y, EMPTY_CHAR)
        ships = setup_ships(n)
        (ship_grid, timeout) = place_ships(max_x, max_y, empty_grid, ships)
        
        if timeout:
            game_over = True

        print_grid(max_x, max_y, ship_grid)
        print("")    # blank line after ship grid
        (max_x, max_y, shot_grid) = create_initial_empty_grid(max_x, max_y, NO_SHOT_CHAR)
        #print_grid(max_x, max_y, shot_grid)  #print empty shot grid

    # Start playing game 
    while not game_over:
        count = play_game(max_x, max_y, ship_grid, shot_grid, shot_pattern, count, last_hit_xy, last_shot_xy)
        game_over = all_ships_sunk(max_x, max_y, ship_grid, shot_grid, count)
        # print_grid(max_x, max_y, shot_grid)

    # if game was played (not "--h" in command line)
    if count > 0:
        print_grid(max_x, max_y, shot_grid)
        print("")

    print(shot_pattern,"     ", "GAME OVER","     "," SHIP GROUPS=", n, "    ", "COUNT=", count, "of", max_x * max_y)

if __name__ == "__main__":
    main()
