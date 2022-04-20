from _09_routes import resolve_routes, find_shortest_distance, find_longest_distance


def test_find_shortest_distance():
    shortest = find_shortest_distance({
        (("Dublin", "London", "Belfast"), 982),
        (("Dublin", "Belfast", "London"), 659),
        (("London", "Dublin", "Belfast"), 605),
        (("London", "Belfast", "Dublin"), 659),
        (("Belfast", "Dublin", "London"), 605),
        (("Belfast", "London", "Dublin"), 982)
    })

    assert 605 == shortest[1]


def test_find_longest_distance():
    longest = find_longest_distance({
        (("Dublin", "London", "Belfast"), 982),
        (("Dublin", "Belfast", "London"), 659),
        (("London", "Dublin", "Belfast"), 605),
        (("London", "Belfast", "Dublin"), 659),
        (("Belfast", "Dublin", "London"), 605),
        (("Belfast", "London", "Dublin"), 982)
    })

    assert 982 == longest[1]


def test_routes_calculator():
    routes_input = (
        "London to Dublin = 464",
        "London to Belfast = 518",
        "Dublin to Belfast = 141"
    )

    assert resolve_routes(routes_input) == {
        (("Dublin", "London", "Belfast"), 982),
        (("Dublin", "Belfast", "London"), 659),
        (("London", "Dublin", "Belfast"), 605),
        (("London", "Belfast", "Dublin"), 659),
        (("Belfast", "Dublin", "London"), 605),
        (("Belfast", "London", "Dublin"), 982)
    }
