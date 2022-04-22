import pytest

from _01_inverse_captcha import captcha, captcha2


@pytest.mark.parametrize(
    "puzzle, result", [
        ("1122", 3),
        ("1111", 4),
        ("1234", 0),
        ("91212129", 9)])
def test_captcha(puzzle, result):
    assert captcha(puzzle) == result


@pytest.mark.parametrize(
    "puzzle, result", [
        ("1212", 6),
        ("1221", 0),
        ("123425", 4),
        ("123123", 12),
        ("12131415", 4)])
def test_captcha2(puzzle, result):
    assert captcha2(puzzle) == result
