import pytest

from _16_permutation_promenade import dance, dance_many, parse_cmd


@pytest.mark.parametrize(
    "start, cmd, end", [
        ("abcde", "s0", "abcde"),
        ("abcde", "s1", "eabcd"),
        ("abcde", "s2", "deabc"),
        ("abcde", "s3", "cdeab"),
        ("abcde", "s4", "bcdea"),
        ("abcde", "s5", "abcde")
    ])
def test_spin(start, cmd, end):
    assert dance(start, [parse_cmd(cmd)]) == end


def test_exchange():
    assert dance("eabcd", [parse_cmd("x3/4")]) == "eabdc"


def test_partner():
    assert dance("eabdc", [parse_cmd("pe/b")]) == "baedc"
    assert dance("cdpabe", [parse_cmd("pp/e")]) == "cdeabp"


@pytest.mark.parametrize(
    "start, count, end", [
        ("abc", 2, "bca"),
        ("abc", 6, "abc"),
        ("abc", 7, "cab"),
        ("abc", 7, "cab"),
        ("abc", 9, "abc")])
def test_dance_many(start, count, end):
    """
    abc
    cab
    bca
    abc
    cab
    bca
    abc
    cab
    bca
    abc
    """
    cmds = [parse_cmd("s1")]

    assert dance_many(start, cmds, count) == end
