import pytest

from _14_chocolate_charts import find_score_part1, find_score_part2


@pytest.mark.parametrize(
    "recipe_count, score", [
        (9, "5158916779"),
        (5, "0124515891"),
        (18, "9251071085"),
        (2018, "5941429882")
    ])
def test_recipe_score(recipe_count, score):
    assert find_score_part1(recipe_count) == score


@pytest.mark.parametrize(
    "recipe, recipe_count", [
        ("51589", 9),
        ("01245", 5),
        ("92510", 18),
        ("59414", 2018)
    ])
def test_recipe_score(recipe, recipe_count):
    assert find_score_part2(recipe) == recipe_count
