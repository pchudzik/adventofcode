import pytest
import importlib

module = importlib.import_module("12_subterranean_sustainability")
parse = module.parse


def test_parse_input(puzzle):
    live_sates = [
        "...##",
        "..#..",
        ".#...",
        ".#.#.",
        ".#.##",
        ".##..",
        ".####",
        "#.#.#",
        "#.###",
        "##.#.",
        "##.##",
        "###..",
        "###.#",
        "####.",
    ]

    parsed = parse(puzzle)

    assert str(parsed.state) == "#..#.#..##......###...###"
    assert parsed.zero_index == 0
    assert len(parsed.notes) == len(live_sates)
    for state in live_sates:
        assert parsed.notes[state] == "#"


@pytest.mark.parametrize(
    "number_of_generations, total_sum, output_state", [
        (1, 91, "#...#....#.....#..#..#..#"),
        (2, 132, "##..##...##....#..#..#..##"),
        (3, 102, "#.#...#..#.#....#..#..#...#"),
        (4, 154, "#.#..#...#.#...#..#..##..##"),
        (5, 115, "#...##...#.#..#..#...#...#"),
        (6, 174, "##.#.#....#...#..##..##..##"),
        (7, 126, "#..###.#...##..#...#...#...#"),
        (8, 213, "#....##.#.#.#..##..##..##..##"),
        (9, 138, "##..#..#####....#...#...#...#"),
        (10, 213, "#.#..#...#.##....##..##..##..##"),
        (11, 136, "#...##...#.#...#.#...#...#...#"),
        (12, 218, "##.#.#....#.#...#.#..##..##..##"),
        (13, 133, "#..###.#....#.#...#....#...#...#"),
        (14, 235, "#....##.#....#.#..##...##..##..##"),
        (15, 149, "##..#..#.#....#....#..#.#...#...#"),
        (16, 226, "#.#..#...#.#...##...#...#.#..##..##"),
        (17, 170, "#...##...#.#.#.#...##...#....#...#"),
        (18, 280, "##.#.#....#####.#.#.#...##...##..##"),
        (19, 287, "#..###.#..#.#.#######.#.#.#..#.#...#"),
        (20, 325, "#....##....#####...#######....#.#..##"),
    ])
def test_generation(parsed_puzzle, number_of_generations, total_sum, output_state):
    parsed_puzzle.generate(number_of_generations)

    assert parsed_puzzle.state == output_state
    assert parsed_puzzle.total_sum == total_sum


@pytest.fixture
def parsed_puzzle(puzzle):
    return parse(puzzle)


@pytest.fixture
def puzzle():
    return """
    initial state: #..#.#..##......###...###
    
    ...## => #
    ..#.. => #
    .#... => #
    .#.#. => #
    .#.## => #
    .##.. => #
    .#### => #
    #.#.# => #
    #.### => #
    ##.#. => #
    ##.## => #
    ###.. => #
    ###.# => #
    ####. => #
    """.split("\n")
