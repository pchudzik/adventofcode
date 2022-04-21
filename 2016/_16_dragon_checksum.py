def data_filler(input_data):
    return input_data + \
           "0" + \
           "".join(
               "0" if x == "1"
               else "1"
               for x in reversed(input_data))


def checksum(input_data):
    def generate_checksum(data):
        return "".join(
            "1" if a_b[0] == a_b[1]
            else "0"
            for a_b in zip(data[::2], data[1::2]))

    chks = generate_checksum(input_data)
    while len(chks) % 2 == 0:
        chks = generate_checksum(chks)

    return chks


def find_checksum(input_data, expected_length):
    data_to_fill = data_filler(input_data)
    while len(data_to_fill) < expected_length:
        data_to_fill = data_filler(data_to_fill)

    data_to_fill = data_to_fill[0:expected_length]

    return checksum(data_to_fill)


if __name__ == "__main__":
    puzzle = "00111101111101000"
    part1_length = 272
    part2_length = 35_651_584
    print(f"part1 {find_checksum(puzzle, part1_length)}")
    print(f"part2 {find_checksum(puzzle, part2_length)}")
