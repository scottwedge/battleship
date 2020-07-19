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
     
        if shot_grid[y][x] == NO_SHOT_CHAR and (x+y) % 2 == 0:
            valid_choice = True

    return (x, y, count)


def find_random_odd_spot(max_x, max_y, shot_grid, count):
    valid_choice = False
    while not valid_choice:
        (x, y) = generate_random_position(max_x, max_y)
     
        if shot_grid[y][x] == NO_SHOT_CHAR and (x+y) % 2 == 1:
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
 

def is_game_over(max_x, max_y, shot_pattern, count):
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

    if shot_pattern == "top_left_to_bottom_right":
        (x, y) = find_available_spot(max_x, max_y, shot_grid)
    elif shot_pattern == "random":
        (x, y, count) = find_random_spot(max_x, max_y, shot_grid, count)
    elif shot_pattern == "random_odd":
        (x, y, count) = find_random_odd_spot(max_x, max_y, shot_grid, count)
    elif shot_pattern == "random_even":
        (x, y, count) = find_random_even_spot(max_x, max_y, shot_grid, count)

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

    (game_over, count) = is_game_over(max_x, max_y, shot_pattern, count)

    (x, y, count) = choose_shot(max_x, max_y, shot_grid, shot_pattern, count)
    
    hit = determine_hit_or_miss(x, y, ship_grid, shot_grid)
    if hit:
        shot_grid[y][x] = ship_grid[y][x] #update shot grid to show hit ship character
    else:
        shot_grid[y][x] = MISS_CHAR #update shot grid to show a miss

    return (game_over, count)



def main():
    # Set grid size and place ships on grid
    (max_x, max_y) = set_grid_size()
    (max_x, max_y, empty_grid) = create_initial_empty_grid(max_x, max_y, EMPTY_CHAR)
    ships = setup_ships()
    ship_grid = place_ships(max_x, max_y, empty_grid, ships)
    print_grid(max_x, max_y, ship_grid)
    (max_x, max_y, shot_grid) = create_initial_empty_grid(max_x, max_y, NO_SHOT_CHAR)
    print_grid(max_x, max_y, shot_grid)

    # Start playing game 

    #shot_pattern = "top_left_to_bottom_right"
    #shot_pattern = "random"
    #shot_pattern = "random_odd"
    shot_pattern = "random_even"

    game_over = False
    count = 0  # initialize number of shots taken

    while not game_over:
        (game_over, count) = play_game(max_x, max_y, ship_grid, shot_grid, shot_pattern, count)
        #print_grid(max_x, max_y, shot_grid)

    print_grid(max_x, max_y, shot_grid)

    print("GAME OVER")

if __name__ == "__main__":
    main()
