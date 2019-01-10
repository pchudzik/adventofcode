import itertools
from functools import reduce

"""
--- Day 9: All in a Single Night ---

Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have provided him the distances between every pair of locations. He can start and end at any two (different) locations he wants, but he must visit each location exactly once. What is the shortest distance he can travel to achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982
The shortest of these is London -> Dublin -> Belfast = 605, and so the answer is 605 in this example.

What is the distance of the shortest route?

Your puzzle answer was 251.

--- Part Two ---

The next year, just to show off, Santa decides to take the route with the longest distance instead.

He can still start and end at any two (different) locations he wants, and he still must visit each location exactly once.

For example, given the distances above, the longest route would be 982 via (for example) Dublin -> London -> Belfast.

What is the distance of the longest route?

Your puzzle answer was 898.
"""


def resolve_routes(input_routes):
    available_routes = [parse_route(route) for route in input_routes]
    all_cities = {city for city_start, city_end, _ in available_routes for city in (city_start, city_end)}

    return set(map(
        lambda route: calculate_distance(available_routes, route),
        itertools.permutations(all_cities)))


def calculate_distance(available_routes, route):
    city_pairs = [{route[city_idx], route[city_idx + 1]} for city_idx in range(len(route) - 1)]
    total_distance = reduce(
        lambda result, cities: result + find_distance(available_routes, cities),
        city_pairs, 0)

    return route, total_distance


def find_shortest_distance(routes):
    return find_max_distance(routes, True)


def find_longest_distance(routes):
    return find_max_distance(routes, False)


def find_max_distance(routes, is_shortest):
    idx = 0 if is_shortest else -1
    return sorted(routes, key=lambda route: route[1])[idx]


def find_distance(available_routes, city_route):
    return next(
        route[2]
        for route in available_routes
        if {route[0], route[1]} == city_route)


def parse_route(route):
    parts = route.replace(" to ", ";").replace(" = ", ";").split(";")
    return parts[0], parts[1], int(parts[2])


if __name__ == "__main__":
    with open("09_routes.lst") as file:
        routes_input = resolve_routes(file.readlines())
        print("Shortest route is: ", find_shortest_distance(routes_input))
        print("Longest route is: ", find_longest_distance(routes_input))
