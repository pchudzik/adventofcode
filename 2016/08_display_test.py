import importlib

Display = importlib.import_module("08_display").Display


def test_create_blank_display():
    display = Display(3, 2)

    assert display.display == [
        "...",
        "..."
    ]


def test_lit_rect():
    display = Display(width=7, height=3)

    display.execute("rect 3x2")

    assert display.display == [
        "###....",
        "###....",
        "......."
    ]


def test_rotate_column():
    display = Display(width=7, height=3, initial=[
        [True, True, True, False, False, False, False],
        [True, True, True, False, False, False, False],
        [False, False, False, False, False, False, False]])

    display.execute("rotate column x=1 by 1")

    assert display.display == [
        "#.#....",
        "###....",
        ".#....."
    ]

    display.execute("rotate column x=1 by 1")

    assert display.display == [
        "###....",
        "#.#....",
        ".#....."
    ]

    display.execute("rotate column x=1 by 1")

    assert display.display == [
        "###....",
        "###....",
        "......."
    ]


def tet_rotate_column2():
    display = Display(width=7, height=3, initial=[
        [False, False, False, False, True, False, True],
        [True, True, True, False, False, False, False],
        [False, True, False, False, False, False, False]])

    display.execute("rotate column x=1 by 1")

    assert display.display == [
        ".#..#.#",
        "#.#....",
        ".#....."""
    ]


def test_rotate_row():
    display = Display(width=7, height=3, initial=[
        [True, False, True, False, False, False, False],
        [True, True, True, False, False, False, False],
        [False, True, False, False, False, False, False]])

    display.execute("rotate row y=0 by 4")

    assert display.display == [
        "....#.#",
        "###....",
        ".#....."
    ]

    display.execute("rotate row y=0 by 1")

    assert display.display == [
        "#....#.",
        "###....",
        ".#....."
    ]

    display.execute("rotate row y=0 by 1")

    assert display.display == [
        ".#....#",
        "###....",
        ".#....."
    ]

    display.execute("rotate row y=0 by 1")

    assert display.display == [
        "#.#....",
        "###....",
        ".#....."
    ]


def test_lit_pixes():
    display = Display(width=7, height=3)

    display.execute("rect 3x2")
    display.execute("rotate column x=1 by 1")
    display.execute("rotate row y=0 by 4")
    display.execute("rotate column x=1 by 1")

    assert display.lit_pixels == 6
    assert display.display == [
        ".#..#.#",
        "#.#....",
        ".#....."
    ]


def test_display_customized():
    display = Display(2, 2, lit_pixel="X", blank_pixel="_")

    display.execute("rect 1x1")

    assert display.display == [
        "X_",
        "__"
    ]
