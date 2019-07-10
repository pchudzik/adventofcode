import importlib
import pytest

module = importlib.import_module("15_timing_is_everything")
Disc = module.Disc
find_button_push_time = module.find_button_push_time


@pytest.mark.parametrize(
    "disc, time, expected_position", [
        (Disc(number_of_positions=5, start_position=4), 1, 0),
        (Disc(number_of_positions=5, start_position=4), 2, 1),
        (Disc(number_of_positions=5, start_position=4), 3, 2),
        (Disc(number_of_positions=5, start_position=4), 4, 3),
        (Disc(number_of_positions=5, start_position=4), 5, 4),
        (Disc(number_of_positions=5, start_position=4), 6, 0),
        (Disc(number_of_positions=2, start_position=1), 2, 1),
        (Disc(number_of_positions=2, start_position=1), 6, 1),
        (Disc(number_of_positions=2, start_position=1), 7, 0)
    ])
def test_get_disc_position(disc, time, expected_position):
    assert disc.position_at_time(time) == expected_position


@pytest.mark.parametrize(
    "disc, time, is_fallthrough", [
        (Disc(number_of_positions=5, start_position=4), 1, True),
        (Disc(number_of_positions=5, start_position=4), 2, False),
        (Disc(number_of_positions=5, start_position=4), 3, False),
        (Disc(number_of_positions=5, start_position=4), 4, False),
        (Disc(number_of_positions=5, start_position=4), 5, False),
        (Disc(number_of_positions=5, start_position=4), 6, True),
        (Disc(number_of_positions=2, start_position=1), 2, False),
        (Disc(number_of_positions=2, start_position=1), 6, False),
        (Disc(number_of_positions=2, start_position=1), 7, True)])
def test_is_fallthrough(disc, time, is_fallthrough):
    assert disc.is_fall_through(time) == is_fallthrough


def test_find_button_push_time():
    disc1 = Disc(number_of_positions=5, start_position=4)
    disc2 = Disc(number_of_positions=2, start_position=1)

    assert find_button_push_time((disc1, disc2)) == 5
