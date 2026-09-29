"""Where the Mindat API key is stored, and what this session already knows about it.

Sources, in the order MindatApiKeyManager tries them:
  1. explicit  - openmindat.set_api_key(...)
  2. env       - the MINDAT_API_KEY environment variable
  3. config    - the per-user credentials file (see config_path), mode 0600
  4. legacy    - ./.apikey.yaml, written by openmindat <= 0.1.3 (read only)

Nothing here talks to the network; validation lives in mindat_api.MindatApiKeyManager.
"""

from __future__ import annotations

import os
import tempfile
import warnings
from dataclasses import dataclass
from pathlib import Path

import yaml

from .exceptions import MindatKeyWarning

ENV_VAR = "MINDAT_API_KEY"
LEGACY_PATH = "./.apikey.yaml"

# Per-process state: validation results (D4: once per session) and one-time notices.
_session: dict[str, str | None] = {"explicit": None, "active": None, "active_source": None}
_validation: dict[str, str] = {}  # key -> "valid" | "invalid" | "unverified"
_notices_shown: set[str] = set()


@dataclass(frozen=True)
class ApiKeyStatus:
    """What openmindat.api_key_status() reports."""

    source: str | None  # explicit | env | config | legacy | None
    state: str  # valid | invalid | unverified | missing
    masked_key: str | None
    config_path: str

    def __str__(self) -> str:
        if self.state == "missing":
            return f"No Mindat API key found (config file: {self.config_path})"
        return f"Mindat API key {self.masked_key} from {self.source}: {self.state}"


def config_path() -> Path:
    """Per-user credentials file, outside any project folder."""
    if os.name == "nt":
        base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(base) / "openmindat" / "credentials.yaml"


def mask(key: str | None) -> str | None:
    if not key:
        return None
    return f"{key[:4]}…{key[-4:]}" if len(key) > 8 else "…"


def _read_key_file(path: Path | str, label: str) -> str | None:
    """Read `api_key` from a YAML file; warn and return None if it is unusable."""
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return None
    except (OSError, yaml.YAMLError) as exc:
        warn_once(f"read:{path}", f"Ignoring {label} {path}: cannot be read ({exc}).")
        return None
    key = data.get("api_key") if isinstance(data, dict) else None
    if not isinstance(key, str) or not key.strip():
        warn_once(f"read:{path}", f"Ignoring {label} {path}: it does not contain an 'api_key' entry.")
        return None
    return key.strip()


def read_config_key() -> str | None:
    return _read_key_file(config_path(), "Mindat API key file")


def read_legacy_key() -> str | None:
    return _read_key_file(LEGACY_PATH, "legacy Mindat API key file")


def write_config_key(key: str) -> Path:
    """Write the key to the per-user file with owner-only permissions (atomic replace)."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(path.parent, 0o700)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".credentials-")
    try:
        with os.fdopen(fd, "w") as f:
            yaml.safe_dump({"api_key": key}, f)
        if os.name != "nt":
            os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    return path


def remove_config_key() -> None:
    try:
        os.remove(config_path())
    except FileNotFoundError:
        pass


def candidates() -> list[tuple[str, str]]:
    """(source, key) pairs in resolution order, skipping empty sources."""
    found = []
    explicit = _session["explicit"]
    if isinstance(explicit, str) and explicit:
        found.append(("explicit", explicit))
    env = os.environ.get(ENV_VAR)
    if env:
        found.append(("env", env.strip()))
    config = read_config_key()
    if config:
        found.append(("config", config))
    legacy = read_legacy_key()
    if legacy:
        found.append(("legacy", legacy))
    return found


def set_explicit(key: str | None) -> None:
    _session["explicit"] = key


def reset_session() -> None:
    _session.update(explicit=None, active=None, active_source=None)
    _validation.clear()
    _notices_shown.clear()


def warn_once(tag: str, message: str) -> None:
    if tag not in _notices_shown:
        _notices_shown.add(tag)
        warnings.warn(message, MindatKeyWarning, stacklevel=4)


def notice_once(tag: str, message: str) -> None:
    if tag not in _notices_shown:
        _notices_shown.add(tag)
        print(message)
