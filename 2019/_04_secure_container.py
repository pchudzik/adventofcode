def numbers_never_decrease(pswd: str) -> bool:
    for i in range(len(pswd) - 1):
        a = int(pswd[i])
        b = int(pswd[i + 1])
        if b < a:
            return False
    return True


def has_double_digit(pswd: str) -> bool:
    for i in range(len(pswd) - 1):
        a = pswd[i]
        b = pswd[i + 1]
        if a == b:
            return True
    return False


def has_no_double_digit_in_part_of_bigger_group(pswd: str) -> bool:
    for i in range(0, 10):
        i_str = str(i)
        if i_str * 2 in pswd:
            index = pswd.index(i_str * 2)
            previous_different = True if index == 0 else pswd[index - 1] != i_str
            next_different = True if index + 2 >= len(pswd) else pswd[index + 2] != i_str
            if next_different and previous_different:
                return True
    return False


def is_valid_password(pswd: str, conditions) -> bool:
    return all(condition(pswd) for condition in conditions)


def run_puzzle(range_start: int, range_end: int, conditions) -> int:
    count = 0
    for i in range(range_start, range_end):
        is_valid = is_valid_password(str(i), conditions)
        if is_valid:
            count += 1
    return count


def part1(range_start: int, range_end: int) -> int:
    return run_puzzle(range_start, range_end, (has_double_digit, numbers_never_decrease))


def part2(range_start: int, range_end: int) -> int:
    return run_puzzle(range_start, range_end, (numbers_never_decrease, has_no_double_digit_in_part_of_bigger_group,))


if __name__ == "__main__":
    print("part 1:", part1(284639, 748759))
    print("part 2:", part2(284639, 748759))
