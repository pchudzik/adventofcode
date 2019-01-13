from functools import reduce


"""
--- Day 2: I Was Told There Would Be No Math ---

The elves are running low on wrapping paper, and so they need to submit an order for more. They have a list of the
dimensions (length l, width w, and height h) of each present, and only want to order exactly as much as they need.

Fortunately, every present is a box (a perfect right rectangular prism), which makes calculating the required wrapping
paper for each gift a little easier: find the surface area of the box, which is 2*l*w + 2*w*h + 2*h*l. The elves also
need a little extra paper for each present: the area of the smallest side.

For example:

A present with dimensions 2x3x4 requires 2*6 + 2*12 + 2*8 = 52 square feet of wrapping paper plus 6 square feet of
slack, for a total of 58 square feet.

A present with dimensions 1x1x10 requires 2*1 + 2*10 + 2*10 = 42 square feet of wrapping paper plus 1 square foot of
slack, for a total of 43 square feet.

All numbers in the elves" list are in feet. How many total square feet of wrapping paper should they order?

Your puzzle answer was 1588178.

--- Part Two ---

The elves are also running low on ribbon. Ribbon is all the same width, so they only have to worry about the length they
need to order, which they would again like to be exact.

The ribbon required to wrap a present is the shortest distance around its sides, or the smallest perimeter of any one
face. Each present also requires a bow made out of ribbon as well; the feet of ribbon required for the perfect bow is
equal to the cubic feet of volume of the present. Don"t ask how they tie the bow, though; they"ll never tell.

For example:

A present with dimensions 2x3x4 requires 2+2+3+3 = 10 feet of ribbon to wrap the present plus 2*3*4 = 24 feet of ribbon
for the bow, for a total of 34 feet.

A present with dimensions 1x1x10 requires 1+1+1+1 = 4 feet of ribbon to wrap the present plus 1*1*10 = 10 feet of ribbon
for the bow, for a total of 14 feet.

How many total feet of ribbon should they order?

Your puzzle answer was 3783758.
"""


def parse_strings(boxes_strings):
    boxes = map(lambda x: x.split("x"), boxes_strings)
    return map(lambda box: list(map(int, box)), boxes)


def calculate_wrapping_paper_area(boxes_strings):
    return reduce(
        lambda result, box: result + calculate_box_wrapping_area(box),
        parse_strings(boxes_strings),
        0)


def calculate_box_wrapping_area(box):
    l = box[0]
    w = box[1]
    h = box[2]

    smallest_side = min(l * w, l * h, w * h)

    return 2 * l * w + 2 * w * h + 2 * h * l + smallest_side


def calculate_ribbon_length(boxes_strings):
    return reduce(
        lambda result, box: result + calculcate_box_ribbon_length(box),
        parse_strings(boxes_strings),
        0)


def calculcate_box_ribbon_length(box):
    l = box[0]
    w = box[1]
    h = box[2]

    sides = sorted([l * 2, w * 2, h * 2])

    return sides[0] + sides[1] + l * w * h


if __name__ == "__main__":
    input_file = open("02_wrapping_paper.lst").readlines()
    print("paper", calculate_wrapping_paper_area(input_file))
    print("ribbon", calculate_ribbon_length(input_file))
