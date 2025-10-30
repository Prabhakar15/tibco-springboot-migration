"""Small example module with basic arithmetic functions."""

from typing import Union

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Return the sum of a and b."""
    return a + b


def divide(a: Number, b: Number) -> float:
    """Return a / b. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("division by zero")
    return a / b
