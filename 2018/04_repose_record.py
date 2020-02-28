"""
--- Day 4: Repose Record ---

You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab. You need
to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as
you can safely get.

As you search the closet for anything that might help, you discover that you're not the first person to want to sneak
in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing
this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided
that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post
(your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up

Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one
whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the
minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....

The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day;
and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's
header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and
asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For
example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into
working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best
guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only
slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other
minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need
to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be
10 * 24 = 240.)

Your puzzle answer was 125444.

--- Part Two ---

Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In
all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be
99 * 45 = 4455.)

Your puzzle answer was 18325.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from datetime import datetime, timedelta
from collections import defaultdict
import re


class Guard:
    def __init__(self, id):
        self.id = id
        self.minutes_asleep = defaultdict(int)
        self.last_fall_asleep = None

    def fall_asleep(self, dt):
        self.last_fall_asleep = dt

    def wake_up(self, dt):
        while self.last_fall_asleep < dt:
            self.minutes_asleep[self.last_fall_asleep.minute] += 1
            self.last_fall_asleep += timedelta(minutes=1)
        self.last_fall_asleep = None

    @property
    def total_asleep(self):
        return sum(self.minutes_asleep.values())

    @property
    def most_sleepy_minute(self):
        if len(self.minutes_asleep) == 0:
            return 0, 0
        return max(self.minutes_asleep.items(), key=lambda i: i[1])


def parse(puzzle):
    def _sort_shifts(puzzle):
        line_pattern = re.compile(r"\[([\d\-\s:]+)] (.*)")
        sorted_shifts = []
        for line in puzzle:
            date, command = line_pattern.match(line).groups()
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            sorted_shifts.append((date, command))

        return sorted(sorted_shifts, key=lambda t: t[0])

    shifts = _sort_shifts(puzzle)
    guards = dict()

    current_guard = None
    guard_start_shift_pattern = re.compile(r"Guard #(\d+) begins shift")
    for date, cmd in shifts:
        starting = guard_start_shift_pattern.match(cmd)
        if starting:
            id = int(starting.group(1))
            if id not in guards:
                guards[id] = Guard(id)
            current_guard = guards[id]
        elif cmd == "wakes up":
            current_guard.wake_up(date)
        elif cmd == "falls asleep":
            current_guard.fall_asleep(date)

    return guards


def find_most_lazy_guard(guards):
    return max(guards, key=lambda g: g.total_asleep)


def find_most_lazy_guard_by_minute(guards):
    return max(guards, key=lambda g: g.most_sleepy_minute[1])


if __name__ == "__main__":
    with open("04_repose_record.txt") as file:
        guards = parse(line.strip() for line in file.readlines())
        strategy1 = find_most_lazy_guard(guards.values())
        strategy2 = find_most_lazy_guard_by_minute(guards.values())

        print(f"part 1: {strategy1.id * strategy1.most_sleepy_minute[0]}")
        print(f"part 2: {strategy2.id * strategy2.most_sleepy_minute[0]}")
