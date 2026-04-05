# Eqavo

<p align="center">
  <img src="./assets/brand/eqavo-logo.svg" alt="Eqavo logo" width="720" />
</p>

<p align="center">
  <img src="./assets/brand/eqavo-icon.svg" alt="Eqavo icon" width="128" />
</p>

<p align="center">
  <a href="./README.md">中文</a> | English
</p>

<p align="center">
  <a href="https://github.com/resment/eqavo/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/resment/eqavo?style=flat-square" /></a>
  <a href="https://github.com/resment/eqavo/network/members"><img alt="GitHub forks" src="https://img.shields.io/github/forks/resment/eqavo?style=flat-square" /></a>
  <a href="https://github.com/resment/eqavo/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/resment/eqavo?style=flat-square" /></a>
  <a href="https://github.com/resment/eqavo/commits/main"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/resment/eqavo?style=flat-square" /></a>
</p>

> An unofficial, macOS-first, Chinese-localized distribution project built on top of Zed source code.

## Product overview

`Eqavo` aims to:

- give macOS users a more complete Chinese-localized editing experience
- minimize end-user setup effort
- use an independent brand instead of the upstream Zed brand
- move toward a local-first build with fewer upstream service dependencies

Ideal user flow:

1. Open GitHub Releases
2. Download the correct macOS package
3. Drag it into `Applications`
4. Launch and use it

## Current positioning

- Name: `Eqavo`
- Type: unofficial community project
- Platform: macOS first
- Language: Chinese first, English second
- Pricing: free
- Repo model: independently maintained

## Growth snapshot

We use live GitHub metrics instead of hardcoded numbers:

- stars, forks, issues, and last commit are shown in the badges above
- more metrics can be added later:
  - release downloads
  - build success rate
  - localization coverage
  - sync speed with upstream releases

Project stage right now:

- Done: repo bootstrap, independent branding, icon generation pipeline, translation scaffold, service-stripping scaffold
- In progress: GitHub Actions release flow, actual service stripping validation, better translation coverage

## Star History

<a href="https://www.star-history.com/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=resment/eqavo&type=date&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=resment/eqavo&type=date&legend=top-left" />
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=resment/eqavo&type=date&legend=top-left" />
  </picture>
</a>

Detailed planning docs:

- [PROJECT_STATUS.md](./PROJECT_STATUS.md)

## What this project is solving

Existing community translation approaches are not ideal for macOS because they are often:

- Linux-first
- tied to outdated source paths
- too manual for normal users
- not independent enough in branding and distribution

Eqavo takes a different path:

1. sync upstream Zed source
2. apply structured Chinese translations
3. strip unnecessary upstream service-connected entry points
4. build macOS distributable artifacts
5. publish them under an independent brand

## Repository layout

```text
eqavo/
  README.md
  README_EN.md
  PROJECT_STATUS.md
  assets/
    brand/
  scripts/
    bootstrap.sh
    sync_zed.py
    apply_translations.py
    disable_services.py
    apply_branding.py
    generate_icons.py
    package_macos.sh
  src/
  translations/
```

## Local development

Bootstrap:

```bash
./scripts/bootstrap.sh
```

Sync upstream source:

```bash
python3 scripts/sync_zed.py
```

Apply localization:

```bash
python3 scripts/apply_translations.py
```

Strip service-connected features:

```bash
python3 scripts/disable_services.py
```

Apply Eqavo branding:

```bash
python3 scripts/apply_branding.py
```

Generate icon assets:

```bash
python3 scripts/generate_icons.py
```

Package a macOS build:

```bash
./scripts/package_macos.sh aarch64-apple-darwin
```

## Compliance notes

- `Eqavo` is an independent community brand
- this project is not affiliated with or endorsed by Zed Industries
- upstream licensing and branding restrictions still need to be respected

## Roadmap

Near-term priorities:

1. produce `.app` and `.dmg` artifacts automatically
2. finish GitHub Actions release automation
3. improve Chinese coverage for newer Zed versions
4. strip more upstream sign-in, collaboration, telemetry, and update entry points
