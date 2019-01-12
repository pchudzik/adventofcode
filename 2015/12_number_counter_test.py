import json
import pytest
import importlib

sum_of_numbers_regexp = importlib \
    .import_module("12_number_counter") \
    .sum_of_numbers_regexp

sum_of_numbers_dict = importlib \
    .import_module("12_number_counter") \
    .sum_of_numbers_dict

sum_of_numbers_dict_exclude_red = importlib \
    .import_module("12_number_counter") \
    .sum_of_numbers_dict_exclude_red

parameters = [
    ('[1,2,3]', 6),
    ('{"a":2,"b":4}', 6),
    ('[[[3]]]', 3),
    ('{"a":{"b":4},"c":-1}', 3),
    ('{"a":[-1,1]}', 0),
    ('[-1,{"a":1}]', 0),
    ('[]', 0),
    ('{}', 0)]


@pytest.mark.parametrize("json, result", parameters)
def test_sum_of_numbers_regexp(json, result):
    assert sum_of_numbers_regexp(json) == result


@pytest.mark.parametrize("input_json, result", parameters)
def test_sum_of_numbers_json(input_json, result):
    assert sum_of_numbers_dict(json.loads(input_json)) == result


@pytest.mark.parametrize("input_json, result", [
    ('[1,2,3]', 6),
    ('[1,{"c":"red","b":2},3]', 4),
    ('{"d":"red","e":[1,2,3,4],"f":5} ', 0),
    ('{"a":{"b":4},"c":-1}', 3),
    ('[1,"red",5]', 6)
])
def test_sum_of_numbers_dict_exclude_red(input_json, result):
    assert sum_of_numbers_dict_exclude_red(json.loads(input_json)) == result
