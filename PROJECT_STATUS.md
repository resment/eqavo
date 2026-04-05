# Eqavo Project Status

This document tracks what Eqavo is trying to become, what has already been done, and what we should do next.

## Product goal

Build an unofficial, macOS-first, Chinese-localized editor distribution based on Zed source code with the simplest possible user flow:

1. Go to GitHub Releases
2. Download a macOS build
3. Drag into `Applications`
4. Open and use it

## Current decisions

- Product name: `Eqavo`
- Positioning: unofficial, macOS-first, local-first
- Pricing: free
- Distribution: separate GitHub repository
- Branding direction: independent from Zed branding
- Technical strategy: source sync + translation overlay + optional service stripping + macOS build

## Completed

- Created separate GitHub repository: [resment/eqavo](https://github.com/resment/eqavo)
- Renamed the local project folder to `eqavo`
- Added project scaffold for syncing Zed source and applying translations
- Added initial structured translation file
- Added a dedicated Chinese glossary layer for reusable product terminology
- Added first-pass logo and app icon SVG assets
- Added generated macOS iconset and `.icns` assets
- Added initial service-stripping script
- Added agent environment patching to preserve user-provided Claude/Bedrock/Vertex credentials
- Added branding application script for bundle metadata and icons
- Added local build script that chains sync, translation, service stripping, and cargo build
- Added GitHub Actions workflow scaffold for macOS release builds

## In progress

- Refine translation coverage for newer Zed source layout without touching Rust identifiers
- Validate service stripping against actual builds and runtime behavior
- Validate end-to-end unsigned `.app` / `.dmg` packaging on macOS

## Next priorities

1. Add GitHub Actions to build and publish macOS artifacts
2. Replace broad string replacement with more stable literal-aware translation rules
3. Strip more upstream service-connected features:
   - sign-in entry points
   - collaboration panels and menu items
   - telemetry UI
   - update UI
   - cloud AI/provider entry points
5. Produce a runnable `Eqavo.app`
6. Package `.dmg` artifacts for Apple Silicon and Intel
7. Add a clearer disclaimer page and release notes template

## Open questions

- Keep all AI features, or strip all cloud-connected AI by default?
- Keep manual update checking, or remove update features entirely?
- Keep extension marketplace access, or local-only extensions?
- Do we want `Eqavo.app` as the final app name, or `Eqavo Editor.app`?

## Definition of done

Eqavo is in a strong first public state when all of the following are true:

- Users can download a macOS artifact from GitHub Releases
- The app opens without requiring local build steps
- The visible UI is meaningfully more Chinese-localized than upstream Zed
- The product uses independent branding
- Service-connected features are either removed or clearly intentional
- The repository documents how the build is produced
