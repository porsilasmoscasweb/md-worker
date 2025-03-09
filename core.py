# -*- coding: utf-8 -*-
import os
import shutil


class MdToc:
    def __init__(self, root_path, destination_path=None, ignore=None, output_toc_filename="TOC"):
        """
        Initializes the class with the base directory, destination directory, and the list of directories to ignore to a file .md.

        Args:
            root_path: Base path of the directory.
            destination_path: Path of the directory.
            ignore: List of directories to ignore.
            output_dir: Make a copy of the root_path without ignored directories and files.
            output_toc_filename: Name of de resulting TOC file name.
        """
        if not os.path.isdir(root_path):
            raise Exception("ERROR", f"The Root Path provided {root_path} is not a correct directory, so we cannot generate the TOC.")

        self.ignore = ['.DS_Store', '.gitignore', '.idea', '*.log']
        if ignore is not None and isinstance(ignore, list):
            self.ignore += ignore

        if self.valid_path(root_path):
            self.root_path = root_path

        if destination_path is None:
            self.destination_path = self.root_path
        else:
            if self.valid_path(destination_path):
                if self.root_path == destination_path:
                    self.destination_path = destination_path
                else:
                    self.copy(root_path=self.root_path, destination_path=destination_path, ignore=self.ignore)
                    self.destination_path = destination_path

        self.output_toc_filename = output_toc_filename + ".md"

        print(
            f"Instance created with:\n"
            f"\t* Root path: {self.root_path}\n"
            f"\t* Destination path: {self.destination_path}\n"
            f"\t* List of directories and files to ignore: [{', '.join(self.ignore)}].\n"
            f"\t* The TOC file will be: {self.output_toc_filename}.\r\n"
        )


    def valid_path(self, full_path):
        """
        Check if the Path is on the ignore list.

        Args:
            full_path (str): Path.

        Returns:
            str: Name formated.
        """
        if any(shutil.fnmatch.fnmatch(full_path, pattern) for pattern in self.ignore):
            raise Exception("ERROR", f"The Path {full_path} is on list of ignore argument.")
        return True


    def has_ignore(self, name):
        """
        Ignore hidden files or files that are on the ignore list.

        Args:
            name (str):

        Returns:
            boolean:
        """
        return name.startswith('.') or name in self.ignore

    def copy(self, root_path=None, destination_path=None, ignore=None):
        """
        Copy all files except ignored ones from root path to destination path

        Args:
            root_path: Base path of the directory. (optional)
            destination_path: Path of the directory (optional).
            ignore: List of directories to ignore (optional).
        """
        if root_path is None:
            root_path = self.root_path
        else:
            if self.valid_path(root_path):
                root_path = self.root_path

        if destination_path is None:
            destination_path = self.root_path
        else:
            if self.valid_path(destination_path):
                destination_path = destination_path

        # Check for ignore files
        if ignore is None and isinstance(ignore, list):
            self.ignore = ignore

        if not os.path.exists(root_path):
            raise Exception("ERROR", f"The root Path {root_path} does not exist.")

        if not os.path.exists(destination_path):
            # Copy everything
            # shutil.copytree(root_path, destination_path, ignore=shutil.ignore_patterns(*ignore))

            # Copy only the files to work off
            for item in os.listdir(root_path):
                if self.has_ignore(os.path.basename(item)):
                    continue

                origen_item = os.path.join(root_path, item)
                destino_item = os.path.join(destination_path, item)

                if os.path.isdir(origen_item):
                    shutil.copytree(origen_item, destino_item, dirs_exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(destino_item), exist_ok=True)
                    shutil.copy2(origen_item, destino_item)
        else:
            raise Exception("ERROR", f"The destination Path {destination_path} already exist.")

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
            with open(os.path.join(self.destination_path, self.output_toc_filename), 'w') as toc_file:
                toc_file.write("# Table of Contents\n\n")
                toc_file.write(toc)
                print(f"The {self.output_toc_filename} file generated successfully with:\n"
                    f"\t* Destination path: '{self.destination_path}'\n"
                    f"\t* Ignoring the directories and file on the ignore list: [{', '.join(self.ignore)}]\n"
                    f"\t* To {self.destination_path}/{self.output_toc_filename} Path.\r\n")
        except:
            raise Exception("ERROR", f"The TOC could not be generated because the path {self.destination_path} is not a directory.")