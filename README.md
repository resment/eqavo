# Eqavo

`Eqavo` is an unofficial macOS-first Chinese localization project based on Zed source code.

The goal is simple:

- End users should not compile anything.
- Maintainers should be able to sync a new Zed release quickly.
- The project should produce a signed-or-unsigned `.app` / `.dmg` artifact that Mac users can open directly.

## User experience

The ideal user flow is:

1. Open the latest GitHub Release.
2. Download `Eqavo-AppleSilicon.dmg` or `Eqavo-Intel.dmg`.
3. Drag `Eqavo.app` into `Applications`.
4. Open and use it.

For advanced users we also keep a local build path:

```bash
./scripts/bootstrap.sh
./scripts/build_local.sh
```

## Why this project exists

The existing community translation project has two main problems for macOS:

1. It is Linux-first.
2. Its translation targets are tied to old file paths, so coverage drops as Zed evolves.

Eqavo is macOS-only on purpose. We optimize for:

- current Zed source layout
- macOS build tooling
- simple release artifacts
- easier translation maintenance

## Recommended architecture

### For users

- Download prebuilt macOS releases.
- Do not run Python, Rust, or build scripts locally unless they want to contribute.

### For maintainers

- Sync the latest Zed version.
- Apply a translation overlay from `translations/`.
- Build on GitHub Actions macOS runners.
- Publish `.app` and `.dmg` artifacts.

## Project layout

```text
eqavo/
  README.md
  BRANDING.md
  assets/
    brand/
      eqavo-logo.svg
      eqavo-icon.svg
  pyproject.toml
  translations/
    strings_zh_CN.json
  scripts/
    bootstrap.sh
    build_local.sh
    sync_zed.py
    apply_translations.py
    disable_services.py
  src/zed_cn_macos/
    __init__.py
    config.py
    zed_sync.py
    translator.py
```

## Current strategy

We keep the source-based approach, but make it maintainable:

1. Download a specific Zed release source snapshot.
2. Apply translation replacements from a structured dictionary.
3. Support per-file replacement rules for unstable UI code.
4. Build macOS binaries.
5. Package the result for end users.

## Better than the old approach

- macOS paths are first-class
- no hardcoded author machine paths
- no proxy assumptions
- no Linux-only build script dependency
- translation data is separated from build logic
- local build and CI build use the same scripts

## Branding

- `Eqavo` is a separate community brand.
- It is not affiliated with or endorsed by Zed Industries.
- We should avoid using Zed's official logo, app icon, or branding assets.

Brand assets for this project live in:

- [BRANDING.md](/Users/resment/Documents/New%20project/zed-cn-macos/BRANDING.md)
- [eqavo-logo.svg](/Users/resment/Documents/New%20project/zed-cn-macos/assets/brand/eqavo-logo.svg)
- [eqavo-icon.svg](/Users/resment/Documents/New%20project/zed-cn-macos/assets/brand/eqavo-icon.svg)

## Local development

Bootstrap:

```bash
./scripts/bootstrap.sh
```

Sync the latest stable Zed release source:

```bash
python3 scripts/sync_zed.py
```

Apply translations:

```bash
python3 scripts/apply_translations.py
```

Disable upstream service-connected features:

```bash
python3 scripts/disable_services.py
```

Build locally:

```bash
./scripts/build_local.sh
```

## Long-term roadmap

- Add GitHub Actions for macOS release builds
- Add automatic diff checks when new Zed versions move UI files
- Add more structured translation coverage reports
- Package as signed `.dmg` if signing resources are available
- Optionally add a tiny installer app that downloads the latest translated build
