from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TranslationStats:
    changed_files: int
    replacements: int


def load_strings(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text())
    return data["strings"]


def translate_tree(source_dir: Path, strings: dict[str, str]) -> TranslationStats:
    changed_files = 0
    replacements = 0

    for file_path in source_dir.rglob("*.rs"):
        original = file_path.read_text()
        updated = original

        for source, target in strings.items():
            count_before = updated.count(source)
            if count_before:
                updated = updated.replace(source, target)
                replacements += count_before

        if updated != original:
            file_path.write_text(updated)
            changed_files += 1

    return TranslationStats(changed_files=changed_files, replacements=replacements)
