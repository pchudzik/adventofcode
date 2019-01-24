import importlib
import pytest

molecules_module = importlib.import_module("19_molecules")
parse_replacement = molecules_module.parse_replacement
generate_all_replacement_molecules = molecules_module.generate_all_replacement_molecules
count_distinct_replacement_molecules = molecules_module.count_distinct_replacement_molecules
count_number_of_steps_to_generate_molecule = molecules_module.count_number_of_steps_to_generate_molecule


def test_parse_replacement():
    replacements = (
        "H => HO",
        "H => OH",
        "O => HH"
    )

    parsed = parse_replacement(replacements)

    assert parsed == {
        "H": ["HO", "OH"],
        "O": ["HH", ]
    }


def test_generate_all_replacement_molecules():
    replacements = {
        "H": ("HO", "OH"),
        "O": ("HH",)
    }

    assert generate_all_replacement_molecules("HOH", replacements) == {
        "HOOH",
        "HOHO",
        "OHOH",
        "HHHH"
    }


def test_count_distinct_replacement_molecules():
    replacements = {
        "H": ("HO", "OH"),
        "O": ("HH",)
    }

    assert count_distinct_replacement_molecules("HOH", replacements) == 4


@pytest.mark.parametrize(
    "dst_molecule, number_of_steps", [
        ("HOH", 3),
        ("HOHOHO", 6)])
def test_from_e_to_molecule(dst_molecule, number_of_steps):
    replacements = {
        "e": ("H", "O"),
        "H": ("HO", "OH"),
        "O": ("HH",)
    }

    assert count_number_of_steps_to_generate_molecule(replacements, dst_molecule) == number_of_steps
