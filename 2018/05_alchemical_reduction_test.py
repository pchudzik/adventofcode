import importlib
import pytest

module = importlib.import_module("05_alchemical_reduction")
reduce_polymer = module.reduce_polymer
is_reducable = module.is_reducable
total_reduce = module.total_reduce
improve_polymer = module.improve_polymer


@pytest.mark.parametrize("in_polymer, out_polymer", [
    ("dabAcCaCBAcCcaDA", "dabCBAcaDA"),
    ("dabCBAcaDA", "dabCBAcaDA"),
])
def test_reduce_polymer(in_polymer, out_polymer):
    assert reduce_polymer(in_polymer) == out_polymer


@pytest.mark.parametrize("a,b, result", [
    ("a", "A", True),
    ("a", "a", False),
    ("A", "A", False)])
def test_is_reducable(a, b, result):
    assert is_reducable(a, b) == result


def test_total_reduce():
    assert total_reduce("dabAcCaCBAcCcaDA") == "dabCBAcaDA"


@pytest.mark.parametrize("in_polymer, removed, out_polymer", [
    ("dabAcCaCBAcCcaDA", "a", "dbCBcD"),
    ("dabAcCaCBAcCcaDA", "b", "daCAcaDA"),
    ("dabAcCaCBAcCcaDA", "c", "daDA"),
    ("dabAcCaCBAcCcaDA", "d", "abCBAc")
])
def test_improve_polymer(in_polymer, removed, out_polymer):
    assert improve_polymer(in_polymer, to_improve=removed) == out_polymer


def test_improve_polymer_auto():
    assert improve_polymer("dabAcCaCBAcCcaDA") == "daDA"
