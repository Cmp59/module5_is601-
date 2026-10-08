from unittest.mock import patch
import runpy
import sys

import pytest

from app.calculator_repl import calculator


@pytest.mark.parametrize(
    "first_number, operator, second_number, expected_result",
    [
        ("2", "+", "3", "Result: 5.0"),
        ("5", "-", "3", "Result: 2.0"),
        ("2", "*", "3", "Result: 6.0"),
        ("6", "/", "3", "Result: 2.0"),
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
    assert "Commands: help, history, exit (q also exits)." in output


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

    assert "Please choose +, -, *, or /." in capsys.readouterr().out


def test_calculator_rejects_non_numeric_first_number(capsys):
    with patch("builtins.input", side_effect=["abc", "+", "2", "q"]):
        calculator()

    assert "could not convert string to float" in capsys.readouterr().out


def test_calculator_rejects_non_numeric_second_number(capsys):
    with patch("builtins.input", side_effect=["2", "+", "abc", "q"]):
        calculator()

    assert "could not convert string to float" in capsys.readouterr().out


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
    assert "Commands: help, history, exit" in output
    assert "Operations: +, -, *, /." in output


def test_calculator_handles_help_at_operator_prompt(capsys):
    with patch("builtins.input", side_effect=["2", "help", "exit"]):
        calculator()

    assert "Commands: help, history, exit" in capsys.readouterr().out


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


def test_calculator_module_starts_repl(monkeypatch):
    monkeypatch.delitem(sys.modules, "app.calculator_repl", raising=False)
    with patch("builtins.input", return_value="q"):
        runpy.run_module("app.calculator_repl", run_name="__main__")