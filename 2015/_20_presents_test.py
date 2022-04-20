import pytest

from _20_presents import house_number_to_receive_gifts1


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
    assert house_number_to_receive_gifts1(number_of_gifts) == house_number
