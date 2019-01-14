import importlib

parse_ingredients = importlib \
    .import_module("15_ingredients") \
    .parse_ingredients
CookingBowl = importlib \
    .import_module("15_ingredients") \
    .CookingBowl
Ingredient = importlib \
    .import_module("15_ingredients") \
    .Ingredient


def test_parse_ingredients():
    ingredients_text = "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8"

    ingredient = parse_ingredients(ingredients_text)

    assert ingredient.name == "Butterscotch"
    assert ingredient.capacity == -1
    assert ingredient.durability == -2
    assert ingredient.flavor == 6
    assert ingredient.texture == 3
    assert ingredient.calories == 8


def test_find_best_mix():
    cooking_bowl = CookingBowl(
        [
            Ingredient(
                name="Butterscotch",
                capacity=-1,
                durability=-2,
                flavor=6,
                texture=3,
                calories=8),
            Ingredient(
                name="Cinnamon",
                capacity=2,
                durability=3,
                flavor=-2,
                texture=-1,
                calories=3)
        ])

    cooking_bowl.mix(100)

    assert cooking_bowl.best_mix.total_score == 62842880


def test_find_best_mix_with_calories_limit():
    cooking_bowl = CookingBowl(
        [
            Ingredient(
                name="Butterscotch",
                capacity=-1,
                durability=-2,
                flavor=6,
                texture=3,
                calories=8),
            Ingredient(
                name="Cinnamon",
                capacity=2,
                durability=3,
                flavor=-2,
                texture=-1,
                calories=3)
        ])

    cooking_bowl.mix(100)

    assert cooking_bowl.best_mix_with_calories_limit(500).total_score == 57600000
