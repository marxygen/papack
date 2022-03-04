import sys
from typing import List
import re
from urllib.request import urlopen


def get_stdlib_modules() -> List[str]:
    """Returns a list of modules present in Python standard library.
    Output may differ from version to version because of the implementation

    :return: List of modules in Python standard library
    """
    version = sys.version_info
    version = f"{version.major}.{version.minor}"
    url = f"https://docs.python.org/{version}/py-modindex.html"
    with urlopen(url) as f:
        page = f.read()
    modules = set()
    for module in re.findall(
        r'#module-(.*?)[\'"]',
        page.decode(
            'ascii',
            'replace')):
        modules.add(module)
    return modules
