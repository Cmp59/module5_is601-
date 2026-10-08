from unittest.mock import patch
import runpy
import sys
from pathlib import Path

import pandas as pd
import pytest

from app.calculator import Calculator
from app.exceptions import ConfigurationError, HistoryError
from app.calculator_repl import calculator


@pytest.mark.parametrize(
    "first_number, operator, second_number, expected_result",
    [
        ("2", "+", "3", "Result: 5.0"),
        ("5", "-", "3", "Result: 2.0"),
        ("2", "*", "3", "Result: 6.0"),
        ("6", "/", "3", "Result: 2.0"),
        ("2", "^", "3", "Result: 8.0"),
        ("27", "root", "3", "Result: 3.0"),
    ],
)
def test_calculator_performs_operations(
    first_number, operator, second_number, expected_result, capsys
):
    with patch(
        "builtins.input",
        side_effect=[first_number, operator, second_number, "q"],
    ):
        calculator()

    assert expected_result in capsys.readouterr().out


@pytest.mark.parametrize("quit_command", ["q", "exit"])
def test_calculator_quits_at_first_number(quit_command, capsys):
    with patch("builtins.input", return_value=quit_command):
        calculator()

    output = capsys.readouterr().out
    assert "Enter exit or q at any prompt to quit" in output
    assert "Commands: help, history, clear, undo, redo, save, load, exit" in output


@pytest.mark.parametrize("quit_command", ["q", "exit"])
def test_calculator_quits_at_operator(quit_command):
    with patch("builtins.input", side_effect=["2", quit_command]):
        calculator()


@pytest.mark.parametrize("quit_command", ["q", "exit"])
def test_calculator_quits_at_second_number(quit_command):
    with patch("builtins.input", side_effect=["2", "+", quit_command]):
        calculator()


def test_calculator_rejects_unsupported_operation(capsys):
    with patch("builtins.input", side_effect=["2", "%", "q"]):
        calculator()

    assert "Please choose +, -, *, /, ^, or root." in capsys.readouterr().out


def test_calculator_rejects_non_numeric_first_number(capsys):
    with patch("builtins.input", side_effect=["abc", "+", "2", "q"]):
        calculator()

    assert "Invalid number: abc" in capsys.readouterr().out


def test_calculator_rejects_non_numeric_second_number(capsys):
    with patch("builtins.input", side_effect=["2", "+", "abc", "q"]):
        calculator()

    assert "Invalid number: abc" in capsys.readouterr().out


def test_calculator_handles_division_by_zero(capsys):
    with patch("builtins.input", side_effect=["2", "/", "0", "q"]):
        calculator()

    assert "You cannot divide by zero." in capsys.readouterr().out


def test_calculator_displays_empty_history(capsys):
    with patch("builtins.input", side_effect=["history", "q"]):
        calculator()

    assert "No calculations yet." in capsys.readouterr().out


def test_calculator_help_command(capsys):
    with patch("builtins.input", side_effect=["help", "exit"]):
        calculator()

    output = capsys.readouterr().out
    assert "Commands: help, history, clear, undo, redo, save, load, exit" in output
    assert "Operations: +, -, *, /, ^, root." in output


def test_calculator_handles_help_at_operator_prompt(capsys):
    with patch("builtins.input", side_effect=["2", "help", "exit"]):
        calculator()

    assert "Commands: help, history, clear, undo, redo, save, load, exit" in capsys.readouterr().out


def test_calculator_handles_history_at_second_number_prompt(capsys):
    with patch("builtins.input", side_effect=["2", "+", "history", "exit"]):
        calculator()

    assert "No calculations yet." in capsys.readouterr().out


def test_calculator_displays_completed_history(capsys):
    with patch("builtins.input", side_effect=["2", "+", "3", "history", "q"]):
        calculator()

    assert "1. 2.0 + 3.0 = 5.0" in capsys.readouterr().out


def test_failed_calculation_is_not_added_to_history(capsys):
    with patch(
        "builtins.input",
        side_effect=["2", "/", "0", "history", "q"],
    ):
        calculator()

    output = capsys.readouterr().out
    assert "You cannot divide by zero." in output
    assert "No calculations yet." in output


def test_calculator_reports_invalid_root(capsys):
    with patch("builtins.input", side_effect=["-9", "root", "2", "exit"]):
        calculator()

    assert "negative number requires an odd integer root degree" in capsys.readouterr().out


def test_calculator_module_starts_repl(monkeypatch):
    monkeypatch.delitem(sys.modules, "app.calculator_repl", raising=False)
    with patch("builtins.input", return_value="q"):
        runpy.run_module("app.calculator_repl", run_name="__main__")


def test_repl_saves_session_csv_when_exiting(capsys, monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(tmp_path / "history.csv"))
    with patch("builtins.input", side_effect=["2", "+", "3", "exit"]):
        calculator()

    output = capsys.readouterr().out
    assert "Result: 5.0" in output
    assert "Session history saved to:" in output
    csv_files = list(tmp_path.glob("history_*.csv"))
    assert csv_files
    saved = pd.read_csv(csv_files[-1])
    assert list(saved.columns) == [
        "first_operand",
        "operator",
        "second_operand",
        "result",
    ]
    assert saved.iloc[-1].to_dict() == {
        "first_operand": 2.0,
        "operator": "+",
        "second_operand": 3.0,
        "result": 5.0,
    }


@pytest.mark.parametrize("prompt_values", [["clear", "exit"], ["2", "clear", "exit"]])
def test_calculator_clear_command(prompt_values, capsys):
    with patch("builtins.input", side_effect=prompt_values):
        calculator()

    assert "History cleared." in capsys.readouterr().out


@pytest.mark.parametrize(
    "command, expected",
    [("undo", "Nothing to undo."), ("redo", "Nothing to redo."),
     ("save", "History saved."), ("load", "History loaded.")],
)
def test_calculator_state_commands(command, expected, capsys):
    with patch("builtins.input", side_effect=[command, "exit"]):
        calculator()

    assert expected in capsys.readouterr().out


@pytest.mark.parametrize("exception_type", [EOFError, KeyboardInterrupt])
@pytest.mark.parametrize(
    "input_before_interrupt",
    [[], ["2"], ["2", "+"]],
)
def test_calculator_exits_gracefully_on_input_interruption(
    exception_type, input_before_interrupt, capsys
):
    with patch(
        "builtins.input",
        side_effect=[*input_before_interrupt, exception_type()],
    ):
        calculator()

    assert "Input interrupted. Exiting calculator." in capsys.readouterr().out


def test_calculator_reports_configuration_error(monkeypatch, capsys):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "invalid")

    calculator()

    assert "Calculator configuration/history error" in capsys.readouterr().out


def test_calculator_reports_save_errors(monkeypatch, capsys):
    monkeypatch.setattr(
        Calculator,
        "save",
        lambda self: (_ for _ in ()).throw(ConfigurationError("save failed")),
    )
    with patch("builtins.input", side_effect=["save", "exit"]):
        calculator()

    assert "Error: save failed" in capsys.readouterr().out


def test_calculator_reports_load_errors(monkeypatch, capsys):
    monkeypatch.setattr(
        Calculator,
        "load",
        lambda self: (_ for _ in ()).throw(ConfigurationError("load failed")),
    )
    with patch("builtins.input", side_effect=["load", "exit"]):
        calculator()

    assert "Error: load failed" in capsys.readouterr().out


def test_calculator_reports_session_save_error(monkeypatch, capsys):
    monkeypatch.setattr(
        Calculator,
        "close",
        lambda self: (_ for _ in ()).throw(HistoryError("session save failed")),
    )
    with patch("builtins.input", return_value="exit"):
        calculator()

    assert "Error saving session history: session save failed" in capsys.readouterr().out