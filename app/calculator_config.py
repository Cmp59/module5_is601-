"""Load and validate calculator configuration from environment variables."""

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from dotenv import load_dotenv

from .exceptions import ConfigurationError


@dataclass(frozen=True)
class CalculatorConfig:
    """Validated settings used by the calculator application."""

    history_file: Path
    auto_save: bool

    def new_session_history_file(self) -> Path:
        """Return a unique CSV path for a new REPL session."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{self.history_file.stem}_{timestamp}_{uuid4().hex[:8]}.csv"
        return self.history_file.with_name(filename)

    @classmethod
    def load(cls, env_file: Optional[Path] = None):
        """Load dotenv values and validate supported settings."""
        load_dotenv(dotenv_path=env_file, override=False)
        history_file_value = os.getenv(
            "CALCULATOR_HISTORY_FILE", "history.csv"
        ).strip()
        auto_save_value = os.getenv("CALCULATOR_AUTO_SAVE", "true").strip().lower()

        if not history_file_value:
            raise ConfigurationError("CALCULATOR_HISTORY_FILE cannot be empty.")
        if auto_save_value not in {"true", "false"}:
            raise ConfigurationError(
                "CALCULATOR_AUTO_SAVE must be 'true' or 'false'."
            )

        try:
            history_file = Path(history_file_value).expanduser()
            if not history_file.name or history_file.name in {".", ".."}:
                raise ConfigurationError(
                    "CALCULATOR_HISTORY_FILE must include a filename prefix."
                )
            if history_file.exists() and history_file.is_dir():
                raise ConfigurationError(
                    "CALCULATOR_HISTORY_FILE must be a file path prefix, not a directory."
                )
            if history_file.parent.exists() and not history_file.parent.is_dir():
                raise ConfigurationError(
                    "The parent of CALCULATOR_HISTORY_FILE must be a directory."
                )
        except OSError as error:
            raise ConfigurationError(
                f"Invalid CALCULATOR_HISTORY_FILE: {error}"
            ) from error

        return cls(
            history_file=history_file,
            auto_save=auto_save_value == "true",
        )