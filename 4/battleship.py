#################################################################
# FILE : battleship.py
# WRITER : Dori_Peleg , dori.plg , 207685306
# EXERCISE : intro2cs ex3 2024
# DESCRIPTION: BATTLESHIPS
# STUDENTS I DISCUSSED THE EXERCISE WITH: Gilad Zomer
# WEB PAGES I USED:
# NOTES: ...
#################################################################

import helper

PLAYER_WINS = 1
CPU_WINS = -1
TIE = 0

def init_board(rows, columns):
    """creates and returns a board"""
    board = []
    for _ in range(rows):
        board.append([helper.WATER]*columns)
    return board


def cell_loc(name):
    """turns lexic locations to tupled coordinates"""
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if helper.is_int(name[1:]) and name[0].upper() in ALPHABET:
        return (int(name[1:])-1), ALPHABET.find(name[0].upper())
    else:
        return cell_loc(helper.get_input("Problem with the input. Retry:  "))


def valid_ship(board, size, loc):
    """Checks if a ship placement is valid"""
    if (len(board) - loc[0] < size) or (len(board[0]) - loc[1] < 1):
        return False
    for i in range(size):
        if board[loc[0]+i][loc[1]] != helper.WATER:
            return False
    return True

def ask_player_for_boat(player_board,ship_size, msg):
    """reduces repetitivity, asks the user to place a ship while displaying a message"""
    helper.print_board(player_board)
    return  cell_loc(helper.get_input(
            "Place a ship " + str(ship_size) + " units long.\n"+msg))

def place_ship(ship_size, board, chosen_location):
    """places a ship in a desired location"""
    for i in range(ship_size):
        board[chosen_location[0]+i][chosen_location[1]] = helper.SHIP
    return board

def create_player_board(rows, columns, ship_sizes):
    """Allows the user to place his battleships!"""
    player_board = init_board(rows, columns)
    for ship_size in ship_sizes:
        user_input = ask_player_for_boat(player_board, ship_size, "Write in XN format.  ")
        while not valid_ship(player_board,ship_size,user_input):
            user_input = ask_player_for_boat(player_board, ship_size, "The previous location was problematic, retry.  ")
        player_board = place_ship(ship_size,player_board,user_input)
    return player_board

def fire_torpedo(board, loc):
    """the actual play of the game"""
    if (0<= loc[0] < len(board)) and (0<= loc[1] < len(board[0])):
        if board[loc[0]][loc[1]] == helper.WATER:
            board[loc[0]][loc[1]] = helper.HIT_WATER
        elif board[loc[0]][loc[1]] == helper.SHIP:
            board[loc[0]][loc[1]] = helper.HIT_SHIP
    else:  # Something here?
        return fire_torpedo(board,cell_loc(helper.get_input("Invalid location, retry:  ")))
    return board

def get_locations_torpedo(board):
    """returns a list of all legitimate locations in a board"""
    loc_list = []
    for (i,row) in enumerate(board):
        for (j,coord) in enumerate(row):
            if coord == helper.WATER or coord == helper.SHIP:
                loc_list.append((i,j))
    return tuple(loc_list)

def get_locations_ship(board,size):
    """returns a list of all legitimate locations in a board"""
    loc_list = []
    for i in range(len(board)-size+1):
        for j in range(len(board[i])):
            lst = [board[i+p][j] for p in range(size)]
            if all(p == helper.WATER for p in lst):
                loc_list.append((i,j))
    return tuple(loc_list)

def rival_board(board, ship_sizes):
    """generates a random computer rival"""
    for ship_size in ship_sizes:
        random_location = helper.choose_ship_location(board,ship_size,
                                                      get_locations_ship(board,ship_size))
        board = place_ship(ship_size,board,random_location)
    return board


def board_hider(board):
    """Neccessary to hide rival boards"""
    hidden = []
    for i,row in enumerate(board):
        hidden.append([])
        for spot in row:
            if spot == helper.SHIP:
                hidden[i].append(helper.WATER)
            else:
                hidden[i].append(spot)
    return hidden


def fleet_status(board, fleet = helper.SHIP_SIZES):
    """made to check if a fleet is still operative"""
    count = 0
    for row in board:
        for spot in row:
            if spot == helper.HIT_SHIP:
                count += 1
    sum_of_ships = 0
    for ship in fleet:
        sum_of_ships += ship
    return sum_of_ships <= count

def check_game_status(cpu_board, player_board):
    """recieves two boards and decides if the game has come to an end, and the outcome"""
    game_active, game_result = True, None
    if fleet_status(cpu_board):
        game_active=False
        game_result=PLAYER_WINS
    if fleet_status(player_board):
        game_active=False
        game_result = CPU_WINS
        if fleet_status(cpu_board):
            game_result = TIE
    return game_active, game_result

def game_start():
    """sets the table for a game of battleships"""
    player_board = init_board(helper.NUM_ROWS,helper.NUM_COLUMNS)
    cpu_board = init_board(helper.NUM_ROWS,helper.NUM_COLUMNS)
    player_board = create_player_board(helper.NUM_ROWS,helper.NUM_COLUMNS,helper.SHIP_SIZES)
    cpu_board = rival_board(cpu_board,helper.SHIP_SIZES)
    helper.print_board(player_board,board_hider(cpu_board))
    return player_board, cpu_board

def game_step(player_board, cpu_board):
    """every turn of the game for both players"""
    cpu_board = fire_torpedo(cpu_board,
                             cell_loc(helper.get_input("Select a target to strike  ")))
    player_board = fire_torpedo(player_board,
                                helper.choose_torpedo_target(board_hider(player_board), 
                                                             get_locations_torpedo(player_board)))
    helper.print_board(player_board,board_hider(cpu_board))
    return player_board, cpu_board

def main():
    """the game"""
    player_board, cpu_board = game_start()
    game_active = True
    while game_active:
        player_board, cpu_board = game_step(player_board,cpu_board)
        game_active, game_result = check_game_status(cpu_board,player_board)
    end_game(game_result)


def end_game(game_result):
    """declares the winner and restarts the game if desired"""
    if game_result == PLAYER_WINS:
        user_input = helper.get_input("You won! Do you wish to play again? Y/N\n")
    elif game_result == CPU_WINS:
        user_input = helper.get_input("CPU won, nevertheless, do you wish to play again? Y/N\n")
    elif game_result == TIE:
        user_input = helper.get_input("You both lost, do you wish to play again? Y/N\n")
    while user_input!="Y" and user_input!="N":
        user_input = helper.get_input("Please answer properly, do you wish to play again? Y/N\n")
    if user_input == "Y":
        main()


if __name__ == "__main__":
    main()
