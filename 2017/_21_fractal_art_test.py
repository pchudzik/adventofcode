import pytest

from _21_fractal_art import pattern_reader, \
    pattern_variants, \
    divide_pattern, \
    join_pattern, \
    rule_definition_parser, \
    transform, \
    lit_pixels


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
            "##.\n"
            "#.#\n"
            "#.."
        ), (
            "#..\n"
            "#.#\n"
            "##."
        ), (
            ".#.\n"
            "#..\n"
            "###"
        ), (
            "###\n"
            "#..\n"
            ".#."
        ), (
            "###\n"
            "..#\n"
            ".#."
        ), (
            "..#\n"
            "#.#\n"
            ".##"
        ), (
            ".#.\n"
            "..#\n"
            "###"
        ), (
            ".##\n"
            "#.#\n"
            "..#"
        )}


def test_divide_pattern_by_2():
    pattern = ("#..#\n"
               "....\n"
               "....\n"
               "#..#").split("\n")

    assert divide_pattern(pattern, 2) == [
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
               "##.##.").split("\n")

    assert divide_pattern(pattern, 3) == [
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


def test_join_pattern_2():
    split = [
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

    assert join_pattern(split) == ("#..#\n"
                                   "....\n"
                                   "....\n"
                                   "#..#")


def test_join_pattern_by_3():
    split = [
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

    assert join_pattern(split) == ("#..##.\n"
                                   "#.##.#\n"
                                   "#.#.#.\n"
                                   "..##..\n"
                                   ".#.#.#\n"
                                   "##.##.")


def test_rule_definition_parser():
    rules = [
        "../.# => ##./#../...",
        ".#./..#/### => #..#/..../..../#..#"
    ]

    assert rule_definition_parser(rules) == {
        "..\n.#": "##.\n#..\n...",
        ".#.\n..#\n###": "#..#\n....\n....\n#..#"
    }


def test_transform():
    rules = rule_definition_parser([
        "../.# => ##./#../...",
        ".#./..#/### => #..#/..../..../#..#"
    ])
    pattern = (".#.\n"
               "..#\n"
               "###")

    pattern = transform(pattern, rules, 1)

    assert pattern == ("#..#\n"
                       "....\n"
                       "....\n"
                       "#..#")

    pattern = transform(pattern, rules, 1)

    assert pattern == ("##.##.\n"
                       "#..#..\n"
                       "......\n"
                       "##.##.\n"
                       "#..#..\n"
                       "......")


def test_sample():
    rules = rule_definition_parser([
        "../.# => ##./#../...",
        ".#./..#/### => #..#/..../..../#..#"
    ])
    pattern = (".#.\n"
               "..#\n"
               "###")

    assert lit_pixels(pattern, rules, 2) == 12
