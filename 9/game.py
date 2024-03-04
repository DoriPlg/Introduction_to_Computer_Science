from board import Board
from helper import load_json
from car import Car

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
        if split_user_input == BREAK_CHAR:
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


    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        user_input = self.__get_user_move()
        while not self.__valid_move(user_input):
            user_input = self.__get_user_move()
        self.__board.move_car(*user_input)

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
            if user_input == BREAK_CHAR:
                break
            while not self.__valid_move(user_input):
                print("invalid move")
                user_input = self.__get_user_move()
            self.__board.move_car(*user_input)
            


if __name__== "__main__":
    example = load_json("car_config.json")
    board = Board()
    for car in example.items():
        board.add_car(Car(car[0],car[1][0],car[1][1],car[1][2]))
    Game(board).play()
    input("Hit Enter to continue and leave the program")
