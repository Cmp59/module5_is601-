import pandas as pd
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import InvalidOperationError


def make_calculator(tmp_path, auto_save=True):
    return Calculator(
        CalculatorConfig(tmp_path / "history.csv", auto_save=auto_save)
    )


def test_calculator_facade_calculates_and_notifies_history(tmp_path):
    calculator = make_calculator(tmp_path)

    result = calculator.calculate("+", 2, 3)

    assert result == 5
    assert "2 + 3 = 5" in calculator.history_text()
    assert (tmp_path / "history.csv").exists()


def test_calculator_facade_rejects_unknown_operation(tmp_path):
    calculator = make_calculator(tmp_path)

    with pytest.raises(InvalidOperationError, match="Unsupported operation"):
        calculator.calculate("%", 2, 3)


def test_calculator_undo_redo_and_empty_stack_results(tmp_path):
    calculator = make_calculator(tmp_path, auto_save=False)

    assert calculator.undo() is False
    assert calculator.redo() is False
    calculator.calculate("+", 2, 3)
    assert calculator.undo() is True
    assert calculator.history_text() == "No calculations yet."
    assert calculator.undo() is False
    assert calculator.redo() is True
    assert "2 + 3 = 5" in calculator.history_text()
    assert calculator.redo() is False


def test_calculator_new_calculation_clears_redo_stack(tmp_path):
    calculator = make_calculator(tmp_path, auto_save=False)
    calculator.calculate("+", 1, 2)
    calculator.undo()
    calculator.calculate("*", 3, 4)

    assert calculator.redo() is False
    assert "3 * 4 = 12" in calculator.history_text()


def test_calculator_clear_is_undoable(tmp_path):
    calculator = make_calculator(tmp_path, auto_save=False)
    calculator.calculate("+", 2, 3)

    calculator.clear()

    assert calculator.history_text() == "No calculations yet."
    assert calculator.undo() is True
    assert "2 + 3 = 5" in calculator.history_text()


def test_calculator_saves_and_loads_history(tmp_path):
    history_file = tmp_path / "history.csv"
    calculator = make_calculator(tmp_path, auto_save=False)
    calculator.calculate("^", 2, 3)
    calculator.save()
    pd.DataFrame(
        [[9, "+", 1, 10]],
        columns=["first_number", "operator", "second_number", "result"],
    ).to_csv(history_file, index=False)

    calculator.load()

    assert "9 + 1 = 10" in calculator.history_text()
    assert calculator.undo() is True
    assert "2 ^ 3 = 8" in calculator.history_text()


def test_calculator_load_missing_file_keeps_empty_history(tmp_path):
    calculator = make_calculator(tmp_path, auto_save=False)

    calculator.load()

    assert calculator.history_text() == "No calculations yet."
    assert calculator.undo() is True


def test_calculator_configuration_failure_is_propagated(monkeypatch):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "invalid")

    with pytest.raises(ValueError, match="CALCULATOR_AUTO_SAVE"):
        Calculator()
