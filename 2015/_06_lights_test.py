import pytest

from _06_lights import SimpleLights, LightsWithBrightnessControll, parse_command


def test_turn_on():
    lights = SimpleLights(1000, False)

    lights.turn_on((0, 0), (999, 999))

    assert lights.number_of_lit_lights == 1000 * 1000


def test_toggle():
    lights = SimpleLights(1000, False)

    lights.toggle((0, 0), (999, 0))

    assert lights.number_of_lit_lights == 1000


def test_turn_off():
    lights = SimpleLights(1000, True)

    lights.turn_off((499, 499), (500, 500))

    assert lights.number_of_lit_lights == 1000 * 1000 - 4


@pytest.mark.parametrize(
    "command_string, command", [
        ("turn off 875,549 through 972,643", ("off", (875, 549), (972, 643))),
        ("toggle 313,212 through 489,723", ("toggle", (313, 212), (489, 723))),
        ("turn on 342,861 through 725,935", ("on", (342, 861), (725, 935)))
    ])
def test_parse_command(command_string, command):
    assert parse_command(command_string) == command


@pytest.mark.parametrize(
    "command, expected_brigtness", [
        (("on", (0, 0), (0, 0)), 1),
        (("toggle", (0, 0), (999, 999)), 2000000),
        (("off", (0, 0), (999, 999)), 0)
    ])
def test_brigntess(command, expected_brigtness):
    lights = LightsWithBrightnessControll(1000, 0)

    lights.execute(command)

    assert lights.total_brightness == expected_brigtness
