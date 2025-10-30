import pytest

from tibco_migration.calc import add, divide


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -1) == -2


def test_divide_normal():
    assert divide(10, 2) == 5


def test_divide_float():
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(1, 0)
