from ast import literal_eval
from collections import Counter
from itertools import product
import anvil.server
import anvil.mpl_util
import numpy as np
import plotly.express as px
import pandas as pd

anvil.server.connect("OQH4NZ7ZDKJ6G676PZWGYT4H-6GXUPVRXW6A67APZ")

def increment_adder(dims, left_edge_coord, top_edge_coord, increment_x, increment_y):
    """
    Adds increments to x and y coordinates, then takes their cartesian product to obtain all necessary tuples.
    :param dims: dimensions
    :param left_edge_coord: the left edge x coordinate
    :param top_edge_coord: the upper edge y coordinate
    :param increment_x: increment of x
    :param increment_y: increment of y
    :return: an array filled with the points
    """

    xs = []
    for i in range(0, int(dims[0])):
        xs.append(left_edge_coord)
        left_edge_coord += increment_x

    ys = []
    for i in range(0, int(dims[1])):
        ys.append(top_edge_coord)
        top_edge_coord -= increment_y

    # round
    xs = [round(x, 2) for x in xs]
    ys = [round(y, 2) for y in ys]

    cartesian_product = list(product(xs, ys))
    xs = np.array([x[0] for x in cartesian_product]).reshape(int(dims[0]), int(dims[1])).T
    ys = np.array([y[1] for y in cartesian_product]).reshape(int(dims[0]), int(dims[1])).T
    solution = np.stack(arrays=[xs, ys], axis=0)
    return solution


def pixel_placer(dims, corners):
    """
    Contains logic for identifying the increments needed to evenly space points for given corners and dimensions.
    :param dims: user-defined dimensions of the rectangle's dots.
    :param corners: user defined corner points of the rectangle
    :return: the coordinates of the evenly spaced points.
    """

    # every rectangle will have an upmost and rightmost corner of interest
    # obtain the maximum x coordinate (which is the rightmost edge)
    # and maximum y coordinate (which is the topmost edge)
    right_edge_coord = max(corners, key=lambda x: x[0])[0]
    top_edge_coord = max(corners, key=lambda y: y[1])[1]

    # same for minimums (leftmost and bottommost edge)
    left_edge_coord = min(corners, key=lambda x: x[0])[0]
    bottom_edge_coord = min(corners, key=lambda y: y[1])[1]

    # number of points to be placed is determined by the dimensions that were passed in by the user
    num_points_x = dims[0] - 1  # one endpoint already accounted for, since the iteration is beginning there.

    # space to place these is the right most x - the left most x
    space_diff_x = right_edge_coord - left_edge_coord

    # and increment x by this amount
    increment_x = space_diff_x / num_points_x

    # repeat for y, but using top and bottom edge y coords, instead of left & right
    num_points_y = dims[1] - 1
    space_diff_y = top_edge_coord - bottom_edge_coord
    increment_y = space_diff_y / num_points_y

    final_coords = increment_adder(dims, left_edge_coord, top_edge_coord, increment_x,
                                   increment_y)
    return final_coords


def rectangle_checker(coords_list):
    """
    Parses corner coordinate inputs to determine if it is a valid rectangle.
    :param coords_list: string representation of corner points
    :return: boolean: true if coordinates form a rectangle, false if not.
    """
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
    """
    Converts the string input of corner points into 4 2-tuples of floats.
    :param coord_string: the string input
    :return: array: of 4 2-tuples representing coordinates of rectangle corners
    """
    unwrapped_xys = []
    coord_string = coord_string.split(';')  # split the string into individual tuples
    for one_tuple in coord_string:
        x, y = literal_eval(one_tuple)  # string -> tuple representation
        unwrapped_xys.append((x, y))
    return unwrapped_xys


@anvil.server.callable
def validate_inputs(x, y, corners):
    try:
        x = float(x)
    except ValueError:
        return (False, "Entry must be an integer (ex: 4) or float (ex: 3.2)")

    try:
        y = float(y)
    except ValueError:
        return (False, "Entry must be an integer (ex: 4) or float (ex: 3.2)")

    if(not rectangle_checker(corners)):
        return (False, "Coordinates were invalid, or don't form a rectangle. Please retry.")
    return True,''

@anvil.server.callable
def main(dims, corners):
    corners = corner_formatter(corners)

    solution = pixel_placer(dims, corners)

    print(solution)

    # numpy handles array dim as (stack, rows, columns). In this case (2, dim_y, dim_x). This is counterintuitive
    # but in this numpy representation, the rows are the y-coordinate and the columns are the x-coordinate.
    print(solution.shape)

    return solution
@anvil.server.callable
def plot(solution):
    x_tuples = solution[0]
    x_points =[]
    for i in x_tuples:
        for j in range(0,len(i)):
            x_points.append(i[j])
    y_tuples = solution[1]
    y_points = []
    for i in y_tuples:
        for j in range(0,len(i)):
            y_points.append(i[j])

    fig = px.scatter(x=x_points,y=y_points,title="Illustration of Evenly Spaced Dots for Given Rectangle")
    fig.show()
    return fig
anvil.server.wait_forever()
