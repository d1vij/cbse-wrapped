from compiler.utils.parse import parse_int


def test_parse_int():
    assert parse_int("1") == 1
    assert parse_int("-1") == -1
    assert parse_int("hi") is None
    assert parse_int("hi", 0) == 0
