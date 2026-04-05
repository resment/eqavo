#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from zed_cn_macos.config import load_paths

ENV_PASSTHROUGH_SNIPPET = """        // Eqavo preserves user-provided agent environment variables.
        for var_name in [
            "ANTHROPIC_API_KEY",
            "ANTHROPIC_BASE_URL",
            "CLAUDE_CODE_USE_BEDROCK",
            "CLAUDE_CODE_USE_VERTEX",
        ] {
            if let Ok(val) = std::env::var(var_name) {
                extra_env.insert(var_name.into(), val);
            }
        }
        for (key, val) in std::env::vars() {
            if key.starts_with("AWS_")
                || key.starts_with("GOOGLE_CLOUD_")
                || key == "CLOUD_ML_REGION"
            {
                extra_env.insert(key, val);
            }
        }
"""


def replace_exact(path: Path, old: str, new: str) -> None:
    content = path.read_text()
    if new in content:
        return
    if old not in content:
        raise RuntimeError(f"Expected snippet not found in {path}")
    path.write_text(content.replace(old, new, 1))


def main() -> int:
    paths = load_paths(ROOT)
    candidate_files = [
        paths.source_dir / "crates" / "agent_servers" / "src" / "custom.rs",
        paths.source_dir / "crates" / "agent_servers" / "src" / "claude.rs",
    ]
    patched_files: list[Path] = []

    for path in candidate_files:
        if not path.exists():
            continue
        replace_exact(
            path,
            '                    extra_env.insert("ANTHROPIC_API_KEY".into(), "".into());\n',
            "                    // Eqavo preserves user-configured Anthropic credentials.\n",
        )
        replace_exact(
            path,
            "        let mut extra_env = load_proxy_env(cx);\n",
            "        let mut extra_env = load_proxy_env(cx);\n" + ENV_PASSTHROUGH_SNIPPET,
        )
        patched_files.append(path)

    if not patched_files:
        raise RuntimeError("Expected agent server source files not found")

    print("Patched agent environment handling:")
    for path in patched_files:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
