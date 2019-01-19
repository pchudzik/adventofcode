import importlib

parse_row = importlib \
    .import_module("16_sue") \
    .parse_row
Aunt = importlib \
    .import_module("16_sue") \
    .Aunt
find_best_match_exact = importlib \
    .import_module("16_sue") \
    .find_best_match_exact
find_best_match_range = importlib \
    .import_module("16_sue") \
    .find_best_match_range


def test_parse_row():
    row = "Sue 64: perfumes: 8, pomeranians: 1, children: 8"

    aunt = parse_row(row)

    assert aunt.name == "Sue 64"


def test_parse_properties_with_missing():
    row = "Sue 64: perfumes: 8, pomeranians: 1, children: 8"

    aunt = parse_row(row)

    assert aunt["perfumes"] == 8
    assert aunt["pomeranians"] == 1
    assert aunt["children"] == 8


def test_parse_properties_full():
    row = "".join((
        "Sue 11: ",
        "children: 3, ",
        "cats: 7, ",
        "samoyeds: 2, ",
        "pomeranians: 3, ",
        "akitas: 0, ",
        "vizslas: 0, "
        "goldfish: 5, "
        "trees: 3, ",
        "cars: 2, ",
        "perfumes: 1"))

    aunt = parse_row(row)

    assert aunt.name == "Sue 11"
    assert aunt["children"] == 3
    assert aunt["cats"] == 7
    assert aunt["samoyeds"] == 2
    assert aunt["pomeranians"] == 3
    assert aunt["akitas"] == 0
    assert aunt["vizslas"] == 0
    assert aunt["goldfish"] == 5
    assert aunt["trees"] == 3
    assert aunt["cars"] == 2
    assert aunt["perfumes"] == 1


def test_aunt_missing_property():
    aunt = Aunt(12)

    assert aunt["missing"] is None


def test_find_best_match_exact():
    aunt1 = parse_row("Sue 1: children: 1, cars: 8, vizslas: 7")
    aunt2 = parse_row("Sue 2: akitas: 10, perfumes: 10, children: 5")

    assert find_best_match_exact([aunt1, aunt2], {"children": 5, "perfumes": 10}) == aunt2


def test_find_best_match_ranges():
    aunt1 = parse_row("Sue 1: trees: 1, cats: 1, goldfish: 7, pomeranians: 10, cars: 3, perfumes: 7")
    aunt2 = parse_row("Sue 2: trees: 9, cats: 12, goldfish: 1, pomeranians: 1, cars: 4, perfumes: 7")

    matching_aunt = find_best_match_range(
        [aunt1, aunt2],
        {
            "cats": 9, "trees": 5,
            "goldfish": 2, "pomeranians": 2,
            "cars": 4, "perfumes": 7
        })

    assert matching_aunt == aunt2


def test_real_ranges():
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
    aunt1 = parse_row("Sue 213: children: 3, goldfish: 5, vizslas: 0")
    aunt2 = parse_row("Sue 323: perfumes: 1, trees: 6, goldfish: 0")

    matching_aunt = find_best_match_range([aunt1, aunt2], mfcsam_analysis)

    assert matching_aunt == aunt2
