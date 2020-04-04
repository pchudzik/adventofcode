import importlib
import pytest

module = importlib.import_module("10_the_stars_align")

parse = module.parse
Message = module.Message

sample = [
    "position=< 9,  1> velocity=< 0,  2>",
    "position=< 7,  0> velocity=<-1,  0>",
    "position=< 3, -2> velocity=<-1,  1>",
    "position=< 6, 10> velocity=<-2, -1>",
    "position=< 2, -4> velocity=< 2,  2>",
    "position=<-6, 10> velocity=< 2, -2>",
    "position=< 1,  8> velocity=< 1, -1>",
    "position=< 1,  7> velocity=< 1,  0>",
    "position=<-3, 11> velocity=< 1, -2>",
    "position=< 7,  6> velocity=<-1, -1>",
    "position=<-2,  3> velocity=< 1,  0>",
    "position=<-4,  3> velocity=< 2,  0>",
    "position=<10, -3> velocity=<-1,  1>",
    "position=< 5, 11> velocity=< 1, -2>",
    "position=< 4,  7> velocity=< 0, -1>",
    "position=< 8, -2> velocity=< 0,  1>",
    "position=<15,  0> velocity=<-2,  0>",
    "position=< 1,  6> velocity=< 1,  0>",
    "position=< 8,  9> velocity=< 0, -1>",
    "position=< 3,  3> velocity=<-1,  1>",
    "position=< 0,  5> velocity=< 0, -1>",
    "position=<-2,  2> velocity=< 2,  0>",
    "position=< 5, -2> velocity=< 1,  2>",
    "position=< 1,  4> velocity=< 2,  1>",
    "position=<-2,  7> velocity=< 2, -2>",
    "position=< 3,  6> velocity=<-1, -1>",
    "position=< 5,  0> velocity=< 1,  0>",
    "position=<-6,  0> velocity=< 2,  0>",
    "position=< 5,  9> velocity=< 1, -2>",
    "position=<14,  7> velocity=<-2,  0>",
    "position=<-3,  6> velocity=< 2, -1>"
]


@pytest.mark.parametrize("line, position, velocity", [
    ("position=<-3,  6> velocity=< 2, -1>", (-3, 6), (2, -1)),
    ("position=<-6, 10> velocity=< 2, -2>", (-6, 10), (2, -2))
])
def test_parse(line, position, velocity):
    points = parse([line])

    assert len(points) == 1
    assert points[0].position == position
    assert points[0].velocity == velocity


def test_tick():
    point = parse(["position=<0, 0> velocity=<2, 1>"])[0]

    assert point.position == (0, 0)

    point.tick()
    assert point.position == (2, 1)

    point.tick()
    assert point.position == (4, 2)

    point.tick()
    assert point.position == (6, 3)


def test_message_print():
    message = Message(parse(sample))

    assert message.snapshot() == [
        "........#.............",
        "................#.....",
        ".........#.#..#.......",
        "......................",
        "#..........#.#.......#",
        "...............#......",
        "....#.................",
        "..#.#....#............",
        ".......#..............",
        "......#...............",
        "...#...#.#...#........",
        "....#..#..#.........#.",
        ".......#..............",
        "...........#..#.......",
        "#...........#.........",
        "...#.......#..........",
    ]


    message.tick()
    assert message.snapshot() == [
        "........#....#....",
        "......#.....#.....",
        "#.........#......#",
        "..................",
        "....#.............",
        "..##.........#....",
        "....#.#...........",
        "...##.##..#.......",
        "......#.#.........",
        "......#...#.....#.",
        "#...........#.....",
        "..#.....#.#.......",
    ]

    message.tick()
    assert message.snapshot() == [
        "..........#...",
        "#..#...####..#",
        "..............",
        "....#....#....",
        "..#.#.........",
        "...#...#......",
        "...#..#..#.#..",
        "#....#.#......",
        ".#...#...##.#.",
        "....#.........",
    ]

    message.tick()
    assert message.snapshot() == [
        "#...#..###",
        "#...#...#.",
        "#...#...#.",
        "#####...#.",
        "#...#...#.",
        "#...#...#.",
        "#...#...#.",
        "#...#..###",
    ]

    message.tick()
    assert message.snapshot() == [
        "........#....",
        "....##...#.#.",
        "..#.....#..#.",
        ".#..##.##.#..",
        "...##.#....#.",
        ".......#....#",
        "..........#..",
        "#......#...#.",
        ".#.....##....",
        "...........#.",
        "...........#.",
    ]
