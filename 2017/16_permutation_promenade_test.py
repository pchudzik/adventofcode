import importlib
import pytest

module = importlib.import_module("16_permutation_promenade")
dance = module.dance
parse_cmd = module.parse_cmd


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
    assert dance([*start], [parse_cmd(cmd)]) == [*end]


def test_exchange():
    assert dance([*"eabcd"], [parse_cmd("x3/4")]) == [*"eabdc"]


def test_partner():
    assert dance([*"eabdc"], [parse_cmd("pe/b")]) == [*"baedc"]
    assert dance([*"cdpabe"], [parse_cmd("pp/e")]) == [*"cdeabp"]
