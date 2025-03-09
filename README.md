# md-worker

**md-worker** is a python tool for creating a Table of Contents `TOC` from a directory with a simple execution.

## Installation

To install and use **md-worker**, follow these steps:

1. **Clone the repository**:

```bash
git clone https://github.com/porsilasmoscasweb/md-worker.git
```

2. **Go to the project folder**:

```bash
cd md-worker
```
3. **Use the helper to now better what args do you will use:**

```bash
python3 main.py -h 
```

```text
# Output

usage: main.py [-h] [-t] [-i [IGNORE ...]] [-otf OUTPUT_TOC_FILENAME] [-o [OUTPUT_DIR ...]] root_dir

Generate TOC for Markdown files.

positional arguments:
  root_dir              Root path

options:
  -h, --help            show this help message and exit
  -t, --toc             To generate TOC.
  -i [IGNORE ...], --ignore [IGNORE ...]
                        List of directories (without absolute path) to ignore (separated by spaces).
  -otf OUTPUT_TOC_FILENAME, --output_toc_filename OUTPUT_TOC_FILENAME
                        Name of the output file (No extension). By default: 'TOC'
  -o [OUTPUT_DIR ...], --output_dir [OUTPUT_DIR ...]
                        Generates a copy of all files to an specified destination path or the default path '_output' and works on this directory.
```

4. **The output from the command will be:**

```bash
python3 main.py [-t | --toc]
```

```text
# Output

Instance created with:
        * Root path: test/test_dir
        * Destination path: test/test_dir
        * List of directories and files to ignore: [.DS_Store, .gitignore, .idea, *.log].

The Name_TOC.md file generated successfully with:
        * Destination path: 'test/test_dir'
        * Ignoring the directories and file on the ignore list: [.DS_Store, .gitignore, .idea, *.log]
        * To test/test_dir/Name_TOC.md Path.
```

## TESTING

You can run tests to see if everything it is working properly.

To do it, follow these steps:

1. **Install dependencies:**

```bash
pip install -r requirements_test.txt
```

2. **Use `pytest` to run the _test_**

```bash
pytest  test/test_args.py [-v -vv]
```
