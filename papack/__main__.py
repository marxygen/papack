"""Main papack execution file"""
import argparse
import os
import sys
import logging
from papack.enums import LOGGING_VERBOSITY_LEVELS
from papack.utils import (list_files, convert_to_module_name, extract_imports,
                          read_requirements, write_file, get_stdlib_modules)


if __name__ == '__main__':
    # Retrieve arguments
    parser = argparse.ArgumentParser(
        description='Papack is a python package helper that is intended to assist you in '
        'managing packages required for your project',
        usage='papack ... or python -m papack ...')
    parser.add_argument('--path', help='Path to project folder I should check')
    parser.add_argument(
        '--implim',
        type=int,
        default=50,
        help='Max number of lines that will be checked for presence of imports. Default=50')
    parser.add_argument(
        '--reqs',
        default='./requirements.txt',
        help='Path to requirements.txt for this project. Used unless --noreqs flag is set')
    parser.add_argument(
        '--noreqs',
        type=bool,
        default=False,
        help='If specified, I will not compare data in requirements and installed packages and list differences')
    parser.add_argument(
        '--freeze',
        type=str,
        default='papack-reqs.txt',
        help='If specified, requirements deduced from project files will be written to specified file')
    parser.add_argument(
        '--verbose',
        '-v',
        action='count',
        default=2,
        help='Verbosity level (0-3)')
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
    logger.info(f'Found {len(files)} files')
    if not files:
        raise SystemExit('Nothing to do here: no Python files')

    # Extract module names from these files. We'll use these later to try to determine what is an external package
    # and what is imported from project file
    project_modules = [convert_to_module_name(entry) for entry in files]

    # Extract imports from files
    imports = []
    for module_imports in [extract_imports(f, imports_line_limit=args.implim) for f in files]:
        imports.extend(module_imports)

    imports = set(imports)

    stdlib_modules = get_stdlib_modules()
    external_imports = [entry for entry in imports if entry not in project_modules and entry not in stdlib_modules]
    logger.info(f'Found {len(external_imports)} required packages: {", ".join(external_imports)}')

    if args.freeze:
        write_file(args.freeze, external_imports)
        logger.info(f'Successfully wrote project requirements to file "{args.freeze}"')

    if args.noreqs:
        logger.debug('Got a --noreqs flag, exiting...')
        raise SystemExit()

    if not os.path.exists(args.reqs):
        raise SystemExit(f'No requirements file is found at "{args.reqs}"')

    requirements = read_requirements(args.reqs)
    not_listed = [entry for entry in external_imports if entry not in requirements]
    not_used = [entry for entry in requirements if entry not in external_imports]

    logger.warning(f'Found some packages that are not present in "{args.reqs}": {", ".join(not_listed)}')
    logger.warning(f'Found some packages that might not be required: {", ".join(not_used)}')


