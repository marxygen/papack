"""Main papack execution file"""
import argparse
import os
import logging
from papack.enums import LOGGING_VERBOSITY_LEVELS
from papack.utils import list_files, convert_to_module_name


if __name__ == '__main__':
    # Retrieve arguments
    parser = argparse.ArgumentParser(description='Papack is a python package helper that is intended to assist you in '
                                                 'managing packages required for your project',
                                     usage='papack ... or python -m papack ...')
    parser.add_argument('--path', help='Path to project folder I should check')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbosity level (0-3)')
    args = parser.parse_args()

    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOGGING_VERBOSITY_LEVELS.get(args.verbose, 0))
    logger.addHandler(console_handler)

    # Get path (use current if not specified)
    path = args.path or os.getcwd()
    logger.debug(f'Checking "{path}"...')

    # Obtain list of files
    files = list_files(path, extensions=['py'])
    logger.debug(f'Found {len(files)} files')
    if not files:
        raise SystemExit('Nothing to do here: no Python files')

    # Extract module names from these files. We'll use these later to try to determine what is an external package
    # and what is imported from project file
    project_modules = [convert_to_module_name(entry) for entry in files]



