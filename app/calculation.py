"""Calculation objects and the factory that creates them."""

from typing import Callable

from .operations import Operations


class Calculation:
    """Store the operands and operation for one calculation."""

    def __init__(
        self,
        first_number: float,
        second_number: float,
        operator_symbol: str,
        operation: Callable[[float, float], float],
    ):
        self.first_number = first_number
        self.second_number = second_number
        self.operator_symbol = operator_symbol
        self.operation = operation

    def perform(self) -> float:
        """Run the stored operation and return its result."""
        return self.operation(self.first_number, self.second_number)

    def __str__(self) -> str:
        """Format the calculation and its result for display."""
        result = self.perform()
        return (
            f"{self.first_number} {self.operator_symbol} "
            f"{self.second_number} = {result}"
        )


class CalculationFactory:
    """Select and create calculations based on an operator symbol."""

    _OPERATIONS = {
        "+": Operations.addition,
        "-": Operations.subtraction,
        "*": Operations.multiplication,
        "/": Operations.division,
    }

    @classmethod
    def supports(cls, operator: str) -> bool:
        """Return whether the operator is supported."""
        return operator in cls._OPERATIONS

    @classmethod
    def create(
        cls, operator: str, first_number: float, second_number: float
    ) -> Calculation:
        """Create a calculation instance, raising for unknown operators."""
        try:
            operation = cls._OPERATIONS[operator]
        except KeyError as error:
            raise ValueError(f"Unsupported operation: {operator}") from error

        return Calculation(first_number, second_number, operator, operation)