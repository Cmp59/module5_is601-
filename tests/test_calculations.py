import pytest

from app.calculation import Calculation, CalculationFactory
from app.history import CalculationHistory


@pytest.mark.parametrize(
    "operator, first_number, second_number, expected_result",
    [
        ("+", 2, 3, 5),
        ("-", 5, 3, 2),
        ("*", 2, 3, 6),
        ("/", 6, 3, 2),
    ],
)
def test_factory_creates_calculation_instances(
    operator, first_number, second_number, expected_result
):
    calculation = CalculationFactory.create(
        operator, first_number, second_number
    )

    assert isinstance(calculation, Calculation)
    assert calculation.perform() == expected_result


@pytest.mark.parametrize("operator", ["+", "-", "*", "/"])
def test_factory_supports_basic_operators(operator):
    assert CalculationFactory.supports(operator)


def test_factory_rejects_unsupported_operator():
    with pytest.raises(ValueError, match="Unsupported operation: %"):
        CalculationFactory.create("%", 2, 3)


def test_factory_reports_unsupported_operator():
    assert not CalculationFactory.supports("%")


def test_history_starts_empty():
    history = CalculationHistory()

    assert history.get_all() == ()
    assert history.format_entries() == "No calculations yet."


def test_history_stores_and_formats_calculations():
    history = CalculationHistory()
    first_calculation = CalculationFactory.create("+", 2, 3)
    second_calculation = CalculationFactory.create("*", 4, 5)

    history.add(first_calculation)
    history.add(second_calculation)

    assert history.get_all() == (first_calculation, second_calculation)
    assert history.format_entries() == "1. 2 + 3 = 5\n2. 4 * 5 = 20"