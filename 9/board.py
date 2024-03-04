from typing import Tuple, List, Optional
from car import Car

Coordinates = Tuple[int, int]
EMPTY = "_"
WIDTH = 7
HEIGHT = 7
BUFFER = "*"
TARGET = "E"


class Board:
    """
    A class responsible for raising rhe framework of the game
    """

    def __init__(self) -> None:
        """
        A constructor for a Board object.
        """
        self.__grid = [[0] * WIDTH] * HEIGHT
        self.__cars = []

    def __str__(self) -> str:
        """
        This function is called when a board object is to be printed.
        :return: A string representing the current status of the board.
        """
        printable = ""
        for row in range(HEIGHT):
            if row != 0:
                printable += "\n"
            for collumn in range(WIDTH):
                if collumn != 0:
                    printable += " "
                if self.__grid[row][collumn] == 0:
                    printable += "_"
                else:
                    printable += self.__grid[row][collumn]
            if row == int((HEIGHT-1)/2):
                printable += TARGET
            else:
                printable += BUFFER
        return printable

    def cell_list(self) -> List[Coordinates]:
        """
        This function returns the coordinates of cells in this board.
        :return: list of coordinates.
        """
        coord_list = [(WIDTH,int((HEIGHT-1)/2))]
        for i in range(HEIGHT):
            for j in range(WIDTH):
                coord_list.append((i,j))
        return coord_list

    def possible_moves(self) -> List[Tuple[str, str, str]]:
        """ 
        This function returns the legal moves of all cars in this board.
        :return: list of tuples of the form (name, move_key, description)
                 representing legal moves. The description should briefly
                 explain what is the movement represented by move_key.
        """
        move_list = []
        for car in self.__cars:
            if 
        pass

    def target_location(self) -> Coordinates:
        """
        This function returns the coordinates of the location that should be 
        filled for victory.
        :return: (row, col) of the goal location.
        """
        # In this board, returns (3,7)
        # implement your code and erase the "pass"
        pass

    def cell_content(self, coordinates: Coordinates) -> Optional[str]:
        """
        Checks if the given coordinates are empty.
        :param coordinates: tuple of (row, col) of the coordinates to check.
        :return: The name of the car in "coordinates", None if it's empty.
        """
        # implement your code and erase the "pass"
        pass

    def add_car(self, car: Car) -> bool:
        """
        Adds a car to the game.
        :param car: car object to add.
        :return: True upon success, False if failed.
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"
        pass

    def move_car(self, name: str, move_key: str) -> bool:
        """
        Moves car one step in a given direction.
        :param name: name of the car to move.
        :param move_key: the key of the required move.
        :return: True upon success, False otherwise.
        """
        # implement your code and erase the "pass"
        pass

if __name__ == "__main__":
    b = Board()
    print(b)
