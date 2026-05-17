from typing import Any


def parse_int[N = None](value: Any, null_value: N = None) -> int | N:  # ty:ignore[invalid-parameter-default]
    """
    parses an integer and returns null_value in case of ValueError or TypeError. This function never raises an exception.
    """
    try:
        return int(value)
    except ValueError, TypeError:
        return null_value
