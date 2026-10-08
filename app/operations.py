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

    @staticmethod
    def power(base, exponent):
        """Raise a base to an exponent."""
        return base**exponent

    @staticmethod
    def root(radicand, degree):
        """Return the real nth root of a radicand."""
        if degree == 0:
            raise ValueError("Root degree cannot be zero.")
        if radicand < 0:
            if not float(degree).is_integer() or int(degree) % 2 == 0:
                raise ValueError(
                    "A negative number requires an odd integer root degree."
                )
            return -((-radicand) ** (1 / degree))
        return radicand ** (1 / degree)