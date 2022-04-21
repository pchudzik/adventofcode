import pytest

from _07_ips import is_tls_supported, is_ssl_supported


@pytest.mark.parametrize(
    "ip, is_supported", [
        ("abba[mnop]qrst", True),
        ("abcd[bddb]xyyx", False),
        ("aaaa[qwer]tyui", False),
        ("ioxxoj[asdfgh]zxcvbn", True)
    ])
def test_is_transport_layer_snooping_supported(ip, is_supported):
    assert is_tls_supported(ip) == is_supported


@pytest.mark.parametrize(
    "ip, is_supported", [
        ("lll[lll]", False),
        ("aba[bab]xyz", True),
        ("xyx[xyx]xyx", False),
        ("aaa[kek]eke", True),
        ("zazbz[bzb]cdb", True),
        ("aba[xyz]bab[cat]dog", False),
        ("abacdc[dcd]asd", True)
    ])
def test_is_ssl_supported(ip, is_supported):
    assert is_ssl_supported(ip) == is_supported
