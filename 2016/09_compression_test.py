import importlib
import pytest

compression = importlib.import_module("09_compression")

decompress = compression.decompress
decompress_len = compression.decompress_len


@pytest.mark.parametrize(
    "string, decompressed", [
        ("ADVENT", "ADVENT"),
        ("A(1x5)BC", "ABBBBBC"),
        ("(3x3)XYZ", "XYZXYZXYZ"),
        ("(6x1)(1x3)A", "(1x3)A"),
        ("X(8x2)(3x3)ABCY", "X(3x3)ABC(3x3)ABCY")
    ])
def test_decompress(string, decompressed):
    assert decompress(string) == decompressed


@pytest.mark.parametrize(
    "string, length", [
        ("ADVENT", 6),
        ("(3x3)XYZ", 9),
        ("A(2x2)BCD(2x2)EFG", 11),
        ("(6x1)(1x3)A", 6),
        ("X(8x2)(3x3)ABCY", 18)
    ])
def test_decompress_len(string, length):
    assert decompress_len(string) == length


@pytest.mark.parametrize(
    "string, decompressed", [
        ("(3x3)XYZ", lambda:"XYZXYZXYZ"),
        ("X(8x2)(3x3)ABCY", lambda:"XABCABCABCABCABCABCY"),
        ("(27x12)(20x12)(13x14)(7x10)(1x12)A", lambda:"A" * 241920)
    ])
def test_decompress2(string, decompressed):
    assert decompress(string, is_v2=True) == decompressed()


@pytest.mark.parametrize(
    "string, length", [
        ("X(8x2)(3x3)ABCY", 20),
        ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
        ("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", 445)
    ])
def test_decompress2_len(string, length):
    assert decompress_len(string, is_v2=True) == length
