from collections import namedtuple

Elve = namedtuple("Elve", "index, presents")


def run_round(elves):
    if len(elves) == 1:
        return elves
    result = []
    for pair in zip(elves[::2], elves[1::2]):
        elve = Elve(pair[0].index, pair[0].presents + pair[1].presents)
        result.append(elve)

    if len(elves) > 2 and len(elves) % 2 == 1:
        last_elve = Elve(elves[-1].index, result[0].presents + elves[-1].presents)
        return result[1:] + [last_elve]

    return result


def find_elve_with_all_presents(elves):
    while len(elves) > 1:
        elves = run_round(elves)

    return elves[0]


if __name__ == "__main__":
    puzzle = 3001330
    winner_part1 = find_elve_with_all_presents([Elve(i + 1, 1) for i in range(puzzle)])

    print(f"part 1: {winner_part1}")
