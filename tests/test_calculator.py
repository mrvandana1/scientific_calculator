# tests/test_calculator.py
import pytest
from app.calculator import sqrt, factorial, ln, power

def test_sqrt():
    assert pytest.approx(sqrt(4)) == 2
    with pytest.raises(ValueError):
        sqrt(-1)

def test_factorial():
    assert factorial(5) == 120
    with pytest.raises(ValueError):
        factorial(-3)

def test_ln():
    assert pytest.approx(ln(1.0)) == 0.0
    with pytest.raises(ValueError):
        ln(0)

def test_power():
    assert pytest.approx(power(2, 3)) == 8
    assert pytest.approx(power(9, 0.5)) == 3
