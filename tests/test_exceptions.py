from app.exceptions import (
    CalculatorError,
    ConfigurationError,
    HistoryError,
    InvalidInputError,
    InvalidOperationError,
    OperationError,
)


def test_application_errors_share_calculator_error_base():
    errors = [
        ConfigurationError(),
        HistoryError(),
        InvalidInputError(),
        InvalidOperationError(),
        OperationError(),
    ]

    assert all(isinstance(error, CalculatorError) for error in errors)
    assert isinstance(InvalidOperationError(), ValueError)
    assert isinstance(OperationError(), ValueError)
