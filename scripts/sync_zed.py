#!/usr/bin/env python3
from __future__ import annotations

import sys

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from zed_cn_macos.config import load_paths
from zed_cn_macos.zed_sync import download_source, fetch_latest_release, unpack_source


def main() -> int:
    paths = load_paths(ROOT)
    release = fetch_latest_release()
    version = release["name"]

    print(f"Latest Zed release: {version}")
    print(f"Downloading source to: {paths.source_zip}")
    download_source(release["zipball_url"], paths.source_zip)

    print(f"Unpacking source to: {paths.source_dir}")
    unpack_source(paths.source_zip, paths.source_dir)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
