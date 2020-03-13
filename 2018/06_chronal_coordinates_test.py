import importlib
import pytest

module = importlib.import_module("06_chronal_coordinates")
parse_points = module.parse_points
Point = module.Point
AreaBounds = module.AreaBounds
manhattan_distance = module.manhattan_distance
calculate_area = module.calculate_area
find_max_area = module.find_max_area
find_all_safe_regions = module.find_all_safe_regions

A = 0
B = 1
C = 2
D = 3
E = 4
F = 5

points_raw = [
    "1, 1",  # 0, A
    "1, 6",  # 1, B
    "8, 3",  # 2, C
    "3, 4",  # 3, D
    "5, 5",  # 4, F
    "8, 9"  # 5, F
]


@pytest.mark.parametrize("point_index, expected", [
    (A, True),
    (B, True),
    (C, True),
    (D, False),
    (E, False),
    (F, True)
])
def test_find_infinite_points(point_index, expected):
    points = parse_points(points_raw)

    point = points[point_index]
    bounds = AreaBounds(points)

    assert bounds.is_outside(point) == expected


def test_manhattan_distance():
    p1 = Point(0, 0)
    p2 = Point(3, 3)

    assert manhattan_distance(p1, p2) == 6


def test_calculate_area():
    points = parse_points(points_raw)

    area = calculate_area(points)

    assert area[points[A]] is None
    assert area[points[B]] is None
    assert area[points[C]] is None
    assert area[points[D]] == 9
    assert area[points[E]] == 17
    assert area[points[F]] is None


def test_find_max_area():
    points = parse_points(points_raw)

    assert find_max_area(points) == 17








"""
..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.
"""


def test_find_all_safe_regions():
    points = parse_points(points_raw)

    safe_regions = find_all_safe_regions(points, max_distance=32)

    assert len(safe_regions) == 16

    assert Point(3, 3) in safe_regions
    assert Point(4, 3) in safe_regions
    assert Point(5, 3) in safe_regions

    assert Point(2, 4) in safe_regions
    assert Point(3, 4) in safe_regions
    assert Point(4, 4) in safe_regions
    assert Point(5, 4) in safe_regions
    assert Point(6, 4) in safe_regions

    assert Point(2, 5) in safe_regions
    assert Point(3, 5) in safe_regions
    assert Point(4, 5) in safe_regions
    assert Point(5, 5) in safe_regions
    assert Point(6, 5) in safe_regions

    assert Point(3, 6) in safe_regions
    assert Point(4, 6) in safe_regions
    assert Point(5, 6) in safe_regions
