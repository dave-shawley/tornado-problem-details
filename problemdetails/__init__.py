import pkg_resources

dist = pkg_resources.get_distribution('tornado-problem-details')
version = dist.version
version_info = [int(c) if c.isdigit() else c for c in version.split('.')]
del pkg_resources

__all__ = ['version', 'version_info']

try:
    from problemdetails.errors import Problem
    from problemdetails.handlers import ErrorWriter, type_link_map
    __all__ = [
        'ErrorWriter', 'Problem', 'type_link_map', 'version', 'version_info'
    ]
except ImportError:  # pragma: nocover
    pass
