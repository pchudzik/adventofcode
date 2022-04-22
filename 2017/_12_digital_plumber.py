"""
--- Day 12: Digital Plumber ---

Walking along the memory banks of the stream, you find a small village that is experiencing a little confusion: some
programs can't communicate with each other.

Programs in this village communicate using a fixed system of pipes. Messages are passed between programs using these
pipes, but most programs aren't connected to each other directly. Instead, programs pass messages between each other
until the message reaches the intended recipient.

For some reason, though, some of these messages aren't ever reaching their intended recipient, and the programs suspect
that some pipes are missing. They would like you to investigate.

You walk through the village and record the ID of each program and the IDs with which it can communicate directly (your
puzzle input). Each program has one or more programs with which it can communicate, and these pipes are bidirectional;
if 8 says it can communicate with 11, then 11 will say it can communicate with 8.

You need to figure out how many programs are in the group that contains program ID 0.

For example, suppose you go door-to-door like a travelling salesman and record the following list:
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
In this example, the following programs are in the group that contains program ID 0:

Program 0 by definition.
Program 2, directly connected to program 0.
Program 3 via program 2.
Program 4 via program 2.
Program 5 via programs 6, then 4, then 2.
Program 6 via programs 4, then 2.
Therefore, a total of 6 programs are in this group; all but program 1, which has a pipe that connects it to itself.

How many programs are in the group that contains program ID 0?

Your puzzle answer was 115.

--- Part Two ---

There are more programs than just the ones in the group containing program ID 0. The rest of them have no way of
reaching that group, and still might have no way of reaching each other.

A group is a collection of programs that can all communicate via pipes either directly or indirectly. The programs you
identified just a moment ago are all part of the same group. Now, they would like you to determine the total number of
groups.

In the example above, there were 2 groups: one consisting of programs 0,2,3,4,5,6, and the other consisting solely of
program 1.

How many groups are there in total?

Your puzzle answer was 221.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

import re
from collections import deque

pipe_pattern = re.compile(r"(\d+) <-> (.*)")


class Pipe:
    def __init__(self, id):
        self.id = id
        self.connections = []

    def can_access(self, program_id, ):
        return program_id in self.programs_in_group()

    def programs_in_group(self):
        group = set()
        to_visit = deque(self.connections)

        while to_visit:
            connection = to_visit.popleft()
            if connection.id in group:
                continue
            else:
                group.add(connection.id)

            to_visit.extend(c for c in connection.connections if c.id not in group)

        return frozenset(group)

    @property
    def connection_ids(self):
        return [p.id for p in self.connections]


def count_programs_with_access_to(all_programs, program_id):
    return sum(p.can_access(program_id) for p in all_programs)


def find_number_of_groups(all_programs):
    return len(set(p.programs_in_group() for p in all_programs))


def parse_pipes(pipes):
    result = dict()
    for pipe in pipes:
        program, connections = parse_single_pipe(pipe)

        source = result.get(program, Pipe(program))
        result[source.id] = source
        for connection_id in connections:
            connection = result.get(connection_id, Pipe(connection_id))
            source.connections.append(connection)
            result[connection_id] = connection

    return result


def parse_single_pipe(pipe):
    matched = pipe_pattern.match(pipe)
    source = int(matched.group(1))
    pipes = matched.group(2)
    return source, (map(int, pipes.split(", ")))


if __name__ == "__main__":
    with open("_12_digital_plumber.txt") as file:
        pipes = parse_pipes(file.readlines())
        print(f"part 1: {count_programs_with_access_to(pipes.values(), 0)}")
        print(f"part 2: {find_number_of_groups(pipes.values())}")
