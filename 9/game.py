from board import Board

EXIT_KEY = "!"
CAR_LENGTHS = (2,3,4)
CAR_NAMES = ('Y','B','O','W','G','R')
DIRECTIONS = ('u','d','l','r')

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
            "Write in NAME DIRECTION format\n" +
            f"name can only be {CAR_NAMES}\n" +
            f"direction can only be {DIRECTIONS}\n").split()
        if len(split_user_input) == 2:
            arg1, arg2 = split_user_input
        else:
            arg1, arg2 =  " ", " "
        while not (arg1 in CAR_NAMES and arg2 in DIRECTIONS):
            split_user_input = input("The input was improper, retry:  ").split()
            if len(split_user_input) == 2:
                arg1,arg2 = split_user_input
        return (arg1,arg2)

    def __check_valid_move(self, move: tuple[str,str]) -> bool:
        """
        ensures that a desired move is possible
        """
        return move in self.__board.possible_moves


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
        # implement your code and erase the "pass"
        pass

    def play(self) -> None:
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # implement your code and erase the "pass"
        pass


if __name__== "__main__":
    pass
