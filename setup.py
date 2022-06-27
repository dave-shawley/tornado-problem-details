#!/usr/bin/env python
import setuptools

version = tuple(int(c) for c in setuptools.__version__.split('.'))
if version < (38, 3):
    raise RuntimeError('Please update setuptools')
setuptools.setup(python_requires='>=3.7')
