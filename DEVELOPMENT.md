# Development Guide

## 🐳 Running scripts with Docker

A `Dockerfile` is provided so you don't need to install Python or system dependencies locally.

**Build the image (one-time):**

    docker build -t awesome-dashboard-icons .

**Convert all SVGs to PNG (skips existing):**

    docker run --rm -v "$(pwd)/icons:/app/icons" awesome-dashboard-icons scripts/convert_svg_to_png.py

**Convert specific icons:**

    docker run --rm -v "$(pwd)/icons:/app/icons" awesome-dashboard-icons scripts/convert_svg_to_png.py icons/spotify.svg

**Force-regenerate existing PNGs:**

    docker run --rm -v "$(pwd)/icons:/app/icons" awesome-dashboard-icons scripts/convert_svg_to_png.py --overwrite

**Regenerate static docs:**

    docker run --rm -v "$(pwd):/app" awesome-dashboard-icons scripts/generate_directory.py
    docker run --rm -v "$(pwd):/app" awesome-dashboard-icons scripts/generate_gallery.py
    docker run --rm -v "$(pwd):/app" awesome-dashboard-icons scripts/update_count.py