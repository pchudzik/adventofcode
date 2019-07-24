"""
--- Day 20: Firewall Rules ---

You'd like to set up a small hidden computer here so you can use it to get back into the network later. However, the
corporate firewall only allows communication with certain external IP addresses.

You've retrieved the list of blocked IPs from the firewall, but the list seems to be messy and poorly maintained, and
it's not clear which IPs are allowed. Also, rather than being written in dot-decimal notation, they are written as plain
32-bit integers, which can have any value from 0 through 4294967295, inclusive.

For example, suppose only the values 0 through 9 were valid, and that you retrieved the following blacklist:

5-8
0-2
4-7

The blacklist specifies ranges of IPs (inclusive of both the start and end value) that are not allowed. Then, the only
IPs that this firewall allows are 3 and 9, since those are the only numbers not in any range.

Given the list of blocked IPs you retrieved from the firewall (your puzzle input), what is the lowest-valued IP that is
not blocked?

Your puzzle answer was 23923783.

--- Part Two ---

How many IPs are allowed by the blacklist?

Your puzzle answer was 125.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def overlaps(self, other):
        if self == other:
            return False

        starts = (self.start, other.start)
        ends = (self.end, other.end)
        return min(starts) <= max(starts) <= min(ends) <= max(ends) or min(ends) == max(starts) - 1

    def merge(self, other):
        all_values = (self.start, other.start, self.end, other.end)
        return Range(min(all_values), max(all_values))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.start == other.start and self.end == other.end

        return False

    def __hash__(self):
        return hash((self.start, self.end))

    @staticmethod
    def parse(str_):
        start, end = str_.split("-")
        start, end = int(start), int(end)
        if end < start:
            raise ValueError(f"{end} can not be greater than {start}")
        return Range(start, end)


def merge_ranges(ranges):
    def any_overlaps(ranges_):
        return any(
            r1.overlaps(r2)
            for r1 in ranges_ for r2 in ranges_)

    result = set(ranges)
    while any_overlaps(result):
        tmp_result = set()
        for r1 in result:
            for r2 in result:
                if r1.overlaps(r2):
                    tmp_result.add(r1.merge(r2))
                    break
            else:
                tmp_result.add(r1)

        result = tmp_result

    return result


def find_first_free_ip(ranges):
    return min(ranges, key=lambda r: r.end).end + 1


def find_number_of_free_ips(ranges, total_available):
    ranges = list(sorted(ranges, key=lambda r: r.end))
    sum = 0
    for idx in range(len(ranges) - 1):
        r1 = ranges[idx]
        r2 = ranges[idx + 1]

        sum += r2.start - r1.end - 1

    sum += total_available - ranges[-1].end
    return sum


if __name__ == "__main__":
    with open("20_firewall_rules.txt") as file:
        ranges = merge_ranges([
            Range.parse(l.strip())
            for l in file.readlines()
        ])

        print(f"part 1: {find_first_free_ip(ranges)}")
        print(f"part 2: {find_number_of_free_ips(ranges, 4_294_967_295)}")
