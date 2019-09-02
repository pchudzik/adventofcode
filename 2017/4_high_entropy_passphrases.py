from collections import defaultdict


def is_valid(password: str):
    counts = defaultdict(int)
    for word in password.split():
        counts[word] += 1

    return len([count for count in counts.values() if count > 1]) == 0


def find_valid_passphases(passwords):
    return list(filter(is_valid, passwords))


if __name__ == "__main__":
    with open("4_high_entropy_passphrases.txt") as file:
        passwords = [line.strip() for line in file.readlines()]
        print(f"part1: {len(find_valid_passphases(passwords))}")
