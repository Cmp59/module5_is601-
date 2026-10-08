"""Manage calculations performed during one calculator session."""

from typing import Tuple

from .calculation import Calculation


class CalculationHistory:
    """Store, retrieve, and format completed calculations."""

    def __init__(self):
        self._calculations = []

    def add(self, calculation: Calculation) -> None:
        """Add a completed calculation to history."""
        self._calculations.append(calculation)

    def get_all(self) -> Tuple[Calculation, ...]:
        """Return a read-only snapshot of the stored calculations."""
        return tuple(self._calculations)

    def format_entries(self) -> str:
        """Format history entries for display in the REPL."""
        if not self._calculations:
            return "No calculations yet."

        return "\n".join(
            f"{index}. {calculation}"
            for index, calculation in enumerate(self._calculations, start=1)
        )