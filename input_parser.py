from ast import literal_eval
from collections import Counter


def rectangle_checker(coords_list):
    '''
    Parses corner coordinate inputs to determine if it is a valid rectangle.
    :param coords_list: string representation of corner points
    :return: boolean: true if coordinates form a rectangle, false if not.
    '''
    unwrapped_xys = []
    coords_list = coords_list.split(';')  # split the string into individual tuples
    for one_tuple in coords_list:
        x, y = literal_eval(one_tuple)  # string -> tuple representation
        unwrapped_xys.extend((x, y))
    cardinalities = list(Counter(unwrapped_xys).values())  # Counter class
    for i in cardinalities:
        if (i != 2):  # each point should have only 2 occurrences -> valid rectangle
            return False
    return True


def corner_formatter(coord_string):
    '''
    Converts the string input of corner points into 4 2-tuples of floats.
    :param coord_string: the string input
    :return: array: of 4 2-tuples representing coordinates of rectangle corners
    '''
    unwrapped_xys = []
    coord_string = coord_string.split(';')  # split the string into individual tuples
    for one_tuple in coord_string:
        x, y = literal_eval(one_tuple)  # string -> tuple representation
        unwrapped_xys.append((x, y))
    return unwrapped_xys