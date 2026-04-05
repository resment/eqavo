# Service Stripping

`Eqavo` is intended to be a local-first, unofficial macOS build.

To reduce legal ambiguity and product complexity, we can strip or disable service-connected features from the upstream Zed source during the build.

## Current target

The current stripping profile focuses on:

- telemetry startup
- auto update initialization
- collaboration UI initialization
- collaboration panels
- notification panels

This is intentionally conservative. It targets obvious service entry points first.

## What this does not fully remove yet

- every cloud-related dependency
- every sign-in string or menu item
- all AI/provider integrations
- all service-related settings pages

Those can be layered on in later passes.

## Usage

Run after syncing Zed source and before building:

```bash
python3 scripts/disable_services.py
```

Or use the build script, which can call it automatically in the future.
