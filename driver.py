import sys
import matplotlib.pyplot as plt
from input_parser import rectangle_checker, corner_formatter
from coord_finder import pixel_placer


def main():
    x = input("Please enter the image x dimension: ")
    try:
        x = float(x)
    except ValueError:
        print("Entry must be an integer (ex: 4) or float (ex: 3.2)")
        sys.exit('Rerun program...')

    y = input("Please enter the image y dimension: ")
    try:
        y = float(y)
    except ValueError:
        print("Entry must be an integer (ex: 4) or float (ex: 3.2)")
        sys.exit('Rerun program...')

    dims = (x, y)

    corners = input(
        "Please enter the coordinates of the 4 corners (separate by a single semicolon ex: '(4,2);(4,1);(6,2);(6,1)': ")
    assert rectangle_checker(corners), "Coordinates were invalid, or don't form a rectangle. Please retry."

    corners = corner_formatter(corners)

    solution = pixel_placer(dims, corners)

    print(solution)

    # numpy handles array dim as (stack, rows, columns). In this case (2, dim_y, dim_x). This is counterintuitive
    # but in this numpy representation, the rows are the y-coordinate and the columns are the x-coordinate.
    print(solution.shape)

    x = solution[0]
    y = solution[1]
    plt.figure()
    plt.title('Illustration of Evenly Spaced Points')
    plt.scatter(x, y, color='r')
    plt.show()


if __name__ == '__main__':
    main()
