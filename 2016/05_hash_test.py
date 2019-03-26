import importlib
import pytest

find_password_door1 = importlib.import_module("05_hash").find_password_door1
find_password_door2 = importlib.import_module("05_hash").find_password_door2


@pytest.mark.parametrize(
    "password_len, seed, start_index, step, expected_password", [
        (1, "abc", 3231929, 1, "1"),
        (2, "abc", 3231929, 1785379, "18")
    ])
def test_find_password_door1(password_len, seed, start_index, step, expected_password):
    assert expected_password == find_password_door1(
        seed,
        password_len=password_len,
        start=start_index,
        step=step)


@pytest.mark.parametrize(
    "password_len, seed, start_index, step, stop_after, expected_password", [
        (2, "abc", 3231929, 1, 1, [None, "5"]),
        (5, "abc", 3231929, 2125596, 2, [None, "5", None, None, "e"])
    ])
def test_find_password_door2(password_len, seed, start_index, step, stop_after, expected_password):
    assert expected_password == find_password_door2(
        seed,
        password_len=password_len,
        start=start_index,
        step=step,
        stop_after=stop_after)
