from typing import List


def generate_pyramid(n: int) -> str:
    """
    Generates a pyramid of asterisks (*) with n rows.

    Parameters:
    n (int): The number of rows in the pyramid. Must be a positive integer.

    Returns:
    str: A string representing the pyramid.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Input must be a positive integer.")

    max_pyramid_height = (n * 2) - 1
    pyramid_rows: List[str] = []

    # Print and calculate central index for the first row
    print(max_pyramid_height)
    central_index = int(max_pyramid_height / 2)
    print(central_index)

    # Generate rows of the pyramid
    for i in range(n):
        row = write_row(n, max_pyramid_height, central_index - i, central_index + i + 1)
        pyramid_rows.append(row)

    # Join all rows into a single string and return it
    stars = "".join(pyramid_rows)
    print(stars)
    return stars


def write_row(n: int, max_pyramid_height: int, left: int, right: int) -> str:
    """
    Generates a row of the pyramid with n asterisks (*).

    Parameters:
    n (int): The number of asterisks in each row.
    max_pyramid_height (int): The maximum height of the pyramid.
    left (int): The index of the first asterisk in the current row.
    right (int): The index of the last asterisk in the current row.

    Returns:
    str: A string representing the generated row.
    """
    # Generate a row with asterisks
    stars_per_row = ["*"] * n
    for i in range(n - 1, left - 1, -1):
        stars_per_row[i] = " "

    return "".join(stars_per_row)


# Test the function
generate_pyramid(5)
