# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Awesome Dashboard Icons** is a curated collection of icons for self-hosted dashboard applications (Homepage, Homarr, Dashy). The repository contains PNG and SVG icon files in `/icons/`, and auto-generated browsable documentation in `/_static/`.

## Regenerating Documentation

When icons are added or modified, regenerate the static docs:

```bash
./scripts/generate_directory.py   # Regenerates _static/directory-*.md files
./scripts/generate_gallery.py     # Regenerates _static/gallery-*.md files
./scripts/update_count.py         # Updates icon count in README.md
```

These scripts run automatically via GitHub Actions on push to `main` when `icons/**` or `scripts/**` changes.

## Architecture

- **`/icons/`** — The icon collection. Both PNG and SVG may exist for the same icon name. Files follow kebab-case naming (e.g., `adguard-home.png`, `spotify.svg`).
- **`/scripts/`** — Python 3 scripts that generate documentation. No external dependencies beyond stdlib.
- **`/_static/`** — Generated markdown files (do not edit manually). Paginated by letter (A-Z + `#` for numerics). Gallery files embed images as HTML `<img>` tags.
- **`.github/workflows/regenerate-static.yml`** — Auto-commits regenerated `_static/**` and `README.md` after icon/script changes.

## Icon Conventions

- Format: PNG and/or SVG, named in kebab-case
- Gallery display: `height="50"` HTML img tags
- Directory display: `width="50"` HTML img tags
- Icon count in README is auto-updated by `update_count.py` via regex
