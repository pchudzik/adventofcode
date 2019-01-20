import pytest
import importlib

lights_module = importlib.import_module("18_lights2")

parse_lights_input = lights_module.parse_lights_input
SingleLight = lights_module.SingleLight
ON = SingleLight.ON
OFF = SingleLight.OFF


def test_parse_two_rows():
    lights_input = (
        ".####.",
        ".####."
    )

    lights = parse_lights_input(lights_input)

    assert lights.size == (2, 6)
    assert lights.number_of_on == 8
    assert lights.number_of_off == 4


def test_parse_input():
    lights_input = (
        ".#.#.#",
        "...##.",
        "#....#",
        "..#...",
        "#.#..#",
        "####.."
    )

    lights = parse_lights_input(lights_input)

    assert lights.size == (6, 6)
    assert lights.number_of_on == 15
    assert lights.number_of_off == 21


def test_neighbours_center():
    lights = parse_lights_input((
        ".....",
        ".###.",
        ".#.#.",
        ".###.",
        "....."
    ))

    neighbours = lights[2, 2].neighbours(lights.size)

    assert set(neighbours) == {
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 3),
        (3, 1), (3, 2), (3, 3)}


def test_neighbours_top_row():
    lights = parse_lights_input((
        "#.#",
        "###"
        "..."
    ))

    neighbours = lights[0, 1].neighbours(lights.size)

    assert set(neighbours) == {
        (0, 0), (0, 2),
        (1, 0), (1, 1), (1, 2)}


def test_neighbours_bottom_row():
    lights = parse_lights_input((
        "...",
        "###",
        "#.#",
    ))

    neighbours = lights[2, 1].neighbours(lights.size)

    assert set(neighbours) == {
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 2)}


def test_neighbours_top_left_corner():
    lights = parse_lights_input((
        ".#.",
        "##.",
        "...",
    ))

    neighbours = lights[0, 0].neighbours(lights.size)

    assert set(neighbours) == {
        (0, 1),
        (1, 0), (1, 1)}


def test_neighbours_top_right_corner():
    lights = parse_lights_input((
        ".#.",
        ".##",
        "...",
    ))

    neighbours = lights[0, 2].neighbours(lights.size)

    assert set(neighbours) == {
        (0, 1),
        (1, 1), (1, 2)}


def test_neighbours_bottom_left_corner():
    lights = parse_lights_input((
        "...",
        "##.",
        ".#.",
    ))

    neighbours = lights[2, 0].neighbours(lights.size)

    assert set(neighbours) == {
        (1, 0), (1, 1),
        (2, 1)}


def test_neighbours_bottom_right_corner():
    lights = parse_lights_input((
        "...",
        ".##",
        ".#.",
    ))

    neighbours = lights[2, 2].neighbours(lights.size)

    assert set(neighbours) == {
        (1, 1), (1, 2),
        (2, 1)}


@pytest.mark.parametrize(
    "state, neighbours_state, result",
    [
        (ON, (OFF, ON, ON, OFF), ON),
        (ON, (OFF, ON, ON, ON), ON),
        (ON, (ON, ON, ON, ON), OFF),
        (OFF, (ON, ON, ON, OFF), ON),
        (OFF, (OFF, ON, ON, OFF), OFF),
        (OFF, (OFF, OFF, ON, OFF), OFF),
        (OFF, (OFF, OFF, OFF, OFF), OFF),
    ]
)
def test_light_next_state(state, neighbours_state, result):
    light = SingleLight(state)

    next_state = light.calculate_next_state(map(SingleLight, neighbours_state))

    assert next_state == result
    assert light.is_lit == state


def test_transition():
    light = SingleLight(ON)

    light.calculate_next_state([SingleLight(OFF)])
    light.transition()

    assert light.next_state is None
    assert light.is_lit == False


def test_states():
    lights = parse_lights_input((
        ".#.#.#",
        "...##.",
        "#....#",
        "..#...",
        "#.#..#",
        "####.."
    ))

    lights.next_state()
    assert str(lights).split("\n") == [
        "..##..",
        "..##.#",
        "...##.",
        "......",
        "#.....",
        "#.##.."
    ]

    lights.next_state()
    assert str(lights).split("\n") == [
        "..###.",
        "......",
        "..###.",
        "......",
        ".#....",
        ".#...."
    ]

    lights.next_state()
    assert str(lights).split("\n") == [
        "...#..",
        "......",
        "...#..",
        "..##..",
        "......",
        "......"
    ]

    lights.next_state()
    assert str(lights).split("\n") == [
        "......",
        "......",
        "..##..",
        "..##..",
        "......",
        "......"
    ]


def test_states_with_stuck_lights():
    lights = parse_lights_input(
        (
            ".#.#.#",
            "...##.",
            "#....#",
            "..#...",
            "#.#..#",
            "####.."
        ),
        stuck=[
            (0, 0),
            (0, 5),
            (5, 0),
            (5, 5)
        ])

    assert str(lights).split("\n") == [
        "##.#.#",
        "...##.",
        "#....#",
        "..#...",
        "#.#..#",
        "####.#"
    ]

    lights.next_state()
    assert str(lights).split("\n") == [
        "#.##.#",
        "####.#",
        "...##.",
        "......",
        "#...#.",
        "#.####"
    ]

    lights.next_state()
    assert str(lights).split("\n") == [
        "#..#.#",
        "#....#",
        ".#.##.",
        "...##.",
        ".#..##",
        "##.###"
    ]

    lights.next_state()
    assert str(lights).split("\n") == [
        "#...##",
        "####.#",
        "..##.#",
        "......",
        "##....",
        "####.#"
    ]

    lights.next_state()
    assert str(lights).split("\n") == [
        "#.####",
        "#....#",
        "...#..",
        ".##...",
        "#.....",
        "#.#..#",
    ]

    lights.next_state()
    assert str(lights).split("\n") == [
        "##.###",
        ".##..#",
        ".##...",
        ".##...",
        "#.#...",
        "##...#",
    ]
