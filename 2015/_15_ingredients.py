import itertools
import re

"""
--- Day 15: Science for Hungry People ---

Today, you set out on the task of perfecting your milk-dunking cookie recipe. All you have to do is find the right
balance of ingredients.

Your recipe leaves room for exactly 100 teaspoons of ingredients. You make a list of the remaining ingredients you could
use to finish the recipe (your puzzle input) and their properties per teaspoon:

capacity (how well it helps the cookie absorb milk)
durability (how well it keeps the cookie intact when full of milk)
flavor (how tasty it makes the cookie)
texture (how it improves the feel of the cookie)
calories (how many calories it adds to the cookie)

You can only measure ingredients in whole-teaspoon amounts accurately, and you have to be accurate so you can reproduce
your results in the future. The total score of a cookie can be found by adding up each of the properties (negative
totals become 0) and then multiplying together everything except calories.

For instance, suppose you have these two ingredients:

Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of cinnamon (because the amounts of each ingredient
must add up to 100) would result in a cookie with the following properties:

A capacity of 44*-1 + 56*2 = 68
A durability of 44*-2 + 56*3 = 80
A flavor of 44*6 + 56*-2 = 152
A texture of 44*3 + 56*-1 = 76

Multiplying these together (68 * 80 * 152 * 76, ignoring calories for now) results in a total score of 62842880, which
happens to be the best score possible given these ingredients. If any properties had produced a negative total, it would
have instead become zero, causing the whole score to multiply to zero.

Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you
can make?

Your puzzle answer was 13882464.

--- Part Two ---

Your cookie recipe becomes wildly popular! Someone asks if you can make another recipe that has exactly 500 calories per
cookie (so they can use it as a meal replacement). Keep the rest of your award-winning process the same (100 teaspoons,
same ingredients, same scoring system).

For example, given the ingredients above, if you had instead selected 40 teaspoons of butterscotch and 60 teaspoons of
cinnamon (which still adds to 100), the total calorie count would be 40*8 + 60*3 = 500. The total score would go down,
though: only 57600000, the best you can do in such trying circumstances.

Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you
can make with a calorie total of 500?

Your puzzle answer was 11171160.
"""


def parse_ingredients(ingredients_text):
    "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8"
    match = re.match(
        r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)",
        ingredients_text)

    return Ingredient(
        name=match.group(1),
        capacity=int(match.group(2)),
        durability=int(match.group(3)),
        flavor=int(match.group(4)),
        texture=int(match.group(5)),
        calories=int(match.group(6)))


class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def __repr__(self):
        return self.name


class MixingResult:
    def __init__(self, ingredients, proportions):
        self.ingredients = ingredients
        self.proportions = proportions

    @property
    def total_score(self):
        def total_ingredient(name):
            return sum([
                getattr(ingredient, name) * proportion
                for ingredient, proportion
                in zip(self.ingredients, self.proportions)
            ])

        capacity_total = total_ingredient("capacity")
        durability_total = total_ingredient("durability")
        flavor_total = total_ingredient("flavor")
        texture_total = total_ingredient("texture")

        if capacity_total < 0 or durability_total < 0 or flavor_total < 0 or texture_total < 0:
            return 0
        else:
            return capacity_total * durability_total * flavor_total * texture_total

    @property
    def total_calories(self):
        return sum(
            ingredient.calories * proportion
            for ingredient, proportion
            in zip(self.ingredients, self.proportions))

    def __repr__(self):
        return "Total: {}, proportions: {}, ingredients: {}" \
            .format(str(self.total_score), self.proportions, self.ingredients)


class CookingBowl:
    def __init__(self, ingredients):
        self.ingredients = list(ingredients)
        self.mixes = []

    @property
    def best_mix(self):
        return max(
            self.mixes,
            key=lambda mix: mix.total_score)

    def best_mix_with_calories_limit(self, calories_limit):
        return max(
            filter(
                lambda mix: mix.total_calories == calories_limit,
                self.mixes),
            key=lambda mix: mix.total_score)

    def mix(self, total_number_of_spoons):
        proportions = [list(range(0, total_number_of_spoons + 1)) for i in self.ingredients]
        proportions = filter(
            lambda spoons: sum(spoons) == total_number_of_spoons,
            itertools.product(*proportions))
        results = []
        for proportion in proportions:
            results.append(MixingResult(self.ingredients, proportion))

        self.mixes = results


if __name__ == "__main__":
    ingredients = [parse_ingredients(text) for text in [
        "Sprinkles: capacity 5, durability -1, flavor 0, texture 0, calories 5",
        "PeanutButter: capacity -1, durability 3, flavor 0, texture 0, calories 1",
        "Frosting: capacity 0, durability -1, flavor 4, texture 0, calories 6",
        "Sugar: capacity -1, durability 0, flavor 0, texture 2, calories 8"
    ]]
    cooking_bowl = CookingBowl(ingredients)
    cooking_bowl.mix(100)

    print("Best mix is ", cooking_bowl.best_mix)
    print("Best mix is with calories limit is", cooking_bowl.best_mix_with_calories_limit(500))
