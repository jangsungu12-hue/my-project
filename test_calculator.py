import pytest

from calculator import add, subtract, multiply, divide, calculate


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0


def test_divide():
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_calculate():
    assert calculate(2, "+", 3) == 5
    assert calculate(10, "-", 4) == 6
    assert calculate(3, "*", 5) == 15
    assert calculate(20, "/", 4) == 5


def test_calculate_invalid_operator():
    with pytest.raises(ValueError):
        calculate(1, "%", 2)
