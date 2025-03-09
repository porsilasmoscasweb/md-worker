# -*- coding: utf-8 -*-
import os
from core import Core


class MarkdownTOCGenerator(Core):
    def __init__(self, root_path, destination_path=None, ignore=None, output_toc_file="TOC"):
        super().__init__(root_path, destination_path=destination_path, ignore=ignore)

        self.output_toc_file = output_toc_file + '.md'

    def funct_format_name(self, name, is_dir=False):
        """
        Format name of the directory or file.

        Args:
            name (str): Name of the directory or file.
            is_dir(bool): Tells if is a directory.

        Returns:
            str: Name formated.
        """
        if is_dir:
            return name.upper()
        else:
            name_not_ext, _ = os.path.splitext(name)
            if name_not_ext.startswith('_'):
                return name_not_ext
            name_not_ext = name_not_ext.replace('_', ' ').strip()
            return name_not_ext.capitalize()

    def generate_markdown_toc(self, root_path, level=0, parent_index="", is_root=False):
        """
        Generates a table of contents in markdown based on the structure of directories and subdirectories.

        Args:
            root_path (str): Base path of the directory.
            level (int): Depth level in the structure (for subdirectories).
            parent_index (str): The index of the parent directory to keep numbering.
            is_root (bool): Indicates whether we are at the root to use readable numbers.

        Returns:
            str: TOC in Markdown format.
        """
        elements = []
        local_index = 1

        # List of directories and files in the base path, ignoring hidden and those in the IGNORE list
        for name in sorted(os.listdir(root_path)):
            if self.has_ignore(name):
                continue

            full_path = os.path.join(root_path, name)
            absolute_path = os.path.abspath(full_path)

            # Create hierarchical index (use readable numbers in root)
            if is_root:
                current_index = f"{local_index}."
            else:
                current_index = f"{parent_index}{local_index}."

            format_name = self.funct_format_name(name, is_dir=os.path.isdir(full_path))

            if os.path.isdir(full_path) and not os.path.islink(full_path):
                # If it is a directory, add to TOC with absolute link and process recursively
                elements.append(f"{'  ' * level}- {current_index} [{format_name}/]({absolute_path}/)")
                sub_elementos = self.generate_markdown_toc(full_path, level + 1, current_index)
                elements.append(sub_elementos)
            else:
                # If it is a file, add it to the TOC with an absolute link
                elements.append(f"{'  ' * level}- {current_index} [{format_name}]({absolute_path})")

            local_index += 1

        return "\n".join(elements)

    def create_toc(self):
        """
        Create the TOC.md file with the contents of the generated TOC.
        """
        toc = self.generate_markdown_toc(self.destination_path, is_root=True)

        try:
            # Save the TOC to the TOC.md file
            with open(os.path.join(self.destination_path, self.output_toc_file), 'w') as toc_file:
                toc_file.write("# Table of Contents\n\n")
                toc_file.write(toc)
                print(f"The {self.output_toc_file} file generated successfully with:\n"
                    f"\t* Destination path: '{self.destination_path}'\n"
                    f"\t* Ignoring the directories and file on the ignore list: [{', '.join(self.ignore)}]\n"
                    f"\t* To {self.destination_path}/{self.output_toc_file} Path.\r\n")
        except:
            raise Exception("ERROR", f"The TOC could not be generated because the path {self.destination_path} is not a directory.")
