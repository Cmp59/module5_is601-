from app.calculator_memento import CalculatorMemento


def test_memento_captures_immutable_rows():
    source_rows = [[1, "+", 2, 3]]

    memento = CalculatorMemento.from_rows(source_rows)
    source_rows[0][0] = 99

    assert memento.rows == ((1, "+", 2, 3),)
