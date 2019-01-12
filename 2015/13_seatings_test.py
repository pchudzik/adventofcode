import importlib

parse_seatings = importlib \
    .import_module("13_seatings") \
    .parse_seatings
count_happiness = importlib \
    .import_module("13_seatings") \
    .count_happiness
happines_change = importlib \
    .import_module("13_seatings") \
    .happines_change
include_me = importlib \
    .import_module("13_seatings") \
    .include_me

attendees = [
    "Alice would gain 54 happiness units by sitting next to Bob.",
    "Alice would lose 79 happiness units by sitting next to Carol.",
    "Alice would lose 2 happiness units by sitting next to David.",
    "Bob would gain 83 happiness units by sitting next to Alice.",
    "Bob would lose 7 happiness units by sitting next to Carol.",
    "Bob would lose 63 happiness units by sitting next to David.",
    "Carol would lose 62 happiness units by sitting next to Alice.",
    "Carol would gain 60 happiness units by sitting next to Bob.",
    "Carol would gain 55 happiness units by sitting next to David.",
    "David would gain 46 happiness units by sitting next to Alice.",
    "David would lose 7 happiness units by sitting next to Bob.",
    "David would gain 41 happiness units by sitting next to Carol."
]


def test_including_me():
    assert include_me({
        "Alice": {
            "David": -2
        },
        "David": {
            "Alice": 46,
        }
    }, 0) == {
               "Alice": {
                   "David": -2,
                   "me": 0
               },
               "David": {
                   "Alice": 46,
                   "me": 0,
               },
               "me": {
                   "Alice": 0,
                   "David": 0
               }
           }


def test_parse_seatings():
    assert parse_seatings(attendees) == {
        "Alice": {
            "Bob": 54,
            "Carol": -79,
            "David": -2
        },
        "Bob": {
            "Alice": 83,
            "Carol": -7,
            "David": -63
        },
        "Carol": {
            "Alice": -62,
            "Bob": 60,
            "David": 55
        },
        "David": {
            "Alice": 46,
            "Bob": -7,
            "Carol": 41
        }
    }


def test_count_happiness():
    assert count_happiness(parse_seatings(attendees), ("Alice", "Bob", "Carol", "David")) == 330


def test_count_happines_change():
    best_seatings = parse_seatings(attendees)
    assert happines_change(best_seatings)[1] == 330
