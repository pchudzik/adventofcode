import importlib
import pytest

module = importlib.import_module("21_fractal_art")
pattern_reader = module.pattern_reader
pattern_variants = module.pattern_variants
divide_pattern = module.divide_pattern


@pytest.mark.parametrize("input, pattern", [
    ("../.#", "..\n.#"),
    (".#./..#/###", ".#.\n..#\n###"),
    ("#..#/..../#..#/.##.", "#..#\n....\n#..#\n.##.")
])
def test_pattern_reader(input, pattern):
    assert pattern_reader(input) == pattern


def test_pattern_variants():
    pattern = (".#.\n"
               "..#\n"
               "###")

    assert set(pattern_variants(pattern)) == {
        (
            ".#.\n"
            "..#\n"
            "###"),
        (
            "###\n"
            "..#\n"
            ".#."),
        (
            ".#.\n"
            "#..\n"
            "###"),
        (
            "#..\n"
            "#.#\n"
            "##.")
    }


def test_divide_pattern_by_2():
    pattern = ("#..#\n"
               "....\n"
               "....\n"
               "#..#")

    assert list(divide_pattern(pattern, 2)) == [
        [
            (
                "#.\n"
                ".."),
            (
                ".#\n"
                "..")
        ], [
            (
                "..\n"
                "#."),
            (
                "..\n"
                ".#")
        ]

    ]


def test_divide_pattern_by_3():
    pattern = ("#..##.\n"
               "#.##.#\n"
               "#.#.#.\n"
               "..##..\n"
               ".#.#.#\n"
               "##.##.")

    assert list(divide_pattern(pattern, 3)) == [
        [
            (
                "#..\n"
                "#.#\n"
                "#.#"),
            (
                "##.\n"
                "#.#\n"
                ".#.")
        ], [
            (
                "..#\n"
                ".#.\n"
                "##."),
            (
                "#..\n"
                "#.#\n"
                "##.")
        ]

    ]
