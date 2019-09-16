def _find_max_used_block(input_state):
    memory_bank, used_blocks = 0, -1
    for bank in range(len(input_state)):
        if input_state[bank] > used_blocks:
            memory_bank = bank
            used_blocks = input_state[bank]

    return memory_bank, used_blocks


def run_redistribution(state):
    state = list(state)
    memory_bank, used_blocks = _find_max_used_block(state)
    state[memory_bank] = 0

    redistributed_memory = int(used_blocks / len(state))
    for bank in range(len(state)):
        state[bank] += redistributed_memory

    left_to_redistribute = used_blocks % len(state)
    bank_index = memory_bank + 1
    while left_to_redistribute > 0:
        if bank_index >= len(state):
            bank_index = 0
        state[bank_index] += 1
        bank_index += 1
        left_to_redistribute -= 1

    return tuple(state)


def find_cycle(input_state):
    seen = set()
    current_state = input_state
    while current_state not in seen:
        seen.add(current_state)
        current_state = run_redistribution(current_state)
    return seen


if __name__ == "__main__":
    input_state = (10, 3, 15, 10, 5, 15, 5, 15, 9, 2, 5, 8, 5, 2, 3, 6)
    print(f"part1: {len(find_cycle(input_state))}")
