#!/usr/bin/python3

from pathlib import Path
import os
import string

def page_link(id):
    return f'[[{id.upper()}](gallery-{id}.md)]'

def pagination():
    page_ids = string.ascii_lowercase
    links = ["[[HOME](..)]", "[[#](gallery.md)]"]
    links += [page_link(id) for id in page_ids]
    return links

def image_tag(file):
    return f'<img src="../icons/{file.name}" alt="{file.stem}" height="50">'

def gallery(dir, page_id, file_ext):
    if page_id == "#":
        files = [Path(file) for file in os.listdir(dir) if file[0].isdigit()]
    else:
        files = sorted(Path(dir).glob(f'{page_id}*.{file_ext}'))

    return [image_tag(file) for file in files]

def page_path(page_id):
    if page_id == "#":
        return '_static/gallery.md'
    else:
        return f'_static/gallery-{page_id.lower()}.md'

def page_name(page_id):
    if page_id == "#":
        return "Numbers"
    else: 
        return page_id.upper()

def create_page(dir, page_id):
    png_tags = gallery(dir, page_id, "png")
    svg_tags = gallery(dir, page_id, "svg")

    with open(page_path(page_id), "wt", encoding="UTF-8") as f:
        f.write("# Awesome Dashboard Icons")
        f.write("\n\n")

        f.write("".join(pagination()))
        f.write("\n\n")

        f.write(f'# Gallery: {page_name(page_id)}')
        f.write("\n\n")

        f.write(f'### PNGs ({len(png_tags)} Icons)\n\n')
        f.write(" ".join(png_tags))
        f.write("\n\n")

        f.write(f'### SVGs ({len(svg_tags)} Icons)\n\n')
        f.write(" ".join(svg_tags))
        f.write("\n\n")

        f.write("".join(pagination()))
        f.write("\n\n")

def page_ids():
    return "#" + string.ascii_lowercase


if __name__ == "__main__":
    dir = "./icons"
    for page_id in page_ids():
        create_page(dir, page_id)
