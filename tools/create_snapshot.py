#!/usr/bin/env python3
"""Utility script to capture a Codex runtime snapshot for the Warmup repo."""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
import subprocess
from typing import Any, Dict, List

SNAPSHOT_NAME = "warmup_main_snapshot_01"
SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"
EXPECTED_ROOT_ITEMS = [
    ("README.md", False),
    ("backend", True),
    ("frontend", True),
    ("ops", True),
    ("tests", True),
    ("tools", True),
    ("docker-compose.yml", False),
    ("dev.ps1", False),
]


def _list_repository_root_files(repo_root: Path) -> List[str]:
    entries: List[str] = []
    for name, is_dir in EXPECTED_ROOT_ITEMS:
        path = repo_root / name
        if not path.exists():
            raise FileNotFoundError(f"Expected repository item '{name}' not found at root")
        suffix = "/" if is_dir else ""
        entries.append(f"{name}{suffix}")
    return entries


def _load_codex_config(repo_root: Path) -> Dict[str, Any]:
    config_path = repo_root / ".codexconfig"
    with config_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _get_active_branch(repo_root: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo_root), "rev-parse", "--abbrev-ref", "HEAD"],
        text=True,
    ).strip()


def build_snapshot(repo_root: Path) -> Dict[str, Any]:
    codex_config = _load_codex_config(repo_root)

    snapshot_time = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)
    snapshot: Dict[str, Any] = {
        "name": SNAPSHOT_NAME,
        "created_at": snapshot_time.isoformat().replace("+00:00", "Z"),
        "repository": {
            "root": str(repo_root),
            "active_branch": _get_active_branch(repo_root),
            "root_files": _list_repository_root_files(repo_root),
        },
        "codex": {
            "config_path": str(repo_root / ".codexconfig"),
            "loaded_configuration": codex_config,
            "environment": {
                "commit_mode": codex_config.get("commit_mode"),
                "auto_branch_creation": codex_config.get("auto_branch_creation"),
                "auto_pull_requests": codex_config.get("auto_pull_requests"),
                "enforce_branch": codex_config.get("enforce_branch"),
            },
        },
    }

    return snapshot


def save_snapshot(snapshot: Dict[str, Any]) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_path = SNAPSHOT_DIR / f"{SNAPSHOT_NAME}.json"
    with snapshot_path.open("w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2, sort_keys=True)
        fh.write("\n")

    default_marker = SNAPSHOT_DIR / "default_snapshot.txt"
    with default_marker.open("w", encoding="utf-8") as fh:
        fh.write(SNAPSHOT_NAME + "\n")

    return snapshot_path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    snapshot = build_snapshot(repo_root)
    snapshot_path = save_snapshot(snapshot)
    print(f"Snapshot '{SNAPSHOT_NAME}' saved to {snapshot_path}.")
    print("This snapshot is now marked as the default Codex restore point.")


if __name__ == "__main__":
    main()
