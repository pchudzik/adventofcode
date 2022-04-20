import itertools
import re

"""
--- Day 13: Knights of the Dinner Table ---

In years past, the holiday feast with your family hasn't gone so well. Not everyone gets along! This year, you resolve,
will be different. You're going to find the optimal seating arrangement and avoid all those awkward conversations.

You start by writing up a list of everyone invited and the amount their happiness would increase or decrease if they
were to find themselves sitting next to each other person. You have a circular table that will be just big enough to fit
everyone comfortably, and so each person will have exactly two neighbors.

For example, suppose you have only four attendees planned, and you calculate their potential happiness as follows:

Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.

Then, if you seat Alice next to David, Alice would lose 2 happiness units (because David talks so much), but David would
gain 46 happiness units (because Alice is such a good listener), for a total change of 44.

If you continue around the table, you could then seat Bob next to Alice (Bob gains 83, Alice gains 54). Finally, seat
Carol, who sits next to Bob (Carol gains 60, Bob loses 7) and David (Carol gains 55, David gains 41). The arrangement
looks like this:

     +41 +46
+55   David    -2
Carol       Alice
+60    Bob    +54
     -7  +83
     
After trying every other seating arrangement in this hypothetical scenario, you find that this one is the most optimal,
with a total change in happiness of 330.

What is the total change in happiness for the optimal seating arrangement of the actual guest list?

Your puzzle answer was 618.

--- Part Two ---

In all the commotion, you realize that you forgot to seat yourself. At this point, you're pretty apathetic toward the
whole thing, and your happiness wouldn't really go up or down regardless of who you sit next to. You assume everyone
else would be just as ambivalent about sitting next to you, too.

So, add yourself to the list, and give all happiness relationships that involve you a score of 0.

What is the total change in happiness for the optimal seating arrangement that actually includes yourself?

Your puzzle answer was 601.
"""


def parse_seatings(attendees):
    def find_happines_modifier(attendee):
        happiness = int(re.match(r".*?(\d+).*", attendee).group(1))
        return happiness if "gain" in attendee else -happiness

    parsed_attendees = [(
        attendee.split(" ")[0],
        attendee.replace(".", "").split(" ")[-1].strip(),
        find_happines_modifier(attendee),
    ) for attendee in attendees]

    result = dict()
    for attendee in parsed_attendees:
        who = attendee[0]
        neighbour = attendee[1]
        happiness = attendee[2]

        if who not in result:
            result[who] = dict()

        result[who][neighbour] = happiness

    return result


def include_me(attendees, happines):
    attendees = attendees.copy()
    for name in attendees.keys():
        attendees[name]["me"] = happines
    attendees["me"] = dict((name, 0) for name in attendees.keys())
    return attendees


def count_happiness(attendees, order):
    total = 0
    for index in range(-1, len(order) - 1):
        who = order[index]
        neighbour = order[index + 1]
        total += attendees[who][neighbour] + attendees[neighbour][who]

    return total


def find_seatings_with_happiness(attendees):
    return map(
        lambda order: (order, count_happiness(attendees, order)),
        itertools.permutations(attendees.keys()))


def happines_change(attendees):
    return max(
        find_seatings_with_happiness(attendees),
        key=lambda order_with_happiness: order_with_happiness[1])


if __name__ == "__main__":
    with open("_13_seatings.txt") as file:
        attendees_list = parse_seatings(file.readlines())
        includeing_me = include_me(attendees_list, 0)
        print("Best order will be: ", happines_change(attendees_list))
        print("Best order with me included will be: ", happines_change(includeing_me))
