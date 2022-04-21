import pytest

from _03_crossed_wires import Point, parse_wire_path, part1, part2


@pytest.mark.parametrize(
    "path, result", [
        ("R3", (Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0))),
        ("L3", (Point(0, 0), Point(-1, 0), Point(-2, 0), Point(-3, 0))),
        ("D3", (Point(0, 0), Point(0, -1), Point(0, -2), Point(0, -3))),
        ("U3", (Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)))
    ]
)
def test_parse_wire_path(path, result):
    parsed = parse_wire_path(path)
    assert parsed == result


@pytest.mark.parametrize(
    "path1, path2, closest_distance", [
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 6),
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R8", 159),
        ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135)
    ]
)
def test_part1(path1, path2, closest_distance):
    distance = part1(
        parse_wire_path(path1),
        parse_wire_path(path2)
    )

    assert distance == closest_distance


@pytest.mark.parametrize(
    "path1, path2, expected_delay", [
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 30),
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 610),
        ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 410)
    ]
)
def test_part2(path1, path2, expected_delay):
    delay = part2(
        parse_wire_path(path1),
        parse_wire_path(path2)
    )

    assert delay == expected_delay
