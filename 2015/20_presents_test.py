import importlib
import pytest

presents_module = importlib.import_module("20_presents")
house_number_to_receive_gifts = presents_module.house_number_to_receive_gifts1


@pytest.mark.parametrize(
    "number_of_gifts, house_number", [
        (10, 1),
        (30, 2),
        (40, 3),
        (70, 4),
        (60, 4),
        (120, 6),
        (80, 6),
        (150, 8),
        (130, 8)])
def test_house_number_to_receive_gifts(number_of_gifts, house_number):
    assert house_number_to_receive_gifts(number_of_gifts) == house_number
