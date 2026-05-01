"""
Configuration management for ODVpy.

A singleton class handle user-editable settings, persisted as TOML
files in the current working directory.
"""

import tomllib
from pathlib import Path

from settings import *


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _write_toml(path: Path, data: dict) -> None:
    """Minimal TOML serializer.

    Relies on no external library. Sufficient for the flat structures
    used by Config.
    """
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"\n[{key}]")
            for k, v in value.items():
                lines.append(_toml_line(k, v))
        else:
            lines.append(_toml_line(key, value))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _toml_line(key: str, value) -> str:
    if isinstance(value, bool):
        return f'{key} = {str(value).lower()}'
    if isinstance(value, str):
        return f'{key} = "{value}"'
    if isinstance(value, Path):
        return f'{key} = "{str(value)}"'
    if isinstance(value, list):
        items = ", ".join(f'"{v}"' if isinstance(v, str) else str(v) for v in value)
        return f"{key} = [{items}]"
    return f"{key} = {value}"


# ---------------------------------------------------------------------------
# UIConfig
# ---------------------------------------------------------------------------

class _Config:
    """Singleton — access via the module-level ``Config`` instance.

    Stores user preferences.
    Persisted in ``config.toml`` in the current working directory.
    """

    def __init__(self) -> None:
        self.filename = Path(CONFIG_FILENAME)

        # init default values

        # loading
        self.loaded_section: list[str] = ["BGND"]

        # paths
        self.installation_path: Path = Path("")
        self.backup_path: Path = Path("backup")

    def load(self) -> None:
        """Load settings from TOML file. Missing keys fall back to defaults."""
        try:
            with open(self.filename, "rb") as f:
                data = tomllib.load(f)
            print(f"[Config] load from '{self.filename}'.")
        except FileNotFoundError:
            print(f"[Config] '{self.filename}' not found — using defaults.")
            return
        except tomllib.TOMLDecodeError as e:
            print(f"[Config] Parse error in '{self.filename}': {e} — using defaults.")
            return

        loading = data.get("loading", {})
        self.loaded_section = loading.get("loaded_section", self.loaded_section)

        paths = data.get("paths", {})
        self.installation_path = Path(paths.get("installation_path", self.installation_path))
        self.backup_path = Path(paths.get("backup_path", self.backup_path))


    def save(self) -> None:
        """Save current settings to TOML file."""
        _write_toml(self.filename, {
            "loading": {
                "loaded_section": self.loaded_section,
            },
            "paths": {
                "installation_path": self.installation_path,
                "backup_path": self.backup_path,
            },
        })
        print(f"[Config] Saved to '{self.filename}'.")


# ---------------------------------------------------------------------------
# Module-level singletons  (import and use directly)
# ---------------------------------------------------------------------------

Config = _Config()
