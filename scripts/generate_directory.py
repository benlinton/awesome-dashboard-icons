#!/usr/bin/python3

from pathlib import Path
import os
import string

def page_link(id):
    return f'[[{id.upper()}](directory-{id.lower()}.md)]'

def pagination():
    page_ids = string.ascii_lowercase
    links = ["[[HOME](..)]", "[[#](directory.md)]"]
    links += [page_link(id) for id in page_ids]
    return links

def image_tag(file):
    return f'<img src="../icons/{file.name}" alt="{file.stem}" width="50">'

def table_column(dir, name, extension):
    path = Path(dir + "/" + name + "." + extension)
    if path.exists():
        return image_tag(path)
    else:
        return ""

def table_row(dir, name):
    png_tag = table_column(dir, name, "png")
    svg_tag = table_column(dir, name, "svg")
    return f'| {name} | {png_tag} |  {svg_tag} |\n'

def unique_names(dir, page_id):
    if page_id == "#":
        files = [file for file in os.listdir(dir) if file[0].isdigit()]
    else:
        files = Path(dir).glob(f'{page_id.lower()}*.*g')
    
    unique_paths = list({os.path.splitext(file)[0] for file in files})
    unique_names = [s.replace("icons/", "") for s in unique_paths]
    unique_names = sorted(unique_names)
    return unique_names

def page_path(page_id):
    if page_id == "#":
        return '_static/directory.md'
    else:
        return f'_static/directory-{page_id.lower()}.md'
    
def page_name(page_id):
    if page_id == "#":
        return "Numbers"
    else: 
        return page_id.upper()
        
def create_page(dir, page_id):
    table_rows = [table_row(dir, name) for name in unique_names(dir, page_id)]

    with open(page_path(page_id), "wt", encoding="UTF-8") as f:
        f.write("# Awesome Dashboard Icons")
        f.write("\n\n")

        f.write("".join(pagination()))
        f.write("\n\n")

        f.write(f'# Directory: {page_name(page_id)}')
        f.write("\n\n")

        f.write("| Icon Name | PNG | SVG |\n")
        f.write("|-----------|-----|-----|\n")
        f.write("".join(table_rows))
        f.write("\n\n")

        f.write("".join(pagination()))
        f.write("\n\n")

def page_ids():
    return "#" + string.ascii_lowercase

if __name__ == "__main__":
    dir = "./icons"

    for page_id in page_ids():
        create_page(dir, page_id)

        