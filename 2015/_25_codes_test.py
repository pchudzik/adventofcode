import pytest

from _25_codes import next_number, diagonal_resolver, get_code


@pytest.mark.parametrize(
    "number,result", [
        (20151125, 31916031),
        (31916031, 18749137),
        (16080970, 21629792),
        (21629792, 17289845)])
def test_next_number(number, result):
    assert next_number(number) == result


@pytest.mark.parametrize(
    "x, y, result", [
        (1, 1, 20151125),
        (1, 2, 31916031),
        (2, 4, 32451966)])
def test_get_code(x, y, result):
    assert get_code(x, y) == result


@pytest.mark.parametrize(
    "x,y,result", [
        (3, 2, 9),
        (6, 4, 42),
        (7, 2, 35)])
def test_diagonal_resolve(x, y, result):
    assert diagonal_resolver(x, y) == result
