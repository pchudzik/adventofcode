import re
from functools import reduce

all_properties = [
    "children", "cats",
    "samoyeds", "pomeranians", "akitas", "vizslas",
    "goldfish", "trees", "cars", "perfumes"
]
greater_than_properties = ["cats", "trees"]
fewer_than_properties = ["pomeranians", "goldfish"]


def parse_row(row):
    aunt_index = re.match(r"Sue (\d+):.*", row).group(1)
    row = row.replace("Sue {}: ".format(aunt_index), "")

    return Aunt(
        int(aunt_index),
        **dict([
            (prop[0], int(prop[1]))
            for prop in re.findall(r"(\w+): (\d+)", row)]))


def find_best_match_exact(aunts, mfcsam_analysis):
    return list(filter(
        lambda aunt: aunt.match_exact(mfcsam_analysis),
        aunts))[0]


def find_best_match_range(aunts, mfcsam_analysis):
    return list(filter(
        lambda aunt: aunt.match_range(mfcsam_analysis),
        aunts))[0]


class Aunt:
    def __init__(self, index, **kwargs):
        self.index = index
        self.properties = kwargs

    def __getitem__(self, item):
        return self.properties[item] if item in self.properties else None

    def match_exact(self, mfcsam_analysis):
        return reduce(
            lambda result, prop: result and self[prop] == mfcsam_analysis[prop],
            self._existing_properties_only(mfcsam_analysis),
            True)

    def match_range(self, mfcsam_analysis):
        def matches(aunt, prop):
            if prop in greater_than_properties:
                return aunt[prop] > mfcsam_analysis[prop]
            elif prop in fewer_than_properties:
                return aunt[prop] < mfcsam_analysis[prop]
            else:
                return aunt[prop] == mfcsam_analysis[prop]

        return reduce(
            lambda result, prop: result and matches(self, prop),
            self._existing_properties_only(mfcsam_analysis),
            True)

    def _existing_properties_only(self, mfcsam_analysis):
        return [key for key in mfcsam_analysis if key in self.properties]

    @property
    def name(self):
        return "Sue {}".format(self.index)


if __name__ == "__main__":
    with open("16_sue.txt") as file:
        aunts = [parse_row(row) for row in file.readlines()]
        mfcsam_analysis = {
            "children": 3,
            "cats": 7,
            "samoyeds": 2,
            "pomeranians": 3,
            "akitas": 0,
            "vizslas": 0,
            "goldfish": 5,
            "trees": 3,
            "cars": 2,
            "perfumes": 1
        }
        match_exact = find_best_match_exact(aunts, mfcsam_analysis)
        match_range = find_best_match_range(aunts, mfcsam_analysis)

        print("Aunt who send present ", match_exact.name)
        print("Fixed methodology aunt who send present", match_range.name)
