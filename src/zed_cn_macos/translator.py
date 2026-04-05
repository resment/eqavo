from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

ALLOWED_PREFIXES = (
    "crates/zed/src/",
    "crates/title_bar/src/",
    "crates/settings_ui/src/",
    "crates/collab_ui/src/",
    "crates/onboarding/src/",
    "crates/extensions_ui/src/",
    "crates/keymap_editor/src/",
    "crates/theme_selector/src/",
    "crates/language_selector/src/",
    "crates/toolchain_selector/src/",
    "crates/encoding_selector/src/",
    "crates/line_ending_selector/src/",
    "crates/image_viewer/src/",
    "crates/file_finder/src/",
    "crates/project_panel/src/",
    "crates/outline_panel/src/",
    "crates/tab_switcher/src/",
    "crates/diagnostics/src/",
    "crates/repl/src/",
    "crates/markdown_preview/src/",
    "crates/csv_preview/src/",
    "crates/svg_preview/src/",
    "crates/feedback/src/",
    "crates/auto_update_ui/src/",
)


@dataclass(frozen=True)
class TranslationStats:
    changed_files: int
    replacements: int


def load_strings(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text())
    return data["strings"]


def replace_string_literals(content: str, source: str, target: str) -> tuple[str, int]:
    replacements = 0

    standard_literal = f'"{source}"'
    standard_replacement = f'"{target}"'
    standard_count = content.count(standard_literal)
    if standard_count:
        content = content.replace(standard_literal, standard_replacement)
        replacements += standard_count

    escaped_source = re.escape(source)
    raw_pattern = re.compile(rf'r(#+)"{escaped_source}"\1')

    def replace_raw(match: re.Match[str]) -> str:
        nonlocal replacements
        replacements += 1
        hashes = match.group(1)
        return f'r{hashes}"{target}"{hashes}'

    content = raw_pattern.sub(replace_raw, content)
    return content, replacements


def translate_tree(source_dir: Path, strings: dict[str, str]) -> TranslationStats:
    changed_files = 0
    replacements = 0

    for file_path in source_dir.rglob("*.rs"):
        relative_path = file_path.relative_to(source_dir).as_posix()
        if not relative_path.startswith(ALLOWED_PREFIXES):
            continue

        original = file_path.read_text()
        updated = original

        for source, target in strings.items():
            updated, count_before = replace_string_literals(updated, source, target)
            replacements += count_before

        if updated != original:
            file_path.write_text(updated)
            changed_files += 1

    return TranslationStats(changed_files=changed_files, replacements=replacements)
