#################################################################
# FILE : ex7.py
# WRITER : Dori_Peleg , dori.plg , 207685306
# EXERCISE : intro2cs ex7 2024
# DESCRIPTION: Let's recourse
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: Recursion is a must, see excercise description
#################################################################

from typing import *
from ex7_helper import *

def mult(x: N, y: int) -> N:
    """multiplies recursively"""
    if y > 1:
        return add(mult(x,subtract_1(y)),x)
    return x 

def is_even(n: int) -> bool:
    """checks if a non-neg integer is even"""
    if n>0:
        return not is_even(subtract_1(n))
    return True

def log_mult(x: N, y: int) -> N:
    """multiplies efficiantly - O(log(y))"""
    if y > 1:
        if is_odd(y):
            return add(add(
                log_mult(x, divide_by_2(y)),
                log_mult(x, divide_by_2(y))),
                  x)
        else:
            return add(
                log_mult(x,divide_by_2(y)),
                log_mult(x,divide_by_2(y)))
    return x

def powerer(base: int, current: int, dest_value: int) -> bool:
    """brings up to power until it can check equality to the dest_value
    O(log(b)*log(x))"""
    if current < dest_value:
        return powerer(base, log_mult(current, base), dest_value)
    return current == dest_value

def is_power(b: int,x: int) -> bool:
    """Not recursive, opens a recursive function"""
    if x in (b, 1):  # x equals base or base^0
        return True
    if b == 1:  # base is 1 but x is not
        return False
    return powerer(b,b,x)

def reverse(s: str) -> str:
    """flips the order of letters in a string"""
    if len(s)>0:
        return append_to_end(reverse(s[1:]),s[0])  # cheating?
    return ""

def play_hanoi(hanoi: Any, n: int, src: Any, dest: Any, temp: Any) -> None:
    """the algorithm for the hanoi towers"""
    if n>0:
        if n > 1:
            play_hanoi(hanoi,n-1,src,temp,dest)
            hanoi.move(src,dest)
            play_hanoi(hanoi,n-1,temp, dest,src)
        else:
            hanoi.move(src, dest)

def digs_in_number(num: int,dig: int) -> int:
    """helper function to find the amount of times a certain digit apears in a number"""
    if num > 0:
        cur = 0
        if num % 10 == dig:
            cur = 1
        return digs_in_number(num//10,dig) + cur
    return 0

def number_of_ones(n: int) -> int:
    """counts how many ones are between 0 and n"""
    if n==1:
        return 1
    return digs_in_number(n,1) + number_of_ones(n-1)

def compare_1d_lists(l1: List[int], l2: List[int]) -> bool:
    """compares the values and place of two 1D lists"""
    if len(l1) == len(l2):
        if len(l1) > 0 and len(l2) > 0:
            return l1.pop(-1) == l2.pop(-1) and compare_1d_lists(l1,l2)
        return True
    return False

def compare_2d_lists(l1: List[List[int]], l2: List[List[int]]) -> bool:
    """compares the values and place of two 2D lists"""
    if len(l1) == len(l2):
        if len(l1) > 0 and len(l2) > 0:
            return compare_1d_lists(l1.pop(-1),l2.pop(-1)) and compare_2d_lists(l1,l2)
        return True
    return False

def magic_list(n: int) -> List[Any]:
    """preforms the magic of a list containing empty lists containing empty lists"""
    if n>0:
        return magic_list(n-1) + [magic_list(n-1)]
    return []



if __name__ == "__main__":
    pass
