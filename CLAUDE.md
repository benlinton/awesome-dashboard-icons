# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Awesome Dashboard Icons** is a curated collection of icons for self-hosted dashboard applications (Homepage, Homarr, Dashy). The repository contains PNG and SVG icon files in `/icons/`, and auto-generated browsable documentation in `/_static/`.

## Scripts

All scripts must be run from the repo root. They have no external dependencies except `convert_svg_to_png.py`, which requires `cairosvg` (`pip install -r requirements.txt`) and system `libcairo2`.

```bash
./scripts/convert_svg_to_png.py              # Convert SVGs to PNGs (skips existing by default)
./scripts/convert_svg_to_png.py --overwrite  # Force regenerate all PNGs
./scripts/generate_directory.py              # Regenerate _static/directory-*.md files
./scripts/generate_gallery.py                # Regenerate _static/gallery-*.md files
./scripts/update_count.py                    # Update icon count in README.md
```

These all run automatically via `.github/workflows/generate-assets.yml` on push to `main` when `icons/**`, `scripts/**`, or the workflow file itself changes.

## Architecture

- **`/icons/`** — The icon collection. Both PNG and SVG may exist for the same base name. Files follow kebab-case naming (e.g., `adguard-home.png`, `spotify.svg`).
- **`/scripts/`** — Python 3 scripts that generate documentation. `convert_svg_to_png.py` is the only script with an external dependency (`cairosvg`).
- **`/_static/`** — Generated markdown files (do not edit manually). Paginated by letter (A–Z) plus `#` for numerics. Gallery pages use `gallery-{letter}.md`; directory pages use `directory-{letter}.md`; numerics use `gallery.md` / `directory.md`.
- **`.github/workflows/generate-assets.yml`** — Converts SVGs to PNGs, regenerates `_static/**`, and auto-commits changes. Skips runs triggered by the bot's own commit to prevent loops.

## Icon Conventions

- Format: PNG and/or SVG, named in kebab-case
- Gallery display: `height="50"` HTML `<img>` tags
- Directory display: `width="50"` HTML `<img>` tags
- Icon count in README is auto-updated by `update_count.py` via regex
- PNGs should be a minimum of 512×512px; `convert_svg_to_png.py` enforces this, scaling up while preserving aspect ratio
