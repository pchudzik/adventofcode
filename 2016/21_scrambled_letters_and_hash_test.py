import importlib
import pytest

module = importlib.import_module("21_scrambled_letters_and_hash")

parse_cmd = module.parse_cmd
password_generator = module.password_generator
unscrabble_password = module.unscrabble_password


def test_password_generator():
    cmds = [
        "swap position 4 with position 0",
        "swap letter d with letter b",
        "reverse positions 0 through 4",
        "rotate left 1 step",
        "move position 1 to position 4",
        "move position 3 to position 0",
        "rotate based on position of letter b",
        "rotate based on position of letter d"
    ]

    assert password_generator(cmds, "abcde") == "decab"


def test_password_unscrabble():
    cmds = [
        "swap position 4 with position 0",
        "swap letter d with letter b",
        "reverse positions 0 through 4",
        "rotate left 1 step",
        "move position 1 to position 4",
        "move position 3 to position 0",
        "rotate based on position of letter b",
        "rotate based on position of letter d"
    ]

    assert unscrabble_password(cmds, "fbdecgha") == "abcdefgh"


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("swap position 4 with position 0", "abcde", "ebcda"),
        ("swap position 0 with position 4", "abcde", "ebcda"),
        ("swap position 0 with position 1", "abcde", "bacde"),
        ("swap position 0 with position 1", "abcde", "bacde")])
def test_swap_position(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("swap position 4 with position 0", "ebcda", "abcde"),
        ("swap position 0 with position 4", "ebcda", "abcde"),
        ("swap position 0 with position 1", "bacde", "abcde"),
        ("swap position 0 with position 1", "bacde", "abcde")])
def test_swap_position_undo(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd.undo(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("swap letter d with letter b", "ebcda", "edcba"),
        ("swap letter a with letter b", "abcde", "bacde")])
def test_swap_letter(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("swap letter d with letter b", "edcba", "ebcda"),
        ("swap letter a with letter b", "bacde", "abcde")])
def test_swap_letter_undo(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd.undo(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("rotate left 1 step", "abcde", "bcdea"),
        ("rotate left 3 steps", "abcde", "deabc"),
        ("rotate right 1 step", "abcde", "eabcd"),
        ("rotate right 2 steps", "abcde", "deabc")])
def test_rotate(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("rotate left 1 step", "bcdea", "abcde"),
        ("rotate left 3 steps", "deabc", "abcde"),
        ("rotate right 1 step", "eabcd", "abcde"),
        ("rotate right 2 steps", "deabc", "abcde")])
def test_rotate_undo(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd.undo(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("rotate based on position of letter b", "abdec", "ecabd"),
        ("rotate based on position of letter d", "ecabd", "decab"),
        ("rotate based on position of letter g", "ghefbcad", "dghefbca")
    ])
def test_rotate_based_on_position(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("rotate based on position of letter X", "7X123456", "X1234567"),
        ("rotate based on position of letter X", "670X2345", "0X234567"),
        ("rotate based on position of letter X", "56701X34", "01X34567"),
        ("rotate based on position of letter X", "4567012X", "012X4567"),
        ("rotate based on position of letter X", "23X56701", "0123X567"),
        ("rotate based on position of letter X", "1234X670", "01234X67"),
        ("rotate based on position of letter X", "012345X7", "012345X7"),
        ("rotate based on position of letter X", "X0123456", "0123456X")])
def test_rotate_based_on_position_undo(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd.undo(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("reverse positions 0 through 4", "edcba", "abcde"),
        ("reverse positions 0 through 1", "abcd", "bacd")])
def test_reverse_positions(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("reverse positions 0 through 4", "abcde", "edcba"),
        ("reverse positions 0 through 1", "bacd", "abcd")])
def test_reverse_positions_undo(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd.undo(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("move position 1 to position 4", "bcdea", "bdeac"),
        ("move position 3 to position 0", "bdeac", "abdec")
    ])
def test_move_position(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd(input) == expected


@pytest.mark.parametrize(
    "cmd, input, expected", [
        ("move position 1 to position 4", "bdeac", "bcdea"),
        ("move position 3 to position 0", "abdec", "bdeac")])
def test_move_position_undo(cmd, input, expected):
    cmd = parse_cmd(cmd)

    assert cmd.undo(input) == expected
