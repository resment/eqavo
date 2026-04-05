from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

import requests


REPO = "zed-industries/zed"


def fetch_latest_release() -> dict:
    response = requests.get(f"https://api.github.com/repos/{REPO}/releases", timeout=30)
    response.raise_for_status()
    releases = response.json()
    stable = [release for release in releases if not release.get("prerelease")]
    if not stable:
        raise RuntimeError("No stable Zed release found")
    return stable[0]


def download_source(zip_url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(zip_url, timeout=60, stream=True) as response:
        response.raise_for_status()
        with destination.open("wb") as output:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    output.write(chunk)


def unpack_source(source_zip: Path, target_dir: Path) -> None:
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source_zip) as archive:
        top_level_dir = archive.namelist()[0].split("/")[0]
        archive.extractall(target_dir.parent)

    extracted = target_dir.parent / top_level_dir
    extracted.rename(target_dir)
