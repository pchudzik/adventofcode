import math
from functools import reduce


def calculate_fuel(mass):
    return math.floor(mass / 3) - 2


def calculate_fuel_with_fuel(mass):
    fuel = calculate_fuel(mass)
    return fuel + calculate_fuel_for_fuel(fuel)


def calculate_fuel_for_fuel(fuel):
    fuel_for_fuel = math.floor(fuel / 3) - 2
    return 0 if fuel_for_fuel < 0 else fuel_for_fuel + calculate_fuel_for_fuel(fuel_for_fuel)


def parse_input(lines):
    return [int(mass) for mass in lines]


def solve_puzzle(puzzle, fuel_calculator):
    fuel_mass = [fuel_calculator(mass) for mass in puzzle]
    return reduce(lambda a, b: a + b, fuel_mass)


def part1(puzzle):
    return solve_puzzle(puzzle, calculate_fuel)


def part2(puzzle):
    return solve_puzzle(puzzle, calculate_fuel_with_fuel)


if __name__ == "__main__":
    with open("01_the_tyranny_of_the_rocket_equation.txt", "r") as file:
        puzzle_input = parse_input(file.readlines())

        print(f"part 1: {part1(puzzle_input)}")
        print(f"part 2: {part2(puzzle_input)}")
