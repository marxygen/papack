import os
from os.path import join
from typing import List, Union


def list_files(path: str, extensions: list = None, ignore: list = None) -> List[str]:
    """List files in a directory and return full paths to these files

    :param path: Root path
    :param extensions: List of extensions to include. Files with other extensions will be ignored
    :param ignore: List of directory or file names that will be ignored
    :return: List of full paths to files in specified directory
    """
    contents = []
    for name, entry in [(e, join(path, e).replace("\\","/")) for e in os.listdir(path)]:
        if ignore and name in ignore:
            continue

        if os.path.isdir(entry):
            contents.extend(list_files(entry, extensions=extensions, ignore=ignore))
            continue

        if not extensions or name.split('.')[-1] in extensions:
            contents.append(entry)

    return contents


def convert_to_module_name(path: str) -> str:
    """Convert path to Python module name (if it is indeed a Python module)

    :param path: Path to Python module
    :return: A string representing module name
    :raises: Value error if passed in file is not a Python module
    """
    _, file_name = os.path.split(path)
    if file_name.split('.')[-1] != 'py':
        raise ValueError(f'File "{path}" is not a Python module!')

    return file_name.split('.')[0]


def extract_imports(file: str, imports_line_limit=50) -> List[str]:
    """Extract imports present in file with specified path

    :param file: Path to python file
    :param imports_line_limit: Max number of lines that will be checked for presence of input statements.
    :return: A list modules that are imported in this file
    """
    imports = []

    with open(file, 'r', encoding='utf-8') as source:
        # Since python import statements can be multiline, we indicate that the
        # following line must contain imports
        expect_imports = False
        for line in source.readlines()[:imports_line_limit]:
            if expect_imports:
                # Check if the string is (1) not empty
                if not line.strip():
                    expect_imports = False
                    continue

            # In other cases skip the line if no import statement is found or
            # the line is a comment
            if 'import' not in line or line.strip().startswith('#') or line.strip().startswith('"'):
                continue

            # If the line contains '\' or '(', indicate that the next line
            # contains imports as well
            if '(' in line:
                expect_imports = True
            else:
                expect_imports = False

            """
            Now we have to convert lines into module names
            There are some things that might get in the way
            1. Comments. For example, if the beginning of the file looks like this
            ```
                import module # Just some test module (my own module)
                print('Program has started!')
             ```
            then code above will add the print statement to list of probable imports.
            """
            # Now we split the line into words
            words = line.strip().replace('(', '').replace(')', '').replace(',', '').replace('\\', '').split(' ')

            # If there are comments, we're interested only in what comes before the comment
            for index, word in enumerate(words):
                if '#' in word or word == 'from' and index > 1 or word == 'import' and index > 1:
                    words = words[:index]
                    continue

            if not any(words):
                continue

            imports.extend(filter(lambda x: x, [w.split('.')[0] for w in words if w != 'import' and w != 'from']))

    return imports


def read_requirements(file: str) -> List[str]:
    """Read requirements file and extract listed packages

    :param file: Path to requirements.txt file
    :return: List of packages specified in requirements.txt
    """
    packages = []
    with open(file, 'r') as source:
        for line in source.readlines():
            packages.append(line[:line.index('=')])
    return packages


def write_file(file: str, contents: Union[List, str]) -> None:
    """Write given contents to file

    :param file: File path. It will be overwritten or created if doesn't exist
    :param contents: Contents. You can specify it either as a list of lines or as a string
    :return: None
    """
    with open(file, 'w', encoding='utf-8') as dest:
        if isinstance(contents, list):
            contents = '\n'.join(contents)
        dest.write(contents)