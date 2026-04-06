from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    repo_root: Path
    workdir: Path
    source_zip: Path
    source_dir: Path
    translations_file: Path
    glossary_file: Path
    zed_version_file: Path


def load_paths(repo_root: Path | None = None) -> Paths:
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    workdir = root / ".workdir"
    return Paths(
        repo_root=root,
        workdir=workdir,
        source_zip=workdir / "zed-src.zip",
        source_dir=workdir / "zed-src",
        translations_file=root / "translations" / "strings_zh_CN.json",
        glossary_file=root / "translations" / "glossary_zh_CN.json",
        zed_version_file=root / "zed-version.txt",
    )
