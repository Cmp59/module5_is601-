"""Basic arithmetic operations."""

from abc import ABC, abstractmethod

from .exceptions import InvalidOperationError, OperationError


class Operations:
    """Provide the calculator's arithmetic operations."""

    @staticmethod
    def addition(first_number, second_number):
        return first_number + second_number

    @staticmethod
    def subtraction(first_number, second_number):
        return first_number - second_number

    @staticmethod
    def multiplication(first_number, second_number):
        return first_number * second_number

    @staticmethod
    def division(first_number, second_number):
        if second_number == 0:
            raise OperationError("You cannot divide by zero.")
        return first_number / second_number

    @staticmethod
    def power(base, exponent):
        """Raise a base to an exponent."""
        return base**exponent

    @staticmethod
    def root(radicand, degree):
        """Return the real nth root of a radicand."""
        if degree == 0:
            raise OperationError("Root degree cannot be zero.")
        if radicand < 0:
            if not float(degree).is_integer() or int(degree) % 2 == 0:
                raise OperationError(
                    "A negative number requires an odd integer root degree."
                )
            return -((-radicand) ** (1 / degree))
        return radicand ** (1 / degree)


class OperationStrategy(ABC):
    """Interface for interchangeable arithmetic strategies."""

    @abstractmethod
    def execute(self, first_number, second_number):
        """Execute this strategy using two operands."""


class AdditionStrategy(OperationStrategy):
    """Strategy for addition."""

    def execute(self, first_number, second_number):
        return Operations.addition(first_number, second_number)


class SubtractionStrategy(OperationStrategy):
    """Strategy for subtraction."""

    def execute(self, first_number, second_number):
        return Operations.subtraction(first_number, second_number)


class MultiplicationStrategy(OperationStrategy):
    """Strategy for multiplication."""

    def execute(self, first_number, second_number):
        return Operations.multiplication(first_number, second_number)


class DivisionStrategy(OperationStrategy):
    """Strategy for division."""

    def execute(self, first_number, second_number):
        return Operations.division(first_number, second_number)


class PowerStrategy(OperationStrategy):
    """Strategy for exponentiation."""

    def execute(self, first_number, second_number):
        return Operations.power(first_number, second_number)


class RootStrategy(OperationStrategy):
    """Strategy for nth roots."""

    def execute(self, first_number, second_number):
        return Operations.root(first_number, second_number)


class OperationFactory:
    """Create an operation strategy for an operator symbol."""

    _STRATEGIES = {
        "+": AdditionStrategy,
        "-": SubtractionStrategy,
        "*": MultiplicationStrategy,
        "/": DivisionStrategy,
        "^": PowerStrategy,
        "root": RootStrategy,
    }

    @classmethod
    def supports(cls, operator):
        """Return whether the factory recognizes an operator."""
        return operator in cls._STRATEGIES

    @classmethod
    def create(cls, operator):
        """Create a strategy for an operator or raise a clear error."""
        try:
            strategy_type = cls._STRATEGIES[operator]
        except KeyError as error:
            raise InvalidOperationError(
                f"Unsupported operation: {operator}"
            ) from error
        return strategy_type()