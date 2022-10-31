from itertools import product
import numpy as np


def increment_adder(dims, left_edge_coord, top_edge_coord, increment_x, increment_y):
    '''
    Adds increments to x and y coordinates, then takes their cartesian product to obtain all necessary tuples.
    :param right_edge_coord: the right edge x coordinate
    :param left_edge_coord: the left edge x coordinate
    :param top_edge_coord: the upper edge y coordinate
    :param bottom_edge_coord: the lower edge y coordinate
    :param increment_x: increment of x
    :param increment_y: increment of y
    :return: an array filled with the each point
    '''

    xs = []
    for i in range(0,int(dims[0])):
        xs.append(left_edge_coord)
        left_edge_coord += increment_x

    ys = []
    for i in range(0,int(dims[1])):
        ys.append(top_edge_coord)
        top_edge_coord -= increment_y

    #round
    xs = [round(x,2) for x in xs]
    ys = [round(y,2) for y in ys]

    cartesian_product = list(product(xs,ys))
    xs = np.array([x[0] for x in cartesian_product]).reshape(int(dims[0]),int(dims[1])).T
    ys = np.array([y[1] for y in cartesian_product]).reshape(int(dims[0]),int(dims[1])).T
    solution = np.stack(arrays=[xs,ys],axis=0)
    return solution


def pixel_placer(dims, corners):
    '''
    Contains logic for identifying the increments needed to evenly space points for given corners and dimensions.
    :param dims: user-defined dimensions of the rectangle's dots.
    :param corners: user defined corner points of the rectangle
    :return: the coordinates of the evenly spaced points.
    '''

    # every rectangle will have an upmost and rightmost corner of interest
    # obtain the maximum x coordinate (which is the rightmost edge)
    # and maximum y coordinate (which is the topmost edge)
    right_edge_coord = max(corners, key=lambda x: x[0])[0]
    top_edge_coord = max(corners, key=lambda y: y[1])[1]

    # same for minimums (leftmost and bottommost edge)
    left_edge_coord = min(corners, key=lambda x: x[0])[0]
    bottom_edge_coord = min(corners, key=lambda y: y[1])[1]

    # number of points to be placed is determined by the dimensions that were passed in by the user
    num_points_x = dims[0]-1    # one endpoint already accounted for, since the iteration is beginning there.

    # space to place these is the right most x - the left most x
    space_diff_x = right_edge_coord - left_edge_coord

    # and increment x by this amount
    increment_x = space_diff_x / num_points_x

    # repeat for y, but using top and bottom edge y coords, instead of left & right
    num_points_y = dims[1]-1
    space_diff_y = top_edge_coord - bottom_edge_coord
    increment_y = space_diff_y / num_points_y

    final_coords = increment_adder(dims, left_edge_coord, top_edge_coord,  increment_x,
                                   increment_y)
    return final_coords