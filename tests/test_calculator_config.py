from pathlib import Path

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_config_loads_defaults(monkeypatch):
    monkeypatch.delenv("CALCULATOR_HISTORY_FILE", raising=False)
    monkeypatch.delenv("CALCULATOR_AUTO_SAVE", raising=False)

    config = CalculatorConfig.load(env_file=Path("missing-test-env"))

    assert config.history_file == Path("history.csv")
    assert config.auto_save is True


def test_config_loads_dotenv_values(monkeypatch, tmp_path):
    monkeypatch.delenv("CALCULATOR_HISTORY_FILE", raising=False)
    monkeypatch.delenv("CALCULATOR_AUTO_SAVE", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text(
        "CALCULATOR_HISTORY_FILE=records/history.csv\nCALCULATOR_AUTO_SAVE=false\n",
        encoding="utf-8",
    )

    config = CalculatorConfig.load(env_file)

    assert config.history_file == Path("records/history.csv")
    assert config.auto_save is False


def test_config_rejects_empty_history_path(monkeypatch):
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", " ")

    with pytest.raises(ConfigurationError, match="cannot be empty"):
        CalculatorConfig.load(env_file=Path("missing-test-env"))


def test_config_rejects_invalid_auto_save_value(monkeypatch):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "sometimes")

    with pytest.raises(ConfigurationError, match="must be 'true' or 'false'"):
        CalculatorConfig.load(env_file=Path("missing-test-env"))
