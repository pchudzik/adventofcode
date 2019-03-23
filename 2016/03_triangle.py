import re

"""
--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways and office furniture that makes up this
part of Easter Bunny HQ. This must be a graphic design department; the walls are covered in specifications for
triangles.

Or are they?

The design document gives the side lengths of each triangle it describes, but... 5 10 25? Some of these aren't
triangles. You can't help but mark the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining side. For example, the "triangle" given
above is impossible, because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

Your puzzle answer was 869.

--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you that triangles are specified in groups of
three vertically. Each set of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?

Your puzzle answer was 1544.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


def is_triangle_possible(triangle):
    return triangle[0] + triangle[1] > triangle[2] \
           and triangle[0] + triangle[2] > triangle[1] \
           and triangle[1] + triangle[2] > triangle[0]


def parse_triangle(triangle_str):
    return tuple(map(
        int,
        re.split("\\s+", triangle_str.strip())))


def count_valid_triangles(triangles):
    return len(list(filter(
        is_triangle_possible,
        map(
            parse_triangle,
            triangles))))


def count_valid_vertical_triangles(triangles):
    valid_triangles = 0
    for row in range(0, len(triangles) - 2, 3):
        triangle_rows = parse_triangle(triangles[row]), \
                        parse_triangle(triangles[row + 1]), \
                        parse_triangle(triangles[row + 2])

        for triangle in range(len(triangle_rows)):
            built_triangle = triangle_rows[0][triangle], triangle_rows[1][triangle], triangle_rows[2][triangle]
            valid_triangles += 1 if is_triangle_possible(built_triangle) else 0

    return valid_triangles


if __name__ == "__main__":
    with open("03_triangle.txt") as file:
        triangles = file.readlines()
        print(f"p1 = {count_valid_triangles(triangles)}")
        print(f"p2 = {count_valid_vertical_triangles(triangles)}")
