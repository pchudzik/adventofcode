import hashlib

"""
--- Day 4: The Ideal Stocking Stuffer ---

Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts for all the economically
forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least five zeroes. The input to the MD5
hash is some secret key (your puzzle input, given below) followed by a number in decimal. To mine AdventCoins, you must
find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.

For example:

If your secret key is abcdef, the answer is 609043, because the MD5 hash of abcdef609043 starts with five zeroes
(000001dbbfa...), and it is the lowest such number to do so.

If your secret key is pqrstuv, the lowest number it combines with to make an MD5 hash starting with five zeroes is
1048970; that is, the MD5 hash of pqrstuv1048970 looks like 000006136ef....

Your puzzle answer was 282749.

--- Part Two ---

Now find one that starts with six zeroes.

Your puzzle answer was 9962624.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your advent calendar and try another puzzle.

Your puzzle input was yzbqklnj.
"""


def find_number_for_hash_code_with_at_least_X_leading_zeros(secret, number_of_leading_zeros):
    hash = ''
    number = 0
    while not str(hash).startswith("0" * number_of_leading_zeros):
        number += 1
        hash = calculate_md5(secret + str(number))

    return number


def calculate_md5(input):
    md5 = hashlib.md5()
    md5.update(bytes(input, "utf-8"))
    return md5.hexdigest()


if __name__ == "__main__":
    secret = "yzbqklnj"
    print("mining key for 5 zeros:",
          find_number_for_hash_code_with_at_least_X_leading_zeros(secret, 5))
    print("mining key for 6 zeros:",
          find_number_for_hash_code_with_at_least_X_leading_zeros(secret, 6))
