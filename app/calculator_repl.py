"""Interactive command-line calculator."""

from .calculation import CalculationFactory
from .history import CalculationHistory

HELP_TEXT = (
    "Commands: help, history, exit (q also exits).\n"
    "Operations: +, -, *, /.\n"
    "Enter two numbers and an operation to calculate."
)


def _handle_command(user_input, history):
    """Handle a REPL command, returning its control-flow action."""
    command = user_input.lower()
    if command in ("q", "exit"):
        return "exit"
    if command == "help":
        print(HELP_TEXT)
        return "handled"
    if command == "history":
        print(history.format_entries())
        return "handled"
    return None


def calculator():
    """Run the calculator until the user chooses to quit."""
    history = CalculationHistory()
    print(
        "Calculator: enter help for commands. Enter exit or q at any prompt to quit."
    )
    print("Commands: help, history, exit (q also exits).")

    while True:
        first_input = input("First number: ").strip()
        command_action = _handle_command(first_input, history)
        if command_action == "exit":
            break
        if command_action == "handled":
            continue

        operator = input("Operation (+, -, *, /): ").strip()
        command_action = _handle_command(operator, history)
        if command_action == "exit":
            break
        if command_action == "handled":
            continue
        if not CalculationFactory.supports(operator):
            print("Please choose +, -, *, or /.")
            continue

        second_input = input("Second number: ").strip()
        command_action = _handle_command(second_input, history)
        if command_action == "exit":
            break
        if command_action == "handled":
            continue

        try:
            first_number = float(first_input)
            second_number = float(second_input)
            calculation = CalculationFactory.create(
                operator, first_number, second_number
            )
            result = calculation.perform()
        except ValueError as error:
            print(f"Error: {error}")
            continue

        history.add(calculation)
        print(f"Result: {result}")


if __name__ == "__main__":
    calculator()