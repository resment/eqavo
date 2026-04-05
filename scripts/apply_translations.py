#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from zed_cn_macos.config import load_paths
from zed_cn_macos.translator import load_glossary, load_strings, merge_translation_sets, translate_tree


def main() -> int:
    paths = load_paths(ROOT)
    glossary = load_glossary(paths.glossary_file)
    strings = load_strings(paths.translations_file)
    translations = merge_translation_sets(glossary, strings)
    stats = translate_tree(paths.source_dir, translations)

    print(f"Changed files: {stats.changed_files}")
    print(f"Total replacements: {stats.replacements}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
