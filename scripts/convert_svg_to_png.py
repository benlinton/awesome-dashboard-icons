#!/usr/bin/env python3
"""Convert SVG icons to PNG with minimum 512x512 dimensions, preserving aspect ratio."""

import argparse
import glob
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg

MIN_DIMENSION = 512


def parse_svg_dimensions(svg_path):
    """Extract width and height from an SVG file.

    Checks viewBox first, then width/height attributes.
    Returns (width, height) as floats, or (512, 512) if undetermined.
    """
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
    except ET.ParseError:
        return float(MIN_DIMENSION), float(MIN_DIMENSION)

    # Strip namespace for attribute access
    tag = root.tag
    ns = ""
    if tag.startswith("{"):
        ns = tag[: tag.index("}") + 1]

    # Try viewBox first
    viewbox = root.get("viewBox") or root.get("viewbox")
    if viewbox:
        parts = re.split(r"[,\s]+", viewbox.strip())
        if len(parts) == 4:
            try:
                w = float(parts[2])
                h = float(parts[3])
                if w > 0 and h > 0:
                    return w, h
            except ValueError:
                pass

    # Fallback to width/height attributes
    w_attr = root.get("width")
    h_attr = root.get("height")
    if w_attr and h_attr:
        w_val = re.sub(r"[a-zA-Z%]+$", "", w_attr.strip())
        h_val = re.sub(r"[a-zA-Z%]+$", "", h_attr.strip())
        try:
            w = float(w_val)
            h = float(h_val)
            if w > 0 and h > 0:
                return w, h
        except ValueError:
            pass

    return float(MIN_DIMENSION), float(MIN_DIMENSION)


def calculate_output_dimensions(w, h, min_size=MIN_DIMENSION):
    """Calculate output dimensions so both sides are >= min_size, preserving aspect ratio."""
    scale = max(min_size / w, min_size / h)
    return math.ceil(w * scale), math.ceil(h * scale)


def main():
    parser = argparse.ArgumentParser(
        description="Convert SVG icons to PNG (minimum 512x512, preserving aspect ratio)."
    )
    parser.add_argument(
        "patterns",
        nargs="*",
        help="Glob patterns for SVG files (default: icons/*.svg)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Regenerate PNGs even if they already exist",
    )
    args = parser.parse_args()

    # Discover SVG files
    if args.patterns:
        svg_paths = []
        for pattern in args.patterns:
            svg_paths.extend(Path(p) for p in glob.glob(pattern))
    else:
        svg_paths = list(Path("icons").glob("*.svg"))

    # Filter to .svg only
    svg_paths = sorted(set(p for p in svg_paths if p.suffix.lower() == ".svg"))

    # Filter out those with existing PNGs unless --overwrite
    skipped = 0
    to_convert = []
    for svg in svg_paths:
        png = svg.with_suffix(".png")
        if not args.overwrite and png.exists():
            skipped += 1
        else:
            to_convert.append(svg)

    print(f"Found {len(to_convert)} SVGs to convert ({skipped} skipped — PNG exists)")

    if not to_convert:
        return

    errors = 0
    for svg in to_convert:
        png = svg.with_suffix(".png")
        w, h = parse_svg_dimensions(svg)
        out_w, out_h = calculate_output_dimensions(w, h)
        try:
            cairosvg.svg2png(
                url=str(svg),
                write_to=str(png),
                output_width=out_w,
                output_height=out_h,
            )
            print(f"  Converting: {svg.name} → {png.name} ({out_w}×{out_h})")
        except Exception as e:
            print(f"  WARNING: Failed to convert {svg.name}: {e}", file=sys.stderr)
            errors += 1

    converted = len(to_convert) - errors
    print(f"\nDone: {converted} converted, {errors} errors, {skipped} skipped")


if __name__ == "__main__":
    main()
