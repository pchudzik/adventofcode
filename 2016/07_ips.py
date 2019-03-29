import re
from itertools import chain, product

"""
--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP addresses (they're IPv7, of course; IPv6 is
much too limited). You'd like to figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An ABBA is any four-character sequence
which consists of a pair of two different characters followed by the reverse of that pair, such as xyyx or abba.
However, the IP also must not have an ABBA within any hypernet sequences, which are contained by square brackets.

For example:

* abba[mnop]qrst supports TLS (abba outside square brackets).
* abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
* aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
* ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?

Your puzzle answer was 105.

--- Part Two ---

You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences (outside any square
bracketed sections), and a corresponding Byte Allocation Block, or BAB, anywhere in the hypernet sequences. An ABA is
any three-character sequence which consists of the same character twice with a different character between them, such as
xyx or aba. A corresponding BAB is the same characters but in reversed positions: yxy and bab, respectively.

For example:

* aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
* xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
* aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because
  the interior character must be different).
* zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz
  overlap).

How many IPs in your puzzle input support SSL?

Your puzzle answer was 258.
"""


def is_tls_supported(ip):
    supernets, hypernets = _parse_ip(ip)
    return any(_has_abba(snet) for snet in supernets) \
           and all(not _has_abba(hnet) for hnet in hypernets)


def is_ssl_supported(ip):
    supernets, hypernets = _parse_ip(ip)

    abas = set(chain.from_iterable(map(_find_aba, supernets)))
    babs = set(map(lambda aba: aba[1] + aba[0] + aba[1], abas))

    return any(map(
        lambda hnet_bab: hnet_bab[1] in hnet_bab[0],
        product(hypernets, babs)))


def _find_aba(ip):
    result = []
    for i in range(len(ip) - 1):
        a = ip[i]
        b = ip[i + 1]

        if a + b + a in ip and a != b:
            result.append(f"{a}{b}{a}")
    return result


def _has_abba(ip_part):
    for i in range(len(ip_part) - 3):
        p1 = ip_part[i:i + 2]
        p2 = ip_part[i + 2:i + 4]

        if p1 == p2[::-1] and p1 != p2:
            return True


def _parse_ip(ip):
    supernets = re.split(r"\[\w+\]", ip)
    hypernets = re.findall(r"\[(\w+)\]", ip)
    return supernets, hypernets


if __name__ == "__main__":
    with open("07_ips.txt") as file:
        ips = [ip.strip() for ip in file.readlines()]

        tls_ips = sum(map(
            lambda ip: is_tls_supported(ip),
            ips))
        ssl_ips = sum(map(
            lambda ip: is_ssl_supported(ip),
            ips))

        print(f"p1 = {tls_ips}")
        print(f"p2 = {ssl_ips}")
