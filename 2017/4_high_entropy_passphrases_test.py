import importlib
import pytest

module = importlib.import_module("4_high_entropy_passphrases")
is_valid = module.is_valid
find_valid_passphases = module.find_valid_passphases


@pytest.mark.parametrize(
    "password, expected", [
        ("aa bb cc dd ee", True),
        ("aa bb cc dd aa", False),
        ("aa bb cc dd aaa", True)])
def test_is_valid(password, expected):
    assert is_valid(password) == expected


def test_find_valid_passphases():
    assert find_valid_passphases((
        "aa bb cc dd ee",
        "aa bb cc dd aa",
        "aa bb cc dd aaa")) == [
               "aa bb cc dd ee",
               "aa bb cc dd aaa"]
