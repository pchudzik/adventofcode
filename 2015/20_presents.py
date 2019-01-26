from math import sqrt

"""
--- Day 20: Infinite Elves and Infinite Houses ---

To keep the Elves busy, Santa has them deliver some presents by hand, door-to-door. He sends them down a street with
infinite houses numbered sequentially: 1, 2, 3, 4, 5, and so on.

Each Elf is assigned a number, too, and delivers presents to houses based on that number:

The first Elf (number 1) delivers presents to every house: 1, 2, 3, 4, 5, ....
The second Elf (number 2) delivers presents to every second house: 2, 4, 6, 8, 10, ....
Elf number 3 delivers presents to every third house: 3, 6, 9, 12, 15, ....

There are infinitely many Elves, numbered starting with 1. Each Elf delivers presents equal to ten times his or her
number at each house.

So, the first nine houses on the street end up like this:

House 1 got 10 presents.
House 2 got 30 presents.
House 3 got 40 presents.
House 4 got 70 presents.
House 5 got 60 presents.
House 6 got 120 presents.
House 7 got 80 presents.
House 8 got 150 presents.
House 9 got 130 presents.

The first house gets 10 presents: it is visited only by Elf 1, which delivers 1 * 10 = 10 presents. The fourth house
gets 70 presents, because it is visited by Elves 1, 2, and 4, for a total of 10 + 20 + 40 = 70 presents.

What is the lowest house number of the house to get at least as many presents as the number in your puzzle input?

Your puzzle answer was 831600.

--- Part Two ---

The Elves decide they don't want to visit an infinite number of houses. Instead, each Elf will stop after delivering
presents to 50 houses. To make up for it, they decide to deliver presents equal to eleven times their number at each
house.

With these changes, what is the new lowest house number of the house to get at least as many presents as the number in
your puzzle input?

Your puzzle answer was 884520.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your advent calendar and try another puzzle.

Your puzzle input was 36000000.
"""

divisors_cache = dict()


def house_number_to_receive_gifts(number_of_gifts, presents_calculator):
    for house_index in range(1, int(number_of_gifts / 10) + 1):
        divisors = find_divisors(house_index)
        number_of_gifts_left_in_house = presents_calculator(house_index, divisors)
        if number_of_gifts_left_in_house >= number_of_gifts:
            return house_index


def house_number_to_receive_gifts1(number_of_gifts):
    return house_number_to_receive_gifts(
        number_of_gifts,
        lambda house_index, divisors: sum(divisors) * 10)


def house_number_to_receive_gifts2(number_of_gifts):
    return house_number_to_receive_gifts(
        number_of_gifts,
        lambda house_index, divisors: sum(d for d in divisors if house_index / d <= 50) * 11)


def find_divisors(n):
    if n in divisors_cache:
        return divisors_cache[n]

    result = []
    i = 1

    while i <= sqrt(n):
        if n % i == 0:
            result.append(i)
            if n / i != i:
                result.append(int(n / i))
        i = i + 1

    divisors_cache[n] = result

    return result


if __name__ == "__main__":
    number_of_gifts = 36000000
    part1 = house_number_to_receive_gifts1(number_of_gifts)
    part2 = house_number_to_receive_gifts2(number_of_gifts)
    print("First house to get {} is {}".format(number_of_gifts, part1))
    print("v2 First house to get {} is {}".format(number_of_gifts, part2))
