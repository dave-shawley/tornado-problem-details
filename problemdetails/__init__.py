from importlib import metadata

from problemdetails.errors import Problem
from problemdetails.handlers import ErrorWriter, type_link_map

version = metadata.version('tornado-problem-details')
version_info = [int(c) if c.isdigit() else c for c in version.split('.')]

__all__ = [
    'ErrorWriter', 'Problem', 'type_link_map', 'version', 'version_info'
]
