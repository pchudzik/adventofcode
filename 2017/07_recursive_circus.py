import re
import collections


class Program:
    def __init__(self, name):
        self.name = name
        self.weight = None
        self.parent = None
        self.children = []


def stack_parser(puzzle):
    stack = dict()

    for info in puzzle:
        program_name = info.split()[0]
        if program_name not in stack:
            stack[program_name] = Program(program_name)

        program = stack[program_name]
        program.weight = int(re.match(r".*\((\d+)\).*", info).group(1))
        children = re.match(r".*\s->\s(.*)", info)
        if children:
            for child in children.group(1).split():
                child_name = child.replace(",", "").strip()
                if child_name not in stack:
                    stack[child_name] = Program(child_name)
                child_program = stack[child_name]
                child_program.parent = program
                program.children.append(child_program)

    return stack


def find_root_program(stack: dict):
    program = next(iter(stack.items()))[1]
    while program.parent:
        program = program.parent
    return program


def find_weight_of_children(stack, root_program_name):
    program = stack[root_program_name]
    weight = program.weight
    for child in program.children:
        weight += find_weight_of_children(stack, child.name)

    return weight


def _find_not_balanced_stack(all_weights):
    counts = collections.defaultdict(int)
    for name, weight in all_weights:
        counts[weight] += 1

    weights = list(sorted(
        counts.items(),
        key=lambda weight_count: weight_count[1]))

    not_balanced_weight, expected_weight = weights[0][0], weights[1][0]

    for name, weight in all_weights:
        if weight == not_balanced_weight:
            if expected_weight > not_balanced_weight:
                return name, not_balanced_weight - expected_weight
            else:
                return name, expected_weight - not_balanced_weight


def balance_tower(stack):
    root_program = find_root_program(stack)
    all_weights = [(child.name, find_weight_of_children(stack, child.name)) for child in root_program.children]
    not_balanced_stack, expected_weight_difference = _find_not_balanced_stack(all_weights)
    not_balanced_program = stack[not_balanced_stack]
    #That's not the right answer; your answer is too high. If you're stuck, there are some general tips on the about page, or you can ask for hints on the subreddit. Please wait one minute before trying again. (You guessed 39159.
    return not_balanced_stack, not_balanced_program.weight + expected_weight_difference


if __name__ == "__main__":
    with open("07_recursive_circus.txt") as file:
        file_content = [line.strip() for line in file.readlines()]

        stack = stack_parser(file_content)
        print(f"part1: {find_root_program(stack).name}")
        print(f"part2: {balance_tower(stack)}")
