import os
from os.path import join
from typing import List


def list_files(path: str, extensions: list = None) -> List[str]:
    """List files in a directory and return full paths to these files

    :param path: Root path
    :param extensions: List of extensions to include. Files with other extensions will be ignored
    :return: List of full paths to files in specified directory
    """
    contents = []
    for entry in [join(path, e) for e in os.listdir(path)]:
        if os.path.isdir(entry):
            contents.append(list_files(entry, extensions=extensions))
            continue

        if not extensions or entry.split('.')[-1] in extensions:
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
