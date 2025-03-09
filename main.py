# -*- coding: utf-8 -*-
import argparse

from core import MdToc

def set_default_path(path, root_path, default=''):
    if path is not None:
        path = path[0] if path else root_path + default
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate TOC for Markdown files.")

    # Required args
    parser.add_argument(
        "root_dir",
        type=str,
        help="Root path"
    )
    # Opcional args
    parser.add_argument(
        "-t",
        "--toc",
        action="store_true",
        help="To generate TOC."
    )
    parser.add_argument(
        "-i",
        "--ignore",
        nargs='*',
        default=[],
        help="List of directories (without absolute path) to ignore (separated by spaces)."
    )
    parser.add_argument(
        "-otf",
        "--output_toc_filename",
        type=str,
        default="TOC",
        help="Name of the output file (No extension).By default: 'TOC'"
    )

    # Optional args: [None | List]
    # This args can be:
    #   No declare.
    #   Declare empty: in which case a default value is assigned later.
    #   Declare with a value: This will come in list format, in that case we will only use the first element.
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        nargs='*',
        default=None,
        help="Generates a copy of all files to an specified destination path or the default path '_output' and works on this directory."
    )

    args = parser.parse_args()

    root_dir = args.root_dir
    toc = args.toc
    ignore = args.ignore
    destination_path = set_default_path(args.output_dir, root_dir, '_output_copy')
    output_toc_filename = args.output_toc_filename


    if toc:
        generador = MdToc(root_dir, destination_path=destination_path, ignore=ignore, output_toc_filename=output_toc_filename)
        generador.create_toc()
