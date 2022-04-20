from functools import reduce

""" --- Day 17: No Such Thing as Too Much ---

The elves bought too much eggnog again - 150 liters this time. To fit it all into your refrigerator, you'll need to move
it into smaller containers. You take an inventory of the capacities of the available containers.

For example, suppose you have containers of size 20, 15, 10, 5, and 5 liters. If you need to store 25 liters, there are
four ways to do it:

15 and 10
20 and 5 (the first 5)
20 and 5 (the second 5)
15, 5, and 5
Filling all containers entirely, how many different combinations of containers can exactly fit all 150 liters of eggnog?

Your puzzle answer was 654.

--- Part Two ---

While playing with all the containers in the kitchen, another load of eggnog arrives! The shipping and receiving
department is requesting as many containers as you can spare.

Find the minimum number of containers that can exactly fit all 150 liters of eggnog. How many different ways can you
fill that number of containers and still hold exactly 150 litres?

In the example above, the minimum number of containers was two. There were three ways to use that many containers, and
so the answer there would be 3.

Your puzzle answer was 57.
"""


def find_combinations(containers, litters_to_fill):
    list_len = len(containers)
    result = []
    for x in range(0, 2 ** list_len):
        containers_to_pick = bin(x)[2:].zfill(list_len)
        combination = [
            containers[index]
            for index, is_picked
            in zip(range(list_len), containers_to_pick)
            if is_picked == "1"
        ]
        if sum(combination) == litters_to_fill:
            result.append(tuple(sorted(combination)))
    return result


def find_minimum_combinations(all_combinations):
    shortest_combinations = len(reduce(
        lambda c1, c2: c1 if len(c1) < len(c2) else c2,
        all_combinations))
    return list(filter(
        lambda combination: len(combination) == shortest_combinations,
        all_combinations))


if __name__ == "__main__":
    puzzle = (50, 44, 11, 49, 42, 46, 18, 32, 26, 40, 21, 7, 18, 43, 10, 47, 36, 24, 22, 40)
    combinations_to_fill = find_combinations(puzzle, 150)
    minimum_combinations = find_minimum_combinations(combinations_to_fill)
    print("number of combinations", len(combinations_to_fill))
    print("minimum number of combinations", len(minimum_combinations))
