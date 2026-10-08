"""Basic arithmetic operations."""


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
            raise ValueError("You cannot divide by zero.")
        return first_number / second_number