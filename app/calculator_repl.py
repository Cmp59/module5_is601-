"""Interactive command-line interface for the Calculator facade."""

from .calculator import Calculator
from .exceptions import CalculatorError
from .input_validators import normalize_command, parse_number

HELP_TEXT = (
    "Commands: help, history, clear, undo, redo, save, load, exit (q also exits).\n"
    "Operations: +, -, *, /, ^, root.\n"
    "For root, enter the radicand first and the root degree second."
)


def _read_input(prompt):
    """Read one prompt, returning None for EOF or an interrupt."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("Input interrupted. Exiting calculator.")
        return None


def _handle_command(user_input, calculator):
    """Handle a REPL command, returning its control-flow action."""
    command = normalize_command(user_input)
    if command in ("q", "exit"):
        return "exit"
    if command == "help":
        print(HELP_TEXT)
        return "handled"
    if command == "history":
        print(calculator.history_text())
        return "handled"
    if command == "clear":
        calculator.clear()
        print("History cleared.")
        return "handled"
    if command == "undo":
        print("Undid last change." if calculator.undo() else "Nothing to undo.")
        return "handled"
    if command == "redo":
        print("Redid last change." if calculator.redo() else "Nothing to redo.")
        return "handled"
    if command == "save":
        try:
            calculator.save()
        except CalculatorError as error:
            print(f"Error: {error}")
        else:
            print("History saved.")
        return "handled"
    if command == "load":
        try:
            calculator.load()
        except CalculatorError as error:
            print(f"Error: {error}")
        else:
            print("History loaded.")
        return "handled"
    return None


def calculator():
    """Run the calculator until the user chooses to quit."""
    try:
        calculator_app = Calculator()
    except CalculatorError as error:
        print(f"Calculator configuration/history error: {error}")
        return
    print(
        "Calculator: enter help for commands. Enter exit or q at any prompt to quit."
    )
    print("Commands: help, history, clear, undo, redo, save, load, exit (q also exits).")

    while True:
        first_input = _read_input("First number: ")
        if first_input is None:
            break
        command_action = _handle_command(first_input, calculator_app)
        if command_action == "exit":
            break
        if command_action == "handled":
            continue

        operator = _read_input("Operation (+, -, *, /, ^, root): ")
        if operator is None:
            break
        operator = normalize_command(operator)
        command_action = _handle_command(operator, calculator_app)
        if command_action == "exit":
            break
        if command_action == "handled":
            continue
        if not calculator_app.supports(operator):
            print("Please choose +, -, *, /, ^, or root.")
            continue

        second_input = _read_input("Second number: ")
        if second_input is None:
            break
        command_action = _handle_command(second_input, calculator_app)
        if command_action == "exit":
            break
        if command_action == "handled":
            continue

        try:
            first_number = parse_number(first_input)
            second_number = parse_number(second_input)
            result = calculator_app.calculate(
                operator, first_number, second_number
            )
        except CalculatorError as error:
            print(f"Error: {error}")
            continue

        print(f"Result: {result}")

    try:
        session_file = calculator_app.close()
    except CalculatorError as error:
        print(f"Error saving session history: {error}")
    else:
        print(f"Session history saved to: {session_file}")


if __name__ == "__main__":
    calculator()