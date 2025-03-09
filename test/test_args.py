# -*- coding: utf-8 -*-
import platform
import os
import shutil
import subprocess

ABSPATH = os.path.abspath('')
INPUT_DIR = ABSPATH + "/test/test_dir"

def rmtree(curr_dir):
    try:
        shutil.rmtree(curr_dir)
    except OSError as e:
        print(f"Error: {e.strerror}")

def rmfile(file_path):
    try:
        os.remove(file_path)
        print(f"File \'{file_path}\' deleted successfully.")
    except FileNotFoundError:
        print(f"File \'{file_path}\' not found.")
    except PermissionError:
        print(f"Permission denied to delete the file \'{file_path}\'.")
    except Exception as e:
        print(f"Error occurred while deleting the file: {e}")

def check_text_on_file(path_file, text_to_check):
    with open(path_file) as f:
        for line in f:
            if text_to_check in line:
                return True
    return False

def test_ERROR_no_args():
    """Ejecuta el script sin argumentos. No se hace nada."""
    result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    assert "" in result.stdout
    assert "" in result.stderr

def test_only_root_dir_args():
    """Ejecuta el script sin argumentos. No se hace nada."""
    result = subprocess.run(["python3", "main.py", INPUT_DIR], capture_output=True, text=True)
    assert "" in result.stdout

def test_toc_args():
    """Ejecuta el script sin argumentos. No se hace nada."""
    try:
        result = subprocess.run(["python3", "main.py", INPUT_DIR, "--toc"], capture_output=True, text=True)
        assert "The TOC.md file generated successfully" in result.stdout
        assert os.path.exists(INPUT_DIR+"/TOC.md")
    finally:
        rmfile(INPUT_DIR + "/TOC.md")

def test_toc_output_file_name_args():
    """Ejecuta el script sin argumentos. No se hace nada."""
    try:
        result = subprocess.run(["python3", "main.py", INPUT_DIR, "--toc", "--output_toc_filename", "test_TOC_file_name"], capture_output=True, text=True)
        assert "The test_TOC_file_name.md file generated successfully" in result.stdout
        assert os.path.exists(INPUT_DIR+"/test_TOC_file_name.md")
    finally:
        rmfile(INPUT_DIR + "/TOC.md")

def test_toc_ignore_dir():
    """Ejecuta el script sin argumentos. No se hace nada."""
    try:
        result = subprocess.run(["python3", "main.py", INPUT_DIR, "--toc", "--ignore", "ignore_dir"], capture_output=True, text=True)
        assert "The TOC.md file generated successfully" in result.stdout
        assert os.path.exists(INPUT_DIR + "/TOC.md")
        assert not check_text_on_file(INPUT_DIR + "/TOC.md", "ignore_dir")
        assert not check_text_on_file(INPUT_DIR + "/TOC.md", ".invisible_dir")
    finally:
        rmfile(INPUT_DIR + "/TOC.md")

def test_toc_ignore_file():
    """Ejecuta el script sin argumentos. No se hace nada."""
    try:
        result = subprocess.run(["python3", "main.py", INPUT_DIR, "--toc", "--ignore", "ignore_file.md"], capture_output=True, text=True)
        assert "The TOC.md file generated successfully" in result.stdout
        assert os.path.exists(INPUT_DIR + "/TOC.md")
        assert not check_text_on_file(INPUT_DIR + "/TOC.md", "ignore_file.md")
        assert not check_text_on_file(INPUT_DIR + "/TOC.md", ".invisible_file")
    finally:
        rmfile(INPUT_DIR + "/TOC.md")

def test_toc_ignore_dir_and_file():
    """Ejecuta el script sin argumentos. No se hace nada."""
    lst = ["ignore_dir", "ignore_file.md"]
    try:
        result = subprocess.run(["python3", "main.py", INPUT_DIR, "--toc", "--ignore"] + lst, capture_output=True, text=True)
        assert "The TOC.md file generated successfully" in result.stdout
        assert os.path.exists(INPUT_DIR + "/TOC.md")
        assert not check_text_on_file(INPUT_DIR + "/TOC.md", "ignore_dir")
        assert not check_text_on_file(INPUT_DIR + "/TOC.md", ".invisible_dir")
        assert not check_text_on_file(INPUT_DIR + "/TOC.md", "ignore_file.md")
        assert not check_text_on_file(INPUT_DIR + "/TOC.md", ".invisible_file")
    finally:
        rmfile(INPUT_DIR + "/TOC.md")

def test_toc_output_dir():
    """Ejecuta el script sin argumentos. No se hace nada."""
    root_path = INPUT_DIR + "_output_dir_copy"
    try:
        result = subprocess.run(["python3", "main.py", INPUT_DIR, "--toc", "--output_dir" , root_path], capture_output=True, text=True)
        assert "The TOC.md file generated successfully" in result.stdout
        assert f"* Destination path: '{root_path}'" in result.stdout
    finally:
        rmtree(root_path)


def test_toc_output_dir_ignored_files():
    """Ejecuta el script sin argumentos. No se hace nada."""
    root_path = INPUT_DIR + "_output_dir_copy"
    try:
        result = subprocess.run(["python3", "main.py", INPUT_DIR, "--toc", "--output_dir" , root_path, "--ignore", "ignore_dir"], capture_output=True, text=True)
        assert not os.path.exists(root_path + "/ignore_dir")
        assert "The TOC.md file generated successfully" in result.stdout
        assert f"* Destination path: '{root_path}'" in result.stdout
    finally:
        rmtree(root_path)


def test_ERROR_toc_output_dir_exists():
    """Ejecuta el script sin argumentos. No se hace nada."""
    root_path = INPUT_DIR + "_output_dir_copy"
    try:
        result = subprocess.run(["python3", "main.py", INPUT_DIR, "--toc", "--output_dir" , root_path], capture_output=True, text=True)
        assert "The TOC.md file generated successfully" in result.stdout
        assert f"* Destination path: '{root_path}'" in result.stdout
        result2 = subprocess.run(["python3", "main.py", INPUT_DIR, "--toc", "--output_dir", root_path], capture_output=True, text=True)
        assert "" in result2.stderr
    finally:
        rmtree(root_path)
