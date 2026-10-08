"""Load and validate calculator configuration from environment variables."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from .exceptions import ConfigurationError


@dataclass(frozen=True)
class CalculatorConfig:
    """Validated settings used by the calculator application."""

    history_file: Path
    auto_save: bool

    @classmethod
    def load(cls, env_file: Optional[Path] = None):
        """Load dotenv values and validate supported settings."""
        load_dotenv(dotenv_path=env_file, override=False)
        history_file_value = os.getenv("CALCULATOR_HISTORY_FILE", "history.csv").strip()
        auto_save_value = os.getenv("CALCULATOR_AUTO_SAVE", "true").strip().lower()

        if not history_file_value:
            raise ConfigurationError("CALCULATOR_HISTORY_FILE cannot be empty.")
        if auto_save_value not in {"true", "false"}:
            raise ConfigurationError(
                "CALCULATOR_AUTO_SAVE must be 'true' or 'false'."
            )

        return cls(
            history_file=Path(history_file_value).expanduser(),
            auto_save=auto_save_value == "true",
        )