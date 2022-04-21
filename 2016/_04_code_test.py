import pytest

from _04_code import room_parser, count_sectors_of_real_rooms


@pytest.mark.parametrize(
    "input, name, sector, checksum", [
        ("aaaaa-bbb-z-y-x-123[abxyz]", "aaaaa-bbb-z-y-x", 123, "abxyz"),
        ("a-b-c-d-e-f-g-h-987[abcde]", "a-b-c-d-e-f-g-h", 987, "abcde"),
        ("not-a-real-room-404[oarel]", "not-a-real-room", 404, "oarel")])
def test_parse_room(input, name, sector, checksum):
    room = room_parser(input)

    assert room.name == name
    assert room.sector == sector
    assert room.checksum == checksum


@pytest.mark.parametrize(
    "room_str, is_real", [
        ("aaaaa-bbb-z-y-x-123[abxyz]", True),
        ("a-b-c-d-e-f-g-h-987[abcde]", True),
        ("not-a-real-room-404[oarel]", True),
        ("totally-real-room-200[decoy]", False)
    ])
def test_is_real_room(room_str, is_real):
    room = room_parser(room_str)

    assert room.is_real == is_real


def test_sum_real_room_sectors():
    rooms = [
        "aaaaa-bbb-z-y-x-123[abxyz]",
        "a-b-c-d-e-f-g-h-987[abcde]",
        "not-a-real-room-404[oarel]",
        "totally-real-room-200[decoy]"
    ]

    assert count_sectors_of_real_rooms(rooms) == 1514


def test_decrypt_name():
    encrypted = "qzmt-zixmtkozy-ivhz-343[zimth]"

    assert room_parser(encrypted).decrypted_name == "very encrypted name"
