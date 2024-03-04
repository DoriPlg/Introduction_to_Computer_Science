#################################################################
# FILE : game.py
# WRITER : Dori_Peleg , dori.plg , 207685306
# EXERCISE : intro2cs ex9 2024
# DESCRIPTION: This file creates the game class for the "rush hour" game
# STUDENTS I DISCUSSED THE EXERCISE WITH: Hadar Soffer
# WEB PAGES I USED:
# NOTES: note the hiddenness of the API and the constants for each class
#################################################################


import sys
from board import Board
from helper import load_json
from car import Car


DEFAULT_PATH = "/home/dori/Documents/UNI/Intro/Exercise/9/additional_files/car_config.json"
ORIENTATION = {0,1}
EXIT_KEY = "!"
CAR_LENGTHS = (2,3,4)
CAR_NAMES = ('Y','B','O','W','G','R')
DIRECTIONS = ('u','d','l','r')
BREAK_CHAR ="!"

class Game:
    """
    The game of "Rush Hour".
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __get_user_move(self) -> tuple[str,str]:
        """
        Gets a users desired move and returns it a tuple of car and direction
        """
        split_user_input = input(
            "Which car do you want to move?\n" +
            "Write in NAME,DIRECTION format\n" +
            f"name can only be {CAR_NAMES}\n" +
            f"direction can only be {DIRECTIONS}\n").split(",")
        if len(split_user_input) == 1 and split_user_input[0] == BREAK_CHAR:
            return split_user_input
        if len(split_user_input) == 2:
            arg1, arg2 = split_user_input
        else:
            arg1, arg2 =  " ", " "
        while not (arg1 in CAR_NAMES and arg2 in DIRECTIONS):
            split_user_input = input("The input was improper, retry:  ").split(",")
            if split_user_input == BREAK_CHAR:
                return split_user_input
            if len(split_user_input) == 2:
                arg1,arg2 = split_user_input
        return (arg1,arg2)

    def __valid_move(self, move: tuple[str,str]) -> bool:
        """
        ensures that a desired move is possible
        """
        return move in [(possible_move[0],possible_move[1]) for possible_move in self.__board.possible_moves()]

    def __win(self):
        """
        checks if the game has been won
        """
        return  self.__board.cell_content(
            self.__board.target_location()) is not None

    def play(self) -> None:
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while not self.__win():
            print(self.__board)
            user_input = self.__get_user_move()
            if user_input[0] == BREAK_CHAR:
                break
            while not self.__valid_move(user_input):
                print("invalid move")
                user_input = self.__get_user_move()
            if not self.__board.move_car(*user_input):
                print("\nIt seems you're trying to move a car out of bounds. Retry\n")
        if self.__win():
            print("\nGood Job!!")

def json_to_board(path):
    """generates the board for the game from a given json"""
    example = load_json(path)
    board = Board()
    for car in example.items():
        car_name = car[0]
        car_length, car_location, car_orientation = [x for x in car[1]]
        if (car_name in CAR_NAMES
            and car_length in CAR_LENGTHS
            and (car_location[0],car_location[1]) in board.cell_list()
            and car_orientation in ORIENTATION):
            board.add_car(Car(car_name,
                              car_length,
                              (car_location[0],car_location[1]),
                              car_orientation))
    return board

if __name__== "__main__":
    args = sys.argv
    path = DEFAULT_PATH
    if len(args) > 1:
        path = args[1]
    Game(json_to_board(path)).play()
    input("Hit Enter to continue and leave the program")
