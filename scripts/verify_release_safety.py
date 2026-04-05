#!/usr/bin/env python3
from __future__ import annotations

import plistlib
import sys
from pathlib import Path


TEXT_SUFFIXES = {
    ".c",
    ".cc",
    ".conf",
    ".cpp",
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsonc",
    ".md",
    ".plist",
    ".py",
    ".rs",
    ".sh",
    ".svg",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

FORBIDDEN_PATH_NAMES = {
    "credentials.json",
    "keymap.json",
    "mcp.json",
    "settings.json",
    "tasks.json",
}

FORBIDDEN_TEXT_MARKERS = {
    "\"api_key\"",
    "\"apiKey\"",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "ZAI_API_KEY",
    "glm-4",
    "z.ai",
}


def iter_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*") if path.is_file()]


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name == "Info.plist"


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    lower_name = path.name.lower()
    if lower_name in FORBIDDEN_PATH_NAMES:
        findings.append(f"forbidden config filename present: {path}")

    if not is_text_candidate(path):
        return findings

    try:
        if path.name == "Info.plist":
            plistlib.loads(path.read_bytes())
            content = path.read_text(errors="ignore")
        else:
            content = path.read_text(errors="ignore")
    except Exception as exc:
        findings.append(f"failed to read text candidate {path}: {exc}")
        return findings

    for marker in FORBIDDEN_TEXT_MARKERS:
        if marker in content:
            findings.append(f"forbidden marker {marker!r} found in {path}")

    return findings


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: verify_release_safety.py /path/to/Eqavo.app", file=sys.stderr)
        return 2

    app_path = Path(sys.argv[1]).resolve()
    if not app_path.exists():
        print(f"App bundle not found: {app_path}", file=sys.stderr)
        return 2

    findings: list[str] = []
    for file_path in iter_files(app_path):
        findings.extend(scan_file(file_path))

    if findings:
        print("Release safety check failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print(f"Release safety check passed: {app_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
