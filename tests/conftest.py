import pytest


@pytest.fixture(autouse=True)
def isolate_calculator_history(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(tmp_path / "history.csv"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")