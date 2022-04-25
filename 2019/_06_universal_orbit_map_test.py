from _06_universal_orbit_map import count_orbits, count_orbit_jumps


def test_count_orbits():
    orbit_map = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
    ]

    assert count_orbits(orbit_map) == 42


def test_count_orbit_jumps():
    orbit_map = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
        "K)YOU",
        "I)SAN",
    ]

    assert count_orbit_jumps(orbit_map, "YOU", "SAN") == 4
