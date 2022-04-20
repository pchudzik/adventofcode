"""
--- Day 14: Reindeer Olympics ---

This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must rest occasionally to recover their energy.
Santa would like to know which of his reindeer is fastest, and so he has them race.

Reindeer can only either be flying (always at their top speed) or resting (not moving at all), and always spend whole
seconds in either state.

For example, suppose you have the following Reindeer:

Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

After one second, Comet has gone 14 km, while Dancer has gone 16 km. After ten seconds, Comet has gone 140 km, while
Dancer has gone 160 km. On the eleventh second, Comet begins resting (staying at 140 km), and Dancer continues on for a
total distance of 176 km. On the 12th second, both reindeer are resting. They continue to rest until the 138th second,
when Comet flies for another ten seconds. On the 174th second, Dancer flies for another 11 seconds.

In this example, after the 1000th second, both reindeer are resting, and Comet is in the lead at 1120 km (poor Dancer
has only gotten 1056 km by that point). So, in this situation, Comet would win (if the race ended at 1000 seconds).

Given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, what distance has the
winning reindeer traveled?

Your puzzle answer was 2660.

--- Part Two ---

Seeing how reindeer move in bursts, Santa decides he's not pleased with the old scoring system.

Instead, at the end of each second, he awards one point to the reindeer currently in the lead. (If there are multiple
reindeer tied for the lead, they each get one point.) He keeps the traditional 2503 second time limit, of course, as
doing otherwise would be entirely ridiculous.

Given the example reindeer from above, after the first second, Dancer is in the lead and gets one point. He stays in the
lead until several seconds into Comet's second burst: after the 140th second, Comet pulls into the lead and gets his
first point. Of course, since Dancer had been in the lead for the 139 seconds before that, he has accumulated 139 points
by the 140th second.

After the 1000th second, Dancer has accumulated 689 points, while poor Comet, our old champion, only has 312. So, with
the new scoring system, Dancer would win (if the race ended at 1000 seconds).

Again given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, how many points does
the winning reindeer have?

Your puzzle answer was 1256.
"""


def reindeer_parser(puzzle):
    import re

    match = re.search(
        r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.",
        puzzle)
    return Reindeer(
        name=match.group(1),
        speed=int(match.group(2)),
        fly_time=int(match.group(3)),
        rest_time=int(match.group(4))
    )


class Reindeer:
    def __init__(self, name, speed, fly_time, rest_time):
        self.name = name
        self.speed = speed
        self.rest_time = rest_time
        self.fly_time = fly_time

    def traveled_distance(self, elapsed_time):
        full_cycle = self.rest_time + self.fly_time

        traveled_distance = (elapsed_time // full_cycle) * self.speed * self.fly_time
        traveled_distance += min(elapsed_time % full_cycle, self.fly_time) * self.speed

        return traveled_distance


def find_top_travelers(reindeers, time):
    traveled_distances = [(r, r.traveled_distance(time)) for r in reindeers]
    return sorted(traveled_distances, key=lambda t: t[1], reverse=True)


def find_best_leaders(reindeers, time):
    race = dict([(r, 0) for r in reindeers])
    for t in range(1, time + 1):
        leaders_in_second = find_top_travelers(reindeers, t)
        most_traveled_distance = max(leaders_in_second, key=lambda t: t[1])[1]
        for raindeer, distance in filter(lambda t: t[1] == most_traveled_distance, leaders_in_second):
            race[raindeer] += 1

    return sorted(race.items(), key=lambda t: t[1], reverse=True)


if __name__ == "__main__":
    with open("_14_reindeer_olympics.txt") as file:
        reindeers = [reindeer_parser(reindeer_input) for reindeer_input in file.readlines()]
        top_traveler = find_top_travelers(reindeers, 2503)[0]
        top_leader = find_best_leaders(reindeers, 2503)[0]
        print("Winner is ", top_traveler[0].name, "with distance", top_traveler[1])
        print("Leader is ", top_leader[0].name, "with scope", top_leader[1])
