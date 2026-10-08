# Module 4 Calculator

A command-line calculator built with Python and object-oriented design.

## Setup

Create and activate a virtual environment, then install the project dependencies:

```powershell
python -m venv .env
.\.env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation scripts, run this once for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Run the Calculator

```powershell
python main.py
```

The calculator supports addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), exponentiation (`^`), and nth roots (`root`). For `root`, enter the radicand first and the root degree second. Enter `help` to view commands and operations, `history` to view completed calculations, or `exit` to quit. These commands are available at any prompt; `q` also quits. The `CalculationFactory` creates a calculation instance for the selected operator, and completed instances are kept in session history.

## Run Tests

Run the test suite with coverage:

```powershell
python -m pytest
```

The project requires 100% test coverage. To enforce that requirement locally, run:

```powershell
python -m pytest --cov-fail-under=100
```

## Project Structure

- `app/calculator_repl.py`: Interactive calculator REPL
- `app/calculation.py`: Calculation instances and `CalculationFactory`
- `app/history.py`: Stores and displays session calculations
- `app/operations.py`: Arithmetic operations
- `tests/test_operations.py`: Parameterized arithmetic tests
- `tests/test_calculations.py`: Calculation, factory, and history tests
- `tests/test_calculator_repl.py`: REPL tests
- `.github/workflows/ci.yml`: GitHub Actions configuration