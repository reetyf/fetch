from ast import literal_eval
from collections import Counter
from itertools import product
import anvil.server
import numpy as np
import plotly.express as px
import json

# connects to anvil app server
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
        left_edge_coord += increment_x # increment left most coordinate by calculated amount

    ys = []
    for i in range(0, int(dims[1])):
        ys.append(top_edge_coord)
        top_edge_coord -= increment_y # decrement top most coordinate by calculated amount


    # round
    xs = [round(x, 2) for x in xs]
    ys = [round(y, 2) for y in ys]

    # take cartesian product and reformat for 3 dimensional stack
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
    """
    :param x: int , passed in x value
    :param y: int , passed in y value
    :param corners: string of 4 2-tuples, will be parsed
    :return: 2 tuple - (boolean,string) : False if invalid input, and corresponding text
    """
    try:
        x = float(x)
    except ValueError:
        return (False, "Entry must be an integer (ex: 4)")

    try:
        y = float(y)
    except ValueError:
        return (False, "Entry must be an integer (ex: 4)")

    if (not rectangle_checker(corners)):
        return (False, "Coordinates were invalid, or don't form a rectangle. Please retry.")
    return True, ''


@anvil.server.callable
def main(dims, corners):
    """
    :param dims: int tuple of dimensions passed in by the user
    :param corners: string of corners, that will be parsed and made into 4 2-tuples
    :return: 2-tuple  of solution and response text for the app
    """
    corners = corner_formatter(corners)

    solution = pixel_placer(dims, corners)

    # numpy handles array dim as (stack, rows, columns). In this case (2, dim_y, dim_x). This is counterintuitive
    # but in this numpy representation, the rows are the y-coordinate and the columns are the x-coordinate.
    return (solution,
            f"The passed in rectangle with dimensions {dims} and corners {corners} has evenly spaced points at the below points. This is not intuitive as printed below, so an attached Plotly Express visualization is displayed.")


@anvil.server.callable
def plot(solution):
    """
    :param solution: 3-d array of evenly spaced x,y coordinates
    :return: fig: the plotly express figure
    """
    #unravel each array iteratively and collect x,y points
    x_tuples = solution[0]
    x_points = []
    for i in x_tuples:
        for j in range(0, len(i)):
            x_points.append(i[j])
    y_tuples = solution[1]
    y_points = []
    for i in y_tuples:
        for j in range(0, len(i)):
            y_points.append(i[j])

    # now, collected x,y points are easily passed into a scatterplot...
    fig = px.scatter(x=x_points, y=y_points, title="Illustration of Evenly Spaced Dots for Given Rectangle")
    ret = fig.to_json()
    return ret,json.loads(ret)['data'],json.loads(ret)['layout']

@anvil.server.callable
def point_getter(solution,where_to_search):
    """ Returns a point.
    :param solution: the answer to the rectangle problem.
    :param where_to_search: coordinate to search
    :return: value at given coordinates
    """
    # 3- tuple passed in , numpy array stores data as (depth, row , cols ) or (z, y, x)
    # for more logic, view readme.
    z,y,x = where_to_search
    try:
        point = solution[z][y][x]
    except IndexError:
        return 'n/a' # placeholder
    return point

# anvil server will remain open on my personal computer. This enables app interaction.
anvil.server.wait_forever()
