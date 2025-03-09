# -*- coding: utf-8 -*-
import os
import shutil


class Core:
    def __init__(self, root_path, destination_path=None, ignore=None):
        """
        Initializes the class with the base directory, destination directory, and the list of directories to ignore.

        Args:
            root_path: Base path of the directory.
            destination_path: Path of the directory (optional).
            ignore: List of directories to ignore (optional).
        """
        if not os.path.isdir(root_path):
            raise Exception("ERROR",
                            f"The Root Path provided {root_path} is not a correct directory, so we cannot generate the TOC.")

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

        print(f"Instance created with:\n"
            f"\t* Root path: {self.root_path}\n"
            f"\t* Destination path: {self.destination_path}\n"
            f"\t* List of directories and files to ignore: [{', '.join(self.ignore)}].\r\n")


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
        if ignore is None:
            ignore = self.ignore
        elif isinstance(ignore, list):
            ignore = self.ignore + ignore


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
