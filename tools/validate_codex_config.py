#!/usr/bin/env python3
"""Validate and synchronize Codex runtime configuration.

The script ensures that the runtime configuration used by Codex matches the
settings tracked in the repository-level `.codexconfig`. It is designed to run
inside CI environments as well as locally.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / ".codexconfig"
RUNTIME_STATE_PATH = Path(
    os.environ.get("CODEX_RUNTIME_STATE_PATH", REPO_ROOT / "tools/.codex_runtime_state.json")
)
LOG_PATH = REPO_ROOT / "tools/.codexconfig_sync.log"

SYNC_FIELDS = (
    "default_branch",
    "auto_branch_creation",
    "auto_pull_requests",
    "commit_mode",
    "commit_template",
    "enforce_branch",
    "sync_with_back4app",
    "pre_commit_validation",
)


class ConfigSyncError(RuntimeError):
    """Raised when validation fails due to missing prerequisites."""


def load_json(path: Path) -> Dict[str, object]:
    if not path.exists():
        raise ConfigSyncError(f"Configuration file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ConfigSyncError(f"Invalid JSON in {path}: {exc}") from exc


def ensure_runtime_state_file(path: Path) -> Dict[str, object]:
    if not path.exists():
        # Initialize runtime state with the repository configuration on first run.
        return {}

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        # Corrupted runtime file; start with an empty state so it can be replaced.
        return {}


def detect_differences(
    repo_config: Dict[str, object], runtime_state: Dict[str, object]
) -> List[Tuple[str, object, object]]:
    differences: List[Tuple[str, object, object]] = []
    for field in SYNC_FIELDS:
        repo_value = repo_config.get(field)
        runtime_value = runtime_state.get(field)
        if repo_value != runtime_value:
            differences.append((field, runtime_value, repo_value))
    return differences


def update_runtime_state(path: Path, repo_config: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        state = {field: repo_config.get(field) for field in SYNC_FIELDS}
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_log_entry(differences: List[Tuple[str, object, object]]) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] ")
        if differences:
            diff_summary = ", ".join(
                f"{field}: runtime={runtime!r} → repo={repo!r}"
                for field, runtime, repo in differences
            )
            handle.write(f"Differences detected | {diff_summary}\n")
        else:
            handle.write("No differences detected.\n")


def main() -> int:
    try:
        repo_config = load_json(CONFIG_PATH)
    except ConfigSyncError as exc:
        print(f"ERROR: {exc}")
        return 1

    runtime_state = ensure_runtime_state_file(RUNTIME_STATE_PATH)
    differences = detect_differences(repo_config, runtime_state)

    if differences:
        print("⚠️ Codex runtime configuration mismatch detected. Synchronizing...")
        update_runtime_state(RUNTIME_STATE_PATH, repo_config)
    else:
        print("Codex runtime configuration already synchronized.")

    write_log_entry(differences)

    if differences:
        for field, runtime_value, repo_value in differences:
            print(
                f"Updated {field!r}: runtime had {runtime_value!r}, repository requires {repo_value!r}."
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
