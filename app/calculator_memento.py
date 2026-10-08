"""Memento object for restoring calculator history state."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CalculatorMemento:
    """Immutable snapshot of calculation-history rows."""

    rows: Tuple[Tuple[object, ...], ...]

    @classmethod
    def from_rows(cls, rows):
        """Capture iterable row values in an immutable snapshot."""
        return cls(tuple(tuple(row) for row in rows))