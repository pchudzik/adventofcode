"""
--- Day 19: Medicine for Rudolph ---

Rudolph the Red-Nosed Reindeer is sick! His nose isn't shining very brightly, and he needs medicine.

Red-Nosed Reindeer biology isn't similar to regular reindeer biology; Rudolph is going to need custom-made medicine.
Unfortunately, Red-Nosed Reindeer chemistry isn't similar to regular reindeer chemistry, either.

The North Pole is equipped with a Red-Nosed Reindeer nuclear fusion/fission plant, capable of constructing any Red-Nosed
Reindeer molecule you need. It works by starting with some input molecule and then doing a series of replacements, one
per step, until it has the right molecule.

However, the machine has to be calibrated before it can be used. Calibration involves determining the number of
molecules that can be generated in one step from a given starting point.

For example, imagine a simpler machine that supports only the following replacements:

H => HO
H => OH
O => HH
Given the replacements above and starting with HOH, the following molecules could be generated:

HOOH (via H => HO on the first H).
HOHO (via H => HO on the second H).
OHOH (via H => OH on the first H).
HOOH (via H => OH on the second H).
HHHH (via O => HH).

So, in the example above, there are 4 distinct molecules (not five, because HOOH appears twice) after one replacement
from HOH. Santa's favorite molecule, HOHOHO, can become 7 distinct molecules (over nine replacements: six from H, and
three from O).

The machine replaces without regard for the surrounding characters. For example, given the string H2O, the transition H
=> OO would result in OO2O.

Your puzzle input describes all of the possible replacements and, at the bottom, the medicine molecule for which you
need to calibrate the machine. How many distinct molecules can be created after all the different ways you can do one
replacement on the medicine molecule?

Your puzzle answer was 518.

--- Part Two ---

Now that the machine is calibrated, you're ready to begin molecule fabrication.

Molecule fabrication always begins with just a single electron, e, and applying replacements one at a time, just like
the ones during calibration.

For example, suppose you have the following replacements:

e => H
e => O
H => HO
H => OH
O => HH
If you'd like to make HOH, you start with e, and then make the following replacements:

e => O to get O
O => HH to get HH
H => OH (on the second H) to get HOH
So, you could make HOH after 3 steps. Santa's favorite molecule, HOHOHO, can be made in 6 steps.

How long will it take to make the medicine? Given the available replacements and the medicine molecule in your puzzle
input, what is the fewest number of steps to go from e to the medicine molecule?

Your puzzle answer was 200.
"""


def parse_replacement(replacements):
    result = dict()
    for replacement in replacements:
        molecule, replacement_result = replacement.split(" => ")
        if molecule not in result:
            result[molecule] = []
        result[molecule].append(replacement_result)
    return result


def generate_all_replacement_molecules(input_molecule, replacements):
    result = set()
    for molecule in replacements:
        result = result.union(generate_replacements(input_molecule, molecule, replacements[molecule]))
    return result


def find_all_occurrences(input_molecule, molecule):
    last_index = 0
    while last_index >= 0:
        last_index = input_molecule.find(molecule, last_index)
        if last_index < 0:
            break
        yield last_index
        last_index += 1


def generate_replacements(input_molecule, molecule_to_replace, replacements):
    for replacement in replacements:
        for index in find_all_occurrences(input_molecule, molecule_to_replace):
            replaced_molecule = input_molecule[:index] + replacement + input_molecule[index + len(molecule_to_replace):]
            yield replaced_molecule


def count_distinct_replacement_molecules(input_molecule, replacements):
    return len(generate_all_replacement_molecules(input_molecule, replacements))


def __count_number_of_steps_to_generate_molecule(
        reversed_replacements,
        start,
        dst_molecule="e",
        number_of_replacements=0):
    if start == dst_molecule:
        return number_of_replacements

    if start.count(dst_molecule) > 0:
        return None

    for replacement in reversed_replacements:
        for index in find_all_occurrences(start, replacement):
            replaced_molecule = start[:index] + reversed_replacements[replacement] + start[index + len(replacement):]
            if len(replaced_molecule) > len(start) or reversed_replacements[replacement] == start:
                continue
            result = __count_number_of_steps_to_generate_molecule(
                reversed_replacements=reversed_replacements,
                dst_molecule=dst_molecule,
                start=replaced_molecule,
                number_of_replacements=number_of_replacements + 1)
            if result:
                return result

    return None


def reverse_lookup(replacements):
    for key in replacements:
        for val in replacements[key]:
            yield (val, key)


def count_number_of_steps_to_generate_molecule(replacements, start, dst_molecule="e"):
    return __count_number_of_steps_to_generate_molecule(
        reversed_replacements=(dict(reverse_lookup(replacements))),
        dst_molecule=dst_molecule,
        start=start,
        number_of_replacements=0)


if __name__ == "__main__":
    input_molecule = "CRnSiRnCaPTiMgYCaPTiRnFArSiThFArCaSiThSiThPBCaCaSiRnSiRnTiTiMgArPBCaPMgYPTiRnFArFArCaSiRnBPMgArPRnCaPTiRnFArCaSiThCaCaFArPBCaCaPTiTiRnFArCaSiRnSiAlYSiThRnFArArCaSiRnBFArCaCaSiRnSiThCaCaCaFYCaPTiBCaSiThCaSiThPMgArSiRnCaPBFYCaCaFArCaCaCaCaSiThCaSiRnPRnFArPBSiThPRnFArSiRnMgArCaFYFArCaSiRnSiAlArTiTiTiTiTiTiTiRnPMgArPTiTiTiBSiRnSiAlArTiTiRnPMgArCaFYBPBPTiRnSiRnMgArSiThCaFArCaSiThFArPRnFArCaSiRnTiBSiThSiRnSiAlYCaFArPRnFArSiThCaFArCaCaSiThCaCaCaSiRnPRnCaFArFYPMgArCaPBCaPBSiRnFYPBCaFArCaSiAl"
    with open("19_molecules.txt") as file:
        replacements = parse_replacement([line.strip() for line in file.readlines()])
        print(
            "Number of distinct molecules: ",
            count_distinct_replacement_molecules(input_molecule, replacements))
        print(
            "Minimum number of steps to get from e to result: ",
            count_number_of_steps_to_generate_molecule(replacements, input_molecule))
