import pytest

from app.operations import Operations


@pytest.mark.parametrize(
    "operation, first_number, second_number, expected_result",
    [
        (Operations.addition, 2, 3, 5),
        (Operations.addition, -2, 3, 1),
        (Operations.addition, 0, 4, 4),
        (Operations.addition, 2.5, 1.5, 4.0),
        (Operations.subtraction, 5, 3, 2),
        (Operations.subtraction, -2, 3, -5),
        (Operations.subtraction, 0, 4, -4),
        (Operations.subtraction, 5.5, 2.5, 3.0),
        (Operations.multiplication, 2, 3, 6),
        (Operations.multiplication, -2, 3, -6),
        (Operations.multiplication, 0, 4, 0),
        (Operations.multiplication, 2.5, 2, 5.0),
        (Operations.division, 6, 3, 2),
        (Operations.division, -6, 3, -2),
        (Operations.division, 0, 4, 0),
        (Operations.division, 7.5, 2.5, 3.0),
    ],
)
def test_operations_with_numeric_values(
    operation, first_number, second_number, expected_result
):
    assert operation(first_number, second_number) == expected_result


def test_division_by_zero():
    with pytest.raises(ValueError, match="divide by zero"):
        Operations.division(6, 0)
