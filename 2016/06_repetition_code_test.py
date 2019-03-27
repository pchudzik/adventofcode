import importlib

decode_repetition_code = importlib.import_module("06_repetition_code").decode_repetition_code
decode_modified_repetition_code = importlib.import_module("06_repetition_code").decode_modified_repetition_code


def test_decode_repetition_code():
    code = (
        "eedadn",
        "drvtee",
        "eandsr",
        "raavrd",
        "atevrs",
        "tsrnev",
        "sdttsa",
        "rasrtv",
        "nssdts",
        "ntnada",
        "svetve",
        "tesnvt",
        "vntsnd",
        "vrdear",
        "dvrsen",
        "enarar")

    assert decode_repetition_code(code) == "easter"


def test_decode_modified_repetition_code():
    code = (
        "eedadn",
        "drvtee",
        "eandsr",
        "raavrd",
        "atevrs",
        "tsrnev",
        "sdttsa",
        "rasrtv",
        "nssdts",
        "ntnada",
        "svetve",
        "tesnvt",
        "vntsnd",
        "vrdear",
        "dvrsen",
        "enarar")

    assert decode_modified_repetition_code(code) == "advent"
