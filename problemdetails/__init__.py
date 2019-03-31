try:
    from problemdetails.handlers import ErrorWriter, type_link_map
except ImportError as error:  # pragma: no cover # noqa: 841

    class ErrorWriter:
        def __init__(self, *args, **kwargs):
            raise error  # noqa: 821


__all__ = ['ErrorWriter', 'type_link_map', 'version_info', 'version']

version_info = (0, 0, 1)
version = '.'.join(str(c) for c in version_info)
