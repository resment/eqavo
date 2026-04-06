#!/usr/bin/env python3
from __future__ import annotations

import sys

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from zed_cn_macos.config import load_paths
from zed_cn_macos.zed_sync import download_source, fetch_latest_release, fetch_release_by_tag, unpack_source


def resolve_release(paths) -> dict:
    pinned_tag = paths.zed_version_file.read_text().strip()
    if pinned_tag:
        return fetch_release_by_tag(pinned_tag)
    return fetch_latest_release()


def main() -> int:
    paths = load_paths(ROOT)
    release = resolve_release(paths)
    version = release["name"]

    print(f"Resolved Zed release: {version}")
    print(f"Downloading source to: {paths.source_zip}")
    download_source(release["zipball_url"], paths.source_zip)

    print(f"Unpacking source to: {paths.source_dir}")
    unpack_source(paths.source_zip, paths.source_dir)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
