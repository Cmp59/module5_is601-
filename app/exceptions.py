"""Application-specific calculator exceptions."""


class CalculatorError(Exception):
    """Base exception for calculator errors."""


class InvalidOperationError(CalculatorError, ValueError):
    """Raised when an operation symbol is not supported."""


class OperationError(CalculatorError, ValueError):
    """Raised when an arithmetic operation cannot be performed."""


class ConfigurationError(CalculatorError, ValueError):
    """Raised when calculator configuration is invalid."""


class InvalidInputError(CalculatorError, ValueError):
    """Raised when a user-provided value is invalid."""


class HistoryError(CalculatorError):
    """Raised when calculation history cannot be read or written."""