"""
--- Day 6: Universal Orbit Map ---

You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves transferring
between orbits, the orbit maps here are useful for finding efficient routes between, for example, you and Santa. You
download a map of the local orbits (your puzzle input).

Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object. An
orbit looks roughly like this:

                  \
                   \
                    |
                    |
AAA--> o            o <--BBB
                    |
                    |
                   /
                  /

In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is only
partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit around AAA".

Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To verify
maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits (like the one
shown above) and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A
orbits B, B orbits C, and C orbits D, then A indirectly orbits D.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L

Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I

In this visual representation, when two objects are connected by a line, the one on the right directly orbits the one on
the left.

Here, we can count the total number of orbits as follows:

D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
COM orbits nothing.
The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?

Your puzzle answer was 204521.

--- Part Two ---

Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets you
move from any object to an object orbiting or orbited by that object.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN

In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a minimum of 4 orbital
transfers are required:

K to J
J to E
E to D
D to I
Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU

What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is
orbiting? (Between the objects they are orbiting - not between YOU and SAN.)

Your puzzle answer was 307.

Both parts of this puzzle are complete! They provide two gold stars: **
"""
from __future__ import annotations

import functools
import operator
from typing import Iterable, Optional


class Planet:
    def __init__(self, name: str):
        self.name = name
        self.orbits = None  # type: Optional[Planet]
        self.satellites = []  # type: list[Planet]

    def orbits_planet(self, planet: Planet):
        self.orbits = planet

    def add_satellite(self, satellite: Planet):
        satellite.orbits_planet(self)
        self.satellites.append(satellite)

    @property
    def orbits_to_center(self) -> int:
        orbit_of = self
        orbits_count = 0
        while orbit_of.orbits is not None:
            orbit_of = orbit_of.orbits
            orbits_count += 1
        return orbits_count

    @property
    def is_edge_planet(self) -> bool:
        return len(self.satellites) == 0

    @property
    def path_to_center(self) -> list[str]:
        path = []
        orbit_of = self
        while orbit_of.orbits is not None:
            orbit_of = orbit_of.orbits
            path.append(orbit_of.name)
        return path

    def __repr__(self):
        to_string = ", ".join(key + "=" + value for (key, value) in {
            "name": self.name,
            "orbits": self.orbits.name if self.orbits else "",
            "satellites": ",".join(s.name for s in self.satellites)
        }.items())
        return "Planet[" + to_string + "]"


def parse(orbit_map: Iterable[str]) -> dict[str, Planet]:
    result = dict()
    for s in orbit_map:
        (planet, satellite) = s.split(")")
        planet = result[planet] if planet in result else Planet(planet)
        satellite = result[satellite] if satellite in result else Planet(satellite)
        planet.add_satellite(satellite)
        result[planet.name] = planet
        result[satellite.name] = satellite

    return result


def count_orbits(orbit_map: Iterable[str]) -> int:
    planet_system = parse(orbit_map)
    return functools.reduce(
        operator.add,
        (planet.orbits_to_center for planet in planet_system.values())
    )


def count_orbit_jumps(orbit_map: Iterable[str], src: str, dst: str):
    planet_system = parse(orbit_map)
    src = planet_system[src]
    dst = planet_system[dst]
    src_path_to_center = src.path_to_center
    dst_path_to_center = dst.path_to_center
    longest_orbit = src_path_to_center if len(src_path_to_center) > len(dst_path_to_center) else dst_path_to_center
    shortest_orbit = src_path_to_center if len(src_path_to_center) < len(dst_path_to_center) else dst_path_to_center
    for common_planet in longest_orbit:
        if common_planet in shortest_orbit:
            break

    return longest_orbit.index(common_planet) + shortest_orbit.index(common_planet)


if __name__ == "__main__":
    with open("_06_universal_orbit_map.txt") as file:
        puzzle = [p.strip() for p in file.readlines()]
        print("part 1:", count_orbits(puzzle))
        print("part 2:", count_orbit_jumps(puzzle, "YOU", "SAN"))
