from collections import defaultdict

"""
--- Day 4: High-Entropy Passphrases ---

A new system policy has been put in place that requires all accounts to use a passphrase instead of simply a password. A
passphrase consists of a series of words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:

aa bb cc dd ee is valid.
aa bb cc dd aa is not valid - the word aa appears more than once.
aa bb cc dd aaa is valid - aa and aaa count as different words.

The system's full passphrase list is available as your puzzle input. How many passphrases are valid?

Your puzzle answer was 451.

--- Part Two ---

For added security, yet another system policy has been put in place. Now, a valid passphrase must contain no two words
that are anagrams of each other - that is, a passphrase is invalid if any word's letters can be rearranged to form any
other word in the passphrase.

For example:

abcde fghij is a valid passphrase.
abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
iiii oiii ooii oooi oooo is valid.
oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.
Under this new system policy, how many passphrases are valid?

Your puzzle answer was 223.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


def has_no_duplicated_words(password):
    counts = defaultdict(int)
    for word in password.split():
        counts[word] += 1

    return len([count for count in counts.values() if count > 1]) == 0


def is_anagram(word1, word2):
    if len(word1) != len(word2):
        return False

    letters_to_find = [letter for letter in word2]

    for letter in word1:
        if letter in letters_to_find:
            letters_to_find.remove(letter)
        else:
            return False

    return len(letters_to_find) == 0


def has_no_anagrams(password):
    for word in password.split():
        tmp_pass = password.replace(word, "", 1)
        for tmp_word in tmp_pass.split():
            if is_anagram(word, tmp_word):
                return False
    return True


def find_valid_passphases(validator, passwords):
    return list(filter(validator, passwords))


if __name__ == "__main__":
    with open("_04_high_entropy_passphrases.txt") as file:
        passwords = [line.strip() for line in file.readlines()]
        print(f"part1: {len(find_valid_passphases(has_no_duplicated_words, passwords))}")
        print(f"part2: {len(find_valid_passphases(has_no_anagrams, passwords))}")
