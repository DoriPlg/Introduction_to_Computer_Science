#################################################################
# FILE : car.py
# WRITER : Dori_Peleg , dori.plg , 207685306
# EXERCISE : intro2cs ex9 2024
# DESCRIPTION: This file creates the car class for the "rush hour" game,
#              applicapble in others as well
# STUDENTS I DISCUSSED THE EXERCISE WITH: Hadar Soffer
# WEB PAGES I USED:
# NOTES: note the hiddenness of the API and the constants for each class
#################################################################


from typing import Tuple, List, Dict

Coordinates = Tuple[int, int]
VERT = 0  # vertical car
HORZ = 1  # horizontal car


class Car:
    """
    A car in the popular "Rush Hour" board game. 
    """

    # defining legal values for certain atributes and variables
    __legal_orientation = (VERT,HORZ)

    def __init__(self, name: str, length: int, location: Coordinates, 
                 orientation: int) -> None:
        """
        A constructor for a Car object.
        :param name: A string representing the car's name.
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head location (row,col).
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL).
        """
        self.__name = name
        self.__length = length
        if orientation in self.__legal_orientation:
            self.__orientation = orientation
        else:
            raise ValueError("illegal orientaion value")
        self.__location = location

    def car_coordinates(self) -> List[Coordinates]:
        """
        :return: A list of coordinates the car is in.
        """
        coordinate_list = []
        if self.__orientation == VERT:
            for index in range(self.__length):
                coordinate_list.append((self.__location[0] + index, self.__location[1]))
        elif self.__orientation == HORZ:
            for index in range(self.__length):
                coordinate_list.append((self.__location[0] ,self.__location[1] + index))
        else:
            raise AttributeError("improper orientation attribute")
        return coordinate_list  

    def possible_moves(self) -> Dict[str, str]:
        """
        :return: A dictionary of strings describing possible movements 
                 permitted by this car.
        """
        if self.__orientation == HORZ:
            return {"l": "moves the car one unit to the left",
                    "r": "moves the car one unit to the right"}
        if self.__orientation == VERT:
            return {"u": "moves the car one unit 'up'",
                    "d": "moves the car one unit 'down'"}
        raise AttributeError("improper orientation")

    def movement_requirements(self, move_key: str) -> List[Coordinates]:
        """ 
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for 
                 this move to be legal.
        """
        cell_list =[]
        if move_key not in self.possible_moves():
            raise ValueError("This move is not possible, it is not in the possible moves dictionary")
        if self.__orientation == VERT:
            if move_key == "u":
                cell_list.append((self.__location[0] - 1, self.__location[1]))
            elif move_key == "d":
                cell_list.append((self.__location[0] + self.__length, self.__location[1]))
        elif self.__orientation == HORZ:
            if move_key == "r":
                cell_list.append((self.__location[0], self.__location[1] + self.__length))
            elif move_key == "l":
                cell_list.append((self.__location[0], self.__location[1] - 1))
        return cell_list

    def move(self, move_key: str) -> bool:
        """ 
        This function moves the car.
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if move_key not in self.possible_moves():
            return False
            # raise ValueError("This move is not possible, it is not in the possible moves dictionary")
        if move_key == "u":
            self.__location = (self.__location[0] - 1, self.__location[1])
            return True
        elif move_key == "d":
            self.__location = (self.__location[0] + 1, self.__location[1])
            return True
        elif move_key == "r":
            self.__location = (self.__location[0], self.__location[1] + 1)
            return True
        elif move_key == "l":
            self.__location = (self.__location[0], self.__location[1] - 1)
            return True
        return False

    def get_name(self) -> str:
        """
        :return: The name of this car.
        """
        return self.__name
