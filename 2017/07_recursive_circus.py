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


def balance_tower(stack):
    leafs = collections.deque([leaf for leaf in stack.values() if len(leaf.children) == 0])
    checked = set()

    while len(leafs) > 0:
        parent = leafs.popleft()
        if parent.name in checked:
            continue
        is_balanced, not_balanced_node, node_weight = _is_tree_balanced(stack, parent)
        if not is_balanced:
            return not_balanced_node.name, node_weight
        else:
            if parent.parent is not None:
                leafs.append(parent.parent)


def _is_tree_balanced(stack, root):
    all_weights = dict((child, find_weight_of_children(stack, child.name)) for child in root.children)
    weights_occurrences = collections.defaultdict(int)
    for weight in all_weights.values():
        weights_occurrences[weight] += 1

    if len(weights_occurrences) <= 1:
        return True, None, None

    not_matching_weight = [weight for weight, count in weights_occurrences.items() if count == 1][0]
    expected_weight = [weight for weight, count in weights_occurrences.items() if count > 1][0]

    for node, weight in all_weights.items():
        if weight == not_matching_weight:
            weight_difference = expected_weight - not_matching_weight
            return False, node, node.weight + weight_difference


if __name__ == "__main__":
    with open("07_recursive_circus.txt") as file:
        file_content = [line.strip() for line in file.readlines()]

        stack = stack_parser(file_content)
        print(f"part1: {find_root_program(stack).name}")
        print(f"part2: {balance_tower(stack)}")
