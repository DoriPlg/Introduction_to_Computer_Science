#################################################################
# FILE : board.py
# WRITER : Dori_Peleg , dori.plg , 207685306
# EXERCISE : intro2cs ex9 2024
# DESCRIPTION: This file creates the board class for the "rush hour" game,
#               applicable in other applications as well
# STUDENTS I DISCUSSED THE EXERCISE WITH: Hadar Soffer
# WEB PAGES I USED:
# NOTES: note the hiddenness of the API and the constants for each class
#################################################################

from typing import Tuple, List, Optional
from car import Car

Coordinates = Tuple[int, int]

EMPTY = "_"
WIDTH = 7
HEIGHT = 7
BUFFER = "*"
TARGET = "E"

"""
COLOR_DICT = {"R": Back.RED,
              "Y": Back.YELLOW,
              "G": Back.GREEN,
              "O": Back.MAGENTA,
              "W": Back.WHITE,
              "B": Back.BLUE}
"""

class Board:
    """
    A class responsible for raising the framework of the game
    """

    def __init__(self) -> None:
        """
        A constructor for a Board object.
        """
        self.__cars = {}

    def __str__(self) -> str:
        """
        This function is called when a board object is to be printed.
        :return: A string representing the current status of the board.
        """
        grid = []
        for _ in range(HEIGHT):
            grid.append([0] * WIDTH)
        for car in self.__cars.values():
            for coordinate in car.car_coordinates():
                grid[coordinate[0]][coordinate[1]] = car.get_name()
        printable = ""
        for row in range(HEIGHT):
            if row != 0:
                printable += "\n"
            for collumn in range(WIDTH):
                if collumn != 0:
                    printable += " "
                if grid[row][collumn] == 0:
                    printable += "_"
                else:
                    printable += f"{grid[row][collumn]}"
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
        coord_list = [self.target_location()]
        for i in range(HEIGHT):
            for j in range(WIDTH):
                coord_list.append((i,j))
        return coord_list

    def __moves_for_car(self,car: Car) -> List[Tuple[str,str,str]]:
        """
        finds the viable moves for a car
        """
        moves = []
        for move, description in car.possible_moves().items():
            move_satisfies = True
            for requirement in car.movement_requirements(move):
                if self.cell_content(requirement) is not None or \
                    not self.__coordinate_in_range(requirement):
                    move_satisfies = False
            if move_satisfies:
                moves.append((car.get_name(), move, description))
        return moves

    def possible_moves(self) -> List[Tuple[str, str, str]]:
        """ 
        This function returns the legal moves of all cars in this board.
        :return: list of tuples of the form (name, move_key, description)
                 representing legal moves. The description should briefly
                 explain what is the movement represented by move_key.
        """
        move_list = []
        for car in self.__cars.values():
            move_list += self.__moves_for_car(car)
        return move_list

    def target_location(self) -> Coordinates:
        """
        This function returns the coordinates of the location that should be 
        filled for victory.
        :return: (row, col) of the goal location.
        """
        return (int((HEIGHT-1) / 2), WIDTH)

    def cell_content(self, coordinates: Coordinates) -> Optional[str]:
        """
        Checks if the given coordinates are empty.
        :param coordinates: tuple of (row, col) of the coordinates to check.
        :return: The name of the car in "coordinates", None if it's empty.
        """
        for car in self.__cars.values():
            if coordinates in car.car_coordinates():
                return car.get_name()
        return None

    def __coordinate_in_range(self,coordinate: Coordinates) -> bool:
        return coordinate in self.cell_list()

    def add_car(self, car: Car) -> bool:
        """
        Adds a car to the game.
        :param car: car object to add.
        :return: True upon success, False if failed.
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        for coordinate in car.car_coordinates():
            if not self.__coordinate_in_range(coordinate) or \
                self.cell_content(coordinate) is not None or \
                    car.get_name() in self.__cars.keys():
                return False
        self.__cars[car.get_name()] = car
        return True

    def move_car(self, name: str, move_key: str) -> bool:
        """
        Moves car one step in a given direction.
        :param name: name of the car to move.
        :param move_key: the key of the required move.
        :return: True upon success, False otherwise.
        """
        if name in self.__cars:
            required = self.__cars[name].movement_requirements(move_key)[0]
            if ((required[0] in range(HEIGHT) and required[1] in range(WIDTH) and \
                 self.cell_content(required) is None) or
                (required[0] == (HEIGHT-1)/2 and required[1] == WIDTH)):
                return self.__cars[name].move(move_key)
        return False
